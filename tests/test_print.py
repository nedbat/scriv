"""Test print logic."""

import freezegun
import pytest

CHANGELOG_HEADER = """\

1.2 - 2020-02-25
================
"""


FRAG = """\
Fixed
-----

- Launching missiles no longer targets ourselves.
"""


@pytest.mark.parametrize("newline", ("\r\n", "\n"))
def test_print_fragment(newline, cli_invoke, changelog_d, temp_dir, capsys):
    fragment = FRAG.replace("\n", newline).encode("utf-8")
    (changelog_d / "20170616_nedbat.rst").write_bytes(fragment)

    with freezegun.freeze_time("2020-02-25T15:18:19"):
        cli_invoke(["print"])

    std = capsys.readouterr()
    assert std.out == FRAG


@pytest.mark.parametrize("newline", ("\r\n", "\n"))
def test_print_fragment_output(
    newline, cli_invoke, changelog_d, temp_dir, capsys
):
    fragment = FRAG.replace("\n", newline).encode("utf-8")
    (changelog_d / "20170616_nedbat.rst").write_bytes(fragment)
    output_file = temp_dir / "output.txt"

    with freezegun.freeze_time("2020-02-25T15:18:19"):
        cli_invoke(["print", "--output", output_file])

    std = capsys.readouterr()
    assert std.out == ""
    assert output_file.read_text().strip() == FRAG.strip()


@pytest.mark.parametrize("newline", ("\r\n", "\n"))
def test_print_changelog(newline, cli_invoke, changelog_d, temp_dir, capsys):
    changelog = (CHANGELOG_HEADER + FRAG).replace("\n", newline).encode("utf-8")
    (temp_dir / "CHANGELOG.rst").write_bytes(changelog)

    with freezegun.freeze_time("2020-02-25T15:18:19"):
        cli_invoke(["print", "--version", "1.2"])

    std = capsys.readouterr()
    assert std.out == FRAG


@pytest.mark.parametrize("newline", ("\r\n", "\n"))
def test_print_changelog_output(
    newline, cli_invoke, changelog_d, temp_dir, capsys
):
    changelog = (CHANGELOG_HEADER + FRAG).replace("\n", newline).encode("utf-8")
    (temp_dir / "CHANGELOG.rst").write_bytes(changelog)
    output_file = temp_dir / "output.txt"

    with freezegun.freeze_time("2020-02-25T15:18:19"):
        cli_invoke(["print", "--version", "1.2", "--output", output_file])

    std = capsys.readouterr()
    assert std.out == ""
    assert output_file.read_bytes().decode() == FRAG.strip().replace(
        "\n", newline
    )


def test_print_no_fragments(cli_invoke):
    result = cli_invoke(["print"], expect_ok=False)

    assert result.exit_code == 2
    assert "No changelog fragments to collect" in result.stderr


def test_print_version_not_in_changelog(cli_invoke, changelog_d, temp_dir):
    (temp_dir / "CHANGELOG.rst").write_bytes(b"BOGUS\n=====\n\n1.0\n===")

    result = cli_invoke(["print", "--version", "123.456"], expect_ok=False)

    assert result.exit_code == 2
    assert "Unable to find version 123.456 in the changelog" in result.stderr
