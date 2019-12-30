"""Scriv command-line interface."""

import logging

import click
import click_log

from scriv.config import read_config
from scriv.create import new_entry_contents, new_entry_path

logger = logging.getLogger(__name__)
click_log.basic_config(logger)


@click.group()
def cli() -> None:
    """Manage changelogs."""


@cli.command()
@click_log.simple_verbosity_option(logger)
def create() -> None:
    """
    Create a new scriv changelog entry.
    """
    config = read_config()
    file_path = new_entry_path(config)
    logger.info("Creating {}".format(file_path))
    with open(file_path, "w") as f:
        f.write(new_entry_contents(config))
