import unittest
import plaster
import os

# Package under test
import plaster_pastedeploy


class TestLoader(unittest.TestCase):
    def setUp(self):
        self.uri = plaster.parse_uri('myapp.ini#some_app')
        self.pastedeploy_spec = 'config:myapp.ini'

    def test_it(self):
        self.loader = plaster_pastedeploy.Loader(self.uri)
        self.assertEqual(self.loader.uri, self.uri)
        self.assertEqual(self.loader.pastedeploy_spec, self.pastedeploy_spec)


class TestSimpleURI(TestLoader):
    def setUp(self):
        self.uri = plaster.parse_uri('myapp.ini')
        self.pastedeploy_spec = 'config:myapp.ini'
        self.name = None


class TestOtherScheme(TestLoader):
    def setUp(self):
        self.uri = plaster.parse_uri('egg:myapp.ini#main')
        self.pastedeploy_spec = 'egg:myapp.ini'


class TestMaybeGetDefaultRelativeTo(unittest.TestCase):
    def test_relative_path(self):
        uri = plaster.parse_uri('foo/bar.ini#test_app')
        self.loader = plaster_pastedeploy.Loader(uri)

        result = self.loader._maybe_get_default_relative_to(None)
        self.assertEqual(result, os.getcwd())

        result = self.loader._maybe_get_default_relative_to(os.getcwd())
        self.assertEqual(result, os.getcwd())

    def test_absolute_path(self):
        uri = plaster.parse_uri('/foo/bar.ini#')
        self.loader = plaster_pastedeploy.Loader(uri)

        result = self.loader._maybe_get_default_relative_to(None)
        self.assertEqual(result, None)

        result = self.loader._maybe_get_default_relative_to(os.getcwd())
        self.assertEqual(result, os.getcwd())


class TestMaybeGetDefaultName(unittest.TestCase):
    def test_none_name(self):
        uri = plaster.parse_uri('foo/bar.ini#test_app')
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
        uri = plaster.parse_uri('foo.ini#test_app')
        self.loader = plaster_pastedeploy.Loader(uri)
        self.assertEqual(self.loader.pastedeploy_spec, 'config:foo.ini')

    def test_simple_uri(self):
        uri = plaster.parse_uri('foo.ini')
        self.loader = plaster_pastedeploy.Loader(uri)
        self.assertEqual(self.loader.pastedeploy_spec, 'config:foo.ini')

    def test_uri_with_scheme(self):
        uri = plaster.parse_uri('egg:foo.ini')
        self.loader = plaster_pastedeploy.Loader(uri)
        self.assertEqual(self.loader.pastedeploy_spec, 'egg:foo.ini')
