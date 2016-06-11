import unittest
import plaster
import os

# Package under test
import plaster_pastedeploy


class TestLoader(unittest.TestCase):
    def setUp(self):
        uri = plaster.parse_uri('config:myapp.ini#some_app')
        self.loader = plaster_pastedeploy.Loader(uri)
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
        uri = plaster.parse_uri('myapp.ini')
        self.loader = plaster_pastedeploy.Loader(uri)
        self.scheme = 'config'
        self.uri = 'myapp.ini'
        self.name = None


class TestOtherScheme(TestLoader):
    def setUp(self):
        uri = plaster.parse_uri('egg:myapp.ini#main')
        self.loader = plaster_pastedeploy.Loader(uri)
        self.scheme = 'egg'
        self.name = 'main'
        self.uri = 'myapp.ini'


class TestMaybeGetDefaultRelativeTo(unittest.TestCase):
    def test_relative_path(self):
        uri = plaster.parse_uri('config:foo/bar.ini#test_app')
        self.loader = plaster_pastedeploy.Loader(uri)

        result = self.loader._maybe_get_default_relative_to(None)
        self.assertEqual(result, os.getcwd())

        result = self.loader._maybe_get_default_relative_to(os.getcwd())
        self.assertEqual(result, os.getcwd())

    def test_absolute_path(self):
        uri = plaster.parse_uri('config:/foo/bar.ini#')
        self.loader = plaster_pastedeploy.Loader(uri)

        result = self.loader._maybe_get_default_relative_to(None)
        self.assertEqual(result, None)

        result = self.loader._maybe_get_default_relative_to(os.getcwd())
        self.assertEqual(result, os.getcwd())


class TestMaybeGetDefaultName(unittest.TestCase):
    def test_none_name(self):
        uri = plaster.parse_uri('config:foo/bar.ini#test_app')
        self.loader = plaster_pastedeploy.Loader(uri)

        result = self.loader._maybe_get_default_name(None)
        self.assertEqual(result, 'test_app')

        uri = plaster.parse_uri('foo.ini')
        self.loader = plaster_pastedeploy.Loader(uri)
        result = self.loader._maybe_get_default_name(None)
        self.assertEqual(result, None)

    def test_explicit_name(self):
        uri = plaster.parse_uri('foo.ini#test_app')
        self.loader = plaster_pastedeploy.Loader(uri)

        result = self.loader._maybe_get_default_name('other_app')
        self.assertEqual(result, 'other_app')


class TestPasteDeployURI(unittest.TestCase):
    def test_full_uri(self):
        uri = plaster.parse_uri('config:foo.ini#test_app')
        self.loader = plaster_pastedeploy.Loader(uri)
        self.assertEqual(self.loader._pastedeploy_uri, 'config:foo.ini')

    def test_simple_uri(self):
        uri = plaster.parse_uri('foo.ini')
        self.loader = plaster_pastedeploy.Loader(uri)
        self.assertEqual(self.loader._pastedeploy_uri, 'config:foo.ini')

    def test_uri_with_scheme(self):
        uri = plaster.parse_uri('egg:foo.ini')
        self.loader = plaster_pastedeploy.Loader(uri)
        self.assertEqual(self.loader._pastedeploy_uri, 'egg:foo.ini')
