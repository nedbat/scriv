
.. _config_categories:

categories
----------


Default: ``['Removed', 'Added', 'Changed', 'Deprecated', 'Fixed', 'Security']``

.. _config_entry_title_template:

entry_title_template
--------------------


Default: A combination of version (if specified) and date.

.. _config_format:

format
------

The format for the output changelog file.
Can be either "rst" or "md".

Default: ``rst``

.. _config_fragment_directory:

fragment_directory
------------------

The directory for fragments.  This directory must exist, it
will not be created.

Default: ``changelog.d``

.. _config_insert_marker:

insert_marker
-------------

NO DOC!

Default: ``scriv-insert-here``

.. _config_main_branches:

main_branches
-------------

NO DOC!

Default: ``['master', 'main', 'develop']``

.. _config_md_header_level:

md_header_level
---------------

NO DOC!

Default: ``1``

.. _config_new_fragment_template:

new_fragment_template
---------------------

NO DOC!

Default: ``file: new_fragment.${config:format}.j2``

.. _config_output_file:

output_file
-----------

NO DOC!

Default: ``CHANGELOG.rst``

.. _config_rst_header_chars:

rst_header_chars
----------------

NO DOC!

Default: ``=-``

.. _config_version:

version
-------

The string to use as the version number in the next header
created by ``scriv collect``.  Often, this will be a
``literal:`` directive, to get the version from a string in a
source file.

Default: (empty)
