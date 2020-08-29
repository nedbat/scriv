"""Tests of the process behavior of scriv."""

import sys

from scriv import __version__
from scriv.shell import run_command


def test_dashm():
    ok, output = run_command([sys.executable, "-m", "scriv"])
    assert ok
    assert "Usage: scriv [OPTIONS] COMMAND [ARGS]..." in output
    assert "Version " + __version__ in output
