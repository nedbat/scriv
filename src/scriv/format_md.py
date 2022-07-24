"""Markdown text knowledge for scriv."""

import re
from typing import Optional

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
        section_mark = None

        for line in lines:
            line = line.rstrip()
            if in_comment:
                if re.search(r"-->$", line):
                    in_comment = False
            else:
                if re.search(r"^\s*<!--.*-->$", line):
                    # A one-line comment, skip it.
                    continue
                if re.search(r"""^<a id=(['"])[-.\w]+\1></a>$""", line):
                    # An anchor, we don't need those.
                    continue
                if re.search(r"^\s*<!--", line):
                    in_comment = True
                    continue
                if re.search(r"^#+ ", line):
                    if section_mark is None or line.startswith(section_mark):
                        section_title = line.split(maxsplit=1)[1]
                        paragraphs = sections.setdefault(section_title, [])
                        paragraphs.append("")
                        section_mark = line.partition(" ")[0] + " "
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
        self, text: str, anchor: Optional[str] = None
    ) -> str:  # noqa: D102 (inherited docstring)
        num = int(self.config.md_header_level)
        header = "\n"
        if anchor:
            header += f"<a id='{anchor}'></a>\n"
        header += "#" * num + " " + text + "\n"
        return header

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

    def convert_to_markdown(
        self, text: str
    ) -> str:  # noqa: D102 (inherited docstring)
        return text
