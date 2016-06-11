import os
import plaster
import unittest

# Testing Utilities

# Manipulates sys.path. Must be before fakeapp.apps import
from tests.fixture import *

import fakeapp.apps

# Class under test
from plaster_pastedeploy import Loader

# Testing Constants
here = os.path.dirname(__file__)


class TestSimpleURI(unittest.TestCase):
    def setUp(self):
        uri = plaster.parse_uri('../sample_configs/basic_app.ini')
        self.loader = Loader(uri)

    def test_get_wsgi_app_with_relative(self):
        app = self.loader.get_wsgi_app(relative_to=here)
        assert app is fakeapp.apps.basic_app

    def test_get_wsgi_app_main(self):
        app = self.loader.get_wsgi_app('main', relative_to=here)
        assert app is fakeapp.apps.basic_app

        same_app = self.loader.get_wsgi_app(relative_to=here)
        assert same_app is fakeapp.apps.basic_app


class TestSectionedURI(TestSimpleURI):
    def setUp(self):
        uri = plaster.parse_uri('../sample_configs/basic_app.ini#main')
        self.loader = Loader(uri)


class TestSchemeAndSectionedURI(TestSimpleURI):
    def setUp(self):
        uri = plaster.parse_uri('config:../sample_configs/basic_app.ini#main')
        self.loader = Loader(uri)


class TestRelativeURI(unittest.TestCase):
    def setUp(self):
        self.here = here
        os.chdir(os.path.join(here, '../sample_configs'))
        uri = plaster.parse_uri('basic_app.ini')
        self.loader = Loader(uri)

    def teadDown(self):
        os.chdir(self.here)

    def test_get_wsgi_app_no_args(self):
        app = self.loader.get_wsgi_app()
        assert app is fakeapp.apps.basic_app

    def test_get_wsgi_app_main(self):
        app = self.loader.get_wsgi_app('main')
        assert app is fakeapp.apps.basic_app

        same_app = self.loader.get_wsgi_app()
        assert same_app is fakeapp.apps.basic_app


class TestRelativeSectionedURI(TestRelativeURI):
    def setUp(self):
        os.chdir(os.path.join(here, '../sample_configs'))
        uri = plaster.parse_uri('basic_app.ini#main')
        self.loader = Loader(uri)


class TestRelativeSchemeAndSectionedURI(TestRelativeURI):
    def setUp(self):
        os.chdir(os.path.join(here, '../sample_configs'))
        uri = plaster.parse_uri('config:basic_app.ini#main')
        self.loader = Loader(uri)
