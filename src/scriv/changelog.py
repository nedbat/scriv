"""Changelog and Fragment definitions for Scriv."""

import datetime
from pathlib import Path

import attr
import jinja2

from .config import Config
from .format import FormatTools, SectionDict, get_format_tools
from .util import partition_lines


@attr.s
class Fragment:
    """A changelog fragment."""

    path = attr.ib(type=Path)
    format = attr.ib(type=str, default=None)
    content = attr.ib(type=str, default=None)

    def __attrs_post_init__(
        self,
    ):  # noqa: D105 (Missing docstring in magic method)
        if self.format is None:
            self.format = self.path.suffix.lstrip(".")

    def write(self) -> None:
        """Write the content to the file."""
        self.path.write_text(self.content)

    def read(self) -> None:
        """Read the content of the fragment."""
        self.content = self.path.read_text()


@attr.s
class Changelog:
    """A changelog file."""

    path = attr.ib(type=Path)
    config = attr.ib(type=Config)
    newline = attr.ib(type=str, default="")
    text_before = attr.ib(type=str, default="")
    changelog = attr.ib(type=str, default="")
    text_after = attr.ib(type=str, default="")

    def read(self) -> None:
        """Read the changelog if it exists."""
        if self.path.exists():
            with self.path.open("r", encoding="utf-8") as f:
                changelog_text = f.read()
                if f.newlines:  # .newlines may be None, str, or tuple
                    if isinstance(f.newlines, str):
                        self.newline = f.newlines
                    else:
                        self.newline = f.newlines[0]
            before, marker, after = partition_lines(
                changelog_text, self.config.insert_marker
            )
            if marker:
                self.text_before = before + marker
                rest = after
            else:
                self.text_before = ""
                rest = before
            self.changelog, marker, after = partition_lines(
                rest, self.config.end_marker
            )
            self.text_after = marker + after

    def format_tools(self) -> FormatTools:
        """Get the appropriate FormatTools for this changelog."""
        return get_format_tools(self.config.format, self.config)

    def entry_header(self, version, date=None) -> str:
        """Format the header for a new entry."""
        title_data = {
            "date": date or datetime.datetime.now(),
            "version": version,
        }
        title_template = jinja2.Template(self.config.entry_title_template)
        new_title = title_template.render(config=self.config, **title_data)
        if new_title.strip():
            anchor = f"changelog-{version}" if version else None
            new_header = self.format_tools().format_header(
                new_title, anchor=anchor
            )
        else:
            new_header = ""
        return new_header

    def entry_text(self, sections: SectionDict) -> str:
        """Format the text of a new entry."""
        return self.format_tools().format_sections(sections)

    def add_entry(self, header: str, text: str) -> None:
        """Add a new entry to the top of the changelog."""
        self.changelog = header + text + self.changelog

    def write(self) -> None:
        """Write the changelog."""
        f = self.path.open("w", encoding="utf-8", newline=self.newline or None)
        with f:
            f.write(self.text_before)
            f.write(self.changelog)
            f.write(self.text_after)

    def entries(self) -> SectionDict:
        """Parse the changelog into a SectionDict."""
        return self.format_tools().parse_text(self.changelog)
