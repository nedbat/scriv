"""Creating fragments."""

import datetime
import logging
import os.path
import re
import sys
import textwrap
from typing import Optional

import click
import click_log
import jinja2

from .config import Config
from .gitinfo import current_branch_name, git_add, git_config_bool, git_edit, user_nick

logger = logging.getLogger()


def new_fragment_path(config: Config) -> str:
    """
    Return the file path for a new fragment.
    """
    file_name = "{:%Y%m%d_%H%M%S}_{}".format(datetime.datetime.now(), user_nick())
    branch_name = current_branch_name()
    if branch_name and branch_name not in config.main_branches:
        branch_name = branch_name.rpartition("/")[-1]
        branch_name = re.sub(r"[^a-zA-Z0-9_]", "_", branch_name)
        file_name += "_{}".format(branch_name)
    file_name += ".{}".format(config.format)
    file_path = os.path.join(config.fragment_directory, file_name)
    return file_path


def new_fragment_contents(config: Config) -> str:
    """Produce the initial contents of a scriv fragment."""
    return jinja2.Template(textwrap.dedent(config.new_fragment_template)).render(config=config)


@click.command()
@click.option("--add/--no-add", default=None, help="'git add' the created file.")
@click.option("--edit/--no-edit", default=None, help="Open the created file in your text editor.")
@click_log.simple_verbosity_option(logger)
def create(add: Optional[bool], edit: Optional[bool]) -> None:
    """
    Create a new scriv changelog fragment.
    """
    if add is None:
        add = git_config_bool("scriv.create.add")
    if edit is None:
        edit = git_config_bool("scriv.create.edit")

    config = Config.read()
    file_path = new_fragment_path(config)
    if os.path.exists(file_path):
        sys.exit("File {} already exists, not overwriting".format(file_path))

    logger.info("Creating {}".format(file_path))
    with open(file_path, "w") as f:
        f.write(new_fragment_contents(config))

    if edit:
        git_edit(file_path)

    if add:
        git_add(file_path)
