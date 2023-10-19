"""Tests of scriv/linkcheck.py"""

import logging
import textwrap

import pytest

from scriv.linkcheck import check_markdown_links, find_links


@pytest.mark.parametrize(
    "markdown_text, links",
    [
        ("Hello", []),
        (
            """\
            [one](https://two.com/hello) and
            [two](https://one.com/xyzzy).
         """,
            ["https://one.com/xyzzy", "https://two.com/hello"],
        ),
        (
            """\
            This is [an example](http://example1.com/ "Title") inline link.
            This is [an example] [id] reference-style link.

            [id]: http://example2.com/  "Optional Title Here"
         """,
            ["http://example1.com/", "http://example2.com/"],
        ),
    ],
)
def test_find_links(markdown_text, links):
    found_links = sorted(find_links(textwrap.dedent(markdown_text)))
    assert links == found_links


def test_check_markdown_link(caplog, responses):
    caplog.set_level(logging.DEBUG, logger="scriv.linkcheck")
    responses.head("https://nedbat.com")
    check_markdown_links("""[hey](https://nedbat.com)!""")
    assert caplog.record_tuples == [
        (
            "scriv.linkcheck",
            logging.DEBUG,
            "OK link: 'https://nedbat.com'",
        )
    ]


def test_check_404_markdown_link(caplog, responses):
    responses.head("https://nedbat.com", status=404)
    check_markdown_links("""[hey](https://nedbat.com)!""")
    assert caplog.record_tuples == [
        (
            "scriv.linkcheck",
            logging.WARNING,
            "Failed check for 'https://nedbat.com': status code 404",
        )
    ]


def test_check_failing_markdown_link(caplog, responses):
    responses.head("https://nedbat.com", body=Exception("Buh?"))
    check_markdown_links("""[hey](https://nedbat.com)!""")
    assert caplog.record_tuples == [
        (
            "scriv.linkcheck",
            logging.WARNING,
            "Failed check for 'https://nedbat.com': Buh?",
        )
    ]
