"""Tests of gitinfo.py"""

from typing import Tuple

import pytest

from scriv.gitinfo import user_nick


class RunCommandFaker:
    """
    A fake implementation of run_command.

    Add results for commands with `add_fake`.
    """

    def __init__(self):
        self.in_out = {}

    def add_fake(self, cmd: str, result: Tuple[bool, str]) -> None:
        self.in_out[cmd] = result

    def __call__(self, cmd: str) -> Tuple[bool, str]:
        return self.in_out.get(cmd, (False, ""))


@pytest.fixture(name="fake_run_command")
def fake_run_command_fixture(mocker):
    """Replace gitinfo.run_command with a fake."""
    frc = RunCommandFaker()
    mocker.patch("scriv.gitinfo.run_command", frc)
    return frc


def test_user_nick_from_github(fake_run_command):
    fake_run_command.add_fake("git config --get github.user", (True, "joedev\n"))
    assert user_nick() == "joedev"


def test_user_nick_from_git(fake_run_command):
    fake_run_command.add_fake("git config --get user.email", (True, "joesomeone@somewhere.org\n"))
    assert user_nick() == "joesomeone"


def test_user_nick_from_env(fake_run_command, monkeypatch):  # pylint: disable=unused-argument
    monkeypatch.setenv("USER", "joseph")
    assert user_nick() == "joseph"


def test_user_nick_from_nowhere(fake_run_command):  # pylint: disable=unused-argument
    assert user_nick() == "somebody"
