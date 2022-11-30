"""Tests of gitinfo.py"""

import re

from scriv.gitinfo import current_branch_name, get_github_repo, user_nick


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
    # With no git information, and no USER env var,
    # we just call the user "somebody"
    monkeypatch.delenv("USER", raising=False)
    assert user_nick() == "somebody"


def test_current_branch_name(fake_git):
    fake_git.set_branch("joedev/feature-123")
    assert current_branch_name() == "joedev/feature-123"


def test_get_github_repo_no_remotes(fake_git):
    assert get_github_repo() is None


def test_get_github_repo_one_github_remote(fake_git):
    fake_git.add_remote("mygithub", "git@github.com:joe/myproject.git")
    assert get_github_repo() == "joe/myproject"


def test_get_github_repo_one_github_remote_no_extension(fake_git):
    fake_git.add_remote("mygithub", "git@github.com:joe/myproject")
    assert get_github_repo() == "joe/myproject"


def test_get_github_repo_two_github_remotes(fake_git):
    fake_git.add_remote("mygithub", "git@github.com:joe/myproject.git")
    fake_git.add_remote("upstream", "git@github.com:psf/myproject.git")
    assert get_github_repo() is None


def test_get_github_repo_one_github_plus_others(fake_git):
    fake_git.add_remote("mygithub", "git@github.com:joe/myproject.git")
    fake_git.add_remote("upstream", "git@gitlab.com:psf/myproject.git")
    assert get_github_repo() == "joe/myproject"


def test_get_github_repo_no_github_remotes(fake_git):
    fake_git.add_remote("mygitlab", "git@gitlab.com:joe/myproject.git")
    fake_git.add_remote("upstream", "git@gitlab.com:psf/myproject.git")
    assert get_github_repo() is None


def test_real_get_github_repo():
    # Since we don't know the name of this repo (forks could be anything),
    # we can't be sure what we get, except it should be word/word, and not end
    # with .git
    repo = get_github_repo()
    assert repo is not None
    assert re.fullmatch(r"\w+/\w+", repo)
    assert not repo.endswith(".git")
