"""
Tests of tests/faker.py

Mostly error paths, since the happy paths are covered by other tests.
"""

import re

import pytest

from scriv import shell


def test_no_such_command(fake_run_command):
    assert shell.run_command("wut") == (
        False,
        "no fake command handler: ['wut']",
    )


def test_no_such_git_command(fake_git):
    assert shell.run_command("git hello") == (
        False,
        "no fake git command: ['git', 'hello']",
    )
    assert shell.run_command("git config --wut") == (
        False,
        "no fake git command: ['git', 'config', '--wut']",
    )


@pytest.mark.parametrize(
    "name",
    [
        "foo.bar",
        "foo.bar12",
        "foo.bar-",
        "foo.bar-bar",
        "foo-foo.bar",
        "section.subsection.bar",
        "section.some/sub_section!ok.bar",
    ],
)
def test_git_set_config_good_names(name, fake_git):
    val = "xyzzy plugh!?"
    fake_git.set_config(name, val)
    result = shell.run_command(f"git config --get {name}")
    assert result == (True, val + "\n")


@pytest.mark.parametrize(
    "name",
    [
        "bar",
        "foo.12bar",
        "foo.bar_bar",
        "foo_foo.bar",
    ],
)
def test_git_set_config_bad_names(name, fake_git):
    with pytest.raises(ValueError, match=re.escape(f"invalid key: {name!r}")):
        fake_git.set_config(name, "hello there")
