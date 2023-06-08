#####
Scriv
#####

Scriv changelog management tool

| |pypi-badge| |ci-badge| |coverage-badge| |doc-badge|
| |pyversions-badge| |license-badge| |sponsor-badge| |mastodon-nedbat|

Overview
========

Scriv is a command-line tool for helping developers maintain useful changelogs.
It manages a directory of changelog fragments. It aggregates them into entries
in a CHANGELOG file.

Installation
============

To install scriv, you can use the following command::

  python3 -m pip install scriv

Install via `pipx <https://pypi.org/project/pipx/>`_ (recommended)
-----------------------------------------------------------------

``pipx`` is an alternative package manager for Python applications.
It allows you to install and run Python applications in isolated environments,
preventing conflicts between dependencies and ensuring that each application
uses its own set of packages.

1. First, install ``pipx`` if you haven't already:

  * On macOS and Linux::

    python3 -m pip install --user pipx
    python3 -m pipx ensurepath

Alternatively, you can use your package manager (``brew``, ``apt``, etc.).

  * On Windows::

    py -m pip install --user pipx
    py -m pipx ensurepath

2. Once ``pipx`` is installed, you can install scriv using the following command::

  pipx install scriv

Getting Started
===============

Scriv writes changelog fragments into a directory called "changelog.d".  Start
by creating this directory.  (By the way, like many aspects of scriv's
operation, you can choose a different name for this directory.)

To make a new changelog fragment, use the ``scriv create`` command.  It will
make a new file with a filename using the current date and time, your GitHub or
Git user name, and your branch name.  Changelog fragments should be committed
along with all the other changes on your branch.

When it is time to release your project, the ``scriv collect`` command
aggregates all the fragments into a new entry in your changelog file.


Documentation
=============

Full documentation is at https://scriv.readthedocs.org.

License
=======

The code in this repository is licensed under the Apache Software License 2.0
unless otherwise noted.

Please see ``LICENSE.txt`` for details.

How To Contribute
=================

Contributions are very welcome.


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
