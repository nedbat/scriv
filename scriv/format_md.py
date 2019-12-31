"""Markdown text knowledge for scriv."""

from scriv.format import FormatTools, SectionDict


class MdTools(FormatTools):
    """Specifics about how to work with Markdown."""

    NEW_TEMPLATE = """\
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

    @staticmethod
    def parse_text(text) -> SectionDict:  # noqa: D102
        return {}

    @staticmethod
    def format_sections(sections: SectionDict) -> str:  # noqa: D102
        pass
