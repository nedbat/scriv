"""Tests of gitinfo.py"""

from scriv.gitinfo import current_branch_name, user_nick


def test_user_nick_from_github(fake_git):
    fake_git.set_config("github.user", "joedev")
    assert user_nick() == "joedev"


def test_user_nick_from_git(fake_git):
    fake_git.set_config("user.email", "joesomeone@somewhere.org")
    assert user_nick() == "joesomeone"


def test_user_nick_from_env(fake_git, monkeypatch):
    monkeypatch.setenv("USER", "joseph")
    assert user_nick() == "joseph"


def test_user_nick_from_nowhere(fake_git, monkeypatch):
    # With no git information, and no USER env var, we just call the user "somebody"
    monkeypatch.delenv("USER", raising=False)
    assert user_nick() == "somebody"


def test_current_branch_name(fake_git):
    fake_git.set_branch("joedev/feature-123")
    assert current_branch_name() == "joedev/feature-123"
