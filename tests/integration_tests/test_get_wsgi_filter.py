import os
import plaster
import unittest

# Test Utilities

# Manipulates sys.path. Must be before fakeapp.apps import
from tests.fixture import *

import fakeapp.apps

# Class under test
from plaster_pastedeploy import Loader

here = os.path.dirname(__file__)


class TestSimpleURI(unittest.TestCase):
    def setUp(self):
        uri = plaster.parse_uri('../sample_configs/test_filter.ini')
        self.loader = Loader(uri)

    def test_get_wsgi_app_main(self):
        app_filter_factory = self.loader.get_wsgi_filter('filt',
                                                         relative_to=here)

        other_loader = Loader('config:../sample_configs/basic_app.ini#main')
        app = other_loader.get_wsgi_app(relative_to=here)
        app_filter = app_filter_factory(app)

        assert isinstance(app_filter, fakeapp.apps.CapFilter)
        assert app_filter.method_to_call == 'lower'
        assert app_filter.app is fakeapp.apps.basic_app


class TestSectionedURI(TestSimpleURI):
    def setUp(self):
        uri = plaster.parse_uri('../sample_configs/test_filter.ini#filt')
        self.loader = Loader(uri)

    def test_get_wsgi_filter(self):
        app_filter_factory = self.loader.get_wsgi_filter(relative_to=here)

        other_loader = Loader('config:../sample_configs/basic_app.ini#main')
        app = other_loader.get_wsgi_app(relative_to=here)
        app_filter = app_filter_factory(app)

        assert isinstance(app_filter, fakeapp.apps.CapFilter)
        assert app_filter.method_to_call == 'lower'
        assert app_filter.app is fakeapp.apps.basic_app


class TestSchemeAndSectionedURI(TestSectionedURI):
    def setUp(self):
        uri = plaster.parse_uri('config:../sample_configs/test_filter.ini#filt')
        self.loader = Loader(uri)
