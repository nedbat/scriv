########
Concepts
########

.. _fragments:

Fragments
=========

Fragments are files describing your latest work, created by the
":ref:`cmd_create`" command.  The files are created in the changelog.d directory
(settable with :ref:`config_fragment_directory`).  Typically, they are
committed with the code change itself, then later aggregated into the changelog
file with ":ref:`cmd_collect`".

Checking Fragments Render in Sphinx
-----------------------------------

If you use Sphinx to build your documentation, you may want to ensure that your changelog fragments contain valid reStructuredText before they are collected into the main changelog.

1. Move your ``changelog.d`` folder under your Sphinx docs folder (so ``toctree`` directives can access it). For example, configure `scriv` to use ``docs/changelog.d``:

   .. code-block:: toml

       [tool.scriv]
       fragment_directory = "docs/changelog.d"

2. Include a hidden ``toctree`` directive in the Sphinx page that includes the main ``CHANGELOG.rst`` file. This will syntax check the unreleased fragments without linking them visibly:

   .. code-block:: rest

       .. Syntax check the changelog fragments

       .. toctree::
          :hidden:
          :glob:

          changelog.d/*

       .. Include the scriv-generated changelog details

       .. include:: ../CHANGELOG.rst


.. _categories:

Categories
==========

Changelog entries can be categorized, for example as additions, fixes,
removals, and breaking changes.  The list of categories is settable with
the :ref:`config_categories` setting.

If you are using categories in your project, new fragments will be
pre-populated with all the categories, commented out. While editing the
fragment, you provide your change information in the appropriate category.
When the fragments are collected, they are grouped by category into a single
changelog entry.

Any fragments that do not specify a category are included as top-level
release notes directly under the release heading.

You can choose not to use categories by setting the :ref:`config_categories`
setting to empty (all notes will appear as top-level release notes).


.. _entries:

Entries
=======

Fragments are collected into changelog entries with the ":ref:`cmd_collect`"
command. The fragments are combined in each category, in chronological order.
The entry is given a header with version and date.
