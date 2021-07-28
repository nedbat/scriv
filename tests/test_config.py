"""Tests of scriv/config.py"""

import re

import pytest

import scriv.config
from scriv.config import Config

from .helpers import without_module

CONFIG1 = """\
[scriv]
output_file = README.md
categories = New, Different, Gone, Bad
"""

CONFIG2 = """\
[someotherthing]
no_idea = what this is

[tool.scriv]
output_file = README.md
categories =
    New
    Different
    Gone
    Bad

[more stuff]
value = 17
"""

GENERIC_TOML_CONFIG = """\
[project]
name = "spam"
version = "2020.0.0"
description = "Lovely Spam! Wonderful Spam!"
readme = "README.rst"
requires-python = ">=3.8"
license = {file = "LICENSE.txt"}
keywords = ["egg", "bacon", "sausage", "tomatoes", "Lobster Thermidor"]
authors = [
  {email = "hi@pradyunsg.me"},
  {name = "Tzu-Ping Chung"}
]
maintainers = [
  {name = "Brett Cannon", email = "brett@python.org"}
]
classifiers = [
  "Development Status :: 4 - Beta",
  "Programming Language :: Python"
]
"""

TOML_CONFIG = (
    GENERIC_TOML_CONFIG
    + """
[tool.scriv]
output_file = "README.md"
categories = [
    "New",
    "Different",
    "Gone",
    "Bad",
]

["more stuff"]
value = 17
"""
)


def test_defaults(temp_dir):
    # No configuration files anywhere, just get all the defaults.
    config = Config.read()
    assert config.fragment_directory == "changelog.d"
    assert config.format == "rst"
    assert config.new_fragment_template.startswith(
        ".. A new scriv changelog fragment"
    )
    assert config.categories == [
        "Removed",
        "Added",
        "Changed",
        "Deprecated",
        "Fixed",
        "Security",
    ]
    assert config.output_file == "CHANGELOG.rst"
    assert config.insert_marker == "scriv-insert-here"
    assert config.rst_header_chars == "=-"
    assert config.md_header_level == "1"
    assert "{{ date.strftime('%Y-%m-%d') }}" in config.entry_title_template
    assert config.main_branches == ["master", "main", "develop"]
    assert config.skip_fragments == "README.*"
    assert config.version == ""


def test_reading_config(temp_dir):
    (temp_dir / "setup.cfg").write_text(CONFIG1)
    config = Config.read()
    assert config.fragment_directory == "changelog.d"
    assert config.output_file == "README.md"
    assert config.categories == ["New", "Different", "Gone", "Bad"]


def test_reading_config_list(temp_dir):
    (temp_dir / "tox.ini").write_text(CONFIG2)
    config = Config.read()
    assert config.categories == ["New", "Different", "Gone", "Bad"]


def test_reading_config_from_directory(changelog_d):
    # The settings file can be changelog.d/scriv.ini .
    (changelog_d / "scriv.ini").write_text(CONFIG1)
    config = Config.read()
    assert config.categories == ["New", "Different", "Gone", "Bad"]


def test_reading_config_from_other_directory(temp_dir):
    # setup.cfg can set the fragment directory, and then scriv.ini will
    # be found there.
    (temp_dir / "scriv.d").mkdir()
    (temp_dir / "scriv.d" / "scriv.ini").write_text(CONFIG1)
    (temp_dir / "setup.cfg").write_text(
        "[tool.scriv]\nfragment_directory = scriv.d\n"
    )
    config = Config.read()
    assert config.fragment_directory == "scriv.d"
    assert config.categories == ["New", "Different", "Gone", "Bad"]


def test_unknown_option():
    config = Config.read()
    expected = "Scriv configuration has no 'foo' option"
    with pytest.raises(AttributeError, match=expected):
        config.foo  # pylint: disable=pointless-statement


def test_custom_template(changelog_d):
    # You can define your own template with your own name.
    (changelog_d / "start_here.j2").write_text("Custom template.")
    fmt = Config(
        new_fragment_template="file: start_here.j2"
    ).new_fragment_template
    assert fmt == "Custom template."


def test_unknown_format():
    with pytest.raises(
        ValueError, match=r"'format' must be in \['rst', 'md'\] \(got 'xyzzy'\)"
    ):
        Config(format="xyzzy")


def test_no_such_template():
    # If you specify a template name, and it doesn't exist, an error will
    # be raised.
    msg = r"No such file: changelog\.d[/\\]foo\.j2"
    with pytest.raises(Exception, match=msg):
        config = Config(new_fragment_template="file: foo.j2")
        config.new_fragment_template  # pylint: disable=pointless-statement


def test_override_default_name(changelog_d):
    # You can define a file named new_fragment.rst.j2, and it will be read
    # as the template.
    (changelog_d / "new_fragment.rst.j2").write_text("Hello there!")
    fmt = Config().new_fragment_template
    assert fmt == "Hello there!"


def test_file_reading(changelog_d):
    # Any setting can be read from a file, even where it doesn't make sense.
    (changelog_d / "hello.txt").write_text("Xyzzy")
    text = Config(output_file="file:hello.txt").output_file
    assert text == "Xyzzy"


def test_literal_reading(temp_dir):
    # Any setting can be read from a literal in a file.
    (temp_dir / "sub").mkdir()
    (temp_dir / "sub" / "foob.py").write_text(
        """# comment\n__version__ = "12.34.56"\n"""
    )
    text = Config(version="literal:sub/foob.py: __version__").version
    assert text == "12.34.56"


def test_literal_no_file():
    # What happens if the file for a literal doesn't exist?
    with pytest.raises(
        FileNotFoundError, match=r"No such file or directory: 'sub/foob.py'"
    ):
        config = Config(version="literal:sub/foob.py: __version__")
        config.version  # pylint: disable=pointless-statement


def test_literal_no_literal(temp_dir):
    # What happens if the literal we're looking for isn't there?
    (temp_dir / "sub").mkdir()
    (temp_dir / "sub" / "foob.py").write_text(
        """# comment\n__version__ = "12.34.56"\n"""
    )
    with pytest.raises(
        Exception,
        match=r"Couldn't find literal: 'literal:sub/foob.py: version'",
    ):
        config = Config(version="literal:sub/foob.py: version")
        config.version  # pylint: disable=pointless-statement


@pytest.mark.parametrize("chars", ["", "#", "#=-", "# ", "  "])
def test_rst_chars_is_two_chars(chars):
    # rst_header_chars must be exactly two non-space characters.
    with pytest.raises(ValueError):
        Config(rst_header_chars=chars)


def test_md_format(changelog_d):
    (changelog_d / "scriv.ini").write_text("[scriv]\nformat = md\n")
    config = Config.read()
    assert config.output_file == "CHANGELOG.md"
    template = re.sub(r"\s+", " ", config.new_fragment_template)
    assert template.startswith("<!-- A new scriv changelog fragment.")


class TestTomlConfig:
    """
    Tests of the TOML configuration support.
    """

    def test_reading_toml_file(self, temp_dir):
        (temp_dir / "pyproject.toml").write_text(TOML_CONFIG)
        config = Config.read()
        assert config.categories == ["New", "Different", "Gone", "Bad"]

    def test_toml_without_us(self, temp_dir):
        (temp_dir / "pyproject.toml").write_text(GENERIC_TOML_CONFIG)
        config = Config.read()
        assert config.categories == [
            "Removed",
            "Added",
            "Changed",
            "Deprecated",
            "Fixed",
            "Security",
        ]

    def test_no_toml_installed(self, temp_dir):
        # Without toml installed, raise an error if we have settings in the toml
        # file.
        (temp_dir / "pyproject.toml").write_text(TOML_CONFIG)
        with without_module(scriv.config, "tomli"):
            msg_pat = r"Can't read .* without TOML support"
            with pytest.raises(Exception, match=msg_pat):
                Config.read()

    def test_no_toml_installed_no_settings(self, temp_dir):
        # Without toml installed, and also none of our settings in the toml
        # file, there is no exception.
        (temp_dir / "pyproject.toml").write_text(GENERIC_TOML_CONFIG)
        with without_module(scriv.config, "tomli"):
            config = Config.read()
        assert config.categories[0] == "Removed"
