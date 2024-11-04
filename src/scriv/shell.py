"""Helpers for using subprocesses."""

import logging
import shlex
import subprocess
from typing import Union

# The return value of run_command.
CmdResult = tuple[bool, str]

logger = logging.getLogger(__name__)


def run_command(cmd: Union[str, list[str]]) -> CmdResult:
    """
    Run a command line (with no shell).

    Returns a tuple:
        bool: true if the command succeeded.
        str: the output of the command.

    """
    logger.debug(f"Running command {cmd!r}")
    if isinstance(cmd, str):
        cmd = shlex.split(cmd, posix=False)
    proc = subprocess.run(
        cmd,
        shell=False,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    output = proc.stdout.decode("utf-8")
    logger.debug(
        f"Command exited with {proc.returncode} status. Output: {output!r}"
    )

    return proc.returncode == 0, output


def run_simple_command(cmd: Union[str, list[str]]) -> str:
    """
    Run a command and return its output, or "" if it fails.
    """
    ok, out = run_command(cmd)
    if not ok:
        return ""
    return out.strip()


def run_shell_command(cmd: str) -> CmdResult:
    """
    Run a command line with a shell.
    """
    logger.debug(f"Running shell command {cmd!r}")
    proc = subprocess.run(
        cmd,
        shell=True,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    output = proc.stdout.decode("utf-8")
    logger.debug(
        f"Command exited with {proc.returncode} status. Output: {output!r}"
    )
    return proc.returncode == 0, output
