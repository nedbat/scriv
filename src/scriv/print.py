"""Collecting fragments."""

from __future__ import annotations

import logging
import os
import pathlib
import sys

import click

from .scriv import Scriv
from .util import Version, scriv_command

logger = logging.getLogger(__name__)


@click.command(name="print")
@click.option(
    "--version",
    default=None,
    help="The version of the changelog entry to extract.",
)
@click.option(
    "--output",
    type=click.Path(),
    default=None,
    help="The path to a file to write the output to.",
)
@scriv_command
def print_(
    version: str | None,
    output: pathlib.Path | None,
) -> None:
    """
    Print collected fragments, or print an entry from the changelog.
    """
    scriv = Scriv()
    changelog = scriv.changelog()
    newline = os.linesep

    if version is None:
        logger.info(f"Generating entry from {scriv.config.fragment_directory}")
        frags = scriv.fragments_to_combine()
        if not frags:
            logger.info("No changelog fragments to collect")
            sys.exit(2)
        contents = changelog.entry_text(scriv.combine_fragments(frags)).strip()
    else:
        logger.info(f"Extracting entry for {version} from {changelog.path}")
        changelog.read()
        newline = changelog.newline
        target_version = Version(version)
        for etitle, sections in changelog.entries().items():
            eversion = Version.from_text(str(etitle))
            if eversion is None:
                continue
            if eversion == target_version:
                contents = f"{changelog.newline * 2}".join(sections).strip()
                break
        else:
            logger.info(f"Unable to find version {version} in the changelog")
            sys.exit(2)

    if output:
        # Standardize newlines to match either the platform default
        # or to match the existing newlines found in the CHANGELOG.
        contents_raw = newline.join(contents.splitlines()).encode("utf-8")
        with open(output, "wb") as file:
            file.write(contents_raw)
    else:
        # Standardize newlines to just '\n' when writing to STDOUT.
        contents = "\n".join(contents.splitlines())
        print(contents)
