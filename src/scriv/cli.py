"""Scriv command-line interface."""

import logging

import click
import click_log

from . import __version__
from .collect import collect
from .create import create

logger = logging.getLogger()
click_log.basic_config(logger)


@click.group(
    help="""\
        Manage changelogs.

        Version {version}
    """.format(
        version=__version__
    )
)
def cli() -> None:  # noqa: D401
    """The main entry point for the scriv command."""


cli.add_command(create)
cli.add_command(collect)
