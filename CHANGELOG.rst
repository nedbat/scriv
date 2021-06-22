.. this will be appended to README.rst

Changelog
=========

..
   All enhancements and patches to scriv will be documented
   in this file.  It adheres to the structure of http://keepachangelog.com/ ,
   but in reStructuredText instead of Markdown (for ease of incorporation into
   Sphinx documentation and the PyPI description).

   This project adheres to Semantic Versioning (http://semver.org/).

Unreleased
----------

See the fragment files in the `changelog.d directory`_.

.. _changelog.d directory: https://github.com/nedbat/scriv/tree/master/changelog.d


.. scriv-insert-here

0.11.0 — 2021-06-22
-------------------

Added
.....

- A new poorly documented API is available.  See the Scriv, Changelog, and
  Fragment classes in the scriv.scriv module.

Changed
.......

- Python 3.6 is now the minimum supported Python version.

Fixed
.....

- The changelog is now always written as UTF-8, regardless of the default
  encoding of the system.  Thanks, Hei (yhlam).

0.10.0 — 2020-12-27
-------------------

Added
.....

- Settings can now be read from a pyproject.toml file.  Install with the
  "[toml]" extra to be sure TOML support is available.  Closes `issue 9`_.

.. _issue 9: https://github.com/nedbat/scriv/issues/9

- Added the Philosophy section of the docs.

Changed
.......

- The default entry header no longer puts the version number in square
  brackets: this was a misunderstanding of the keepachangelog formatting.

- Respect the existing newline style of changelog files. (`#14`_)
  This means that a changelog file with Linux newlines on a Windows platform
  will be updated with Linux newlines, not rewritten with Windows newlines.
  Thanks, Kurt McKee.

.. _#14: https://github.com/nedbat/scriv/issues/14

Fixed
.....

- Support Windows' directory separator (``\``) in unit test output. (`#15`_)
  This allows the unit tests to run in Windows environments. Thanks, Kurt
  McKee.

- Explicitly specify the directories and files that Black should scan. (`#15`_)
  This prevents Black from scanning every file in a virtual environment.
  Thanks, Kurt McKee.

- Using "literal:" values in the configuration file didn't work on Python 3.6
  or 3.7, as reported in `issue 18`_.  This is now fixed.

.. _#15: https://github.com/nedbat/scriv/issues/15
.. _issue 18: https://github.com/nedbat/scriv/issues/18

0.9.2 — 2020-08-29
------------------

- Packaging fix.

0.9.0 — 2020-08-29
------------------

Added
.....

- Markdown format is supported, both for fragments and changelog entries.

- Fragments can be mixed (some .rst and some .md). They will be collected and
  output in the format configured in the settings.

- Documentation.

- "python -m scriv" now works.

Changed
.......

- The version number is displayed in the help message.

0.8.1 — 2020-08-09
------------------

Added
.....

- When editing a new fragment during "scriv create", if the edited fragment has
  no content (only comments or blank lines), then the create operation will be
  aborted, and the file will be removed. (Closes `issue 2`_.)

.. _issue 2: https://github.com/nedbat/scriv/issues/2

Changed
.......

- If the fragment directory doesn't exist, a simple direct message is shown,
  rather than a misleading FileNotFound error (closes `issue 1`_).

.. _issue 1: https://github.com/nedbat/scriv/issues/1

Fixed
.....

- When not using categories, comments in fragment files would be copied to the
  changelog file (`issue 3`_).  This is now fixed.

.. _issue 3: https://github.com/nedbat/scriv/issues/3

- RST syntax is better understood, so that hyperlink references and directives
  will be preserved. Previously, they were mistakenly interpreted as comments
  and discarded.

0.8.0 — 2020-08-04
------------------

Added
.....

- Added the `collect` command.

- Configuration is now read from setup.cfg or tox.ini.

- A new configuration setting, rst_section_char, determines the character used
  in the underlines for the section headings in .rst files.

- The `new_entry_template` configuration setting is the name of the template
  file to use when creating new entries.  The file will be found in the
  `fragment_directory` directory.  The file name defaults to ``new_entry.FMT.j2``.
  If the file doesn't exist, an internal default will be used.

- Now the collect command also includes a header for the entire entry.  The
  underline is determined by the "rst_header_char" settings.  The heading text
  is determined by the "header" setting, which defaults to the current date.

- The categories list in the config can be empty, meaning entries are not
  categorized.

- The create command now accepts --edit (to open the new entry in your text
  editor), and --add (to "git add" the new entry).

- The collect command now accepts --edit (to open the changelog file in an
  editor after the new entries have been collected) and --add (to git-add the
  changelog file and git rm the entries).

- The names of the main git branches are configurable as "main_branches" in the
  configuration file.  The default is "master", "main", and "develop".

- Configuration values can now be read from files by prefixing them with
  "file:".  File names will be interpreted relative to the changelog.d
  directory, or will be found in a few files installed with scriv.

- Configuration values can interpolate the currently configured format (rst or
  md) with "${config:format}".

- The default value for new templates is now
  "file: new_entry.${config:format}.j2".

- Configuratsion values can be read from string literals in Python code with a
  "literal:" prefix.

- "version" is now a configuration setting.  This will be most useful when used
  with the "literal:" prefix.

- By default, the title of collected changelog entries includes the version if
  it's defined.

- The collect command now accepts a ``--version`` option to set the version
  name used in the changelog entry title.

Changed
.......

- RST now uses minuses instead of equals.

- The `create` command now includes the time as well as the date in the entry
  file name.

- The --delete option to collect is now called --keep, and defaults to False.
  By default, the collected entry files are removed.

- Created file names now include the seconds from the current time.

- "scriv create" will refuse to overwrite an existing entry file.

- Made terminology more uniform: files in changelog.d are "fragments."  When
  collected together, they make one changelog "entry."

- The title text for the collected changelog entry is now created from the
  "entry_title_template" configuration setting.  It's a Jinja2 template.

- Combined the rst_header_char and rst_section_char settings into one:
  rst_header_chars, which much be exactly two characters.

- Parsing RST fragments is more flexible: the sections can use any valid RST
  header characters for the underline.  Previously, it had to match the
  configured RST header character.

Fixed
.....

- Fragments with no category header were being dropped if categories were in
  use.  This is now fixed.  Uncategorized fragments get sorted before any
  categorized fragments.


0.1.0 — 2019-12-30
------------------

* Doesn't really do anything yet.
