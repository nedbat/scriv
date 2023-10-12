Changed
.......

- RST to Markdown conversion is now stricter, using the pandoc
  ``--fail-if-warnings=true`` option.  The ``scriv github-releases`` command
  will fail if your RST conversion generates warnings, for example due to
  malformed link references.
