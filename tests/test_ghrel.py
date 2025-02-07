"""Tests of scriv/ghrel.py."""

import json
import logging
from typing import Any
from unittest.mock import call

import pytest

from .helpers import check_logs

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

v0.1 -- 2010-01-01
------------------

Didn't bother to tag this one.

v0.0.1 -- 2001-01-01
--------------------

Very first.

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
    "v0.0.1": {
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

V001_REL = {
    "body": "Very first.\n",
    "name": "v0.0.1",
    "tag_name": "v0.0.1",
    "draft": False,
    "prerelease": False,
}


@pytest.fixture()
def scenario1(temp_dir, fake_git, mocker):
    """A common scenario for the tests."""
    fake_git.add_remote("origin", "git@github.com:joe/project.git")
    fake_git.add_tags(["v1.2.3", "v1.0", "v0.9a7", "v0.0.1"])
    (temp_dir / "CHANGELOG.rst").write_text(CHANGELOG1)
    mock_get_releases = mocker.patch("scriv.ghrel.get_releases")
    mock_get_releases.return_value = RELEASES1


@pytest.fixture()
def mock_create_release(mocker):
    """Create a mock create_release that checks arguments."""

    def _create_release(repo: str, release_data: dict[str, Any]) -> None:
        assert repo
        assert release_data["name"]
        assert json.dumps(release_data)[0] == "{"

    return mocker.patch(
        "scriv.ghrel.create_release", side_effect=_create_release
    )


@pytest.fixture()
def mock_update_release(mocker):
    """Create a mock update_release that checks arguments."""

    def _update_release(
        release: dict[str, Any], release_data: dict[str, Any]
    ) -> None:
        assert release_data["name"]
        assert release["url"]
        assert json.dumps(release_data)[0] == "{"

    return mocker.patch(
        "scriv.ghrel.update_release", side_effect=_update_release
    )


def test_default(
    cli_invoke, scenario1, mock_create_release, mock_update_release, caplog
):
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


def test_dash_all(
    cli_invoke, scenario1, mock_create_release, mock_update_release, caplog
):
    cli_invoke(["github-release", "--all"])

    assert mock_create_release.mock_calls == [call("joe/project", V123_REL)]
    assert mock_update_release.mock_calls == [
        call(RELEASES1["v0.9a7"], V097_REL),
        call(RELEASES1["v0.0.1"], V001_REL),
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
            "Version v0.1 has no tag. No release will be made.",
        ),
    ]


def test_explicit_repo(
    cli_invoke, scenario1, fake_git, mock_create_release, mock_update_release
):
    # Add another GitHub remote, now there are two.
    fake_git.add_remote("upstream", "git@github.com:psf/project.git")

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


def test_check_links(cli_invoke, scenario1, mocker):
    mock_check_links = mocker.patch("scriv.ghrel.check_markdown_links")
    cli_invoke(["github-release", "--all", "--dry-run", "--check-links"])
    assert mock_check_links.mock_calls == [
        call("A good release\n"),
        call("Nothing to say.\n"),
        call("A beginning\n"),
        call("Very first.\n"),
    ]


@pytest.fixture()
def no_actions(mock_create_release, mock_update_release, responses):
    """Check that nothing really happened."""

    yield

    assert mock_create_release.mock_calls == []
    assert mock_update_release.mock_calls == []
    assert len(responses.calls) == 0


def test_default_dry_run(cli_invoke, scenario1, no_actions, caplog):
    cli_invoke(["github-release", "--dry-run"])
    check_logs(
        caplog,
        [
            (
                "scriv.changelog",
                logging.INFO,
                "Reading changelog CHANGELOG.rst",
            ),
            ("scriv.ghrel", logging.INFO, "Would create release v1.2.3"),
        ],
    )


def test_dash_all_dry_run(cli_invoke, scenario1, no_actions, caplog):
    cli_invoke(["github-release", "--all", "--dry-run"])
    check_logs(
        caplog,
        [
            (
                "scriv.changelog",
                logging.INFO,
                "Reading changelog CHANGELOG.rst",
            ),
            ("scriv.ghrel", logging.INFO, "Would create release v1.2.3"),
            (
                "scriv.ghrel",
                logging.WARNING,
                "Entry 'Some fixes' has no version, skipping.",
            ),
            ("scriv.ghrel", logging.INFO, "Would update release v0.9a7"),
            (
                "scriv.ghrel",
                logging.WARNING,
                "Version v0.1 has no tag. No release will be made.",
            ),
            ("scriv.ghrel", 20, "Would update release v0.0.1"),
        ],
    )


def test_dash_all_dry_run_debug(cli_invoke, scenario1, no_actions, caplog):
    cli_invoke(["github-release", "--all", "--dry-run", "--verbosity=debug"])
    check_logs(
        caplog,
        [
            (
                "scriv.changelog",
                logging.INFO,
                "Reading changelog CHANGELOG.rst",
            ),
            (
                "scriv.ghrel",
                logging.DEBUG,
                "Creating release, data = {'body': 'A good release\\n', 'name': 'v1.2.3', "
                + "'tag_name': 'v1.2.3', 'draft': False, 'prerelease': False}",
            ),
            ("scriv.ghrel", logging.INFO, "Would create release v1.2.3"),
            ("scriv.ghrel", logging.DEBUG, "Body:\nA good release\n"),
            (
                "scriv.ghrel",
                logging.WARNING,
                "Entry 'Some fixes' has no version, skipping.",
            ),
            (
                "scriv.ghrel",
                logging.DEBUG,
                "Updating release v0.9a7, data = {'body': 'A beginning\\n', 'name': "
                + "'v0.9a7', 'tag_name': 'v0.9a7', 'draft': False, 'prerelease': True}",
            ),
            ("scriv.ghrel", logging.INFO, "Would update release v0.9a7"),
            ("scriv.ghrel", logging.DEBUG, "Body:\nA beginning\n"),
            (
                "scriv.ghrel",
                logging.WARNING,
                "Version v0.1 has no tag. No release will be made.",
            ),
            (
                "scriv.ghrel",
                logging.DEBUG,
                "Updating release v0.0.1, data = {'body': 'Very first.\\n', 'name': "
                + "'v0.0.1', 'tag_name': 'v0.0.1', 'draft': False, 'prerelease': False}",
            ),
            ("scriv.ghrel", logging.INFO, "Would update release v0.0.1"),
            ("scriv.ghrel", logging.DEBUG, "Body:\nVery first.\n"),
        ],
    )


def test_no_github_repo(cli_invoke, scenario1, fake_git):
    fake_git.remove_remote("origin")
    result = cli_invoke(["github-release"], expect_ok=False)
    assert result.exit_code == 1
    assert result.output == "Couldn't find a GitHub repo\n"


def test_no_clear_github_repo(cli_invoke, scenario1, fake_git):
    # Add another GitHub remote, now there are two.
    fake_git.add_remote("upstream", "git@github.com:psf/project.git")
    result = cli_invoke(["github-release"], expect_ok=False)
    assert result.exit_code == 1
    assert result.output == (
        "More than one GitHub repo found: joe/project, psf/project\n"
    )


def test_with_template(cli_invoke, temp_dir, scenario1, mock_create_release):
    (temp_dir / "setup.cfg").write_text(
        """
        [scriv]
        ghrel_template = |{{body}}|{{config.format}}|{{version}}
        """
    )
    cli_invoke(["github-release"])

    expected = dict(V123_REL)
    expected["body"] = "|A good release\n|rst|v1.2.3"

    assert mock_create_release.mock_calls == [call("joe/project", expected)]
