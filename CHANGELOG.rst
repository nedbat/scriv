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

.. _changelog-1.6.0:

1.6.0 — 2025-03-24
------------------

Added
.....

- Add a ``print`` command that can write changelog entries to standard out
  or to a file, closing `issue 115`_. Thanks, `Kurt McKee <pull 140_>`_

Changed
.......

- Dropped support for Python 3.7 and 3.8, and added 3.13.

Fixed
.....

- A final newline is no longer stripped when rendering the new fragment
  template, fixing `issue 108`_.

- Configuration setting ``md_header_level`` is allowed to be an integer in
  TOML files, closing `issue 90`_.  Thanks, `Michael Makukha <pull 137_>`_.

.. _issue 90: https://github.com/nedbat/scriv/issues/90
.. _issue 108: https://github.com/nedbat/scriv/issues/108
.. _issue 115: https://github.com/nedbat/scriv/issues/115
.. _pull 137: https://github.com/nedbat/scriv/pull/137
.. _pull 140: https://github.com/nedbat/scriv/pull/140


.. _changelog-1.5.1:

1.5.1 — 2023-12-14
------------------

Fixed
.....

- Fixed the documentation build on ReadTheDocs. Fixes `issue 118`_.

.. _issue 118: https://github.com/nedbat/scriv/issues/118


.. _changelog-1.5.0:

1.5.0 — 2023-10-18
------------------

Added
.....

- RST to Markdown conversion can now be stricter.  Using the ``--fail-if-warn``
  option on the ``scriv github-releases`` command will fail the command if your
  RST conversion generates warnings, for example due to malformed link
  references.

- The ``scriv github-release`` command now has a ``--check-links`` option to
  check URLs.  Each is fetched, and if an error occurs, warnings will show the
  URLs that didn't succeed.

Fixed
.....

- Commands no longer display full tracebacks for exceptions raised by scriv
  code.


.. _changelog-1.4.0:

1.4.0 — 2023-10-12
------------------

Added
.....

- Literals can be extracted from .cabal files.
  Thanks `Javier Sagredo <pull 91_>`_.

- Use the git config ``scriv.user_nick`` for the user nick part
  of the fragment file. Thanks to `Ronny Pfannschmidt <pull 106_>`_,
  fixing `issue 103`_.

- Settings can now be prefixed with ``command:`` to execute the rest of the
  setting as a shell command.  The output of the command will be used as the
  value of the setting.

Fixed
.....

- If there are no changelog fragments, ``scriv collect`` now exits with status
  code of 2, fixing `issue 110`_.

- Changelogs with non-version headings now produce an understandable error
  message from ``scriv collect``, thanks to `James Gerity <pull 101_>`_, fixing
  `issue 100`_.

.. _pull 91: https://github.com/nedbat/scriv/pull/91
.. _issue 100: https://github.com/nedbat/scriv/issues/100
.. _pull 101: https://github.com/nedbat/scriv/pull/101
.. _issue 103: https://github.com/nedbat/scriv/pull/103
.. _pull 106: https://github.com/nedbat/scriv/pull/106
.. _issue 110: https://github.com/nedbat/scriv/issues/110


.. _changelog-1.3.1:

1.3.1 — 2023-04-16
------------------

Fixed
.....

- The Version class introduced in 1.3.0 broke the ``scriv github-release``
  command.  This is now fixed.

.. _changelog-1.3.0:

1.3.0 — 2023-04-16
------------------

Added
.....

- ``.cfg`` files can now be read with ``literal:`` settings, thanks to `Matias
  Guijarro <pull 88_>`_.

.. _pull 88: https://github.com/nedbat/scriv/pull/88

Fixed
.....

- In compliance with `PEP 440`_, comparing version numbers now ignores a
  leading "v" character.  This makes scriv more flexible about how you present
  version numbers in various places (code literals, changelog entries, git
  tags, and so on).  Fixes `issue 89`_.

.. _PEP 440: https://peps.python.org/pep-0440/
.. _issue 89: https://github.com/nedbat/scriv/issues/89

.. _changelog-1.2.1:

1.2.1 — 2023-02-18
------------------

Fixed
.....

- Scriv would fail trying to import tomllib on Python <3.11 if installed
  without the ``[toml]`` extra.  This is now fixed, closing `issue 80`_.

- Settings specified as ``file:`` will now search in the changelog directory
  and then the current directory for the file.  The only exception is if the
  first component is ``.`` or ``..``, then only the current directory is
  considered.  Fixes `issue 82`_.

- Python variables with type annotations can now be read with ``literal:``
  settings, fixing `issue 85`_.

- Error messages for mis-formed ``literal:`` configuration values are more
  precise, as requested in `issue 84`_.

- Error messages from settings validation are ScrivExceptions now, and report
  configuration problems more clearly and earlier in some cases.

.. _issue 80: https://github.com/nedbat/scriv/issues/80
.. _issue 82: https://github.com/nedbat/scriv/issues/82
.. _issue 84: https://github.com/nedbat/scriv/issues/84
.. _issue 85: https://github.com/nedbat/scriv/issues/85


.. _changelog-1.2.0:

1.2.0 — 2023-01-18
------------------

Added
.....

- ``scriv github-release`` now has a ``--repo=`` option to specify which GitHub
  repo to use when you have multiple remotes.

Changed
.......

- Improved the error messages from ``scriv github-release`` when a GitHub repo
  can't be identified among the git remotes.

.. _changelog-1.1.0:

1.1.0 — 2023-01-16
------------------

Added
.....

- The ``scriv github-release`` command has a new setting, ``ghrel_template``.
  This is a template to use when building the release text, to add text before
  or after the Markdown extracted from the changelog.

- The ``scriv github-release`` command now has a ``--dry-run`` option to show
  what would happen, without posting to GitHub.

Changed
.......

- File names specified for ``file:`` settings will be interpreted relative to
  the current directory if they have path components.  If the file name has no
  slashes or backslashes, then the old behavior remains: the file will be found
  in the fragment directory, or as a built-in template.

- All exceptions raised by Scriv are now ScrivException.

Fixed
.....

- Parsing changelogs now take the `insert-marker` setting into account. Only
  content after the insert-marker line is parsed.

- More internal activities are logged, to help debug operations.


.. _changelog-1.0.0:

1.0.0 — 2022-12-03
------------------

Added
.....

- Now literal configuration settings can be read from YAML files. Closes `issue 69`_.
  Thanks, `Florian Küpper <pull 70_>`_.

.. _pull 70: https://github.com/nedbat/scriv/pull/70
.. _issue 69: https://github.com/nedbat/scriv/issues/69

Fixed
.....

- Fixed truncated help summaries by shortening them, closing `issue 63`_.

.. _issue 63: https://github.com/nedbat/scriv/issues/63

.. _changelog-0.17.0:

0.17.0 — 2022-09-18
-------------------

Added
.....

- The ``collect`` command now has a ``--title=TEXT`` option to provide the
  exact text to use as the title of the new changelog entry.  Finishes `issue
  48`_.

.. _issue 48: https://github.com/nedbat/scriv/issues/48

Changed
.......

- The ``github_release`` command now only considers the top-most entry in the
  changelog.  You can use the ``--all`` option to continue the old behavior of
  making or updating GitHub releases for all of the entries.

  This change makes it easier for projects to start using scriv with an
  existing populated changelog file.

  Closes `issue 57`_.

.. _issue 57: https://github.com/nedbat/scriv/issues/57

Fixed
.....

- If there were no fragments to collect, `scriv collect` would make a new empty
  section in the changelog.  This was wrong, and is now fixed. Now the
  changelog remains unchanged in this case.  Closes `issue 55`_.

.. _issue 55: https://github.com/nedbat/scriv/issues/55

- The ``github-release`` command will now issue a warning for changelog entries
  that have no version number. These can't be made into releases, so they are
  skipped.  (`issue 56`_).

.. _issue 56: https://github.com/nedbat/scriv/issues/56

- ``scriv collect`` will end with an error now if the version number would
  duplicate a version number on an existing changelog entry. Fixes `issue 26`_.

.. _issue 26: https://github.com/nedbat/scriv/issues/26

.. _changelog-0.16.0:

0.16.0 — 2022-07-24
-------------------

Added
.....

- The ``github_release`` command will use a GitHub personal access token stored
  in the GITHUB_TOKEN environment variable, or from a .netrc file.

Fixed
.....

- The github_release command was using `git tags` as a command when it should
  have used `git tag`.

- Anchors in the changelog were being included in the previous sections when
  creating GitHub releases.  This has been fixed, closing `issue 53`_.

.. _issue 53: https://github.com/nedbat/scriv/issues/53

.. _changelog-0.15.2:

0.15.2 — 2022-06-18
-------------------

Fixed
.....

- Quoted commands failed, so we couldn't determine the GitHub remote.

.. _changelog-0.15.1:

0.15.1 — 2022-06-18
-------------------

Added
.....

- Added docs for ``scriv github-release``.

Fixed
.....

- Call pandoc properly on Windows for the github_release command.

.. _changelog-0.15.0:

0.15.0 — 2022-04-24
-------------------

Removed
.......

- Dropped support for Python 3.6.

Added
.....

- The `github-release` command parses the changelog and creates GitHub releases
  from the entries.  Changed entries will update the corresponding release.

- Added a ``--version`` option.

Changed
.......

- Parsing of fragments now only attends to the top-level section headers, and
  includes nested headers instead of splitting on all headers.


.. _changelog-0.14.0:

0.14.0 — 2022-03-23
-------------------

Added
.....

- Add an anchor before each version section in the output of ``scriv collect``
  so URLs for the sections are predictable and stable for each new version
  (Fixes `issue 46`_). Thanks Abhilash Raj and Rodrigo Girão Serrão.

Fixed
.....

- Markdown fragments weren't combined properly. Now they are. Thanks Rodrigo
  Girão Serrão.

.. _issue 46: https://github.com/nedbat/scriv/issues/46


0.13.0 — 2022-01-23
-------------------

Added
.....

-   Support finding version information in TOML files (like ``pyproject.toml``)
    using the ``literal`` configuration directive.  Thanks, Kurt McKee

0.12.0 — 2021-07-28
-------------------

Added
.....

- Fragment files in the fragment directory will be skipped if they match the
  new configuration value ``skip_fragments``, a glob pattern.  The default
  value is "README.*". This lets you put a README.md file in that directory to
  explain its purpose, as requested in `issue 40`_.

.. _issue 40: https://github.com/nedbat/scriv/issues/40

Changed
.......

- Switched from "toml" to "tomli" for reading TOML files.

Fixed
.....

- Setting ``format=md`` didn't properly cascade into other default settings,
  leaving you with RST settings that needed to be explicitly overridden
  (`issue 39`_).  This is now fixed.

.. _issue 39: https://github.com/nedbat/scriv/issues/39

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

- Explicitly specify the directories and files that Black should scan. (`#16`_)
  This prevents Black from scanning every file in a virtual environment.
  Thanks, Kurt McKee.

- Using "literal:" values in the configuration file didn't work on Python 3.6
  or 3.7, as reported in `issue 18`_.  This is now fixed.

.. _#15: https://github.com/nedbat/scriv/issues/15
.. _#16: https://github.com/nedbat/scriv/issues/16
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

- Configuration values can be read from string literals in Python code with a
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
