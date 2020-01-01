"""Fixture definitions."""

from typing import Tuple

import pytest


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
