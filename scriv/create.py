"""Creating entries."""

import datetime
import logging
import os.path
import re
import textwrap

import click
import click_log
import jinja2

from .config import Config, read_config
from .format import get_format_tools
from .gitinfo import current_branch_name, user_nick

logger = logging.getLogger()


def new_entry_path(config: Config) -> str:
    """
    Return the file path for a new entry.
    """
    file_name = "{:%Y%m%d_%H%M}_{}".format(datetime.datetime.now(), user_nick())
    branch_name = current_branch_name()
    if branch_name and branch_name != "master":
        branch_name = branch_name.rpartition("/")[-1]
        branch_name = re.sub(r"[^a-zA-Z0-9_]", "_", branch_name)
        file_name += "_{}".format(branch_name)
    file_name += ".{}".format(config.format)
    file_path = os.path.join(config.entry_directory, file_name)
    return file_path


def new_entry_contents(config: Config) -> str:
    """Produce the initial contents of a scriv entry."""
    tools = get_format_tools(config.format)
    return jinja2.Template(textwrap.dedent(tools.NEW_TEMPLATE)).render(config=config)


@click.command()
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
