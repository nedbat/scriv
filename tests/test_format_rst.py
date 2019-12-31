"""Tests for scriv.format_rst.py."""

import textwrap

import pytest

from scriv.format_rst import RstTools


@pytest.mark.parametrize(
    "text, parsed",
    [
        (
            """\
            .. Comments can be here
            .. and here.

            Added
            -----

            - This thing was added.
              And we liked it.
            """,
            {"Added": ["- This thing was added.\n  And we liked it.\n"]},
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
                    "- This thing was added.\n  And we liked it.\n",
                    "- Also added\n  this thing\n  that is very important.\n",
                ],
                "Fixed": ["- This thing was fixed.\n", "- Another thing was fixed.\n"],
            },
        ),
    ],
)
def test_parse_text(text, parsed):
    actual = RstTools().parse_text(textwrap.dedent(text))
    assert parsed == actual
