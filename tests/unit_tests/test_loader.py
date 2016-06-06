import unittest
import os

# Package under test
import plaster_pastedeploy


class TestLoader(unittest.TestCase):
    def setUp(self):
        self.loader = plaster_pastedeploy.Loader('config:myapp.ini#some_app')
        self.scheme = 'config'
        self.uri = 'myapp.ini'
        self.name = 'some_app'

    def test_loader_init_scheme(self):
        self.assertEqual(self.loader.scheme, self.scheme)

    def test_loader_init_uri(self):
        self.assertEqual(self.loader.uri, self.uri)

    def test_loader_init_name(self):
        self.assertEqual(self.loader.name, self.name)


class TestSimpleURI(TestLoader):
    def setUp(self):
        self.loader = plaster_pastedeploy.Loader('myapp.ini')
        self.scheme = 'config'
        self.uri = 'myapp.ini'
        self.name = None


class TestOtherScheme(TestLoader):
    def setUp(self):
        self.loader = plaster_pastedeploy.Loader('egg:myapp.ini#main')
        self.scheme = 'egg'
        self.name = 'main'
        self.uri = 'myapp.ini'


class TestMaybeGetDefaultRelativeTo(unittest.TestCase):
    def test_relative_path(self):
        self.loader = plaster_pastedeploy.Loader('config:foo/bar.ini#test_app')

        result = self.loader._maybe_get_default_relative_to(None)
        self.assertEqual(result, os.getcwd())

        result = self.loader._maybe_get_default_relative_to(os.getcwd())
        self.assertEqual(result, os.getcwd())

    def test_absolute_path(self):
        self.loader = plaster_pastedeploy.Loader('config:/foo/bar.ini#')

        result = self.loader._maybe_get_default_relative_to(None)
        self.assertEqual(result, None)

        result = self.loader._maybe_get_default_relative_to(os.getcwd())
        self.assertEqual(result, os.getcwd())


class TestMaybeGetDefaultName(unittest.TestCase):
    def test_none_name(self):
        self.loader = plaster_pastedeploy.Loader('config:foo/bar.ini#test_app')

        result = self.loader._maybe_get_default_name(None)
        self.assertEqual(result, 'test_app')

        self.loader = plaster_pastedeploy.Loader('foo.ini')
        result = self.loader._maybe_get_default_name(None)
        self.assertEqual(result, None)

    def test_explicit_name(self):
        self.loader = plaster_pastedeploy.Loader('foo.ini#test_app')

        result = self.loader._maybe_get_default_name('other_app')
        self.assertEqual(result, 'other_app')


class TestPasteDeployURI(unittest.TestCase):
    def test_full_uri(self):
        self.loader = plaster_pastedeploy.Loader('config:foo.ini#test_app')
        self.assertEqual(self.loader._pastedeploy_uri, 'config:foo.ini')

    def test_simple_uri(self):
        self.loader = plaster_pastedeploy.Loader('foo.ini')
        self.assertEqual(self.loader._pastedeploy_uri, 'config:foo.ini')

    def test_uri_with_scheme(self):
        self.loader = plaster_pastedeploy.Loader('egg:foo.ini')
        self.assertEqual(self.loader._pastedeploy_uri, 'egg:foo.ini')
