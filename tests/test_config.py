"""Tests of scriv/config.py"""

import re

import pytest

import scriv.config
from scriv.config import Config
from scriv.exceptions import ScrivException
from scriv.optional import tomllib

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
requires-python = ">=3.9"
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
# other scriv options

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


def test_unknown_option(temp_dir):
    config = Config.read()
    expected = "Scriv configuration has no 'foo' option"
    with pytest.raises(AttributeError, match=expected):
        _ = config.foo


def test_custom_template(changelog_d):
    # You can define your own template with your own name.
    (changelog_d / "start_here.j2").write_text("Custom template.")
    fmt = Config(
        new_fragment_template="file: start_here.j2"
    ).new_fragment_template
    assert fmt == "Custom template."


def test_file_with_dots(temp_dir, changelog_d):
    # A file: spec with dot components is relative to the current directory.
    (changelog_d / "start_here.j2").write_text("The wrong one")
    (temp_dir / "start_here.j2").write_text("The right one")
    fmt = Config(
        new_fragment_template="file: ./start_here.j2"
    ).new_fragment_template
    assert fmt == "The right one"


def test_file_with_path_search_order(temp_dir, changelog_d):
    # A file: spec with path components is relative to the changelog directory
    # and then the current directory.
    (changelog_d / "files").mkdir()
    (changelog_d / "files" / "start_here.j2").write_text("The right one")
    (temp_dir / "files").mkdir()
    (temp_dir / "files" / "start_here.j2").write_text("The wrong one")
    fmt = Config(
        new_fragment_template="file: files/start_here.j2"
    ).new_fragment_template
    assert fmt == "The right one"


def test_file_with_path_only_current_dir(temp_dir, changelog_d):
    # A file: spec with path components is relative to the changelog directory
    # and then the current directory.
    (temp_dir / "files").mkdir()
    (temp_dir / "files" / "start_here.j2").write_text("The right one")
    fmt = Config(
        new_fragment_template="file: files/start_here.j2"
    ).new_fragment_template
    assert fmt == "The right one"


def test_missing_file_with_path(temp_dir, changelog_d):
    # A file: spec with path components is relative to the current directory.
    (changelog_d / "start_here.j2").write_text("The wrong one")
    msg = (
        r"Couldn't read 'new_fragment_template' setting: "
        + r"No such file: there[/\\]start_here.j2"
    )
    with pytest.raises(ScrivException, match=msg):
        config = Config(new_fragment_template="file: there/start_here.j2")
        _ = config.new_fragment_template


def test_unknown_format():
    with pytest.raises(
        ScrivException,
        match=r"'format' must be in \['rst', 'md'\] \(got 'xyzzy'\)",
    ):
        Config(format="xyzzy")


def test_no_such_template():
    # If you specify a template name, and it doesn't exist, an error will
    # be raised.
    msg = (
        r"Couldn't read 'new_fragment_template' setting: "
        + r"No such file: foo\.j2"
    )
    with pytest.raises(ScrivException, match=msg):
        config = Config(new_fragment_template="file: foo.j2")
        _ = config.new_fragment_template


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


@pytest.mark.parametrize(
    "bad_spec, msg_rx",
    [
        (
            "literal: myproj.py",
            (
                r"Couldn't read 'version' setting: "
                + r"Missing value name: 'literal: myproj.py'"
            ),
        ),
        (
            "literal: myproj.py:",
            (
                r"Couldn't read 'version' setting: "
                + r"Missing value name: 'literal: myproj.py:'"
            ),
        ),
        (
            "literal: myproj.py:  version",
            (
                r"Couldn't read 'version' setting: "
                + r"Couldn't find literal 'version' in myproj.py: "
                + r"'literal: myproj.py:  version'"
            ),
        ),
        (
            "literal: : version",
            (
                r"Couldn't read 'version' setting: "
                + r"Missing file name: 'literal: : version'"
            ),
        ),
        (
            "literal: no_file.py: version",
            (
                r"Couldn't read 'version' setting: "
                + r"Couldn't find literal 'literal: no_file.py: version': "
                + r".* 'no_file.py'"
            ),
        ),
    ],
)
def test_bad_literal_spec(bad_spec, msg_rx, temp_dir):
    (temp_dir / "myproj.py").write_text("""nothing_to_see_here = 'hello'\n""")
    with pytest.raises(ScrivException, match=msg_rx):
        config = Config(version=bad_spec)
        _ = config.version


@pytest.mark.parametrize("chars", ["", "#", "#=-", "# ", "  "])
def test_rst_chars_is_two_chars(chars):
    # rst_header_chars must be exactly two non-space characters.
    msg = rf"Invalid configuration: 'rst_header_chars' must match.*'{chars}'"
    with pytest.raises(ScrivException, match=msg):
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

    @pytest.mark.skipif(tomllib is None, reason="No TOML support installed")
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
        with without_module(scriv.config, "tomllib"):
            msg_pat = r"Can't read .* without TOML support"
            with pytest.raises(ScrivException, match=msg_pat):
                Config.read()

    def test_no_toml_installed_no_settings(self, temp_dir):
        # Without toml installed, and also none of our settings in the toml
        # file, there is no exception.
        (temp_dir / "pyproject.toml").write_text(GENERIC_TOML_CONFIG)
        with without_module(scriv.config, "tomllib"):
            config = Config.read()
        assert config.categories[0] == "Removed"

    @pytest.mark.skipif(tomllib is None, reason="No TOML support installed")
    def test_nonstring_options(self, temp_dir):
        # Some config options are allowed to be e.g. TOML integers; for these,
        # both string and non-string values are valid.
        marker = "# other scriv options"
        for value in ('"6"', "6"):
            custom = f"{marker}\nmd_header_level = {value}"
            CUSTOM_TOML = TOML_CONFIG.replace(marker, custom)
            (temp_dir / "pyproject.toml").write_text(CUSTOM_TOML)
            config = Config.read()
            assert config.md_header_level == "6"


@pytest.mark.parametrize(
    "cmd_output, result",
    [
        ("Xyzzy 2 3\n", "Xyzzy 2 3"),
        ("Xyzzy 2 3\nAnother line\n", "Xyzzy 2 3\nAnother line\n"),
    ],
)
def test_command_running(mocker, cmd_output, result):
    # Any setting can be the output of a command.
    mocker.patch(
        "scriv.config.run_shell_command", lambda cmd: (True, cmd_output)
    )
    text = Config(output_file="command: doesnt-matter").output_file
    assert text == result


def test_real_command_running():
    text = Config(output_file="command: echo Xyzzy 2 3").output_file
    assert text == "Xyzzy 2 3"


@pytest.mark.parametrize(
    "bad_cmd, msg_rx",
    [
        (
            "xyzzyplugh",
            "Couldn't read 'output_file' setting: Command 'xyzzyplugh' failed:",
        ),
        (
            "'hi!2><",
            "Couldn't read 'output_file' setting: Command \"'hi!2><\" failed:",
        ),
    ],
)
def test_bad_command(fake_run_command, bad_cmd, msg_rx):
    # Any setting can be the output of a command.
    with pytest.raises(ScrivException, match=msg_rx):
        _ = Config(output_file=f"command: {bad_cmd}").output_file
