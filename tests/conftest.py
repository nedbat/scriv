"""Fixture definitions."""

import pathlib
from typing import Tuple

import pytest
from click.testing import CliRunner


class RunCommandFaker:
    """
    A fake implementation of run_command.

    Add results for commands with `add_fake`.
    """

    def __init__(self):
        """Make the faker."""
        self.in_out = {}

    def add_fake(self, cmd: str, result: Tuple[bool, str]) -> None:
        """If `cmd` is executed, return `result`."""
        self.in_out[cmd] = result

    def __call__(self, cmd: str) -> Tuple[bool, str]:
        """Do the faking!."""
        return self.in_out.get(cmd, (False, ""))


@pytest.fixture()
def fake_run_command(mocker):
    """Replace gitinfo.run_command with a fake."""
    frc = RunCommandFaker()
    mocker.patch("scriv.gitinfo.run_command", frc)
    return frc


@pytest.fixture()
def temp_dir(tmpdir) -> pathlib.Path:
    """Make and change into the tmpdir directory, as a Path."""
    tmpdir.chdir()
    return pathlib.Path(str(tmpdir))


@pytest.fixture()
def cli_runner(temp_dir):  # pylint: disable=unused-argument, redefined-outer-name
    """Return a CliRunner, and run in a temp directory."""
    return CliRunner()


@pytest.fixture()
def changelog_d(temp_dir) -> pathlib.Path:  # pylint: disable=redefined-outer-name
    """Make a changelog.d directory, and return a Path() to it."""
    the_changelog_d = temp_dir / "changelog.d"
    the_changelog_d.mkdir()
    return the_changelog_d
