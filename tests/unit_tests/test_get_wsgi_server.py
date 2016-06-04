import os
import unittest
try:
    import unittest.mock as mock
except ImportError:
    import mock

# Package under test
import plaster_pastedeploy

######################################################
# Set up Dummy Objects
######################################################

class DummyAppConfigReturn(dict):
    pass

app_config_return_value = DummyAppConfigReturn({
    'foo': 'bar',
    'baz': 'foo',
})
app_config_return_value.local_conf = 'bar'
app_config_return_value.global_conf = 'foo'
app_config_return_value.context = 'baz'

######################################################
# Tests
######################################################

@mock.patch('plaster_pastedeploy.loadserver', autospec=True)
class TestSimpleURI(unittest.TestCase):

    def setUp(self):
        self.loader = plaster_pastedeploy.Loader('/foo/bar/myapp.ini')

    def test_explicit_name(self, loadserver):
        result = self.loader.get_wsgi_server('some_app')
        args, kwargs = loadserver.call_args

        self.assertEqual(args[0], 'config:/foo/bar/myapp.ini')
        self.assertEqual(kwargs['name'], 'some_app')
        self.assertIsNone(kwargs['global_conf'])
        self.assertIsNone(kwargs['relative_to'])


    def test_default_name(self, loadserver):
        result = self.loader.get_wsgi_server()
        args, kwargs = loadserver.call_args

        self.assertEqual(args[0], 'config:/foo/bar/myapp.ini')
        self.assertIsNone(kwargs['name'])
        self.assertIsNone(kwargs['global_conf'])
        self.assertIsNone(kwargs['relative_to'])


@mock.patch('plaster_pastedeploy.loadserver', autospec=True)
class TestHashedURI(unittest.TestCase):

    def setUp(self):
        self.loader = plaster_pastedeploy.Loader('/foo/bar/myapp.ini#my_app')

    def test_hash_and_name_override(self, loadserver):
        values = {'a':1}
        result = self.loader.get_wsgi_server('your_app', defaults=values)
        args, kwargs = loadserver.call_args

        self.assertEqual(args[0], 'config:/foo/bar/myapp.ini')
        self.assertEqual(kwargs['name'], 'your_app')
        self.assertEqual(kwargs['global_conf'], values)
        self.assertIsNone(kwargs['relative_to'])


    def test_default_name(self, loadserver):
        result = self.loader.get_wsgi_server()
        args, kwargs = loadserver.call_args

        self.assertEqual(args[0], 'config:/foo/bar/myapp.ini')
        self.assertEqual(kwargs['name'], 'my_app')
        self.assertIsNone(kwargs['global_conf'])
        self.assertIsNone(kwargs['relative_to'])

class TestFullURI(TestHashedURI):

    def setUp(self):
        self.loader = plaster_pastedeploy.Loader('config:/foo/bar/myapp.ini#my_app')

@mock.patch('plaster_pastedeploy.loadserver', autospec=True, return_value=app_config_return_value)
class TestRelativeFilePath(unittest.TestCase):

    def setUp(self):
        self.loader = plaster_pastedeploy.Loader('foo/bar/myapp.ini')

    def test_default_relative_to(self, loadserver):
        result = self.loader.get_wsgi_server()
        args, kwargs = loadserver.call_args

        self.assertEqual(kwargs['relative_to'], os.getcwd())
        self.assertEqual(args[0], 'config:foo/bar/myapp.ini')

    def test_explicit_relative_to(self, loadserver):
        result = self.loader.get_wsgi_server(relative_to='/baz')
        args, kwargs = loadserver.call_args

        self.assertIsNotNone(os.path.isabs(args[0].split(':')[1]))

        self.assertEqual(kwargs['relative_to'], '/baz')
        self.assertEqual(args[0], 'config:foo/bar/myapp.ini')

