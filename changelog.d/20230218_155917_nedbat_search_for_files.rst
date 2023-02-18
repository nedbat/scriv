Fixed
.....

- Settings specified as ``file:`` will now search in the changelog directory
  and then the current directory for the file.  The only exception is if the
  first component is ``.`` or ``..``, then only the current directory is
  considered.  Fixes `issue 82`_.

.. _issue 82: https://github.com/nedbat/scriv/issues/82
