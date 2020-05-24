"""Markdown text knowledge for scriv."""

from .format import FormatTools, SectionDict


class MdTools(FormatTools):
    """Specifics about how to work with Markdown."""

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
        pass

    def format_sections(self, sections: SectionDict) -> str:  # noqa: D102 (inherited docstring)
        pass
