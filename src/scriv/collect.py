"""Collecting fragments."""

import collections
import datetime
import itertools
import logging
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple, TypeVar

import click
import click_log
import jinja2

from .config import Config
from .format import SectionDict, get_format_tools
from .gitinfo import git_add, git_config_bool, git_edit, git_rm

logger = logging.getLogger()


def files_to_combine(config: Config) -> List[Path]:
    """
    Find all the files to be combined.

    The files are returned in the order they should be processed.

    """
    return sorted(
        itertools.chain.from_iterable(
            [
                Path(config.fragment_directory).glob(pattern)
                for pattern in ["*.rst", "*.md"]
            ]
        )
    )


def sections_from_file(config: Config, filename: Path) -> SectionDict:
    """
    Collect the sections from a file.
    """
    format_tools = get_format_tools(filename.suffix.lstrip("."), config)
    text = filename.read_text().rstrip()
    file_sections = format_tools.parse_text(text)
    return file_sections


def combine_sections(config: Config, files: Iterable[Path]) -> SectionDict:
    """
    Read files, and produce a combined SectionDict of their contents.
    """
    sections = collections.defaultdict(list)  # type: SectionDict
    for file in files:
        file_sections = sections_from_file(config, file)
        for section, paragraphs in file_sections.items():
            sections[section].extend(paragraphs)
    return sections


T = TypeVar("T")
K = TypeVar("K")


def order_dict(
    d: Dict[Optional[K], T], keys: Sequence[Optional[K]]
) -> Dict[Optional[K], T]:
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

    config = Config.read()
    logger.info("Collecting from {}".format(config.fragment_directory))
    files = files_to_combine(config)
    sections = combine_sections(config, files)
    sections = order_dict(sections, [None] + config.categories)

    changelog = Path(config.output_file)
    newline = ""
    if changelog.exists():
        with changelog.open("r") as f:
            changelog_text = f.read()
            if f.newlines:  # .newlines may be None, str, or tuple
                if isinstance(f.newlines, str):
                    newline = f.newlines
                else:
                    newline = f.newlines[0]
        text_before, text_after = cut_at_line(
            changelog_text, config.insert_marker
        )
    else:
        text_before = ""
        text_after = ""

    format_tools = get_format_tools(config.format, config)
    title_data = {
        "date": datetime.datetime.now(),
        "version": version or config.version,
    }
    new_title = jinja2.Template(config.entry_title_template).render(
        config=config, **title_data
    )
    if new_title.strip():
        new_header = format_tools.format_header(new_title)
    else:
        new_header = ""
    new_text = format_tools.format_sections(sections)
    with changelog.open("w", newline=newline or None) as f:
        f.write(text_before + new_header + new_text + text_after)

    if edit:
        git_edit(changelog)

    if add:
        git_add(changelog)

    if not keep:
        for file in files:
            logger.info("Deleting fragment file {}".format(file))
            if add:
                git_rm(file)
            else:
                file.unlink()
