"""Tests of gitinfo.py"""

from scriv.gitinfo import current_branch_name, user_nick


def test_user_nick_from_github(fake_run_command):
    fake_run_command.add_fake("git config --get github.user", (True, "joedev\n"))
    assert user_nick() == "joedev"


def test_user_nick_from_git(fake_run_command):
    fake_run_command.add_fake("git config --get user.email", (True, "joesomeone@somewhere.org\n"))
    assert user_nick() == "joesomeone"


def test_user_nick_from_env(fake_run_command, monkeypatch):  # pylint: disable=unused-argument
    monkeypatch.setenv("USER", "joseph")
    assert user_nick() == "joseph"


def test_user_nick_from_nowhere(fake_run_command, monkeypatch):  # pylint: disable=unused-argument
    # With no git information, and no USER env var, we just call the user "somebody"
    monkeypatch.delenv("USER", raising=False)
    assert user_nick() == "somebody"


def test_current_branch_name(fake_run_command):
    fake_run_command.add_fake("git rev-parse --abbrev-ref HEAD", (True, "joedev/feature-123"))
    assert current_branch_name() == "joedev/feature-123"
