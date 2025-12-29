"""Markdown text knowledge for scriv."""

import re

from .format import FormatTools, SectionDict


class MdTools(FormatTools):
    """Specifics about how to work with Markdown."""

    def parse_text(
        self,
        text,
    ) -> SectionDict:  # noqa: D102 (inherited docstring)
        lines = text.splitlines()

        # If there's an insert marker, start there.
        for lineno, line in enumerate(lines):
            if self.config.start_marker in line:
                lines = lines[lineno + 1 :]
                break

        sections: SectionDict = {}
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
        self,
        text: str,
        anchor: str | None = None,
    ) -> str:  # noqa: D102 (inherited docstring)
        header = "\n"
        if anchor and self.config.md_html_anchors:
            header += f"<a id='{anchor}'></a>\n"
        if self.config.md_setext_chars:
            header += text + "\n"
            header += self.config.md_setext_chars[0] * len(text) + "\n"
        else:
            num = int(self.config.md_header_level)
            header += "#" * num + " " + text + "\n"
        return header

    def format_sections(
        self,
        sections: SectionDict,
    ) -> str:  # noqa: D102 (inherited docstring)
        lines = [""]
        for section, paragraphs in sections.items():
            if section:
                if self.config.md_setext_chars:
                    lines.append(section)
                    lines.append(self.config.md_setext_chars[1] * len(section))
                else:
                    header_level = int(self.config.md_header_level) + 1
                    lines.append("#" * header_level + " " + section)
                lines.append("")
            for paragraph in paragraphs:
                lines.append(paragraph)
                if not self.config.compact_fragments:
                    lines.append("")
            if self.config.compact_fragments and lines[-1] != "":
                lines.append("")

        return "\n".join(lines)

    def convert_to_markdown(
        self, text: str, name: str = "", fail_if_warn: bool = False
    ) -> str:  # noqa: D102 (inherited docstring)
        return text
