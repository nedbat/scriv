"""Tests of the process behavior of scriv."""

import sys

from scriv.shell import run_command


def test_dashm():
    ok, output = run_command([sys.executable, "-m", "scriv"])
    assert ok
    assert "Usage: scriv [OPTIONS] COMMAND [ARGS]..." in output
