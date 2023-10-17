"""Tests of scriv/linkcheck.py"""

import pytest

from scriv.linkcheck import find_links


@pytest.mark.parametrize(
    "markdown_text, links",
    [
        ("Hello", []),
    ],
)
def test_find_links(markdown_text, links):
    found_links = sorted(find_links(markdown_text))
    assert links == found_links
