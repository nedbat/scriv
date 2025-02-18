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
.. [[[end]]] (checksum: d41d8cd98f00b204e9800998ecf8427e)

Scriv changelog management tool

.. [[[cog include_readme_section("badges") ]]]

| |pypi-badge| |ci-badge| |coverage-badge| |doc-badge|
| |pyversions-badge| |license-badge| |sponsor-badge| |mastodon-nedbat|

.. [[[end]]] (checksum: 8f16614e7d2eb8fa4e13bacbec12cb24)

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


How To Contribute
=================

`Contributions on GitHub <repo_>`_ are very welcome.
Thanks to all the contributors so far:

.. [[[cog include_readme_section("contributors") ]]]

| Ned Batchelder
| Abhilash Raj
| Agustín Piqueres
| Alyssa Coughlan
| Flo Kuepper
| James Gerity
| Javier Sagredo
| Kurt McKee
| Matias Guijarro
| Michael Makukha
| Rodrigo Girão Serrão
| Ronny Pfannschmidt

.. [[[end]]] (checksum: 69c390284832f0854ceb4ef0a1f1042c)

.. _repo: https://github.com/nedbat/scriv

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

.. |mastodon-nedbat| image:: https://img.shields.io/badge/dynamic/json?style=flat&labelColor=450657&logo=mastodon&logoColor=ffffff&link=https%3A%2F%2Fhachyderm.io%2F%40nedbat&url=https%3A%2F%2Fhachyderm.io%2Fusers%2Fnedbat%2Ffollowers.json&query=totalItems&label=Mastodon
    :target: https://hachyderm.io/@nedbat
    :alt: nedbat on Mastodon

.. |sponsor-badge| image:: https://img.shields.io/badge/%E2%9D%A4-Sponsor%20me-brightgreen?style=flat&logo=GitHub
    :target: https://github.com/sponsors/nedbat
    :alt: Sponsor me on GitHub

.. [[[end]]] (checksum: 352ff7e93ca0b80b402cbc07179c225f)
