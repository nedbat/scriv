"""Creating fragments."""

import logging
import sys
from typing import Optional

import click
import click_log

from .gitinfo import git_add, git_config_bool, git_edit
from .scriv import Scriv

logger = logging.getLogger()


@click.command()
@click.option(
    "--add/--no-add", default=None, help="'git add' the created file."
)
@click.option(
    "--edit/--no-edit",
    default=None,
    help="Open the created file in your text editor.",
)
@click_log.simple_verbosity_option(logger)
def create(add: Optional[bool], edit: Optional[bool]) -> None:
    """
    Create a new scriv changelog fragment.
    """
    if add is None:
        add = git_config_bool("scriv.create.add")
    if edit is None:
        edit = git_config_bool("scriv.create.edit")

    scriv = Scriv()
    frag = scriv.new_fragment()
    file_path = frag.path
    if not file_path.parent.exists():
        sys.exit(
            "Output directory {!r} doesn't exist, please create it.".format(
                str(file_path.parent)
            )
        )

    if file_path.exists():
        sys.exit("File {} already exists, not overwriting".format(file_path))

    logger.info("Creating {}".format(file_path))
    frag.write()

    if edit:
        git_edit(file_path)
        sections = scriv.sections_from_fragment(frag)
        if not sections:
            logger.info("Empty fragment, aborting...")
            file_path.unlink()
            sys.exit()

    if add:
        git_add(file_path)
