"""Tests of scriv/github.py"""

import json
import logging

import pytest
import requests

from scriv.github import (
    create_release,
    get_releases,
    github_paginated,
    update_release,
)


def test_one_page(responses):
    url = "https://api.github.com/repos/user/small_project/tags"
    data = [{"tag": word} for word in ["one", "two", "three", "four"]]
    responses.add(responses.GET, url, json=data)
    res = list(github_paginated(url))
    assert res == data


def test_three_pages(responses):
    # Three pages, referring to each other in the "link" header.
    url = "https://api.github.com/repos/user/large_project/tags"
    next_url = "https://api.github.com/repositories/138421996/tags"
    next_urls = [f"{next_url}?page={num}" for num in range(1, 4)]
    data = [
        [{"tag": f"{word}{num}"} for word in ["one", "two", "three", "four"]]
        for num in range(3)
    ]
    responses.add(
        responses.GET,
        url,
        json=data[0],
        headers={
            "link": f'<{next_urls[1]}>; rel="next", '
            + f'<{next_urls[2]}>; rel="last", ',
        },
    )
    responses.add(
        responses.GET,
        next_urls[1],
        json=data[1],
        headers={
            "link": f'<{next_urls[0]}>; rel="prev", '
            + f'<{next_urls[2]}>; rel="next", '
            + f'<{next_urls[2]}>; rel="last", '
            + f'<{next_urls[0]}>; rel="first"',
        },
    )
    responses.add(
        responses.GET,
        next_urls[2],
        json=data[2],
        headers={
            "link": f'<{next_urls[1]}>; rel="prev", '
            + f'<{next_urls[0]}>; rel="first"',
        },
    )
    res = list(github_paginated(url))
    assert res == data[0] + data[1] + data[2]


def test_bad_page(responses):
    url = "https://api.github.com/repos/user/small_project/secretstuff"
    responses.add(responses.GET, url, json=[], status=403)
    with pytest.raises(requests.HTTPError, match="403 Client Error"):
        list(github_paginated(url))


def test_get_releases(responses):
    url = "https://api.github.com/repos/user/small/releases"
    responses.add(
        responses.GET,
        url,
        json=[
            {"tag_name": "a", "name": "a", "prerelease": False},
            {"tag_name": "b", "name": "b", "prerelease": True},
        ],
    )
    releases = get_releases("user/small")
    assert releases == {
        "a": {"tag_name": "a", "name": "a", "prerelease": False},
        "b": {"tag_name": "b", "name": "b", "prerelease": True},
    }


RELEASE_DATA = {
    "name": "v3.14",
    "tag_name": "v3.14",
    "draft": False,
    "prerelease": False,
    "body": "this is a great release",
}


def test_create_release(responses, caplog):
    responses.add(
        responses.POST,
        "https://api.github.com/repos/someone/something/releases",
    )
    create_release("someone/something", RELEASE_DATA)
    assert json.loads(responses.calls[0].request.body) == RELEASE_DATA
    assert caplog.record_tuples == [
        ("root", logging.INFO, "Creating release v3.14")
    ]


def test_create_release_fails(responses):
    responses.add(
        responses.POST,
        "https://api.github.com/repos/someone/something/releases",
        status=500,
    )
    with pytest.raises(requests.HTTPError, match="500 Server Error"):
        create_release("someone/something", RELEASE_DATA)


def test_update_release(responses, caplog):
    url = "https://api.github.com/repos/someone/something/releases/60006815"
    responses.add(responses.PATCH, url)
    release = {"url": url}
    update_release(release, RELEASE_DATA)
    assert json.loads(responses.calls[0].request.body) == RELEASE_DATA
    assert caplog.record_tuples == [
        ("root", logging.INFO, "Updating release v3.14")
    ]


def test_update_release_fails(responses):
    url = "https://api.github.com/repos/someone/something/releases/60006815"
    responses.add(responses.PATCH, url, status=500)
    release = {"url": url}
    with pytest.raises(requests.HTTPError, match="500 Server Error"):
        update_release(release, RELEASE_DATA)
