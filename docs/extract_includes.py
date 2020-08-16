"""
Extract information for documentation includes.
"""

import contextlib
import io
import textwrap
from pathlib import Path

import attr

from scriv.cli import cli
from scriv.config import Config

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
            with contextlib.redirect_stdout(out):
                print("\n.. code::\n")
                print(f"    $ scriv {cmd} --help")
                print(help_text)


def extract_config():
    """
    Get the documentation for all the configuration settings.
    """
    fields = sorted(attr.fields(Config), key=lambda f: f.name)
    with open(INCLUDE_DIR / "config.rst", "w") as out:
        with contextlib.redirect_stdout(out):
            for field in fields:
                name = field.name
                print(f"\n.. _config_{name}:\n")
                print(name)
                print("-" * len(name))
                print()
                text = field.metadata.get("doc", "NO DOC!\n")
                text = textwrap.dedent(text)
                print(text)
                default = field.metadata.get("doc_default")
                if default is None:
                    default = f"``{field.default}``"
                print(f"Default: {default}")


if __name__ == "__main__":
    extract_help()
    extract_config()
