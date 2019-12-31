"""ReStructured text knowledge for scriv."""

from typing import Dict, List

from scriv.format import FormatTools


class RstTools(FormatTools):
    """Specifics about how to work with ReStructured Text."""

    NEW_TEMPLATE = """\
        .. A new scriv entry.
        ..
        .. Uncomment the header that is right (remove the leading dots).
        ..
        {% for cat in config.categories -%}
        .. {{ cat }}
        .. {{ '=' * (cat|length) }}
        ..
        .. - A bullet item for the {{ cat }} category.
        ..
        {% endfor -%}
        """

    @staticmethod
    def parse_text(text: str) -> Dict[str, List[str]]:  # noqa: D102
        # Parse a very restricted subset of rst.
        sections = {}  # type: Dict[str, List[str]]

        lines = text.splitlines()
        lines.append("")

        prev_line = ""
        paragraphs = None

        for line in lines:
            line = line.rstrip()

            if line[:3] == ".. ":
                # Comment, do nothing.
                continue

            if line[:3] == "---":
                # Section underline. Previous line was the heading.
                if paragraphs is not None:
                    # Heading was made a paragraph, undo that.
                    if paragraphs[-1] == prev_line + "\n":  # pylint: disable=unsubscriptable-object
                        paragraphs.pop()
                paragraphs = sections.setdefault(prev_line, [])
                paragraphs.append("")
                continue

            if not line:
                # A blank, start a new paragraph.
                if paragraphs is not None:
                    paragraphs.append("")
                continue

            if paragraphs is not None:
                paragraphs[-1] += line + "\n"

            prev_line = line

        # Trim out all empty paragraphs.
        for section, paragraphs in sections.items():
            sections[section] = list(filter(None, paragraphs))

        return sections
