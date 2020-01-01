"""Test collection logic."""

from scriv.collect import collect

ENTRY1 = """\
Fixed
-----

- Launching missiles no longer targets ourselves.
"""

ENTRY2 = """\
Added
-----

- Now you can send email with this tool.

Fixed
-----

- Typos corrected.
"""

ENTRY3 = """\
Obsolete
--------

- This section has the wrong name.
"""

CHANGELOG_1_2 = """\

Added
-----

- Now you can send email with this tool.

Fixed
-----

- Launching missiles no longer targets ourselves.

- Typos corrected.
"""

CHANGELOG_2_1_3 = """\

Added
-----

- Now you can send email with this tool.

Fixed
-----

- Typos corrected.

- Launching missiles no longer targets ourselves.

Obsolete
--------

- This section has the wrong name.
"""


def test_collect_simple(cli_runner, changelog_d, temp_dir):
    # Sections are ordered by the config file.
    # Entries in sections are in time order.
    (changelog_d / "20170616_nedbat.rst").write_text(ENTRY1)
    (changelog_d / "20170617_nedbat.rst").write_text(ENTRY2)
    result = cli_runner.invoke(collect)
    assert result.exit_code == 0
    changelog = (temp_dir / "CHANGELOG.rst").read_text()
    assert CHANGELOG_1_2 == changelog


def test_collect_ordering(cli_runner, changelog_d, temp_dir):
    # Entries in sections are in time order.
    # Unknown sections come after the known ones.
    (changelog_d / "20170616_nedbat.rst").write_text(ENTRY2)
    (changelog_d / "20170617_nedbat.rst").write_text(ENTRY1)
    (changelog_d / "20170618_joedev.rst").write_text(ENTRY3)
    result = cli_runner.invoke(collect)
    assert result.exit_code == 0
    changelog = (temp_dir / "CHANGELOG.rst").read_text()
    assert CHANGELOG_2_1_3 == changelog
