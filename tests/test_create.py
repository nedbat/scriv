"""Test creation logic."""

import freezegun
import pytest

from scriv.config import Config
from scriv.create import create, new_entry_contents, new_entry_path


@freezegun.freeze_time("2012-10-01T07:08:09")
def test_new_entry_path(mocker):
    mocker.patch("scriv.create.user_nick", side_effect=["joedev"])
    mocker.patch("scriv.create.current_branch_name", side_effect=["master"])
    config = Config(entry_directory="notes")
    assert new_entry_path(config) == "notes/20121001_0708_joedev.rst"


@freezegun.freeze_time("2013-02-25T15:16:17")
def test_new_entry_path_with_branch(mocker):
    mocker.patch("scriv.create.user_nick", side_effect=["joedev"])
    mocker.patch("scriv.create.current_branch_name", side_effect=["joedeveloper/feature-123.4"])
    config = Config(entry_directory="notes")
    assert new_entry_path(config) == "notes/20130225_1516_joedev_feature_123_4.rst"


def test_new_entry_contents_rst():
    config = Config(format="rst")
    contents = new_entry_contents(config)
    assert contents.startswith(".. ")
    assert "A new scriv entry" in contents
    assert ".. Added\n.. -----\n" in contents
    assert all(cat in contents for cat in config.categories)


def test_new_entry_contents_md():
    config = Config(format="md")
    contents = new_entry_contents(config)
    assert contents.startswith("<!--")
    assert "A new scriv entry" in contents
    assert "### Added\n" in contents
    assert all(cat in contents for cat in config.categories)


def test_new_entry_contents_unknown():
    config = Config(format="xyzzy")
    with pytest.raises(Exception, match="Unknown format: xyzzy"):
        new_entry_contents(config)


def test_create_no_output_directory(cli_runner):
    # With no changelog.d directory, create fails with a FileNotFoundError.
    result = cli_runner.invoke(create)
    assert result.exit_code == 1
    assert isinstance(result.exception, FileNotFoundError)
    assert "changelog.d" in str(result.exception)


def test_create_entry(cli_runner, changelog_d):
    # Create will make one file with the current time in the name.
    with freezegun.freeze_time("2013-02-25T15:16:17"):
        result = cli_runner.invoke(create)

    assert result.exit_code == 0
    entries = sorted(changelog_d.iterdir())
    assert len(entries) == 1
    entry = entries[0]
    assert "20130225_1516_somebody.rst" == entry.name
    contents = entry.read_text()
    assert "A new scriv entry" in contents
    assert ".. Added\n.. -----\n" in contents

    # Using create later will make a second file with a new timestamp.
    with freezegun.freeze_time("2013-02-25T15:18:19"):
        result = cli_runner.invoke(create)

    assert result.exit_code == 0
    entries = sorted(changelog_d.iterdir())
    assert len(entries) == 2
    entry = entries[-1]
    assert "20130225_1518_somebody.rst" == entry.name
