"""Dispatcher for format-based knowledge."""

import abc
import pkgutil
from pathlib import Path
from typing import Dict, List

from .config import Config

# Parsed changelogs entries are called Sections. An ordered dict mapping
# section names to lists of paragraphs.
SectionDict = Dict[str, List[str]]


class FormatTools(abc.ABC):
    """Methods and data about specific formats."""

    def __init__(self, config: Config = None):
        """Create a FormatTools with the specified configuration."""
        self.config = config or Config()

    def new_template(self) -> str:
        """
        Produce a Jinja2 template string for new entries.
        """
        return new_template_text(self.config)

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


def new_template_text(config: Config) -> str:
    """
    Find the text of a Jinja2 template for new entries.

    `config.new_entry_template` is used as a file name inside the
    `config.entry_directory` directory.  If the file is specified, but does
    not exist, an exception is raised.

    The default for new_entry_template is new_entry.<FMT>.j2, and will be
    read from an internal default if the file doesn't exist.

    Args:
        config: The configuration settings to use.

    Returns:
        The text of the template.

    """
    j2_name = config.new_entry_template
    j2_must_exist = bool(j2_name)
    if not j2_name:
        j2_name = "new_entry.{}.j2".format(config.format)
    template_file = Path(config.entry_directory) / j2_name
    if template_file.exists():
        template = template_file.read_text()
    else:
        if j2_must_exist:
            raise Exception("No such template: {}".format(template_file))
        template_bytes = pkgutil.get_data("scriv", "templates/" + j2_name)
        assert template_bytes
        template = template_bytes.decode("utf-8")
    return template
