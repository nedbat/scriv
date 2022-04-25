"""Scriv configuration."""

import configparser
import pkgutil
import re
from pathlib import Path
from typing import Any, List

import attr

try:
    import tomli
except ImportError:  # pragma: no cover
    tomli = None  # type: ignore

from scriv.literals import find_literal


@attr.s
class _Options:
    """
    All the settable options for Scriv.
    """

    # The directory for fragments waiting to be collected. Also can have
    # templates and settings for scriv.
    fragment_directory = attr.ib(
        type=str,
        default="changelog.d",
        metadata={
            "doc": """\
                The directory for fragments.  This directory must exist, it
                will not be created.
                """,
        },
    )

    # What format for fragments? reStructuredText ("rst") or Markdown ("md").
    format = attr.ib(
        type=str,
        default="rst",
        validator=attr.validators.in_(["rst", "md"]),
        metadata={
            "doc": """\
                The format to use for fragments and for the output changelog
                file.  Can be either "rst" or "md".
                """,
        },
    )

    # The categories for changelog fragments. Can be empty for no
    # categorization.
    categories = attr.ib(
        type=list,
        default=[
            "Removed",
            "Added",
            "Changed",
            "Deprecated",
            "Fixed",
            "Security",
        ],
        metadata={
            "doc": """\
                Categories to use as headings for changelog items.
                See :ref:`categories`.
                """,
        },
    )

    output_file = attr.ib(
        type=str,
        default="CHANGELOG.${config:format}",
        metadata={
            "doc": """\
                The changelog file updated by ":ref:`cmd_collect`".
                """,
        },
    )

    insert_marker = attr.ib(
        type=str,
        default="scriv-insert-here",
        metadata={
            "doc": """\
                A marker string indicating where in the changelog file new
                entries should be inserted.
                """,
        },
    )

    end_marker = attr.ib(
        type=str,
        default="scriv-end-here",
        metadata={
            "doc": """\
                A marker string indicating where in the changelog file the
                changelog ends.
                """,
        },
    )

    # The characters to use for header and section underlines in rst files.
    rst_header_chars = attr.ib(
        type=str,
        default="=-",
        validator=attr.validators.matches_re(r"\S\S"),
        metadata={
            "doc": """\
                Two characters: for reStructuredText changelog files, these
                are the two underline characters to use.  The first is for the
                heading for each changelog entry, the second is for the
                category sections within the entry.
                """,
        },
    )

    # What header level to use for markdown changelog entries?
    md_header_level = attr.ib(
        type=str,
        default="1",
        validator=attr.validators.matches_re(r"[123456]"),
        metadata={
            "doc": """\
                A number: for Markdown changelog files, this is the heading
                level to use for the entry heading.
                """,
        },
    )

    # The name of the template for new fragments.
    new_fragment_template = attr.ib(
        type=str,
        default="file: new_fragment.${config:format}.j2",
        metadata={
            "doc": """\
                The `Jinja`_ template to use for new fragments.
                """,
        },
    )

    # The template for the title of the changelog entry.
    entry_title_template = attr.ib(
        type=str,
        default=(
            "{% if version %}{{ version }} — {% endif %}"
            + "{{ date.strftime('%Y-%m-%d') }}"
        ),
        metadata={
            "doc": """\
                The `Jinja`_ template to use for the entry heading text for
                changelog entries created by ":ref:`cmd_collect`".
                """,
            "doc_default": "A combination of version (if specified) and date.",
        },
    )

    # The version string to include in the title if wanted.
    version = attr.ib(
        type=str,
        default="",
        metadata={
            "doc": """\
                The string to use as the version number in the next header
                created by ``scriv collect``.  Often, this will be a
                ``literal:`` directive, to get the version from a string in a
                source file.
                """,
            "doc_default": "(empty)",
        },
    )

    # Branches that aren't interesting enough to use in fragment file names.
    main_branches = attr.ib(
        type=list,
        default=["master", "main", "develop"],
        metadata={
            "doc": """\
                The branch names considered uninteresting to use in new
                fragment file names.
                """,
        },
    )

    # Glob for files in the fragments directory that should not be collected.
    skip_fragments = attr.ib(
        type=str,
        default="README.*",
        metadata={
            "doc": """\
                A glob pattern for files in the fragment directory that should
                not be collected.
                """,
        },
    )


class Config:
    """
    Configuration for Scriv.

    All the settable options for Scriv, with resolution of values within other
    values.

    """

    def __init__(self, **kwargs):
        """All values in _Options can be set as keywords."""
        self._options = _Options(**kwargs)

    def __getattr__(self, name):
        """Proxy to self._options, and resolve the value."""
        fields = attr.fields_dict(_Options)
        if name not in fields:
            raise AttributeError(f"Scriv configuration has no {name!r} option")
        attrdef = fields[name]
        value = getattr(self._options, name)
        if attrdef.type is list:
            if isinstance(value, str):
                value = convert_list(value)
        else:
            value = self.resolve_value(value)
        setattr(self, name, value)
        return value

    @classmethod
    def read(cls) -> "Config":
        """
        Read the configuration to use.

        Configuration will be read from setup.cfg, tox.ini, or
        changelog.d/scriv.ini.  If setup.cfg or tox.ini defines
        a new fragment_directory, then scriv.ini is read from there.

        The section can be named ``[scriv]`` or ``[tool.scriv]``.

        """
        config = cls()
        for configfile in ["setup.cfg", "tox.ini"]:
            config.read_one_config(configfile)
        config.read_one_toml("pyproject.toml")
        config.read_one_config(
            str(Path(config.fragment_directory) / "scriv.ini")
        )
        return config

    def read_one_config(self, configfile: str) -> None:
        """
        Read one configuration file, adding values to `self`.
        """
        parser = configparser.ConfigParser()
        parser.read(configfile)
        section_names = ["scriv", "tool.scriv"]
        section_name = next(
            (name for name in section_names if parser.has_section(name)), None
        )
        if section_name:
            for attrdef in attr.fields(_Options):
                try:
                    val = parser[section_name][attrdef.name]  # type: Any
                except KeyError:
                    pass
                else:
                    setattr(self._options, attrdef.name, val)

    def read_one_toml(self, tomlfile: str) -> None:
        """
        Read one .toml file if it exists, adding values to `self`.
        """
        tomlpath = Path(tomlfile)
        if not tomlpath.exists():
            return

        toml_text = tomlpath.read_text(encoding="utf-8")

        if tomli is None:
            # Toml support isn't installed. Only print an exception if the
            # config file seems to have settings for us.
            has_scriv = re.search(r"(?m)^\[tool\.scriv\]", toml_text)
            if has_scriv:
                msg = (
                    "Can't read {!r} without TOML support. "
                    + "Install with [toml] extra"
                ).format(tomlfile)
                raise Exception(msg)
        else:
            # We have toml installed, parse the file and look for our settings.
            data = tomli.loads(toml_text)
            try:
                scriv_data = data["tool"]["scriv"]
            except KeyError:
                # No settings for us
                return
            for attrdef in attr.fields(_Options):
                try:
                    val = scriv_data[attrdef.name]
                except KeyError:
                    pass
                else:
                    setattr(self._options, attrdef.name, val)

    def resolve_value(self, value: str) -> str:
        """
        Interpret prefixes in config files to find the actual value.

        Also, "${config:format}" is replaced with the configured
        format ("rst" or "md").

        Prefixes:
            "file:" read the content from a file.
            "literal:" read a literal string from a file.

        """
        value = value.replace("${config:format}", self._options.format)
        if value.startswith("file:"):
            file_name = value.partition(":")[2].strip()
            file_path = Path(self.fragment_directory) / file_name
            if file_path.exists():
                value = file_path.read_text()
            else:
                try:
                    file_bytes = pkgutil.get_data(
                        "scriv", "templates/" + file_name
                    )
                except OSError as err:
                    msg = f"No such file: {file_path}"
                    raise Exception(msg) from err
                assert file_bytes
                value = file_bytes.decode("utf-8")
        elif value.startswith("literal:"):
            _, file_name, literal_name = value.split(":", maxsplit=2)
            found = find_literal(file_name.strip(), literal_name.strip())
            if found is None:
                raise Exception(f"Couldn't find literal: {value!r}")
            value = found
        return value


def convert_list(val: str) -> List[str]:
    """
    Convert a string value from a config into a list of strings.

    Elements can be separated by commas or newlines.
    """
    vals = re.split(r"[\n,]", val)
    vals = [v.strip() for v in vals]
    vals = [v for v in vals if v]
    return vals
