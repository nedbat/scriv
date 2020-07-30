"""Tests of scriv/config.py"""

from scriv.config import Config

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


def test_defaults(temp_dir):
    # No configuration files anywhere, just get all the defaults.
    config = Config.read()
    assert config.entry_directory == "changelog.d"
    assert config.format == "rst"
    assert config.categories == ["Removed", "Added", "Changed", "Deprecated", "Fixed", "Security"]
    assert config.output_file == "CHANGELOG.rst"
    assert config.insert_marker == "scriv:insert-here"
    assert config.rst_header_char == "="
    assert config.rst_section_char == "-"
    assert config.header == "{date:%Y-%m-%d}"
    assert config.main_branches == ["master", "main", "develop"]


def test_reading_config(temp_dir):
    (temp_dir / "setup.cfg").write_text(CONFIG1)
    config = Config.read()
    assert config.entry_directory == "changelog.d"
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
    # setup.cfg can set the entry directory, and then scriv.ini will be found there.
    (temp_dir / "scriv.d").mkdir()
    (temp_dir / "scriv.d" / "scriv.ini").write_text(CONFIG1)
    (temp_dir / "setup.cfg").write_text("[tool.scriv]\nentry_directory = scriv.d\n")
    config = Config.read()
    assert config.entry_directory == "scriv.d"
    assert config.categories == ["New", "Different", "Gone", "Bad"]
