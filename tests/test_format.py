"""Tests for scriv/format.py"""

import pytest

from scriv.config import Config
from scriv.format import new_template_text


def test_default_template():
    fmt = new_template_text(Config())
    assert "A new scriv entry" in fmt


def test_custom_template(changelog_d):
    # You can define your own template with your own name.
    (changelog_d / "start_here.j2").write_text("Custom template.")
    fmt = new_template_text(Config(new_entry_template="start_here.j2"))
    assert "Custom template." == fmt


def test_no_such_template():
    # If you specify a template name, and it doesn't exist, an error will be raised.
    config = Config(new_entry_template="foo.j2")
    with pytest.raises(Exception, match="No such template: changelog.d/foo.j2"):
        new_template_text(config)


def test_override_default_name(changelog_d):
    # You can define a file named new_entry.rst.j2, and it will be read
    # as the template.
    (changelog_d / "new_entry.rst.j2").write_text("Hello there!")
    fmt = new_template_text(Config())
    assert "Hello there!" == fmt
