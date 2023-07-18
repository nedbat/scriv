"""Scriv command-line interface."""

import logging

import click
import click_log

from . import __version__
from .collect import collect
from .create import create
from .ghrel import github_release

# Configure the root logger, so all logging works.
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


# These type: pragmas can be removed when click 8.1.6 is out, to fix
# https://github.com/pallets/click/issues/2558.
cli.add_command(create)  # type: ignore[attr-defined]
cli.add_command(collect)  # type: ignore[attr-defined]
cli.add_command(github_release)  # type: ignore[attr-defined]
