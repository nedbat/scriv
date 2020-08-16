"""
Extract information for documentation includes.
"""

import contextlib
import io
import textwrap
from pathlib import Path

from scriv.cli import cli

INCLUDE_DIR = Path("docs/include")


def extract_help():
    """
    Get the help text for all commands.
    """
    for cmd in ["create", "collect"]:
        help_out = io.StringIO()
        with contextlib.redirect_stdout(help_out):
            with contextlib.suppress(SystemExit):
                # pylint: disable=too-many-function-args
                cli([cmd, "--help"])
        help_text = help_out.getvalue()
        help_text = help_text.replace("extract_includes.py", "scriv")
        help_text = textwrap.indent(help_text, "    ")

        with open(INCLUDE_DIR / (cmd + "_help.rst"), "w") as out:
            print("\n.. code::\n", file=out)
            print(f"    $ scriv {cmd} --help", file=out)
            print(help_text, file=out)


if __name__ == "__main__":
    extract_help()
