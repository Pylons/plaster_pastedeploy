from collections import OrderedDict
from logging.config import fileConfig
import os

# Cover the top level paste.deploy API
from paste.deploy import (
    loadapp,
    loadserver,
    loadfilter,
    appconfig,
)
import paste.deploy.loadwsgi as loadwsgi

from plaster import (
    NoSectionError,
    Loader as LoaderBase,
)

from .compat import configparser


class Loader(LoaderBase):
    """
    This is a loader conforming to the required interface defined by
    :class:`plaster.interfaces.Loader`. Given a uri to a configuration source,
    this can load and return WSGI applications, servers, filters and settings
    from .ini files written against the PasteDeploy spec.

    :ivar uri: A :class:`plaster.PlasterURL` instance.

    """
    def _get_parser(self, defaults=None):
        parser = loadwsgi.NicerConfigParser(self.uri.path, defaults=defaults)
        parser.optionxform = str
        with open(parser.filename) as fp:
            parser.read_file(fp)
        return parser

    def get_sections(self):
        """
        Find all of the sections in the config file.

        :return: A list of the section names in the file.

        """
        parser = self._get_parser()
        return parser.sections()

    def get_settings(self, section=None, defaults=None):
        """
        Gets a named section from the configuration source. ``name`` must
        either be included in the ``uri`` passed to the class during
        instantiation, or must be passed to get settings.

        :param name: a :class:`str` representing the section you want to
            retrieve from the configuration source.
        :param defaults: a :class:`dict` that will get passed to
            :class:`configparser.ConfigParser` and will populate the DEFAULT
            section.
        :return: A :class:`collections.OrderedDict` with key value pairs as
            parsed by :class:`configparser.ConfigParser`.

        """
        name = self._maybe_get_default_name(section)
        parser = self._get_parser()
        try:
            return OrderedDict(parser.items(name))
        except configparser.NoSectionError:
            raise NoSectionError

    def get_wsgi_app(self, name=None, defaults=None, relative_to=None):
        """
        Reads the configuration source and finds and loads a WSGI
        application defined by the entry with name ``name`` per the
        PasteDeploy configuration format and loading mechanism.

        :param name: The named WSGI app to find, load and return. Defaults to
            ``None`` which becomes ``main`` inside
            :func:`paste.deploy.loadapp`.
        :param defaults: The ``global_conf`` that will be used during app
            instantiation.
        :param relative_to: A path indicating what path the uri configuration
            file is relative to. Defaults to ``None`` and may be be set
            internally to :func:`os.getcwd` if ``self.uri`` is not an absolute
            path.
        :return: A WSGI application.

        """
        name = self._maybe_get_default_name(name)
        relative_to = self._maybe_get_default_relative_to(relative_to)
        return loadapp(self.path,
                       name=name,
                       relative_to=relative_to,
                       global_conf=defaults)

    def get_wsgi_server(self, name=None, defaults=None, relative_to=None):
        """
        Reads the configuration source and finds and loads a WSGI server
        defined by the server entry with the name ``name`` per the PasteDeploy
        configuration format and loading mechanism.

        :param name: The named WSGI server to find, load and return. Defaults
            to ``None`` which becomes ``main`` inside
            :func:`paste.deploy.loadserver`.
        :param defaults: The ``global_conf`` that will be used during server
            instantiation.
        :param relative_to: A path indicating what path the uri configuration
            file is relative to. Defaults to ``None`` and may be be set
            internally to :func:`os.getcwd` if ``self.uri`` is not an absolute
            path.
        :return: A WSGI server runner callable which accepts a WSGI app.

        """
        name = self._maybe_get_default_name(name)
        relative_to = self._maybe_get_default_relative_to(relative_to)
        return loadserver(self.path,
                          name=name,
                          relative_to=relative_to,
                          global_conf=defaults)

    def get_wsgi_filter(self, name=None, defaults=None, relative_to=None):
        """Reads the configuration soruce and finds and loads a WSGI filter
        defined by the filter entry with the name ``name`` per the PasteDeploy
        configuration format and loading mechanism.

        :param name: The named WSGI filter to find, load and return. Defaults
            to ``None`` which becomes ``main`` inside
            :func:`paste.deploy.loadfilter`.
        :param defaults: The ``global_conf`` that will be used during filter
            instantiation.
        :param relative_to: A path indicating what path the uri configuration
            file is relative to. Defaults to ``None`` and may be be set
            internally to :func:`os.getcwd` if ``self.uri`` is not an absolute
            path.
        :return: A callable that can filter a WSGI application.
        """
        name = self._maybe_get_default_name(name)
        relative_to = self._maybe_get_default_relative_to(relative_to)
        return loadfilter(self.path,
                          name=name,
                          relative_to=relative_to,
                          global_conf=defaults)

    def get_wsgi_app_config(self, name=None, defaults=None, relative_to=None):
        """
        Return an :class:`collections.OrderedDict` representing the
        application config for a WSGI application named ``name`` in the
        PasteDeploy config file specified by ``self.uri``.

        ``defaults``, if passed, should be a dictionary used as variable
        assignments like ``{'http_port': 8080}``.  This is useful if e.g.
        ``%(http_port)s`` is used in the config file.

        If the ``name`` is None, this will attempt to parse the name from
        the ``config_uri`` string expecting the format ``inifile#name``.
        If no name is found, the name will default to "main".

        If ``relative_to`` is None and ``self.uri`` is not an absolute path,
        ``relative_to`` will be set to the current working directory.

        :param name: The named WSGI app for which to find the settings.
            Defaults to ``None`` which becomes ``main``
            inside :func:`paste.deploy.loadapp`.
        :param defaults: The ``global_conf`` that will be used during settings
            generation.
        :param relative_to: A path indicating what path the uri configuration
            file is relative to. Defaults to ``None`` and may be be set
            internally to :func:`os.getcwd` if ``self.uri`` is not an absolute
            path.
        :return: :class:`plaster_pastedeploy.ConfigDict`.

        """
        name = self._maybe_get_default_name(name)
        relative_to = self._maybe_get_default_relative_to(relative_to)
        conf = appconfig(
            self._pastedeploy_uri,
            name=name,
            relative_to=relative_to,
            global_conf=defaults)
        conf = _ordered_dict_from_attr_dict(conf)
        return conf

    def setup_logging(self, defaults=None):
        """
        Set up logging via :func:`logging.config.fileConfig`.

        Defaults are specified for the special ``__file__`` and ``here``
        variables, similar to PasteDeploy config loading. Extra defaults can
        optionally be specified as a dict in ``defaults``.

        :param defaults: The defaults that will be used when passed to
            :func:`logging.config.fileConfig`.
        :return: ``None``.

        """
        if 'loggers' in self.get_sections():
            config_file = os.path.abspath(self.uri.path)
            full_conf = {
                '__file__': config_file,
                'here': os.path.dirname(config_file)
            }
            if defaults is not None:
                full_conf.update(defaults)

            fileConfig(config_file, full_conf)

    def _maybe_get_default_relative_to(self, relative_to):
        """Returns either ``relative_to`` or the value of :func:`os.getcwd` if
        ``relative_to`` was unset and ``self.uri`` is not an absolute path.

        :param relative_to: The relative_to argument to check.
        :return: Either ``None`` or a default path.
        """

        is_absolute_path = os.path.isabs(self.uri.path)

        if not is_absolute_path and relative_to is None:
            # Default to the current working directory
            relative_to = os.getcwd()

        return relative_to

    def _maybe_get_default_name(self, name):
        """Checks a name and determines whether to use the default name.

        :param name: The current name to check.
        :return: Either None or a :class:`str` representing the name.
        """
        if name is None and self.uri.fragment is not None:
            name = self.uri.fragment

        return name

    def __repr__(self):
        return 'plaster_pastedeploy.Loader(uri="{0}")'.format(self.uri)


class ConfigDict(OrderedDict, loadwsgi.AttrDict):
    """A subclass to use so that the return values for getting settings can be
    an instance of :class:`collections.OrderedDict` and
    :class:`loadwsgi.AttrDict`.

    This is so that any code writen against PasteDeploy will get an expected
    return value.
    """
    pass


def _ordered_dict_from_attr_dict(attr_dict):
    """Given an attr_dict turns it into a ConfigDict. This is an
    :class:`collections.OrderedDict` with the following

    additonal attributes:
        - local_conf
        - global_conf
        - context

    :param attr_dict: The :class:`paste.deploy.loadwsgi.AttrDict`.
    :return: :class:`ConfigDict`.
    """
    conf_dict = ConfigDict(attr_dict)
    conf_dict.local_conf = attr_dict.local_conf
    conf_dict.global_conf = attr_dict.global_conf
    conf_dict.context = attr_dict.context

    return conf_dict
