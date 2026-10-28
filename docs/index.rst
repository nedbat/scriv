#####
Scriv
#####

.. [[[cog
    import textwrap
    def include_readme_section(sectname):
        """Pull a chunk from README.rst"""
        with open("README.rst") as freadme:
            for line in freadme:
                if f".. begin-{sectname}" in line:
                    break
            for line in freadme:
                if ".. end" in line:
                    break
                print(line.rstrip())
.. ]]]
.. [[[end]]] (sum: 1B2M2Y8Asg)

Scriv changelog management tool

.. [[[cog include_readme_section("badges") ]]]

| |pypi-badge| |ci-badge| |coverage-badge| |doc-badge|
| |pyversions-badge| |license-badge|
| |sponsor-badge| |mastodon-nedbat|

.. [[[end]]] (sum: haxcrjYNQd)

Overview
========

Scriv is a command-line tool for maintaining changelogs.  It manages a
directory of changelog fragments committed with the code changes, then
aggregates them into a CHANGELOG file when the code is being released.


Getting Started
===============

In your project, create a directory called ``changelog.d``. This is where scriv
will create changelog fragments.

Many aspects of scriv's operation are configurable: you can choose a different
directory name if you like: put a setting in pyproject.toml:

.. code-block:: toml

    [tool.scriv]
    fragment_directory = "changes"

Create a fragment using the ":ref:`cmd_create`" command. It will create a new
file in the fragment directory and open your editor to edit the contents.  The
file name will include the date and time, your user name, and your branch name
to keep it separate from other changelog fragments.

The template for new fragments includes categories of changes. Put your
description in the proper category.  By default, ":ref:`cmd_create`" will add
the new fragment to git so that you can commit it along with the other changes
on your branch.

When it is time to release your project, use the ":ref:`cmd_collect`" command
to aggregate all the fragments into a new entry in your changelog file. By
default the file is called ``CHANGELOG.rst`` but you can specify a different
name with the ``changelog`` setting:

.. code-block:: toml

    [tool.scriv]
    fragment_directory = "changes"
    changelog = "CHANGELOG.md"

You can also choose to publish your changelog entries as GitHub releases with
the ":ref:`cmd_github_release`" command.  It parses the changelog file and
creates or updates GitHub releases to match.  It can be used even with
changelog files that were not created by scriv.

Details
=======

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


.. [[[cog include_readme_section("badge-links") ]]]

.. |pypi-badge| image:: https://img.shields.io/pypi/v/scriv.svg
    :target: https://pypi.python.org/pypi/scriv/
    :alt: PyPI

.. |ci-badge| image:: https://github.com/nedbat/scriv/workflows/Test%20Suite/badge.svg
    :target: https://github.com/nedbat/scriv/actions?query=workflow%3A%22Test+Suite%22
    :alt: Build status

.. |coverage-badge| image:: https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/nedbat/5a304c1c779d4bcc57be95f847e9327f/raw/covbadge.json
    :target: https://github.com/nedbat/scriv/actions?query=workflow%3A%22Test+Suite%22
    :alt: Coverage

.. |doc-badge| image:: https://readthedocs.org/projects/scriv/badge/?version=latest
    :target: http://scriv.readthedocs.io/en/latest/
    :alt: Documentation

.. |pyversions-badge| image:: https://img.shields.io/pypi/pyversions/scriv.svg
    :target: https://pypi.python.org/pypi/scriv/
    :alt: Supported Python versions

.. |license-badge| image:: https://img.shields.io/github/license/nedbat/scriv.svg
    :target: https://github.com/nedbat/scriv/blob/master/LICENSE.txt
    :alt: License

.. |bluesky-nedbat| image:: https://img.shields.io/badge/dynamic/json?style=flat&color=96a3b0&labelColor=3686f7&logo=icloud&logoColor=white&label=@nedbat&url=https%3A%2F%2Fpublic.api.bsky.app%2Fxrpc%2Fapp.bsky.actor.getProfile%3Factor=nedbat.com&query=followersCount
    :target: https://bsky.app/profile/nedbat.com
    :alt: nedbat on Bluesky

.. |mastodon-nedbat| image:: https://img.shields.io/badge/dynamic/json?style=flat&labelColor=450657&logo=mastodon&logoColor=ffffff&label=@nedbat&query=followers_count&url=https%3A%2F%2Fhachyderm.io%2Fapi%2Fv1%2Faccounts%2Flookup%3Facct=nedbat
    :target: https://hachyderm.io/@nedbat
    :alt: nedbat on Mastodon

.. |sponsor-badge| image:: https://img.shields.io/badge/%E2%9D%A4-Sponsor%20me-brightgreen?style=flat&logo=GitHub
    :target: https://github.com/sponsors/nedbat
    :alt: Sponsor me on GitHub

.. [[[end]]] (sum: ixLtq/oX1n)
