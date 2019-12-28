"""Tests of scriv/config.py"""

from scriv.config import Config


def test_defaults():
    config = Config()
    assert config.entry_directory == "changelog.d"
    assert config.format == "rst"
