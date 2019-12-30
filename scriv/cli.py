"""Scriv command-line interface."""

import click

from scriv.config import read_config
from scriv.create import new_entry_contents, new_entry_path


@click.group()
def cli() -> None:
    """Manage changelogs."""


@cli.command()
def create() -> None:
    """
    Create a new scriv changelog entry.
    """
    config = read_config()
    file_path = new_entry_path(config)
    click.echo("Creating {}".format(file_path))
    with open(file_path, "w") as f:
        f.write(new_entry_contents(config))
