"""Markdown text knowledge for scriv."""

from .format import FormatTools, SectionDict


class MdTools(FormatTools):
    """Specifics about how to work with Markdown."""

    def parse_text(self, text) -> SectionDict:  # noqa: D102 (inherited docstring)
        pass

    def format_header(self, text: str) -> str:  # noqa: D102 (inherited docstring)
        pass

    def format_sections(self, sections: SectionDict) -> str:  # noqa: D102 (inherited docstring)
        pass
