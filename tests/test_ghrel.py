"""Tests of scriv/ghrel.py."""

import logging
from unittest.mock import call

import pytest

CHANGELOG1 = """\
Some text before

v1.2.3 -- 2022-04-21
--------------------

A good release

Some fixes
----------

No version number in this section.

v1.0 -- 2020-02-20
------------------

Nothing to say.

v0.9a7 -- 2017-06-16
--------------------

A beginning

v0.0.1 -- 2001-01-01
--------------------

Didn't bother to tag this one.
"""

RELEASES1 = {
    "v1.0": {
        "url": "https://api.github.com/repos/joe/project/releases/120",
        "body": "Nothing to say.\n",
    },
    "v0.9a7": {
        "url": "https://api.github.com/repos/joe/project/releases/123",
        "body": "original body",
    },
}

V123_REL = {
    "body": "A good release\n",
    "name": "v1.2.3",
    "tag_name": "v1.2.3",
    "draft": False,
    "prerelease": False,
}

V097_REL = {
    "body": "A beginning\n",
    "name": "v0.9a7",
    "tag_name": "v0.9a7",
    "draft": False,
    "prerelease": True,
}


@pytest.fixture()
def scenario1(temp_dir, fake_git, mocker):
    """A common scenario for the tests."""
    fake_git.add_remote("origin", "git@github.com:joe/project.git")
    fake_git.add_tags(["v1.2.3", "v1.0", "v0.9a7"])
    (temp_dir / "CHANGELOG.rst").write_text(CHANGELOG1)
    mock_get_releases = mocker.patch("scriv.ghrel.get_releases")
    mock_get_releases.return_value = RELEASES1


def test_default(cli_invoke, scenario1, mocker, caplog):
    mock_create_release = mocker.patch("scriv.ghrel.create_release")
    mock_update_release = mocker.patch("scriv.ghrel.update_release")

    cli_invoke(["github-release"])

    assert mock_create_release.mock_calls == [call("joe/project", V123_REL)]
    assert mock_update_release.mock_calls == []
    assert caplog.record_tuples == [
        (
            "scriv.changelog",
            logging.INFO,
            "Reading changelog CHANGELOG.rst",
        ),
    ]


def test_dash_all(cli_invoke, scenario1, mocker, caplog):
    mock_create_release = mocker.patch("scriv.ghrel.create_release")
    mock_update_release = mocker.patch("scriv.ghrel.update_release")

    cli_invoke(["github-release", "--all"])

    assert mock_create_release.mock_calls == [call("joe/project", V123_REL)]
    assert mock_update_release.mock_calls == [
        call(RELEASES1["v0.9a7"], V097_REL),
    ]
    assert caplog.record_tuples == [
        (
            "scriv.changelog",
            logging.INFO,
            "Reading changelog CHANGELOG.rst",
        ),
        (
            "scriv.ghrel",
            logging.WARNING,
            "Entry 'Some fixes' has no version, skipping.",
        ),
        (
            "scriv.ghrel",
            logging.WARNING,
            "Version v0.0.1 has no tag. No release will be made.",
        ),
    ]


def test_explicit_repo(cli_invoke, scenario1, fake_git, mocker):
    # Add another GitHub remote, now there are two.
    fake_git.add_remote("upstream", "git@github.com:psf/project.git")

    mock_create_release = mocker.patch("scriv.ghrel.create_release")
    mock_update_release = mocker.patch("scriv.ghrel.update_release")

    cli_invoke(["github-release", "--repo=xyzzy/plugh"])

    assert mock_create_release.mock_calls == [call("xyzzy/plugh", V123_REL)]
    assert mock_update_release.mock_calls == []


@pytest.mark.parametrize(
    "repo", ["xyzzy", "https://github.com/xyzzy/plugh.git"]
)
def test_bad_explicit_repo(cli_invoke, repo):
    result = cli_invoke(["github-release", f"--repo={repo}"], expect_ok=False)
    assert result.exit_code == 1
    assert str(result.exception) == f"Repo must be owner/reponame: {repo!r}"


@pytest.fixture()
def no_actions(mocker, responses):
    """Check that nothing really happened."""
    mock_create_release = mocker.patch("scriv.ghrel.create_release")
    mock_update_release = mocker.patch("scriv.ghrel.update_release")

    yield

    assert mock_create_release.mock_calls == []
    assert mock_update_release.mock_calls == []
    assert len(responses.calls) == 0


def test_default_dry_run(cli_invoke, scenario1, no_actions, caplog):
    cli_invoke(["github-release", "--dry-run"])
    assert caplog.record_tuples == [
        (
            "scriv.changelog",
            logging.INFO,
            "Reading changelog CHANGELOG.rst",
        ),
        ("scriv.ghrel", logging.INFO, "Would create release v1.2.3"),
        ("scriv.ghrel", logging.INFO, "Body:\nA good release\n"),
    ]


def test_dash_all_dry_run(cli_invoke, scenario1, no_actions, caplog):
    cli_invoke(["github-release", "--all", "--dry-run"])
    assert caplog.record_tuples == [
        (
            "scriv.changelog",
            logging.INFO,
            "Reading changelog CHANGELOG.rst",
        ),
        ("scriv.ghrel", logging.INFO, "Would create release v1.2.3"),
        ("scriv.ghrel", logging.INFO, "Body:\nA good release\n"),
        (
            "scriv.ghrel",
            logging.WARNING,
            "Entry 'Some fixes' has no version, skipping.",
        ),
        ("scriv.ghrel", logging.INFO, "Would update release v0.9a7"),
        ("scriv.ghrel", logging.INFO, "Body:\nA beginning\n"),
        (
            "scriv.ghrel",
            logging.WARNING,
            "Version v0.0.1 has no tag. No release will be made.",
        ),
    ]


def test_no_github_repo(cli_invoke, scenario1, fake_git):
    fake_git.remove_remote("origin")
    result = cli_invoke(["github-release"], expect_ok=False)
    assert result.exit_code == 1
    assert result.output == (
        "Reading changelog CHANGELOG.rst\n" + "Couldn't find a GitHub repo\n"
    )


def test_no_clear_github_repo(cli_invoke, scenario1, fake_git):
    # Add another GitHub remote, now there are two.
    fake_git.add_remote("upstream", "git@github.com:psf/project.git")
    result = cli_invoke(["github-release"], expect_ok=False)
    assert result.exit_code == 1
    assert result.output == (
        "Reading changelog CHANGELOG.rst\n"
        + "More than one GitHub repo found: joe/project, psf/project\n"
    )


def test_with_template(cli_invoke, temp_dir, scenario1, mocker):
    (temp_dir / "setup.cfg").write_text(
        """
        [scriv]
        ghrel_template = |{{body}}|{{config.format}}|{{version}}
        """
    )
    mock_create_release = mocker.patch("scriv.ghrel.create_release")

    cli_invoke(["github-release"])

    expected = dict(V123_REL)
    expected["body"] = "|A good release\n|rst|v1.2.3"

    assert mock_create_release.mock_calls == [call("joe/project", expected)]
