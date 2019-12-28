"""Test creation logic."""

from freezegun import freeze_time

from scriv.config import Config
from scriv.create import new_entry_path


@freeze_time("2012-10-01")
def test_new_entry_path(mocker):
    mocker.patch("scriv.create.user_nick", side_effect=["joedev"])
    mocker.patch("scriv.create.current_branch_name", side_effect=["master"])
    config = Config(entry_directory="notes")
    assert new_entry_path(config) == "notes/20121001_joedev.rst"


@freeze_time("2013-02-25")
def test_new_entry_path_with_branch(mocker):
    mocker.patch("scriv.create.user_nick", side_effect=["joedev"])
    mocker.patch("scriv.create.current_branch_name", side_effect=["joedeveloper/feature-123.4"])
    config = Config(entry_directory="notes")
    assert new_entry_path(config) == "notes/20130225_joedev_feature_123_4.rst"
