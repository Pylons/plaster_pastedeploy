0.3 (2017-06-02)
================

- Drop the ``ini`` scheme and replace with ``file+ini`` and ``pastedeploy``.
  Also rename ``ini+pastedeploy`` and ``egg+pastedeploy`` to
  ``pastedeploy+ini`` and ``pastedeploy+egg`` respectively.
  See https://github.com/Pylons/plaster_pastedeploy/pull/4

0.2.1 (2017-03-29)
==================

- Fix a bug in 0.2 in which an exception was raised for an invalid section
  if the a non-config-file-based protocol was used.

0.2 (2017-03-29)
================

- No longer raise ``plaster.NoSectionError`` exceptions. Empty dictionaries
  are returned for missing sections and a user should check ``get_sections``
  for the list of valid sections.

0.1 (2017-03-27)
================

- Initial release.
