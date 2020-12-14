"""Test collection logic."""

from unittest.mock import call

import freezegun
import pytest

COMMENT = """\
.. this line should be dropped

"""

COMMENT_MD = """\
<!-- this line should be dropped -->
"""

FRAG1 = """\
Fixed
-----

- Launching missiles no longer targets ourselves.
"""

FRAG2 = """\
Added
-----

- Now you can send email with this tool.

Fixed
-----

- Typos corrected.
"""

FRAG2_MD = """\
# Added

- Now you can send email with this tool.

# Fixed

- Typos corrected.
"""

FRAG3 = """\
Obsolete
--------

- This section has the wrong name.
"""

CHANGELOG_1_2 = """\

2020-02-25
==========

Added
-----

- Now you can send email with this tool.

Fixed
-----

- Launching missiles no longer targets ourselves.

- Typos corrected.
"""

CHANGELOG_2_1_3 = """\

2020-02-25
==========

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

MARKED_CHANGELOG_A = """\
================
My Great Project
================

Blah blah.

Changes
=======

.. scriv-insert-here
"""

UNMARKED_CHANGELOG_B = """\

Other stuff
===========

Blah blah.
"""

CHANGELOG_HEADER = """\

2020-02-25
==========
"""


def test_collect_simple(cli_invoke, changelog_d, temp_dir):
    # Sections are ordered by the config file.
    # Fragments in sections are in time order.
    (changelog_d / "scriv.ini").write_text("# this shouldn't be collected\n")
    (changelog_d / "20170616_nedbat.rst").write_text(COMMENT + FRAG1 + COMMENT)
    (changelog_d / "20170617_nedbat.rst").write_text(COMMENT + FRAG2)
    with freezegun.freeze_time("2020-02-25T15:18:19"):
        cli_invoke(["collect"])
    changelog_text = (temp_dir / "CHANGELOG.rst").read_text()
    assert changelog_text == CHANGELOG_1_2
    # We didn't use --keep, so the files should be gone.
    assert (changelog_d / "scriv.ini").exists()
    assert not (changelog_d / "20170616_nedbat.rst").exists()
    assert not (changelog_d / "20170617_nedbat.rst").exists()


def test_collect_ordering(cli_invoke, changelog_d, temp_dir):
    # Fragments in sections are in time order.
    # Unknown sections come after the known ones.
    (changelog_d / "20170616_nedbat.rst").write_text(COMMENT + FRAG2)
    (changelog_d / "20170617_nedbat.rst").write_text(COMMENT + FRAG1)
    (changelog_d / "20170618_joedev.rst").write_text(COMMENT + FRAG3)
    with freezegun.freeze_time("2020-02-25T15:18:19"):
        cli_invoke(["collect"])
    changelog_text = (temp_dir / "CHANGELOG.rst").read_text()
    assert changelog_text == CHANGELOG_2_1_3


def test_collect_mixed_format(cli_invoke, changelog_d, temp_dir):
    # Fragments can be in mixed formats.
    (changelog_d / "20170616_nedbat.md").write_text(COMMENT_MD + FRAG2_MD)
    (changelog_d / "20170617_nedbat.rst").write_text(COMMENT + FRAG1)
    (changelog_d / "20170618_joedev.rst").write_text(COMMENT + FRAG3)
    with freezegun.freeze_time("2020-02-25T15:18:19"):
        cli_invoke(["collect"])
    changelog_text = (temp_dir / "CHANGELOG.rst").read_text()
    assert changelog_text == CHANGELOG_2_1_3


def test_collect_inserts_at_marker(cli_invoke, changelog_d, temp_dir):
    # Collected text is inserted into CHANGELOG where marked.
    changelog = temp_dir / "CHANGELOG.rst"
    changelog.write_text(MARKED_CHANGELOG_A + UNMARKED_CHANGELOG_B)
    (changelog_d / "20170617_nedbat.rst").write_text(FRAG1)
    with freezegun.freeze_time("2020-02-25T15:18:19"):
        cli_invoke(["collect"])
    changelog_text = changelog.read_text()
    expected = (
        MARKED_CHANGELOG_A
        + CHANGELOG_HEADER
        + "\n"
        + FRAG1
        + UNMARKED_CHANGELOG_B
    )
    assert changelog_text == expected


def test_collect_inserts_at_marker_no_header(cli_invoke, changelog_d, temp_dir):
    # No title this time.
    (changelog_d / "scriv.ini").write_text("[scriv]\nentry_title_template =\n")
    # Collected text is inserted into CHANGELOG where marked.
    changelog = temp_dir / "CHANGELOG.rst"
    changelog.write_text(MARKED_CHANGELOG_A + UNMARKED_CHANGELOG_B)
    (changelog_d / "20170617_nedbat.rst").write_text(FRAG1)
    with freezegun.freeze_time("2020-02-25T15:18:19"):
        cli_invoke(["collect"])
    changelog_text = changelog.read_text()
    expected = MARKED_CHANGELOG_A + "\n" + FRAG1 + UNMARKED_CHANGELOG_B
    assert changelog_text == expected


def test_collect_prepends_if_no_marker(cli_invoke, changelog_d, temp_dir):
    # Collected text is inserted at the top of CHANGELOG if no marker.
    changelog = temp_dir / "CHANGELOG.rst"
    changelog.write_text(UNMARKED_CHANGELOG_B)
    (changelog_d / "20170617_nedbat.rst").write_text(FRAG1)
    with freezegun.freeze_time("2020-02-25T15:18:19"):
        cli_invoke(["collect"])
    changelog_text = changelog.read_text()
    expected = CHANGELOG_HEADER + "\n" + FRAG1 + UNMARKED_CHANGELOG_B
    assert changelog_text == expected


def test_collect_keep(cli_invoke, changelog_d, temp_dir):
    # --keep tells collect to not delete the fragment files.
    (changelog_d / "scriv.ini").write_text("# this shouldn't be collected\n")
    (changelog_d / "20170616_nedbat.rst").write_text(FRAG1)
    (changelog_d / "20170617_nedbat.rst").write_text(FRAG2)
    with freezegun.freeze_time("2020-02-25T15:18:19"):
        cli_invoke(["collect", "--keep"])
    changelog_text = (temp_dir / "CHANGELOG.rst").read_text()
    assert changelog_text == CHANGELOG_1_2
    # We used --keep, so the collected files should still exist.
    assert (changelog_d / "scriv.ini").exists()
    assert (changelog_d / "20170616_nedbat.rst").exists()
    assert (changelog_d / "20170617_nedbat.rst").exists()


def test_collect_no_categories(cli_invoke, changelog_d, temp_dir):
    # Categories can be empty, making a simpler changelog.
    changelog = temp_dir / "CHANGELOG.rst"
    (changelog_d / "scriv.ini").write_text("[scriv]\ncategories=\n")
    (changelog_d / "20170616_nedbat.rst").write_text("- The first change.\n")
    (changelog_d / "20170617_nedbat.rst").write_text(
        COMMENT + "- The second change.\n"
    )
    with freezegun.freeze_time("2020-02-25T15:18:19"):
        cli_invoke(["collect"])
    changelog_text = changelog.read_text()
    expected = (
        "\n"
        + "2020-02-25\n"
        + "==========\n\n"
        + "- The first change.\n\n"
        + "- The second change.\n"
    )
    assert changelog_text == expected


def test_collect_uncategorized_fragments(cli_invoke, changelog_d, temp_dir):
    # If using categories, even uncategorized fragments will be collected.
    changelog = temp_dir / "CHANGELOG.rst"
    (changelog_d / "20170616_nedbat.rst").write_text(FRAG1)
    (changelog_d / "20170617_nedbat.rst").write_text("- The second change.\n")
    with freezegun.freeze_time("2020-02-25T15:18:19"):
        cli_invoke(["collect"])
    changelog_text = changelog.read_text()
    expected = "\n2020-02-25\n==========\n\n- The second change.\n\n" + FRAG1
    assert changelog_text == expected


def test_collect_add(mocker, cli_invoke, changelog_d, temp_dir):
    # --add tells collect to tell git what's going on.
    (changelog_d / "scriv.ini").write_text("# this shouldn't be collected\n")
    (changelog_d / "20170616_nedbat.rst").write_text(FRAG1)
    (changelog_d / "20170617_nedbat.rst").write_text(FRAG2)
    mock_call = mocker.patch("subprocess.call")
    mock_call.return_value = 0
    with freezegun.freeze_time("2020-02-25T15:18:19"):
        cli_invoke(["collect", "--add"])
    changelog_text = (temp_dir / "CHANGELOG.rst").read_text()
    assert changelog_text == CHANGELOG_1_2
    # We used --add, so the collected files were git rm'd
    assert mock_call.mock_calls == [
        call(["git", "add", "CHANGELOG.rst"]),
        call(
            [
                "git",
                "rm",
                str(
                    (changelog_d / "20170616_nedbat.rst").relative_to(temp_dir)
                ),
            ]
        ),
        call(
            [
                "git",
                "rm",
                str(
                    (changelog_d / "20170617_nedbat.rst").relative_to(temp_dir)
                ),
            ]
        ),
    ]


def test_collect_add_rm_fail(mocker, cli_invoke, changelog_d, temp_dir):
    # --add, but fail to remove a file.
    (changelog_d / "scriv.ini").write_text("# this shouldn't be collected\n")
    (changelog_d / "20170616_nedbat.rst").write_text(FRAG1)
    (changelog_d / "20170617_nedbat.rst").write_text(FRAG2)
    mock_call = mocker.patch("subprocess.call")
    mock_call.side_effect = [0, 99]
    with freezegun.freeze_time("2020-02-25T15:18:19"):
        result = cli_invoke(["collect", "--add"], expect_ok=False)
    assert result.exit_code == 99
    changelog_text = (temp_dir / "CHANGELOG.rst").read_text()
    assert changelog_text == CHANGELOG_1_2
    # We used --add, so the collected files were git rm'd
    assert mock_call.mock_calls == [
        call(["git", "add", "CHANGELOG.rst"]),
        call(
            [
                "git",
                "rm",
                str(
                    (changelog_d / "20170616_nedbat.rst").relative_to(temp_dir)
                ),
            ]
        ),
    ]


def test_collect_edit(fake_git, mocker, cli_invoke, changelog_d, temp_dir):
    # --edit tells collect to open the changelog in an editor.
    fake_git.set_editor("my_fav_editor")
    (changelog_d / "scriv.ini").write_text("# this shouldn't be collected\n")
    (changelog_d / "20170616_nedbat.rst").write_text(FRAG1)
    (changelog_d / "20170617_nedbat.rst").write_text(FRAG2)
    mock_edit = mocker.patch("click.edit")
    with freezegun.freeze_time("2020-02-25T15:18:19"):
        cli_invoke(["collect", "--edit"])
    changelog_text = (temp_dir / "CHANGELOG.rst").read_text()
    assert changelog_text == CHANGELOG_1_2
    mock_edit.assert_called_once_with(
        filename="CHANGELOG.rst", editor="my_fav_editor"
    )


def test_collect_version_in_config(cli_invoke, changelog_d, temp_dir):
    # The version number to use in the changelog entry can be specified in the
    # config file.
    changelog = temp_dir / "CHANGELOG.rst"
    (changelog_d / "scriv.ini").write_text("[scriv]\nversion = v12.34b\n")
    (changelog_d / "20170616_nedbat.rst").write_text("- The first change.\n")
    with freezegun.freeze_time("2020-02-26T15:18:19"):
        cli_invoke(["collect"])
    changelog_text = changelog.read_text()
    expected = (
        "\n"
        + "v12.34b — 2020-02-26\n"
        + "====================\n\n"
        + "- The first change.\n"
    )
    assert changelog_text == expected


@pytest.mark.parametrize(
    "platform, newline",
    (
        ("Windows", "\r\n"),
        ("Linux", "\n"),
        ("Mac", "\r"),
    ),
)
def test_collect_respect_existing_newlines(
    cli_invoke,
    changelog_d,
    temp_dir,
    platform,
    newline,
):
    """Verify that existing newline styles are preserved during collection."""

    index_map = {
        "\r\n": 0,
        "\n": 1,
        "\r": 2,
    }

    changelog = temp_dir / "CHANGELOG.rst"
    existing_text = "Line one" + newline + "Line two"
    with changelog.open("wb") as file:
        file.write(existing_text.encode("utf8"))
    (changelog_d / "20170616_nedbat.rst").write_text(COMMENT + FRAG1 + COMMENT)
    with freezegun.freeze_time("2020-02-25T15:18:19"):
        cli_invoke(["collect"])
    with changelog.open("rb") as file:
        new_text = file.read().decode("utf8")

    counts = [new_text.count("\r\n")]  # Windows
    counts.append(new_text.count("\n") - counts[0])  # Linux
    counts.append(new_text.count("\r") - counts[0])  # Mac

    msg = platform + " newlines were not preserved"
    assert counts.pop(index_map[newline]), msg
    assert counts == [0, 0], msg
