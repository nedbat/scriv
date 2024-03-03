##########
Philosophy
##########

.. _philosophy:

Scriv's design is guided by a few principles:

- Changelogs should be captured in a file in the repository. Scriv writes a
  CHANGELOG file.

- Writing about changes to code should happen close in time to the changes
  themselves. Scriv encourages writing fragment files to be committed when you
  commit your code changes.

- How you describe a change depends on who you are describing it for. You may
  need multiple descriptions of the same change.  Scriv encourages writing
  changelog entries directly, rather than copying text from commit messages or
  pull requests.

- The changelog file in the repo should be the source of truth.  The
  information can also be published elsewhere, like GitHub releases.

- Different projects have different needs; flexibility is a plus. Scriv doesn't
  assume any particular issue tracker or packaging system, and allows either
  .rst or .md files.


.. _other_tools:

Other Tools
===========

Scriv is not the first tool to help manage changelogs, there have been many.
None fully embodied scriv's philopsophy.

Tools most similar to scriv:

- `towncrier`_: built for Twisted, with some unusual specifics: fragment type
  is the file extension, issue numbers in the file name.  Defaults to using
  ``.rst`` files, but can be configured to produce Markdown or any other
  output format, provided enough configuration.

- `blurb`_: built for CPython development, specific to their workflow: issue
  numbers from bugs.python.org, only .rst files.

- `setuptools-changelog`_: particular to Python projects (uses a setup.py
  command), and only supports .rst files.

- `gitchangelog`_: collects git commit messages into a changelog file.

Tools that only read GitHub issues, or only write GitHub releases:

- `Chronicler`_: a web hook that watched for merged pull requests, then appends
  the pull request message to the most recent draft GitHub release.

- `fastrelease`_: reads information from GitHub issues, and writes GitHub
  releases.

- `Release Drafter`_: adds text from merged pull requests to the latest draft
  GitHub release.

Other release note tools:

- `reno`_: built for Open Stack.  It stores changelogs forever as fragment
  files, only combining for publication.

.. _towncrier: https://github.com/hawkowl/towncrier
.. _blurb: https://github.com/python/core-workflow/tree/master/blurb
.. _setuptools-changelog: https://pypi.org/project/setuptools-changelog/
.. _gitchangelog: https://pypi.org/project/gitchangelog/
.. _fastrelease: https://fastrelease.fast.ai/
.. _Chronicler: https://github.com/NYTimes/Chronicler
.. _Release Drafter: https://probot.github.io/apps/release-drafter/
.. _reno: https://docs.openstack.org/reno/latest/user/usage.html
