"""Tests for scriv/format_rst.py."""

import collections
import textwrap

import pytest

from scriv.config import Config
from scriv.format_rst import RstTools


@pytest.mark.parametrize(
    "text, parsed",
    [
        # Comments are ignored, and the section headers found.
        pytest.param(
            """\
            .. Comments can be here
            .. and here.
            ..
            .. and here.
            Added
            -----

            - This thing was added.
              And we liked it.

            .. More comments can be here
            ..
            .. And here.

            """,
            {"Added": ["- This thing was added.\n  And we liked it."]},
            id="comments_ignored",
        ),
        # Multiple section headers.
        pytest.param(
            """\
            Added
            -----

            - This thing was added.
              And we liked it.


            Fixed
            -----

            - This thing was fixed.

            - Another thing was fixed.

            Added
            -----

            - Also added
              this thing
              that is very important.

            """,
            {
                "Added": [
                    "- This thing was added.\n  And we liked it.",
                    "- Also added\n  this thing\n  that is very important.",
                ],
                "Fixed": [
                    "- This thing was fixed.",
                    "- Another thing was fixed.",
                ],
            },
            id="multiple_headers",
        ),
        # The specific character used for the header line is unimportant.
        pytest.param(
            """\
            Added
            ^^^^^
            - This thing was added.

            Fixed
            ^^^^^
            - This thing was fixed.
            """,
            {
                "Added": ["- This thing was added."],
                "Fixed": ["- This thing was fixed."],
            },
            id="different_underlines",
        ),
        # You can even use periods as the underline, it won't be confused for a
        # comment.
        pytest.param(
            """\
            Fixed
            .....
            - This thing was fixed.

            Added
            .....

            .. a comment.

            - This thing was added.
            """,
            {
                "Added": ["- This thing was added."],
                "Fixed": ["- This thing was fixed."],
            },
            id="period_underline",
        ),
        # It's fine to have no header at all.
        pytest.param(
            """\
            - No header at all.
            """,
            {None: ["- No header at all."]},
            id="no_header",
        ),
        # It's fine to have comments with no header, and multiple bulllets.
        pytest.param(
            """\
            .. This is a scriv fragment.

            - No header at all.

            - Just plain bullets.
            """,
            {None: ["- No header at all.", "- Just plain bullets."]},
            id="no_header_2",
        ),
        # RST syntax is intricate. We understand a subset of it.
        pytest.param(
            """\
            .. _fixed.1:

            Fixed
            .....
            - This thing was fixed: `issue 42`_.

            .. _issue 42: https://github.com/thing/issue/42

            .. _added:

            Added
            .....

            .. a comment.

            - This thing was added.

            .. note::
                This thing doesn't work yet.
                Not sure it ever will... :(

            """,
            {
                "Added": [
                    "- This thing was added.",
                    (
                        ".. note::\n"
                        + "    This thing doesn't work yet.\n"
                        + "    Not sure it ever will... :("
                    ),
                ],
                "Fixed": [
                    "- This thing was fixed: `issue 42`_.",
                    ".. _issue 42: https://github.com/thing/issue/42",
                ],
            },
            id="intricate_syntax",
        ),
        # A file with only comments and blanks will produce nothing.
        pytest.param(
            """\
            .. Nothing to see here.
            ..

            .. Or here.


            """,
            {},
            id="empty",
        ),
        # Multiple levels of headings only splits on the top-most one.
        pytest.param(
            """\
            (prelude)

            Section one
            ===========

            subhead
            -------

            In the sub

            subhead 2
            ---------

            Also sub

            Section two
            ===========

            In section two.

            subhead 3
            ---------
            s2s3
            """,
            {
                None: ["(prelude)"],
                "Section one": [
                    "subhead\n-------",
                    "In the sub",
                    "subhead 2\n---------",
                    "Also sub",
                ],
                "Section two": [
                    "In section two.",
                    "subhead 3\n---------\ns2s3",
                ],
            },
            id="multilevel",
        ),
    ],
)
def test_parse_text(text, parsed):
    actual = RstTools().parse_text(textwrap.dedent(text))
    assert actual == parsed


@pytest.mark.parametrize(
    "sections, expected",
    [
        pytest.param(
            [
                (
                    "Added",
                    [
                        "- This thing was added.\n  And we liked it.",
                        "- Also added\n  this thing\n  that is very important.",
                    ],
                ),
                (
                    "Fixed",
                    ["- This thing was fixed.", "- Another thing was fixed."],
                ),
            ],
            """\

            Added
            ~~~~~

            - This thing was added.
              And we liked it.

            - Also added
              this thing
              that is very important.

            Fixed
            ~~~~~

            - This thing was fixed.

            - Another thing was fixed.
            """,
            id="one",
        ),
        pytest.param(
            [
                (
                    None,
                    [
                        "- This thing was added.\n  And we liked it.",
                        "- Also added\n  this thing\n  that is very important.",
                    ],
                ),
            ],
            """\

            - This thing was added.
              And we liked it.

            - Also added
              this thing
              that is very important.
            """,
            id="two",
        ),
    ],
)
def test_format_sections(sections, expected):
    sections = collections.OrderedDict(sections)
    actual = RstTools(Config(rst_header_chars="#~")).format_sections(sections)
    assert actual == textwrap.dedent(expected)


@pytest.mark.parametrize(
    "config_kwargs, text, fh_kwargs, result",
    [
        ({}, "2020-07-26", {}, "\n2020-07-26\n==========\n"),
        (
            {"rst_header_chars": "*-"},
            "2020-07-26",
            {},
            "\n2020-07-26\n**********\n",
        ),
        (
            {},
            "2022-04-03",
            {"anchor": "here"},
            "\n.. _here:\n\n2022-04-03\n==========\n",
        ),
    ],
)
def test_format_header(config_kwargs, text, fh_kwargs, result):
    actual = RstTools(Config(**config_kwargs)).format_header(text, **fh_kwargs)
    assert actual == result
