"""reStructuredText knowledge for scriv."""

import os
import re
import tempfile
from typing import Optional

from .format import FormatTools, SectionDict
from .shell import run_command


class RstTools(FormatTools):
    """Specifics about how to work with reStructuredText."""

    HEADER_CHARS = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"

    def _is_underline(self, line: str) -> bool:
        """
        Determine if `line` is a valid RST underline.
        """
        return (
            len(line) >= 3
            and line[0] in self.HEADER_CHARS
            and len(set(line)) == 1
        )

    def _is_comment(self, line: str) -> bool:
        """
        Determine if a line is a comment.

        RST syntax is subtle, so we have to check for other kinds of dot-dot
        lines that are not comments.
        """
        if line.startswith(".."):
            if line == "..":
                return True
            elif line.startswith(("...", ".. _", ".. [", ".. |")):
                # It's an underline, hyperlink, citation, or substitution, so
                # not a comment.
                return False
            elif re.search(r"^.. [\w_+:.-]+::", line):
                # A directive: not a comment.
                return False
            else:
                return True
        else:
            return False

    def _is_anchor(self, line: str) -> bool:
        """
        Determine if a line is an anchor.
        """
        return bool(re.search(r"^.. _[-.\w]+:$", line))

    def parse_text(
        self, text: str
    ) -> SectionDict:  # noqa: D102 (inherited docstring)
        # Parse a very restricted subset of rst.
        sections = {}  # type: SectionDict

        lines = text.splitlines()
        lines.append("")

        prev_line = ""
        paragraphs = None
        section_char = None

        for line in lines:
            line = line.rstrip()

            if self._is_comment(line):
                # Comment, do nothing.
                continue

            if self._is_anchor(line):
                continue

            if self._is_underline(line):
                if section_char is None or line[0] == section_char:
                    # Section underline. Previous line was the heading.
                    # General RST can have overlines as well as underlines, but
                    # we only deal with underlines, so some paragraphs must have
                    # preceded us.
                    assert paragraphs is not None
                    # Heading was made a paragraph, undo that.
                    assert paragraphs[-1] == prev_line + "\n"
                    paragraphs.pop()
                    paragraphs = sections.setdefault(prev_line, [])
                    paragraphs.append("")
                    section_char = line[0]
                    continue

            if not line:
                # A blank, start a new paragraph.
                if paragraphs is not None:
                    paragraphs.append("")
                continue

            if paragraphs is None:
                paragraphs = sections.setdefault(None, [])
                paragraphs.append("")

            paragraphs[-1] += line + "\n"

            prev_line = line

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
        header = "\n"
        if anchor:
            header += f".. _{anchor}:\n\n"
        header += (
            text + "\n" + self.config.rst_header_chars[0] * len(text) + "\n"
        )
        return header

    def format_sections(
        self, sections: SectionDict
    ) -> str:  # noqa: D102 (inherited docstring)
        lines = []
        for section, paragraphs in sections.items():
            if section:
                lines.append("")
                lines.append(section)
                lines.append(self.config.rst_header_chars[1] * len(section))
            for paragraph in paragraphs:
                lines.append("")
                lines.append(paragraph)

        return "\n".join(lines) + "\n"

    def convert_to_markdown(
        self, text: str
    ) -> str:  # noqa: D102 (inherited docstring)
        rst_file = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", prefix="scriv_rst_", delete=False
            ) as rst_file:
                rst_file.write(text)
                rst_file.flush()
                ok, output = run_command(
                    "pandoc -frst -tmarkdown_strict "
                    + "--markdown-headings=atx --wrap=none "
                    + rst_file.name
                )
                if not ok:
                    raise Exception(
                        f"Couldn't convert ReST to Markdown: {output!r}"
                    )
                return output.replace("\r\n", "\n")
        finally:
            if rst_file is not None:
                os.unlink(rst_file.name)
