"""Markdown text knowledge for scriv."""

from .config import Config
from .format import FormatTools, SectionDict


class MdTools(FormatTools):
    """Specifics about how to work with Markdown."""

    def __init__(self, config: Config = None):
        """Create a MdTools with the specified configuration."""
        self.config = config or Config()

    def new_template(self) -> str:  # noqa: D102 (inherited docstring)
        return """\
        <!--
        A new scriv entry.

        Uncomment the section that is right (remove the HTML comment wrapper).
        -->

        {% for cat in config.categories -%}
        <!--
        ### {{ cat }}

        - A bullet item for the {{ cat }} category.

        -->
        {% endfor -%}
        """

    def parse_text(self, text) -> SectionDict:  # noqa: D102 (inherited docstring)
        return {}

    def format_sections(self, sections: SectionDict) -> str:  # noqa: D102 (inherited docstring)
        pass
