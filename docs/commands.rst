########
Commands
########

.. [[[cog
    # Force help text to be wrapped narrow enough to not trigger doc8 warnings.
    import os
    os.environ["COLUMNS"] = "78"

    import contextlib
    import io
    import textwrap
    from scriv.cli import cli

    def show_help(cmd):
        with contextlib.redirect_stdout(io.StringIO()) as help_out:
            with contextlib.suppress(SystemExit):
                cli([cmd, "--help"])
        help_text = help_out.getvalue()
        help_text = help_text.replace("python -m cogapp", "scriv")
        print("\n.. code::\n")
        print(f"    $ scriv {cmd} --help")
        print(textwrap.indent(help_text, "    ").rstrip())
.. ]]]
.. [[[end]]] (checksum: d41d8cd98f00b204e9800998ecf8427e)

.. _cmd_create:

scriv create
============

.. [[[cog show_help("create") ]]]

.. code::

    $ scriv create --help
    Usage: scriv create [OPTIONS]

      Create a new changelog fragment.

    Options:
      --add / --no-add     'git add' the created file.
      --edit / --no-edit   Open the created file in your text editor.
      -v, --verbosity LVL  Either CRITICAL, ERROR, WARNING, INFO or DEBUG
      --help               Show this message and exit.
.. [[[end]]] (checksum: 45edec1fd1ebc343358cbf774ba5a49c)

The create command creates new :ref:`fragments <fragments>`.

File creation
-------------

Fragments are created in the changelog.d directory. The name of the directory
can be configured with the :ref:`config_fragment_directory` setting.

The file name starts with the current date and time, so that entries can later
be collected in chronological order. To help make the files understandable, the
file name also includes the creator's git name, and the branch name you are
working on.  "Main" branch names aren't included, to cut down on uninteresting
noise.  The branch names considered uninteresting are settable with the
:ref:`config_main_branches` setting.

The initial contents of the fragment file are populated from the
:ref:`config_new_fragment_template` template.  The format is either
reStructuredText or Markdown, selectable with the :ref:`config_format`
setting.

The default new fragment templates create empty sections for each
:ref:`category <categories>`.  Uncomment the one you want to use, and create a
bullet for the changes you are describing.  If you need a different template
for new fragments, you can create a `Jinja`_ template and name it in the
:ref:`config_new_fragment_template` setting.

Editing
-------

If ``--edit`` is provided, or if ``scriv.create.edit`` is set to true in your
:ref:`git settings <git_settings>`, scriv will launch an editor for you to edit
the new fragment.  Scriv uses the same editor that git launches for commit
messages.

The format of the fragment should be sections for the categories, with bullets
for each change.  The file is re-parsed when it is collected, so the specifics
of things like header underlines don't have to match the changelog file, that
will be adjusted later.

Once you save and exit the editor, scriv will continue working on the file.  If
the file is empty because you removed all of the non-comment content, scriv
will stop.

Adding
------

If ``--add`` is provided, or if ``scriv.create.add`` is set to true in your
:ref:`git settings <git_settings>`, scriv will "git add" the new file so that
it is ready to commit.


.. _cmd_collect:

scriv collect
=============

.. [[[cog show_help("collect") ]]]

.. code::

    $ scriv collect --help
    Usage: scriv collect [OPTIONS]

      Collect and combine fragments into the changelog.

    Options:
      --add / --no-add     'git add' the updated changelog file and removed
                           fragments.
      --edit / --no-edit   Open the changelog file in your text editor.
      --title TEXT         The title text to use for this entry.
      --keep               Keep the fragment files that are collected.
      --version TEXT       The version name to use for this entry.
      -v, --verbosity LVL  Either CRITICAL, ERROR, WARNING, INFO or DEBUG
      --help               Show this message and exit.
.. [[[end]]] (checksum: e93ca778396310ce406f1cc439cefdd4)

The collect command aggregates all the current fragments into the changelog
file.

Entry Creation
--------------

All of the .rst or .md files in the fragment directory are read, parsed, and
re-assembled into a changelog entry.  The entry's title is determined by the
:ref:`config_entry_title_template` setting. The default uses the version string
(if one is specified in the :ref:`config_version` setting) and the current
date.

Instead of using the title template, you can provide an exact title to use for
the new entry with the ``--title`` option.

The output file is specified by the :ref:`config_output_file` setting.  Scriv
looks in the file for a special marker (usually in a comment) to determine
where to insert the new entry.  The marker is "scriv-insert-here", but can be
changed with the :ref:`config_insert_marker` setting.  Using a marker like
this, you can have your changelog be just part of a larger README file.  If
there is no marker in the file, the new entry is inserted at the top of the
file.


Fragment Deletion
-----------------

The fragment files that are read will be deleted, because they are no longer
needed.  If you would prefer to keep the fragment files, use the ``--keep``
option.

Editing
-------

If ``--edit`` is provided, or if ``scriv.collect.edit`` is set to true in your
:ref:`git settings <git_settings>`, scriv will launch an editor for you to edit
the changelog file.  Mostly you shouldn't need to do this, but you might want
to make some tweaks.  Scriv uses the same editor that git launches for commit
messages.

Adding
------

If ``--add`` is provided, or if ``scriv.collect.add`` is set to true in your
:ref:`git settings <git_settings>`, scriv will "git add" the updates to the
changelog file, and the fragment file deletions, so that they are ready to
commit.


.. _cmd_github_release:

scriv github-release
====================

.. [[[cog show_help("github-release") ]]]

.. code::

    $ scriv github-release --help
    Usage: scriv github-release [OPTIONS]

      Create GitHub releases from the changelog.

      Only the most recent changelog entry is used, unless --all is provided.

    Options:
      --all                Use all of the changelog entries.
      --check-links        Check that links are valid (EXPERIMENTAL).
      --dry-run            Don't post to GitHub, just show what would be done.
      --fail-if-warn       Fail if a conversion generates warnings.
      --repo TEXT          The GitHub repo (owner/reponame) to create the
                           release in.
      -v, --verbosity LVL  Either CRITICAL, ERROR, WARNING, INFO or DEBUG
      --help               Show this message and exit.
.. [[[end]]] (checksum: ec63a3f79902b40a74e633cdeb1bf3dc)

The ``github-release`` command reads the changelog file, parses it into
entries, and then creates or updates GitHub releases to match.  Only the most
recent changelog entry is used, unless ``--all`` is provided.

An entry must have a version number in the title, and that version number must
correspond to a git tag.  For example, this changelog entry with the title
``v1.2.3 -- 2022-04-06`` will be processed and the version number will be
"v1.2.3".  If there's a "v1.2.3" git tag, then the entry is a valid release.
If there's no detectable version number in the header, or there isn't a git
tag with the same number, then the entry can't be created as a GitHub release.

The ``--fail-if-warn`` option will end the command if a format conversion
generates a warning, usually because of a missing reference.  The
``--check-links`` option will find the URLs in the release description, and
check if they are valid.  Warnings are displayed for invalid URLs, but the
command still creates the release.

This command is independent of the other commands.  It can be used with a
hand-edited changelog file that wasn't created with scriv.

For writing to GitHub, you need a GitHub personal access token, either stored
in your .netrc file, or in the GITHUB_TOKEN environment variable.

The GitHub repo will be determined by examining the git remotes.  If there
is just one GitHub repo in the remotes, it will be used to create the release.
You can explicitly specify a repo in ``owner/reponame`` form with the
``--repo=`` option if needed.

If your changelog file is in reStructuredText format, you will need `pandoc`_
2.11.2 or later installed for the command to work.

.. _pandoc: https://pandoc.org/

scriv print
===========

.. [[[cog show_help("print") ]]]

.. code::

    $ scriv print --help
    Usage: scriv print [OPTIONS]

      Print collected fragments, or print an entry from the changelog.

    Options:
      --version TEXT       The version of the changelog entry to extract.
      --output PATH        The path to a file to write the output to.
      -v, --verbosity LVL  Either CRITICAL, ERROR, WARNING, INFO or DEBUG
      --help               Show this message and exit.
.. [[[end]]] (checksum: f652a3470da5f726b13ba076471b2444)

The ``print`` command writes a changelog entry to standard out.

If ``--output`` is provided, the changelog entry is written to the given file.

If ``--version`` is given, the requested changelog entry is extracted
from the CHANGELOG.
If not, then the changelog entry is generated from uncollected fragment files.

.. include:: include/links.rst
