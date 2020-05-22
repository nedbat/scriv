"""Dispatcher for format-based knowledge."""

import abc
from typing import Dict, List

from .config import Config

# Parsed changelogs entries are called Sections. An ordered dict mapping
# section names to lists of paragraphs.
SectionDict = Dict[str, List[str]]


class FormatTools(abc.ABC):
    """Methods and data about specific formats."""

    @abc.abstractmethod
    def new_template(self) -> str:
        """
        Produce a Jinja2 template string for new entries.
        """

    @abc.abstractmethod
    def parse_text(self, text: str) -> SectionDict:
        """
        Parse text to find sections.

        Args:
            text: the marked-up text.

        Returns:
            A dict mapping section headers to a list of the paragraphs in each
            section.
        """

    @abc.abstractmethod
    def format_sections(self, sections: SectionDict) -> str:
        """
        Format a series of sections into marked-up text.
        """


def get_format_tools(fmt: str, config: Config) -> FormatTools:
    """
    Return the FormatTools to use.

    Args:
        fmt: One of the supported formats ("rst" or "md").
        config: The configuration settings to use.

    """
    if fmt == "rst":
        from . import format_rst  # pylint: disable=cyclic-import

        return format_rst.RstTools(config)
    elif fmt == "md":
        from . import format_md  # pylint: disable=cyclic-import

        return format_md.MdTools(config)
    else:
        raise Exception("Unknown format: {}".format(fmt))
