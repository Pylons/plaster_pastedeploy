from collections import OrderedDict
from logging.config import fileConfig
import os
from plaster_pastedeploy.compat import configparser

# Cover the top level paste.deploy API
from paste.deploy import (
    loadapp,
    loadserver,
    loadfilter,
    appconfig,
)

# This is being imported so that we can sub class loadwsgi.AttrDict so we won't break existing
# isinstance callers on the return value from getting an app configuration.
import paste.deploy.loadwsgi as loadwsgi


class Loader(object):
    def __init__(self, uri):

        if '#' in uri:
            uri, section = uri.split('#', 1)
        else:
            section = None

        if ':' in uri:
            scheme, uri = uri.split(':', 1)
        else:
            scheme = 'config'

        self.uri = uri
        self.section = section
        self.scheme = scheme

    def get_settings(self, section=None, defaults=None):
        """

        :param section:
        :param defaults:
        :return:
        """
        section = self._maybe_get_default_section(section)

        parser = configparser.ConfigParser(defaults=defaults)
        parser.read([self.uri])

        return OrderedDict(parser.items(section))

    def get_wsgi_app(self, name=None, defaults=None, relative_to=None):
        """

        :param name:
        :param defaults:
        :param relative_to:
        :return:
        """
        name = self._maybe_get_default_section(name)

        relative_to = self._maybe_get_default_relative_to(relative_to)

        return loadapp(self._pastedeploy_uri, name=name, relative_to=relative_to, global_conf=defaults)

    def get_wsgi_server(self, name=None, defaults=None, relative_to=None):
        """

        :param name:
        :param defaults:
        :param relative_to:
        :return:
        """

        name = self._maybe_get_default_section(name)
        relative_to = self._maybe_get_default_relative_to(relative_to)

        return loadserver(self._pastedeploy_uri, name=name, relative_to=relative_to, global_conf=defaults)

    def get_wsgi_filter(self, name=None, defaults=None, relative_to=None):
        """

        :param name:
        :param defaults:
        :param relative_to:
        :return:
        """

        name = self._maybe_get_default_section(name)
        relative_to = self._maybe_get_default_relative_to(relative_to)

        return loadfilter(self._pastedeploy_uri, name=name, relative_to=relative_to, global_conf=defaults)

    def get_wsgi_app_config(self, name=None, defaults=None, relative_to=None):
        """ Return an :class:`collections.OrderedDict` representing the application config
        for a WSGI application named ``name`` in the PasteDeploy config file specified
        by ``self.uri``.

        ``defaults``, if passed, should be a dictionary used as variable assignments
        like ``{'http_port': 8080}``.  This is useful if e.g. ``%(http_port)s`` is
        used in the config file.

        If the ``name`` is None, this will attempt to parse the name from
        the ``config_uri`` string expecting the format ``inifile#name``.
        If no name is found, the name will default to "main".

        If ``relative_to`` is None and ``self.uri`` is not an absolute path, ``relative_to``
        will be set to the current working directory.
        """

        name = self._maybe_get_default_section(name)
        relative_to = self._maybe_get_default_relative_to(relative_to)

        conf = appconfig(
            self._pastedeploy_uri,
            name=name,
            relative_to=relative_to,
            global_conf=defaults)

        conf = _ordered_dict_from_attr_dict(conf)

        return conf

    def setup_logging(self, defaults=None):
        """Set up logging via :func:`logging.config.fileConfig`.

        Defaults are specified for the special ``__file__`` and ``here`` variables, similar to PasteDeploy config
        loading. Extra defaults can optionally be specified as a dict in ``defaults``.
        """

        parser = configparser.ConfigParser(defaults=defaults)
        parser.read([self.uri])

        if parser.has_section('loggers'):

            config_file = os.path.abspath(self.uri)

            full_conf = {
                '__file__': config_file,
                'here': os.path.dirname(config_file)
            }

            if defaults is not None:
                full_conf.update(defaults)

            fileConfig(config_file, full_conf)

    @property
    def _pastedeploy_uri(self):
        """Returns the ``self.uri`` with the scheme ``config`` prepended to the uri so that PasteDeploy
        dispatches to the correct loading functions.
        """
        return "{}:{}".format(self.scheme, self.uri)

    def _maybe_get_default_relative_to(self, relative_to):
        """Returns either ``relative_to`` or the value of :func:`os.getcwd` if ``relative_to was unset and ``self.uri``
        is not an absolute path.
        """

        is_absolute_path = os.path.isabs(self.uri)

        if not is_absolute_path and relative_to is None:
            # Default to the current working directory
            relative_to = os.getcwd()

        return relative_to

    def _maybe_get_default_section(self, section):
        if section is None and self.section is not None:
            section = self.section

        return section


class ConfigDict(OrderedDict, loadwsgi.AttrDict):
    pass


def _ordered_dict_from_attr_dict(attr_dict):
    conf_dict = ConfigDict(attr_dict)
    conf_dict.local_conf = attr_dict.local_conf
    conf_dict.global_conf = attr_dict.global_conf
    conf_dict.context = attr_dict.context

    return conf_dict
