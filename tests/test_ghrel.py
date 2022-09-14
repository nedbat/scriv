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


@pytest.fixture()
def scenario1(temp_dir, fake_git):
    """A common scenario for the tests."""
    fake_git.add_remote("origin", "git@github.com:joe/project.git")
    fake_git.add_tags(["v1.2.3", "v1.0", "v0.9a7"])
    (temp_dir / "CHANGELOG.rst").write_text(CHANGELOG1)


@pytest.mark.parametrize("all_entries", [False, True])
def test_everything(all_entries, cli_invoke, scenario1, mocker, caplog):
    mock_get_releases = mocker.patch("scriv.ghrel.get_releases")
    releases = {
        "v1.0": {
            "url": "https://api.github.com/repos/joe/project/releases/120",
            "body": "Nothing to say.\n",
        },
        "v0.9a7": {
            "url": "https://api.github.com/repos/joe/project/releases/123",
            "body": "original body",
        },
    }
    mock_get_releases.return_value = releases
    mock_create_release = mocker.patch("scriv.ghrel.create_release")
    mock_update_release = mocker.patch("scriv.ghrel.update_release")

    if all_entries:
        cli_invoke(["github-release", "--all"])
    else:
        cli_invoke(["github-release"])

    assert mock_create_release.mock_calls == [
        call(
            "joe/project",
            {
                "body": "A good release\n",
                "name": "v1.2.3",
                "tag_name": "v1.2.3",
                "draft": False,
                "prerelease": False,
            },
        ),
    ]
    if all_entries:
        assert mock_update_release.mock_calls == [
            call(
                releases["v0.9a7"],
                {
                    "body": "A beginning\n",
                    "name": "v0.9a7",
                    "tag_name": "v0.9a7",
                    "draft": False,
                    "prerelease": True,
                },
            ),
        ]
        assert caplog.record_tuples == [
            (
                "root",
                logging.WARNING,
                "Entry 'Some fixes' has no version, skipping.",
            ),
            (
                "root",
                logging.WARNING,
                "Version v0.0.1 has no tag. No release will be made.",
            ),
        ]
    else:
        assert mock_update_release.mock_calls == []
        assert caplog.record_tuples == []


def test_no_clear_github_repo(cli_invoke, scenario1, fake_git):
    # Add another GitHub remote, now there are two.
    fake_git.add_remote("upstream", "git@github.com:psf/project.git")
    result = cli_invoke(["github-release"], expect_ok=False)
    assert result.exit_code == 1
    assert result.output == "Couldn't determine GitHub repo.\n"
