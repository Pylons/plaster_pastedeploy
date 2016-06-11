import collections
import mock
import os
import plaster
import unittest

# Testing Utilities
from plaster_pastedeploy import loadwsgi

# Package under test
import plaster_pastedeploy


######################################################
# Set up Dummy Objects
######################################################

class DummyAppConfigReturn(dict):
    pass


app_config_return_value = DummyAppConfigReturn(**{
    'foo': 'bar',
    'baz': 'foo',
})
app_config_return_value.local_conf = 'bar'
app_config_return_value.global_conf = 'foo'
app_config_return_value.context = 'baz'


######################################################
# Tests
######################################################

@mock.patch('plaster_pastedeploy.appconfig', autospec=True,
            return_value=app_config_return_value)
class TestSimpleURI(unittest.TestCase):
    def setUp(self):
        uri = plaster.parse_uri('/foo/bar/myapp.ini')
        self.loader = plaster_pastedeploy.Loader(uri)

    def test_explicit_name(self, appconfig):
        result = self.loader.get_wsgi_app_config('some_app')
        args, kwargs = appconfig.call_args

        self.assertEqual(args[0], 'config:/foo/bar/myapp.ini')
        self.assertEqual(kwargs['name'], 'some_app')
        self.assertIsNone(kwargs['global_conf'])
        self.assertIsNone(kwargs['relative_to'])

        self.assertIsInstance(result, collections.OrderedDict)
        self.assertIsInstance(result, loadwsgi.AttrDict)

    def test_default_name(self, appconfig):
        result = self.loader.get_wsgi_app_config()
        args, kwargs = appconfig.call_args

        self.assertEqual(args[0], 'config:/foo/bar/myapp.ini')
        self.assertIsNone(kwargs['name'])
        self.assertIsNone(kwargs['global_conf'])
        self.assertIsNone(kwargs['relative_to'])

        self.assertIsInstance(result, collections.OrderedDict)
        self.assertIsInstance(result, loadwsgi.AttrDict)


@mock.patch('plaster_pastedeploy.appconfig', autospec=True,
            return_value=app_config_return_value)
class TestHashedURI(unittest.TestCase):
    def setUp(self):
        uri = plaster.parse_uri('/foo/bar/myapp.ini#my_app')
        self.loader = plaster_pastedeploy.Loader(uri)

    def test_hash_and_name_override(self, appconfig):
        values = {'a': 1}
        result = self.loader.get_wsgi_app_config('your_app', defaults=values)
        args, kwargs = appconfig.call_args

        self.assertEqual(args[0], 'config:/foo/bar/myapp.ini')
        self.assertEqual(kwargs['name'], 'your_app')
        self.assertEqual(kwargs['global_conf'], values)
        self.assertIsNone(kwargs['relative_to'])

        self.assertIsInstance(result, collections.OrderedDict)
        self.assertIsInstance(result, loadwsgi.AttrDict)

    def test_default_name(self, appconfig):
        result = self.loader.get_wsgi_app_config()
        args, kwargs = appconfig.call_args

        self.assertEqual(args[0], 'config:/foo/bar/myapp.ini')
        self.assertEqual(kwargs['name'], 'my_app')
        self.assertIsNone(kwargs['global_conf'])
        self.assertIsNone(kwargs['relative_to'])

        self.assertIsInstance(result, collections.OrderedDict)
        self.assertIsInstance(result, loadwsgi.AttrDict)


class TestFullURI(TestHashedURI):
    def setUp(self):
        uri = plaster.parse_uri('config:/foo/bar/myapp.ini#my_app')
        self.loader = plaster_pastedeploy.Loader(uri)


@mock.patch('plaster_pastedeploy.appconfig', autospec=True,
            return_value=app_config_return_value)
class TestRelativeFilePath(unittest.TestCase):
    def setUp(self):
        uri = plaster.parse_uri('foo/bar/myapp.ini')
        self.loader = plaster_pastedeploy.Loader(uri)

    def test_default_relative_to(self, appconfig):
        result = self.loader.get_wsgi_app_config()
        args, kwargs = appconfig.call_args

        self.assertEqual(kwargs['relative_to'], os.getcwd())
        self.assertEqual(args[0], 'config:foo/bar/myapp.ini')

    def test_explicit_relative_to(self, appconfig):
        result = self.loader.get_wsgi_app_config(relative_to='/baz')
        args, kwargs = appconfig.call_args

        self.assertIsNotNone(os.path.isabs(args[0].split(':')[1]))

        self.assertEqual(kwargs['relative_to'], '/baz')
        self.assertEqual(args[0], 'config:foo/bar/myapp.ini')
