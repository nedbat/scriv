"""Scriv command-line interface."""

import logging

import click
import click_log

from . import __version__
from .collect import collect
from .create import create
from .ghrel import github_release
from .print import print_

click_log.basic_config(logging.getLogger())


@click.group(
    help=f"""\
        Manage changelogs.

        Version {__version__}
    """
)
@click.version_option()
def cli() -> None:  # noqa: D401
    """The main entry point for the scriv command."""


cli.add_command(create)
cli.add_command(collect)
cli.add_command(github_release)
cli.add_command(print_)
