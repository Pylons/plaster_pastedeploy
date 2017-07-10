unreleased
==========

- Fix ``get_settings`` for an arbitrary section to follow the same rules as
  PasteDeploy with regards to the handling of defaults. The goal of this
  package is to be compliant with PasteDeploy's format for all sections in
  the file such that there are no surprising format changes in various
  sections.

  Supported added for ``set default_foo = bar`` and ``get foo = default_foo``
  syntax to override a default value and to pull a default value into the
  settings, respectively. In the above example the value ``foo = bar`` would
  be returned. Any other defaults not pulled into the section via either
  interpolation or the ``get`` syntax will be ignored.

  See https://github.com/Pylons/plaster_pastedeploy/pull/6

- Inject environment variables into the defaults automatically. These will
  be available for interpolation as ``ENV_<foo>``. For example if environment
  variable ``APP_DEBUG=true`` then ``%(ENV_APP_DEBUG)s`` will work within the
  ini file. See https://github.com/Pylons/plaster_pastedeploy/pull/7

0.3.2 (2017-07-01)
==================

- Resolve an issue in which ``NoSectionError`` would not be properly caught on
  Python 2.7 if the ``configparser`` module was installed from PyPI.
  See https://github.com/Pylons/plaster_pastedeploy/issues/5

0.3.1 (2017-06-02)
==================

- Recognize the ``pastedeploy+egg`` scheme as an ``egg`` type.

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
