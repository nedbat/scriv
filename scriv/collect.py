"""Collecting entries."""

import collections
import logging
from pathlib import Path
from typing import Iterable, List

import click
import click_log

from scriv.config import read_config
from scriv.format import SectionDict, get_format_tools

logger = logging.getLogger()


def files_to_combine(directory: str) -> Iterable[Path]:
    """
    In the directory, find the names of files to combine.

    The files are returned in the order they should be processed.

    """
    return sorted(Path(directory).glob("**/*.*"))


def combine_sections(files: Iterable[Path]) -> SectionDict:
    """
    Read files, and produce a combined SectionDict of their contents.
    """
    sections = collections.defaultdict(list)  # type: SectionDict
    for file in files:
        with file.open() as f:
            format_tools = get_format_tools(file.suffix)
            file_sections = format_tools.parse_text(f.read())
            for section, paragraphs in file_sections.items():
                sections[section].extend(paragraphs)
    return sections


def order_sections(sections: SectionDict, categories: List[str]) -> SectionDict:
    """
    Re-order the sections to match the categories list.
    """
    with_order = collections.OrderedDict()
    to_insert = set(sections)
    for category in categories:
        if category not in to_insert:
            continue
        with_order[category] = sections[category]
        to_insert.remove(category)

    for category in to_insert:
        with_order[category] = sections[category]

    return with_order


@click.command()
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
