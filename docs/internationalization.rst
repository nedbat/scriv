.. _chapter-i18n:

Internationalization
====================
All user-facing text content should be marked for translation. Even if this application is only run in English, our
open source users may choose to use another language. Marking content for translation ensures our users have
this choice.

Follow the `internationalization coding guidelines`_ in the edX Developer's Guide when developing new features.

.. _internationalization coding guidelines: http://edx.readthedocs.org/projects/edx-developer-guide/en/latest/internationalization/i18n.html

Updating Translations
~~~~~~~~~~~~~~~~~~~~~
This project uses `Transifex`_ to translate content. After new features are developed the translation source files
should be pushed to Transifex. Our translation community will translate the content, after which we can retrieve the
translations.

.. _Transifex: https://www.transifex.com/

Pushing source translation files to Transifex requires access to the edx-platform. Request access from the Open Source
Team if you will be pushing translation files. You should also `configure the Transifex client`_ if you have not done so
already.

.. _configure the Transifex client: http://docs.transifex.com/client/config/

The `make` targets listed below can be used to push or pull translations.

..  list-table::
    :widths: 25 75
    :header-rows: 1

    * - Target
      - Description
    * - pull_translations
      - Pull translations from Transifex
    * - push_translations
      - Push source translation files to Transifex

Fake Translations
~~~~~~~~~~~~~~~~~
As you develop features it may be helpful to know which strings have been marked for translation, and which are not.
Use the `fake_translations` make target for this purpose. This target will extract all strings marked for translation,
generate fake translations in the Esperanto (eo) language directory, and compile the translations.

You can trigger the display of the translations by setting your browser's language to Esperanto (eo), and navigating to
a page on the site. Instead of plain English strings, you should see specially-accented English strings that look
like this:

    Thé Fütüré øf Ønlïné Édüçätïøn Ⱡσяєм ι# Før änýøné, änýwhéré, änýtïmé Ⱡσяєм #

