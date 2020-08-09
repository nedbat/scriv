"""Creating fragments."""

import datetime
import logging
import re
import sys
import textwrap
from pathlib import Path
from typing import Optional

import click
import click_log
import jinja2

from .collect import sections_from_file
from .config import Config
from .gitinfo import current_branch_name, git_add, git_config_bool, git_edit, user_nick

logger = logging.getLogger()


def new_fragment_path(config: Config) -> Path:
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
    file_path = Path(config.fragment_directory) / file_name
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
    if not Path(config.fragment_directory).exists():
        sys.exit("Output directory {!r} doesn't exist, please create it.".format(config.fragment_directory))

    file_path = new_fragment_path(config)
    if file_path.exists():
        sys.exit("File {} already exists, not overwriting".format(file_path))

    logger.info("Creating {}".format(file_path))
    file_path.write_text(new_fragment_contents(config))

    if edit:
        git_edit(file_path)
        sections = sections_from_file(config, file_path)
        if not sections:
            logger.info("Empty fragment, aborting...")
            file_path.unlink()
            sys.exit()

    if add:
        git_add(file_path)
