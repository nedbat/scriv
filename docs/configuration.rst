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

- ``new_fragment.rst.j2``: The default Jinja template for new reStructuredText
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

It is also possible to specify a variable in a TOML file
using periods to separate the sections and key names::

    [scriv]
    version = literal: pyproject.toml: project.version

Currently only Python and TOML files are supported for literals,
but other syntaxes can be supported in the future.

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

.. [[[cog
    import attr
    import textwrap
    from scriv.config import _Options

    fields = sorted(attr.fields(_Options), key=lambda f: f.name)
    for field in fields:
        name = field.name
        print(f"\n.. _config_{name}:\n")
        print(name)
        print("-" * len(name))
        print()
        text = field.metadata.get("doc", "NO DOC!\n")
        text = textwrap.dedent(text)
        print(text)
        default = field.metadata.get("doc_default")
        if default is None:
            default = field.default
            if isinstance(default, list):
                default = ", ".join(default)
            default = f"``{default}``"
        print(f"Default: {default}")
    print()
.. ]]]

.. _config_categories:

categories
----------

Categories to use as headings for changelog items.
See :ref:`categories`.

Default: ``Removed, Added, Changed, Deprecated, Fixed, Security``

.. _config_end_marker:

end_marker
----------

A marker string indicating where in the changelog file the
changelog ends.

Default: ``scriv-end-here``

.. _config_entry_title_template:

entry_title_template
--------------------

The `Jinja`_ template to use for the entry heading text for
changelog entries created by ":ref:`cmd_collect`".

Default: A combination of version (if specified) and date.

.. _config_format:

format
------

The format to use for fragments and for the output changelog
file.  Can be either "rst" or "md".

Default: ``rst``

.. _config_fragment_directory:

fragment_directory
------------------

The directory for fragments.  This directory must exist, it
will not be created.

Default: ``changelog.d``

.. _config_insert_marker:

insert_marker
-------------

A marker string indicating where in the changelog file new
entries should be inserted.

Default: ``scriv-insert-here``

.. _config_main_branches:

main_branches
-------------

The branch names considered uninteresting to use in new
fragment file names.

Default: ``master, main, develop``

.. _config_md_header_level:

md_header_level
---------------

A number: for Markdown changelog files, this is the heading
level to use for the entry heading.

Default: ``1``

.. _config_new_fragment_template:

new_fragment_template
---------------------

The `Jinja`_ template to use for new fragments.

Default: ``file: new_fragment.${config:format}.j2``

.. _config_output_file:

output_file
-----------

The changelog file updated by ":ref:`cmd_collect`".

Default: ``CHANGELOG.${config:format}``

.. _config_rst_header_chars:

rst_header_chars
----------------

Two characters: for reStructuredText changelog files, these
are the two underline characters to use.  The first is for the
heading for each changelog entry, the second is for the
category sections within the entry.

Default: ``=-``

.. _config_skip_fragments:

skip_fragments
--------------

A glob pattern for files in the fragment directory that should
not be collected.

Default: ``README.*``

.. _config_version:

version
-------

The string to use as the version number in the next header
created by ``scriv collect``.  Often, this will be a
``literal:`` directive, to get the version from a string in a
source file.

Default: (empty)

.. [[[end]]] (checksum: d03f710518bf8c94238e821fbb22b3e1)


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
