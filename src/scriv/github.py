"""Helpers for the GitHub REST API."""

import logging
import os
from typing import Any, Dict, Iterable

import requests

logger = logging.getLogger()


# Only wait up to a minute for GitHub to respond.
TIMEOUT = 60


def check_ok(resp):
    """
    Check that the Requests response object was successful.

    Raise an exception if not.
    """
    if not resp:
        logger.error(f"text: {resp.text!r}")
        resp.raise_for_status()


def auth_headers() -> Dict[str, str]:
    """
    Get the authorization headers needed for GitHub.

    Will read the GITHUB_TOKEN environment variable.
    """
    headers = {}
    token = os.environ.get("GITHUB_TOKEN", "")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def github_paginated(url: str) -> Iterable[Dict[str, Any]]:
    """
    Get all the results from a paginated GitHub url.
    """
    while True:
        resp = requests.get(url, headers=auth_headers(), timeout=TIMEOUT)
        check_ok(resp)
        yield from resp.json()
        next_link = resp.links.get("next", None)
        if not next_link:
            break
        url = next_link["url"]


RELEASES_URL = "https://api.github.com/repos/{repo}/releases"


def get_releases(repo: str) -> Dict[str, Dict[str, Any]]:
    """
    Get all the releases from a name/project repo.

    Returns:
        A dict mapping tag names to release dictionaries.
    """
    url = RELEASES_URL.format(repo=repo)
    releases = {r["tag_name"]: r for r in github_paginated(url)}
    return releases


def create_release(repo: str, release_data: Dict[str, Any]) -> None:
    """
    Create a GitHub release.

    Arguments:
        repo: A user/repo string, like "nedbat/scriv".
        release_data: A dict with the data needed to create the release.
            It should have these keys:
                body: the markdown description of the release.
                name: the name of the release
                tag_name: the Git tag for the release
                draft: a boolean
                prerelease: a boolean
    """
    logger.info(f"Creating release {release_data['name']}")
    url = RELEASES_URL.format(repo=repo)
    resp = requests.post(
        url, json=release_data, headers=auth_headers(), timeout=TIMEOUT
    )
    check_ok(resp)


def update_release(
    release: Dict[str, Any], release_data: Dict[str, Any]
) -> None:
    """
    Update a GitHub release.

    Arguments:
        release: the full data from GitHub for the release to update.
        release_data: a dict with the data we want to update.
            See create_release for the accepted keys.
    """
    logger.info(f"Updating release {release_data['name']}")
    resp = requests.patch(
        release["url"],
        json=release_data,
        headers=auth_headers(),
        timeout=TIMEOUT,
    )
    check_ok(resp)
