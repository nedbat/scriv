"""Tests for scriv/format_rst.py."""

import collections
import re
import textwrap

import pytest

from scriv.config import Config
from scriv.exceptions import ScrivException
from scriv.format_rst import RstTools


@pytest.mark.parametrize(
    "text, parsed",
    [
        # Comments are ignored, and the section headers found.
        pytest.param(
            """\
            .. Comments can be here
            .. and here.
            ..
            .. and here.
            Added
            -----

            - This thing was added.
              And we liked it.

            .. More comments can be here
            ..
            .. And here.

            """,
            {"Added": ["- This thing was added.\n  And we liked it."]},
            id="comments_ignored",
        ),
        # Multiple section headers.
        pytest.param(
            """\
            Added
            -----

            - This thing was added.
              And we liked it.


            Fixed
            -----

            - This thing was fixed.

            - Another thing was fixed.

            Added
            -----

            - Also added
              this thing
              that is very important.

            """,
            {
                "Added": [
                    "- This thing was added.\n  And we liked it.",
                    "- Also added\n  this thing\n  that is very important.",
                ],
                "Fixed": [
                    "- This thing was fixed.",
                    "- Another thing was fixed.",
                ],
            },
            id="multiple_headers",
        ),
        # The specific character used for the header line is unimportant.
        pytest.param(
            """\
            Added
            ^^^^^
            - This thing was added.

            Fixed
            ^^^^^
            - This thing was fixed.
            """,
            {
                "Added": ["- This thing was added."],
                "Fixed": ["- This thing was fixed."],
            },
            id="different_underlines",
        ),
        # You can even use periods as the underline, it won't be confused for a
        # comment.
        pytest.param(
            """\
            Fixed
            .....
            - This thing was fixed.

            Added
            .....

            .. a comment.

            - This thing was added.
            """,
            {
                "Added": ["- This thing was added."],
                "Fixed": ["- This thing was fixed."],
            },
            id="period_underline",
        ),
        # It's fine to have no header at all.
        pytest.param(
            """\
            - No header at all.
            """,
            {None: ["- No header at all."]},
            id="no_header",
        ),
        # It's fine to have comments with no header, and multiple bulllets.
        pytest.param(
            """\
            .. This is a scriv fragment.

            - No header at all.

            - Just plain bullets.
            """,
            {None: ["- No header at all.", "- Just plain bullets."]},
            id="no_header_2",
        ),
        # RST syntax is intricate. We understand a subset of it.
        pytest.param(
            """\
            .. _fixed.1:

            Fixed
            .....
            - This thing was fixed: `issue 42`_.

            .. _issue 42: https://github.com/thing/issue/42

            .. _added:

            Added
            .....

            .. a comment.

            - This thing was added.

            .. note::
                This thing doesn't work yet.
                Not sure it ever will... :(

            .. [cite] A citation

            .. |subst| image:: substitution.png

            ..

            """,
            {
                "Added": [
                    "- This thing was added.",
                    (
                        ".. note::\n"
                        + "    This thing doesn't work yet.\n"
                        + "    Not sure it ever will... :("
                    ),
                    ".. [cite] A citation",
                    ".. |subst| image:: substitution.png",
                ],
                "Fixed": [
                    "- This thing was fixed: `issue 42`_.",
                    ".. _issue 42: https://github.com/thing/issue/42",
                ],
            },
            id="intricate_syntax",
        ),
        # A file with only comments and blanks will produce nothing.
        pytest.param(
            """\
            .. Nothing to see here.
            ..

            .. Or here.


            """,
            {},
            id="empty",
        ),
        # Multiple levels of headings only splits on the top-most one.
        pytest.param(
            """\
            =====
            TITLE
            =====

            Irrelevant stuff

            Heading
            =======

            Ignore this

            .. scriv-insert-here

            (prelude)

            ===========
            Section one
            ===========

            subhead
            -------

            In the sub

            subhead 2
            ---------

            Also sub

            Section two
            ===========

            In section two.

            subhead 3
            ---------
            s2s3
            """,
            {
                None: ["(prelude)"],
                "Section one": [
                    "subhead\n-------",
                    "In the sub",
                    "subhead 2\n---------",
                    "Also sub",
                ],
                "Section two": [
                    "In section two.",
                    "subhead 3\n---------\ns2s3",
                ],
            },
            id="multilevel",
        ),
    ],
)
def test_parse_text(text, parsed):
    actual = RstTools().parse_text(textwrap.dedent(text))
    assert actual == parsed


@pytest.mark.parametrize(
    "sections, expected",
    [
        pytest.param(
            [
                (
                    "Added",
                    [
                        "- This thing was added.\n  And we liked it.",
                        "- Also added\n  this thing\n  that is very important.",
                    ],
                ),
                (
                    "Fixed",
                    ["- This thing was fixed.", "- Another thing was fixed."],
                ),
            ],
            """\

            Added
            ~~~~~

            - This thing was added.
              And we liked it.

            - Also added
              this thing
              that is very important.

            Fixed
            ~~~~~

            - This thing was fixed.

            - Another thing was fixed.
            """,
            id="one",
        ),
        pytest.param(
            [
                (
                    None,
                    [
                        "- This thing was added.\n  And we liked it.",
                        "- Also added\n  this thing\n  that is very important.",
                    ],
                ),
            ],
            """\

            - This thing was added.
              And we liked it.

            - Also added
              this thing
              that is very important.
            """,
            id="two",
        ),
    ],
)
def test_format_sections(sections, expected):
    sections = collections.OrderedDict(sections)
    actual = RstTools(Config(rst_header_chars="#~")).format_sections(sections)
    assert actual == textwrap.dedent(expected)


@pytest.mark.parametrize(
    "config_kwargs, text, fh_kwargs, result",
    [
        ({}, "2020-07-26", {}, "\n2020-07-26\n==========\n"),
        (
            {"rst_header_chars": "*-"},
            "2020-07-26",
            {},
            "\n2020-07-26\n**********\n",
        ),
        (
            {},
            "2022-04-03",
            {"anchor": "here"},
            "\n.. _here:\n\n2022-04-03\n==========\n",
        ),
    ],
)
def test_format_header(config_kwargs, text, fh_kwargs, result):
    actual = RstTools(Config(**config_kwargs)).format_header(text, **fh_kwargs)
    assert actual == result


@pytest.mark.parametrize("fail_if_warn", [False, True])
def test_fake_pandoc(fake_run_command, fail_if_warn):
    fake_run_command.patch_module("scriv.format_rst")
    expected_args = [
        "pandoc",
        "-frst",
        "-tmarkdown_strict",
        "--markdown-headings=atx",
        "--wrap=none",
    ]
    if fail_if_warn:
        expected_args.append("--fail-if-warnings")
    expected_text = "The converted text!\nis multi-line\n"

    def fake_pandoc(argv):
        # We got the arguments we expected, plus one more.
        assert argv[:-1] == expected_args
        return (True, expected_text)

    fake_run_command.add_handler("pandoc", fake_pandoc)
    assert (
        RstTools().convert_to_markdown("Hello", fail_if_warn=fail_if_warn)
        == expected_text
    )


def test_fake_pandoc_failing(fake_run_command):
    fake_run_command.patch_module("scriv.format_rst")
    error_text = "There was a problem!!?!"

    def fake_pandoc(argv):  # pylint: disable=unused-argument
        return (False, error_text)

    fake_run_command.add_handler("pandoc", fake_pandoc)
    expected = f"Couldn't convert ReST to Markdown in '':\n{error_text}"
    with pytest.raises(ScrivException, match=re.escape(expected)):
        _ = RstTools().convert_to_markdown("Hello")


@pytest.mark.parametrize(
    "rst_text, md_text",
    [
        (
            """\
            Look at this list:

            - One issue fixed: `issue 123`_.

            - One change merged: `Big change <pull 234_>`_.

            - Improved the `home page <https://example.com/homepage>`_.

            - One more `small change`__.

            .. _issue 123: https://github.com/joe/project/issues/123
            .. _pull 234: https://github.com/joe/project/pull/234
            __ https://github.com/joe/project/issues/999
            """,
            """\
            Look at this list:

            - One issue fixed: [issue 123](https://github.com/joe/project/issues/123).
            - One change merged: [Big change](https://github.com/joe/project/pull/234).
            - Improved the [home page](https://example.com/homepage).
            - One more [small change](https://github.com/joe/project/issues/999).
            """,
        ),
    ],
)
def test_convert_to_markdown(rst_text, md_text):
    converted = RstTools().convert_to_markdown(textwrap.dedent(rst_text))
    # Different versions of pandoc produce slightly different results.  But the
    # markdown is rendered the same regardless of spaces after the
    # bullet-hyphens, so fix them.
    converted = re.sub(r"(?m)^-\s+", "- ", converted)
    expected = textwrap.dedent(md_text)
    assert expected == converted


@pytest.mark.parametrize(
    "rst_text, msg",
    [
        # Various styles of broken links:
        (
            "One issue fixed: `issue 123`_.",
            "Reference not found for 'issue 123'",
        ),
        (
            "One change merged: `Big change <pull 234>_`_.",
            "Reference not found for 'big change <",
        ),
        (
            "Improved the `home page <https://example.com/homepage`_.",
            "Reference not found for 'home page <",
        ),
        # ("One more `small change`__.", "xxx"),     # Hmm, this doesn't error!
        (
            # Not a mistake in RST, but pandoc can't handle it:
            """\
            A big change, thanks to `Jane Contributor <pull
            91_>`_.

            .. _pull 91: https://github.com/joe/project/91
            """,
            "[WARNING] Reference not found for 'pull91'",
        ),
    ],
)
def test_bad_convert_to_markdown(rst_text, msg):
    with pytest.raises(ScrivException, match=re.escape(msg)):
        converted = RstTools().convert_to_markdown(
            textwrap.dedent(rst_text), fail_if_warn=True
        )
        # if we don't get the exception, we can debug the test:
        print(converted)
