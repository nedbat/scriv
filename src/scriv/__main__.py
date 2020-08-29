"""Enable 'python -m scriv'."""

from scriv.cli import cli

# pylint: disable=unexpected-keyword-arg
cli(prog_name="scriv")
