"""Dispatcher for format-based knowledge."""

import abc
from typing import Dict, List, Optional

from .config import Config

# When collecting changelog fragments, we group them by their category into
# Sections.  A SectionDict maps category names to a list of the paragraphs in
# that section.  For projects not using categories, the key will be None.
SectionDict = Dict[Optional[str], List[str]]


class FormatTools(abc.ABC):
    """Methods and data about specific formats."""

    def __init__(self, config: Optional[Config] = None):
        """Create a FormatTools with the specified configuration."""
        self.config = config or Config()

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
    def format_header(self, text: str, anchor: Optional[str] = None) -> str:
        """
        Format the header for a new changelog entry.
        """

    @abc.abstractmethod
    def format_sections(self, sections: SectionDict) -> str:
        """
        Format a series of sections into marked-up text.
        """

    @abc.abstractmethod
    def convert_to_markdown(self, text: str) -> str:
        """
        Convert this format to Markdown.
        """


def get_format_tools(fmt: str, config: Config) -> FormatTools:
    """
    Return the FormatTools to use.

    Args:
        fmt: One of the supported formats ("rst" or "md").
        config: The configuration settings to use.

    """
    if fmt == "rst":
        from . import (  # pylint: disable=cyclic-import,import-outside-toplevel
            format_rst,
        )

        return format_rst.RstTools(config)
    else:
        assert fmt == "md"
        from . import (  # pylint: disable=cyclic-import,import-outside-toplevel
            format_md,
        )

        return format_md.MdTools(config)
