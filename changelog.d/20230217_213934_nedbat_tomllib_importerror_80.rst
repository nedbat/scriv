Fixed
.....

- Scriv would fail trying to import tomllib on Python <3.11 if installed
  without the ``[toml]`` extra.  This is now fixed, closing `issue 80`_.

.. _issue 80: https://github.com/nedbat/scriv/issues/80
