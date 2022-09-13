"""Tests of scriv/changelog.py"""

import pytest

from scriv.changelog import Changelog
from scriv.config import Config

A = """\
Hello
Goodbye
"""

B = """\
Now
more than
ever.
"""

BODY = """\
2022-09-13
==========

Added
-----

- Wrote tests for Changelog.

2022-02-25
==========

Added
-----

- Now you can send email with this tool.

Fixed
-----

- Launching missiles no longer targets ourselves.

- Typos corrected.
"""

BODY_SECTIONS = {
    "2022-09-13": [
        "Added\n-----",
        "- Wrote tests for Changelog.",
    ],
    "2022-02-25": [
        "Added\n-----",
        "- Now you can send email with this tool.",
        "Fixed\n-----",
        "- Launching missiles no longer targets ourselves.",
        "- Typos corrected.",
    ],
}


@pytest.mark.parametrize(
    "text",
    [
        BODY,
        ".. INSERT\n" + BODY,
        A + "(INSERT)\n" + BODY,
        A + "INSERT\n" + BODY + ".. END\n",
        A + ".. INSERT\n" + BODY + "(END)\n" + B,
        BODY + ".. END\n",
        BODY + ".. END\n" + B,
    ],
)
def test_round_trip(text, temp_dir):
    path = temp_dir / "foo.rst"
    config = Config(insert_marker="INSERT", end_marker="END")
    path.write_text(text)
    changelog = Changelog(path, config)
    changelog.read()
    assert changelog.entries() == BODY_SECTIONS
    changelog.write()
    assert path.read_text() == text
