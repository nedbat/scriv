#############
Configuration
#############

.. highlight:: ini

Scriv tries hard to be adaptable to your project's needs.  Many aspects of its
behavior can be customized with a settings file.

Files Read
==========

Scriv will read settings from any of these files:

- setup.cfg

- tox.ini

- pyproject.toml

- scriv.ini in the fragment directory ("changelog.d/" by default)

In .ini or .cfg files, scriv will read settings from a section named either
``[scriv]`` or ``[tool.scriv]``.

A .toml file will only be read if the tomli or tomllib modules is available.
You can install scriv with the ``[toml]`` extra to install tomli, or tomllib is
available with Python 3.11 or greater.  In a .toml file, settings will only be
read from the ``[tool.scriv]`` section.

All of the possible files will be read, and settings will cascade.  So for
example, setup.cfg can set the fragment directory to "scriv.d", then
"scriv.d/scriv.ini" will be read.

The settings examples here show .ini syntax.  If you are using a pyproject.toml
file for settings, you will need to adjust for TOML syntax.  This .ini
example::

    [scriv]
    version = literal: pyproject.toml: project.version

would become:

.. code-block:: toml

    [tool.scriv]
    version = "literal: pyproject.toml: project.version"


Settings Syntax
===============

Settings use the usual syntax, but with some extra features:

- A prefix of ``file:`` reads the setting from a file.

- A prefix of ``literal:`` reads a literal data from a source file.

- A prefix of ``command:`` runs the command and uses the output as the setting.

- Value substitutions can make a setting depend on another setting.

These are each explained below:


File Prefix
-----------

A ``file:`` prefix means the setting is a file name or path, and the actual
setting value will be read from that file.  The file name will be searched for
in three places: the fragment directory (changelog.d by default), the current
directory, or one of a few built-in templates.  If the first path component is
``.`` or ``..``, then only the current directory is considered.

Scriv provides two built-in templates:

.. [[[cog
    import textwrap
    def include_file(fname):
        """Include a source file into the docs as a code block."""
        print(".. code-block:: jinja\n")
        with open(fname) as f:
            print(textwrap.indent(f.read(), prefix="    "))
.. ]]]
.. [[[end]]] (checksum: d41d8cd98f00b204e9800998ecf8427e)

- ``new_fragment.md.j2``: The default Jinja template for new Markdown
  fragments:

  .. [[[cog include_file("src/scriv/templates/new_fragment.md.j2") ]]]
  .. code-block:: jinja

      <!--
      A new scriv changelog fragment.

      Uncomment the section that is right (remove the HTML comment wrapper).
      For top level release notes, leave all the headers commented out.
      -->

      {% for cat in config.categories -%}
      <!--
      ### {{ cat }}

      - A bullet item for the {{ cat }} category.

      -->
      {% endfor -%}

  .. [[[end]]] (checksum: 5ea187a050bfc23014591238b22520ff)

- ``new_fragment.rst.j2``: The default Jinja template for new reStructuredText
  fragments:

  .. [[[cog include_file("src/scriv/templates/new_fragment.rst.j2") ]]]
  .. code-block:: jinja

      .. A new scriv changelog fragment.
      {% if config.categories -%}
      ..
      .. Uncomment the section that is right (remove the leading dots).
      .. For top level release notes, leave all the headers commented out.
      ..
      {% for cat in config.categories -%}
      .. {{ cat }}
      .. {{ config.rst_header_chars[1] * (cat|length) }}
      ..
      .. - A bullet item for the {{ cat }} category.
      ..
      {% endfor -%}
      {% else %}
      - A bullet item for this fragment. EDIT ME!
      {% endif -%}

  .. [[[end]]] (checksum: 307b2d307df5eb3a5d316dc850c68011)

Literal Prefix
--------------

A ``literal:`` prefix means the setting value will be a literal string read
from a source file.  The setting provides a file name and value name separated
by colons::

    [scriv]
    version = literal: myproj/__init__.py: __version__

In this case, the file ``myproj/__init__.py`` will be read, and the
``__version__`` value will be found and used as the version setting.

Currently Python, .cfg, TOML, YAML and Cabal files are supported for literals,
but other syntaxes can be supported in the future.

When reading a literal from a TOML file, the value is specified using periods
to separate the sections and key names::

    [scriv]
    version = literal: pyproject.toml: project.version

For data from a YAML file, use periods in the value name to access dictionary
keys::

    [scriv]
    version = literal: galaxy.yaml: myproduct.versionString

When using a Cabal file, the version of the package can be accessed using::

    [scriv]
    version = literal: my-package.cabal: version

Commands
--------

A ``command:`` prefix indicates that the setting is a shell command to run.
The output will be used as the setting::

    [scriv]
    version = command: my_version_tool --next

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
        print(f"\n\n.. _config_{name}:\n")
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
        print("\n".join(textwrap.wrap(f"Default: {default}")))
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

Default: ``{% if version %}{{ version }} — {% endif %}{{
date.strftime('%Y-%m-%d') }}``


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


.. _config_ghrel_template:

ghrel_template
--------------

The template to use for GitHub releases created by the
``scriv github-release`` command.

The extracted Markdown text is available as ``{{body}}``.  You
must include this to use the text from the changelog file.  The
version is available as ``{{version}}``.

The data for the release is available in a ``{{release}}``
object, including ``{{release.prerelease}}``.  It's  a boolean,
true if this is a pre-release version.

The scriv configuration is available in a ``{{config}}`` object.

Default: ``{{body}}``


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

.. [[[end]]] (checksum: 675df32fb207262bd0c69a94a99c2fb7)


.. _git_settings:

Per-User Git Settings
=====================

Some aspects of scriv's behavior are configurable for each user rather than for
the project as a whole.  These settings are read from git.

Editing and Adding
------------------

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

User Nickname
-------------

Scriv includes your git or GitHub username in the file names of changelog
fragments you create.  If you don't like the name it finds for you, you can set
a name as the ``scriv.user_nick`` git setting.


.. _git config: https://git-scm.com/book/en/v2/Customizing-Git-Git-Configuration

.. include:: include/links.rst
