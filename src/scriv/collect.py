"""Collecting fragments."""

import logging
from typing import Optional

import click
import click_log

from .gitinfo import git_add, git_config_bool, git_edit, git_rm
from .scriv import Scriv

logger = logging.getLogger()


@click.command()
@click.option(
    "--add/--no-add", default=None, help="'git add' the updated changelog file."
)
@click.option(
    "--edit/--no-edit",
    default=None,
    help="Open the changelog file in your text editor.",
)
@click.option(
    "--keep", is_flag=True, help="Keep the fragment files that are collected."
)
@click.option(
    "--version", default=None, help="The version name to use for this entry."
)
@click_log.simple_verbosity_option(logger)
def collect(
    add: Optional[bool], edit: Optional[bool], keep: bool, version: str
) -> None:
    """
    Collect fragments and produce a combined entry in the CHANGELOG file.
    """
    if add is None:
        add = git_config_bool("scriv.collect.add")
    if edit is None:
        edit = git_config_bool("scriv.collect.edit")

    scriv = Scriv()
    logger.info("Collecting from {}".format(scriv.config.fragment_directory))
    frags = scriv.fragments_to_combine()

    changelog = scriv.changelog()
    changelog.read()

    new_header = changelog.entry_header(version=version)
    new_text = changelog.entry_text(scriv.combine_fragments(frags))
    changelog.write(new_header, new_text)

    if edit:
        git_edit(changelog.path)

    if add:
        git_add(changelog.path)

    if not keep:
        for frag in frags:
            logger.info("Deleting fragment file {!r}".format(str(frag.path)))
            if add:
                git_rm(frag.path)
            else:
                frag.path.unlink()
