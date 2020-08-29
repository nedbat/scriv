"""Helpers for using subprocesses."""

import logging
import shlex
import subprocess
from typing import List, Tuple, Union


def run_command(cmd: Union[str, List[str]]) -> Tuple[bool, str]:
    """
    Run a command line (with no shell).

    Returns a tuple:
        bool: true if the command succeeded.
        str: the output of the command.

    """
    logging.debug("Running command {!r}".format(cmd))
    if isinstance(cmd, str):
        cmd = shlex.split(cmd)
    proc = subprocess.run(
        cmd,
        shell=False,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    output = proc.stdout.decode("utf-8")
    logging.debug(
        "Command exited with {} status. Output: {!r}".format(
            proc.returncode, output
        )
    )

    return proc.returncode == 0, output


def run_simple_command(cmd: str) -> str:
    """
    Run a command and return its output, or "" if it fails.
    """
    ok, out = run_command(cmd)
    if not ok:
        return ""
    return out.strip()
