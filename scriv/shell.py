"""Helpers for using subprocesses."""

import shlex
import subprocess
from typing import Tuple


def run_command(cmd: str) -> Tuple[bool, str]:
    """
    Run a command line (with no shell).

    Returns a tuple:
        bool: true if the command succeeded.
        str: the output of the command.

    """
    proc = subprocess.run(shlex.split(cmd), shell=False, check=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return proc.returncode == 0, proc.stdout.decode("utf-8")
