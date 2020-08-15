"""Markdown text knowledge for scriv."""

import re

from .format import FormatTools, SectionDict


class MdTools(FormatTools):
    """Specifics about how to work with Markdown."""

    def parse_text(
        self, text
    ) -> SectionDict:  # noqa: D102 (inherited docstring)
        sections = {}  # type: SectionDict
        lines = text.splitlines()
        in_comment = False
        paragraphs = None

        for line in lines:
            line = line.rstrip()
            if in_comment:
                if re.search(r"-->$", line):
                    in_comment = False
            else:
                if re.search(r"^\s*<!--.*-->$", line):
                    # A one-line comment, skip it.
                    continue
                if re.search(r"^\s*<!--", line):
                    in_comment = True
                    continue
                if line.startswith("# "):
                    section_title = line[2:]
                    paragraphs = sections.setdefault(section_title, [])
                    paragraphs.append("")
                    continue

                if not line:
                    if paragraphs is not None:
                        paragraphs.append("")
                    continue

                if paragraphs is None:
                    paragraphs = sections.setdefault(None, [])
                    paragraphs.append("")

                paragraphs[-1] += line + "\n"

        # Trim out all empty paragraphs.
        sections = {
            section: [par.rstrip() for par in paragraphs if par]
            for section, paragraphs in sections.items()
            if paragraphs
        }
        return sections

    def format_header(
        self, text: str
    ) -> str:  # noqa: D102 (inherited docstring)
        num = int(self.config.md_header_level)
        return "\n" + "#" * num + " " + text + "\n"

    def format_sections(
        self, sections: SectionDict
    ) -> str:  # noqa: D102 (inherited docstring)
        lines = []
        for section, paragraphs in sections.items():
            if section:
                lines.append("")
                lines.append(
                    "#" * (int(self.config.md_header_level) + 1) + " " + section
                )
            for paragraph in paragraphs:
                lines.append("")
                lines.append(paragraph)

        return "\n".join(lines) + "\n"
