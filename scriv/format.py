"""Dispatcher for format-based knowledge."""

import abc
from typing import Dict, List

from scriv.config import Config

# Parsed changelogs entries are called Sections. An ordered dict mapping
# section names to lists of paragraphs.
SectionDict = Dict[str, List[str]]


class FormatTools(abc.ABC):
    """Methods and data about specific formats."""

    # The Jinja2 template for new entries in this format.
    NEW_TEMPLATE = ""

    @staticmethod
    @abc.abstractmethod
    def parse_text(text: str) -> SectionDict:
        """
        Parse text to find sections.

        Args:
            text: the marked-up text.

        Returns:
            A dict mapping section headers to a list of the paragraphs in each
            section.
        """

    @staticmethod
    @abc.abstractmethod
    def format_sections(sections: SectionDict) -> str:
        """
        Format a series of sections into marked-up text.
        """


def get_format_tools(config: Config) -> FormatTools:
    """Return the FormatTools to use."""
    if config.format == "rst":
        from scriv import format_rst  # pylint: disable=cyclic-import

        return format_rst.RstTools()
    elif config.format == "md":
        from scriv import format_md  # pylint: disable=cyclic-import

        return format_md.MdTools()
    else:
        raise Exception("Unknown format: {}".format(config.format))
