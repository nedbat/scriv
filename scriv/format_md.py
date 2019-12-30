"""Markdown text knowledge for scriv."""

import textwrap

from scriv.format import FormatTools


class MdTools(FormatTools):
    """Specifics about how to work with Markdown."""

    NEW_TEMPLATE = textwrap.dedent(
        """\
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
    )
