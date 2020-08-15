"""Tests for scriv/format_md.py."""

import collections
import textwrap

import pytest

from scriv.config import Config
from scriv.format_md import MdTools


@pytest.mark.parametrize(
    "text, parsed",
    [
        # Comments are ignored, and the section headers found.
        pytest.param(
            """\
            <!--
            Comments can be here
            and here.

            and here.
            -->

            # Added

            - This thing was added.
              And we liked it.

            <!-- don't worry about this... -->

            - Another thing we added.

            <!--
            More comments can be here

            And here.
            -->
            """,
            {
                "Added": [
                    "- This thing was added.\n  And we liked it.",
                    "- Another thing we added.",
                ]
            },
            id="comments_ignored",
        ),
        # Multiple section headers.
        pytest.param(
            """\
            # Added

            - This thing was added.
              And we liked it.


            # Fixed

            - This thing was fixed.

            - Another thing was fixed.

            # Added

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
            <!-- This is a scriv fragment. -->

            - No header at all.

            - Just plain bullets.
            """,
            {None: ["- No header at all.", "- Just plain bullets."]},
            id="no_header_2",
        ),
        # A file with only comments and blanks will produce nothing.
        pytest.param(
            """\
            <!-- Nothing to see here.
            -->

            <!-- Or here. -->


            """,
            {},
            id="empty",
        ),
    ],
)
def test_parse_text(text, parsed):
    actual = MdTools().parse_text(textwrap.dedent(text))
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

            ### Added

            - This thing was added.
              And we liked it.

            - Also added
              this thing
              that is very important.

            ### Fixed

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
    actual = MdTools(Config(md_header_level="2")).format_sections(sections)
    assert actual == textwrap.dedent(expected)


@pytest.mark.parametrize(
    "config_kwargs, text, result",
    [
        ({}, "2020-07-26", "\n# 2020-07-26\n"),
        ({"md_header_level": "3"}, "2020-07-26", "\n### 2020-07-26\n"),
    ],
)
def test_format_header(config_kwargs, text, result):
    actual = MdTools(Config(**config_kwargs)).format_header(text)
    assert actual == result
