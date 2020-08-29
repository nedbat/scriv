#####
Scriv
#####

Scriv changelog management tool

Overview
========

Scriv is a command-line tool for helping developers maintain useful changelogs.
It manages a directory of changelog fragments. It aggregates them into entries
in a CHANGELOG file.

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


.. toctree::
    :maxdepth: 1

    concepts
    commands
    configuration
    changelog

..    scenarios
..        lib, every commit published
..        app, no version numbers
..        lib, occasional publish
