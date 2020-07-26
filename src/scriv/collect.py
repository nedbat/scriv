"""Collecting entries."""

import collections
import datetime
import logging
from pathlib import Path
from typing import Dict, Iterable, List, Tuple, TypeVar

import click
import click_log

from .config import Config, read_config
from .format import SectionDict, get_format_tools

logger = logging.getLogger()


def files_to_combine(config: Config) -> List[Path]:
    """
    Find all the files to be combined.

    The files are returned in the order they should be processed.

    """
    pattern = "**/*.{}".format(config.format)
    return sorted(Path(config.entry_directory).glob(pattern))


def combine_sections(config: Config, files: Iterable[Path]) -> SectionDict:
    """
    Read files, and produce a combined SectionDict of their contents.
    """
    sections = collections.defaultdict(list)  # type: SectionDict
    for file in files:
        format_tools = get_format_tools(file.suffix.lstrip("."), config)
        with file.open() as f:
            text = f.read().rstrip()
        if config.categories:
            file_sections = format_tools.parse_text(text)
            for section, paragraphs in file_sections.items():
                sections[section].extend(paragraphs)
        else:
            sections[None].append(text)
    return sections


T = TypeVar("T")
K = TypeVar("K")


def order_dict(d: Dict[K, T], keys: List[K]) -> Dict[K, T]:
    """
    Produce an OrderedDict of `d`, but with the keys in `keys` order.
    """
    with_order = collections.OrderedDict()
    to_insert = set(d)
    for k in keys:
        if k not in to_insert:
            continue
        with_order[k] = d[k]
        to_insert.remove(k)

    for k in to_insert:
        with_order[k] = d[k]

    return with_order


def cut_at_line(text: str, marker: str) -> Tuple[str, str]:
    """
    Split text into two parts: up to the line with marker, and lines after.

    If `marker` isn't in the text, return ("", text)
    """
    lines = text.splitlines(keepends=True)
    for i, line in enumerate(lines):
        if marker in line:
            return "".join(lines[: i + 1]), "".join(lines[i + 1 :])
    return ("", text)


@click.command()
@click.option("--delete", is_flag=True, help="Delete changelog entry files that are collected.")
@click_log.simple_verbosity_option(logger)
def collect(delete: bool) -> None:
    """
    Collect entries and produce a combined file.
    """
    config = read_config()
    logger.info("Collecting from {}".format(config.entry_directory))
    files = files_to_combine(config)
    sections = combine_sections(config, files)
    sections = order_dict(sections, config.categories)

    changelog = Path(config.output_file)
    if changelog.exists():
        changelog_text = changelog.read_text()
        text_before, text_after = cut_at_line(changelog_text, config.insert_marker)
    else:
        text_before = ""
        text_after = ""

    format_tools = get_format_tools(config.format, config)
    header_data = {
        "date": datetime.datetime.now(),
    }
    new_header = format_tools.format_header(header_data)
    new_text = format_tools.format_sections(sections)
    print(repr(new_header))
    print(repr(new_text))
    changelog.write_text(text_before + new_header + new_text + text_after)

    if delete:
        for file in files:
            logger.debug("Deleting entry file {}".format(file))
            file.unlink()
