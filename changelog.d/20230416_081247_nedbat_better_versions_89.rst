Fixed
.....

- In compliance with `PEP 440`_, comparing version numbers now ignores a
  leading "v" character.  This makes scriv more flexible about how you present
  version numbers in various places (code literals, changelog entries, git
  tags, and so on).  Fixes `issue 89`_.

.. _PEP 440: https://peps.python.org/pep-0440/
.. _issue 89: https://github.com/nedbat/scriv/issues/89
