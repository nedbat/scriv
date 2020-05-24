"""Tests for scriv.format_rst.py."""

import collections
import textwrap

import pytest

from scriv.config import Config
from scriv.format_rst import RstTools


@pytest.mark.parametrize(
    "text, parsed",
    [
        (
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
        ),
        (
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
                "Fixed": ["- This thing was fixed.", "- Another thing was fixed."],
            },
        ),
    ],
)
def test_parse_text(text, parsed):
    actual = RstTools().parse_text(textwrap.dedent(text))
    assert parsed == actual


def test_format_sections():
    sections = collections.OrderedDict(
        [
            (
                "Added",
                [
                    "- This thing was added.\n  And we liked it.",
                    "- Also added\n  this thing\n  that is very important.",
                ],
            ),
            ("Fixed", ["- This thing was fixed.", "- Another thing was fixed."]),
        ]
    )
    expected = """\

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
        """
    actual = RstTools(Config(rst_header_char="~")).format_sections(sections)
    assert textwrap.dedent(expected) == actual
