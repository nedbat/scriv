"""ReStructured text knowledge for scriv."""

from typing import Dict

from .format import FormatTools, SectionDict


class RstTools(FormatTools):
    """Specifics about how to work with ReStructured Text."""

    def parse_text(self, text: str) -> SectionDict:  # noqa: D102 (inherited docstring)
        # Parse a very restricted subset of rst.
        sections = {}  # type: SectionDict

        lines = text.splitlines()
        lines.append("")

        prev_line = ""
        paragraphs = None

        for line in lines:
            line = line.rstrip()

            if line[:2] == "..":
                # Comment, do nothing.
                continue

            if line[:3] == self.config.rst_section_char * 3:
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
            sections[section] = [par.rstrip() for par in paragraphs if par]

        return sections

    def format_header(self, data: Dict) -> str:  # noqa: D102 (inherited docstring)
        if self.config.header:
            text = self.config.header.format_map(data)
            return "\n" + text + "\n" + self.config.rst_header_char * len(text) + "\n"
        else:
            return ""

    def format_sections(self, sections: SectionDict) -> str:  # noqa: D102 (inherited docstring)
        lines = []
        for section, paragraphs in sections.items():
            lines.append("")
            lines.append(section)
            lines.append(self.config.rst_section_char * len(section))
            for paragraph in paragraphs:
                lines.append("")
                lines.append(paragraph)

        return "\n".join(lines) + "\n"
