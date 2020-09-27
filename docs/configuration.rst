#############
Configuration
#############

Scriv tries hard to be adaptable to your project's needs.  Many aspects of its
behavior can be customized with a settings file.

Files read
==========

Scriv will read settings from any of these files:

- setup.cfg

- tox.ini

- changelog.d/scriv.ini

In any of these files, scriv will read settings from a section named either
``[scriv]`` or ``[tool.scriv]``.

If the ``[toml]`` extra is installed, then scriv will also read settings from
pyproject.toml, in the ``[tool.scriv]`` section.


Settings Syntax
===============

Settings use the usual ".ini" syntax, but with some extra features:

- A prefix of ``file:`` reads the setting from a file.

- A prefix of ``literal:`` reads a string literal from a source file.

- Value substitutions can make a setting depend on another setting.

File Prefix
-----------

A ``file:`` prefix means the setting value is a file name, and the actual
setting value will be read from that file.  The file name is relative to the
fragment directory (changelog.d), or is the name of a built-in file provided by
scriv:

- ``new_fragment.md.j2``: The default Jinja template for new Markdown
  fragments.

- ``new_fragment.rst.j2``: The default Jinja template for new ReStructured Text
  fragments.

Literal Prefix
--------------

A ``literal:`` prefix means the setting value will be a literal string read
from a source file.  The setting provides a file name and variable name
separated by colons::

    [scriv]
    version = literal: myproj/__init__.py: __version__

In this case, the file ``myproj/__init__.py`` will be read, and the
``__version__`` value will be found and used as the version setting.

Currently only Python files are supported for literals, but other syntaxes
can be supported in the future.

Value Substitution
------------------

The chosen fragment format can be used in settings by referencing
``${config:format}`` in the setting.  For example, the default template for
new fragments depends on the format because the default setting is::

    new_fragment_template = file: new_fragment.${config:format}.j2


Settings
========

These are the specifics about all of the settings read from the configuration
file.

.. include:: include/config.rst


.. _git_settings:

Per-User Git Settings
=====================

Some aspects of scriv's behavior are configurable for each user rather than for
the project as a whole.  These settings are read from git.

These settings determine whether the ":ref:`cmd_create`" and
":ref:`cmd_collect`" commands will launch an editor, and "git add" the result:

- ``scriv.create.edit``
- ``scriv.create.add``
- ``scriv.collect.edit``
- ``scriv.collect.add``

All of these are either "true" or "false", and default to false. You can create
these settings with `git config`_ commands, either in the current repo::

    $ git config scriv.create.edit true

or globally for all of your repos::

    $ git config --global scriv.create.edit true


.. _git config: https://git-scm.com/book/en/v2/Customizing-Git-Git-Configuration

.. include:: include/links.rst
