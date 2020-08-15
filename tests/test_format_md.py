"""Tests for scriv/format_md.py."""

# import collections
import textwrap

import pytest

# from scriv.config import Config
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
            {"Added": ["- This thing was added.\n  And we liked it.", "- Another thing we added."]},
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
                "Fixed": ["- This thing was fixed.", "- Another thing was fixed."],
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
