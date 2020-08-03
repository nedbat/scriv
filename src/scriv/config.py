"""Scriv configuration."""

import configparser
import pkgutil
import re
from pathlib import Path
from typing import Any, List

import attr

from scriv.literals import find_literal


@attr.s
class Config:
    """
    All the settable options for Scriv.
    """

    # The directory for fragments waiting to be collected. Also can have
    # templates and settings for scriv.
    fragment_directory = attr.ib(type=str, default="changelog.d")

    # What format for fragments? ReStructuredText ("rst") or Markdown ("md").
    format = attr.ib(type=str, default="rst", validator=attr.validators.in_(["rst", "md"]))

    # The categories for changelog fragments. Can be empty for no categorization.
    categories = attr.ib(type=list, default=["Removed", "Added", "Changed", "Deprecated", "Fixed", "Security"])

    output_file = attr.ib(type=str, default="CHANGELOG.rst")
    insert_marker = attr.ib(type=str, default="scriv-insert-here")

    # The characters to use for header and section underlines in rst files.
    rst_header_chars = attr.ib(type=str, default="=-", validator=attr.validators.matches_re(r"\S\S"))

    # The name of the template for new fragments.
    new_fragment_template = attr.ib(type=str, default="file: new_fragment.${config:format}.j2")

    # The template for the title of the changelog entry.
    entry_title_template = attr.ib(
        type=str, default="{% if version %}[{{ version }}] — {% endif %}{{ date.strftime('%Y-%m-%d') }}"
    )

    # The version string to include in the title if wanted.
    version = attr.ib(type=str, default="")

    # Branches that aren't interesting enough to use in fragment file names.
    main_branches = attr.ib(type=list, default=["master", "main", "develop"])

    def __attrs_post_init__(self):  # noqa: D105 (Missing docstring in magic method)
        self.resolve_all()

    def resolve_all(self):
        """
        Prepare all fields in the config.

        Call resolve_value on them, and convert strings to lists as needed.
        """
        for attrdef in attr.fields(Config):
            value = getattr(self, attrdef.name)
            if attrdef.type is list:
                if isinstance(value, str):
                    value = convert_list(value)
            else:
                value = self.resolve_value(value)
            setattr(self, attrdef.name, value)

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
        config.read_one_config(str(Path(config.fragment_directory) / "scriv.ini"))
        config.resolve_all()
        return config

    def read_one_config(self, configfile: str) -> None:
        """
        Read one configuration file, adding values to `config`.
        """
        parser = configparser.ConfigParser()
        parser.read(configfile)
        section_names = ["scriv", "tool.scriv"]
        section_name = next((name for name in section_names if parser.has_section(name)), None)
        if section_name:
            for attrdef in attr.fields(Config):
                try:
                    val = parser[section_name][attrdef.name]  # type: Any
                except KeyError:
                    pass
                else:
                    setattr(self, attrdef.name, val)

    def resolve_value(self, value: str) -> str:
        """
        Interpret prefixes in config files to find the actual value.

        Also, "${config:format}" is replaced with the configured
        format ("rst" or "md").

        Prefixes:
            "file:" read the content from a file.

        """
        value = value.replace("${config:format}", self.format)
        if value.startswith("file:"):
            file_name = value.partition(":")[2].strip()
            file_path = Path(self.fragment_directory) / file_name
            if file_path.exists():
                with open(str(file_path)) as f:
                    value = f.read()
            else:
                try:
                    file_bytes = pkgutil.get_data("scriv", "templates/" + file_name)
                except IOError:
                    raise Exception("No such file: {}".format(file_path))
                assert file_bytes
                value = file_bytes.decode("utf-8")
        elif value.startswith("literal:"):
            _, file_name, literal_name = value.split(":", maxsplit=2)
            found = find_literal(file_name.strip(), literal_name.strip())
            if found is None:
                raise Exception("Couldn't find literal: {!r}".format(value))
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
