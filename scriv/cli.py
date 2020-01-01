"""Scriv command-line interface."""

import logging

import click
import click_log

from scriv.collect import combine_sections, files_to_combine
from scriv.config import read_config
from scriv.create import new_entry_contents, new_entry_path
from scriv.format import get_format_tools

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


@cli.command()
@click_log.simple_verbosity_option(logger)
def collect() -> None:
    """
    Collect entries and produce a combined file.
    """
    config = read_config()
    logger.info("Collecting from {}".format(config.entry_directory))
    sections = combine_sections(files_to_combine(config.entry_directory))
    format_tools = get_format_tools(config.format)
    with open(config.output_file, "w") as f:
        f.write(format_tools.format_sections(sections))
