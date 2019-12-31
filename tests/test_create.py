"""Test creation logic."""

import freezegun
import pytest

from scriv.config import Config
from scriv.create import new_entry_contents, new_entry_path


@freezegun.freeze_time("2012-10-01")
def test_new_entry_path(mocker):
    mocker.patch("scriv.create.user_nick", side_effect=["joedev"])
    mocker.patch("scriv.create.current_branch_name", side_effect=["master"])
    config = Config(entry_directory="notes")
    assert new_entry_path(config) == "notes/20121001_joedev.rst"


@freezegun.freeze_time("2013-02-25")
def test_new_entry_path_with_branch(mocker):
    mocker.patch("scriv.create.user_nick", side_effect=["joedev"])
    mocker.patch("scriv.create.current_branch_name", side_effect=["joedeveloper/feature-123.4"])
    config = Config(entry_directory="notes")
    assert new_entry_path(config) == "notes/20130225_joedev_feature_123_4.rst"


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
