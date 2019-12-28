"""Tests of gitinfo.py"""

from typing import Callable, Dict, Tuple

import scriv.gitinfo
from scriv.gitinfo import user_nick


def run_command_faker(in_out: Dict[str, Tuple[bool, str]]) -> Callable[[str], Tuple[bool, str]]:
    def fake_run_command(cmd: str) -> Tuple[bool, str]:
        return in_out[cmd]

    return fake_run_command


def test_user_nick_from_github(mocker):
    mocker.patch.object(
        scriv.gitinfo, "run_command", run_command_faker({"git config --get github.user": (True, "joedev\n")})
    )
    assert user_nick() == "joedev"


def test_user_nick_from_git(mocker):
    mocker.patch.object(
        scriv.gitinfo,
        "run_command",
        run_command_faker(
            {
                "git config --get github.user": (False, ""),
                "git config --get user.email": (True, "joesomeone@somewhere.org\n"),
            }
        ),
    )
    assert user_nick() == "joesomeone"


def test_user_nick_from_env(mocker, monkeypatch):
    mocker.patch.object(
        scriv.gitinfo,
        "run_command",
        run_command_faker({"git config --get github.user": (False, ""), "git config --get user.email": (False, "")}),
    )
    monkeypatch.setenv("USER", "joseph")
    assert user_nick() == "joseph"


def test_user_nick_from_nowhere(mocker):
    mocker.patch.object(
        scriv.gitinfo,
        "run_command",
        run_command_faker({"git config --get github.user": (False, ""), "git config --get user.email": (False, "")}),
    )
    assert user_nick() == "somebody"
