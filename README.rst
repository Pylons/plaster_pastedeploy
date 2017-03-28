===================
plaster_pastedeploy
===================

.. image:: https://img.shields.io/pypi/v/plaster_pastedeploy.svg
        :target: https://pypi.python.org/pypi/plaster_pastedeploy

.. image:: https://img.shields.io/travis/Pylons/plaster_pastedeploy.svg
        :target: https://travis-ci.org/Pylons/plaster_pastedeploy

``plaster_pastedeploy`` is a plaster_ plugin that provides a ``plaster.Loader``
that can parse ini files according to the standard set by PasteDeploy_. It
supports the ``wsgi`` plaster protocol, implementing the
``plaster.protocols.IWSGIProtocol`` interface.

Usage
=====

Applications should use ``plaster_pastedeploy`` to load settings from named
sections in a configuration source (usually a file).

- Please look at the documentation for plaster_ on how to integrate this
  loader into your application.

- Please look at the documentation for PasteDeploy_ on the specifics of the
  supported INI file format.

Most applications will want to use
``plaster.get_loader(uri, protocols=['wsgi'])`` to get this loader. It then
exposes ``get_wsgi_app``, ``get_wsgi_app_settings``, ``get_wsgi_filter`` and
``get_wsgi_server``.

.. code-block:: python

    import plaster

    loader = plaster.get_loader('development.ini', protocols=['wsgi'])
    # to get any section out of the config file
    settings = loader.get_settings('app:main')

    # to get settings for a WSGI app
    app_config = loader.get_wsgi_app_settings() # defaults to main

    # to get an actual WSGI app
    app = loader.get_wsgi_app() # defaults to main

    # to get a filter and compose it with an app
    filter = loader.get_wsgi_filter('filt')
    app = filter(app)

    # to get a WSGI server
    server = loader.get_wsgi_server() # defaults to main

    # to start the WSGI server
    server(app)

Any ``plaster.PlasterURL`` options are forwarded as defaults to the loader.
Some examples are below:

- ``development.ini#myapp``

- ``development.ini?http_port=8080#main``

- ``ini+pastedeploy:///path/to/development.ini``

- ``ini+pastedeploy://development.ini#foo``

- ``egg:MyApp?debug=false#foo``

.. _PasteDeploy: http://pastedeploy.readthedocs.io/en/latest/
.. _plaster: http://docs.pylonsproject.org/projects/plaster/en/latest/
