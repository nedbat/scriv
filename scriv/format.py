"""Dispatcher for format-based knowledge."""

import abc
from typing import Dict, List

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


def get_format_tools(fmt: str) -> FormatTools:
    """
    Return the FormatTools to use.

    Args:
        fmt: One of the supported formats ("rst" or "md"), or a file extension
            implying one of them (".rst", ".md").

    """
    if fmt.startswith("."):
        fmt = fmt[1:]
    if fmt == "rst":
        from . import format_rst  # pylint: disable=cyclic-import

        return format_rst.RstTools()
    elif fmt == "md":
        from . import format_md  # pylint: disable=cyclic-import

        return format_md.MdTools()
    else:
        raise Exception("Unknown format: {}".format(fmt))
