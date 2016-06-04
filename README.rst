=======
plaster_pastedeploy
=======

.. image:: https://img.shields.io/pypi/v/plaster_pastedeploy.svg
        :target: https://pypi.python.org/pypi/plaster_pastedeploy

.. image:: https://img.shields.io/travis/mmerickel/plaster_pastedeploy.svg
        :target: https://travis-ci.org/mmerickel/plaster_pastedeploy

.. image:: https://readthedocs.org/projects/plaster_pastedeploy/badge/?version=latest
        :target: https://readthedocs.org/projects/plaster_pastedeploy/?badge=latest
        :alt: Documentation Status

``plaster_pastedeploy`` is a loader that can parse ini files according to
the standard set by PasteDeploy. It is intended as a plugin for plaster.

Usage
=====

Applications should use ``plaster_pastedeploy`` to load settings from named sections in
a configuration source (usually a file).

Most applications will want to use
``plaster.get_loader(uri, section=None, defaults=None) to get this loader. It then exposes
``get_wsgi_app`` and ``get_wsgi_server``.

.. code-block:: python

    import plaster

    loader = plaster.get_loader('development.ini')
    app_settings = loader.get_wsgi_config()
    app = loader.get_wsgi_app()
