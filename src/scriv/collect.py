"""Collecting fragments."""

import logging
import sys
from typing import Optional

import click
import click_log

from .gitinfo import git_add, git_config_bool, git_edit, git_rm
from .scriv import Scriv
from .util import extract_version

logger = logging.getLogger()


@click.command()
@click.option(
    "--add/--no-add",
    default=None,
    help="'git add' the updated changelog file and removed fragments.",
)
@click.option(
    "--edit/--no-edit",
    default=None,
    help="Open the changelog file in your text editor.",
)
@click.option(
    "--title", default=None, help="The title text to use for this entry."
)
@click.option(
    "--keep", is_flag=True, help="Keep the fragment files that are collected."
)
@click.option(
    "--version", default=None, help="The version name to use for this entry."
)
@click_log.simple_verbosity_option(logger)
def collect(
    add: Optional[bool],
    edit: Optional[bool],
    title: str,
    keep: bool,
    version: str,
) -> None:
    """
    Collect and combine fragments into the changelog.
    """
    if title is not None and version is not None:
        sys.exit("Can't provide both --title and --version.")

    if add is None:
        add = git_config_bool("scriv.collect.add")
    if edit is None:
        edit = git_config_bool("scriv.collect.edit")

    scriv = Scriv()
    logger.info(f"Collecting from {scriv.config.fragment_directory}")
    frags = scriv.fragments_to_combine()
    if not frags:
        logger.info("No changelog fragments to collect")
        return

    changelog = scriv.changelog()
    changelog.read()

    if title is None:
        version = version or scriv.config.version
        if version:
            # Check that we haven't used this version before.
            for etitle in changelog.entries().keys():
                if etitle is None:
                    continue
                eversion = extract_version(etitle)
                if eversion == version:
                    sys.exit(
                        f"Entry {etitle!r} already uses version {version!r}."
                    )
        new_header = changelog.entry_header(version=version)
    else:
        new_header = changelog.format_tools().format_header(title)

    new_text = changelog.entry_text(scriv.combine_fragments(frags))
    changelog.add_entry(new_header, new_text)
    changelog.write()

    if edit:
        git_edit(changelog.path)

    if add:
        git_add(changelog.path)

    if not keep:
        for frag in frags:
            logger.info(f"Deleting fragment file {str(frag.path)!r}")
            if add:
                git_rm(frag.path)
            else:
                frag.path.unlink()
