#####
Scriv
#####

Scriv changelog management tool

Overview
========

Scriv is a command-line tool for helping developers maintain useful changelogs.
It manages a directory of changelog fragments. It aggregates them into entries
in a CHANGELOG file.

Currently scriv implements a simple workflow. The goal is to adapt to more
styles of changelog management in the future.


Getting Started
===============

Scriv writes changelog fragments into a directory called "changelog.d".  Start
by creating this directory.  (By the way, like many aspects of scriv's
operation, you can choose a different name for this directory.)

To make a new changelog fragment, use the ":ref:`cmd_create`" command.  It will
make a new file with a filename using the current date and time, your GitHub or
Git user name, and your branch name.  Changelog fragments should be committed
along with all the other changes on your branch.

When it is time to release your project, the ":ref:`cmd_collect`" command
aggregates all the fragments into a new entry in your changelog file.

You can also choose to publish your changelog entries as GitHub releases with
the ":ref:`cmd_github_release`" command.  It parses the changelog file and
creates or updates GitHub releases to match.  It can be used even with
changelog files that were not created by scriv.

.. toctree::
    :maxdepth: 1

    philosophy
    concepts
    commands
    configuration
    changelog

..    scenarios
..        lib, every commit published
..        app, no version numbers
..        lib, occasional publish
