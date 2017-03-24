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
        self.loader = plaster.get_loader('../sample_configs/basic_app.ini')

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
        self.loader = plaster.get_loader('../sample_configs/basic_app.ini#main')


class TestSchemeAndSectionedURI(TestSimpleURI):
    def setUp(self):
        self.loader = plaster.get_loader(
            'config:../sample_configs/basic_app.ini#main')


class TestRelativeURI(unittest.TestCase):
    def setUp(self):
        self.original_cwd = os.getcwd()
        os.chdir(os.path.join(here, '../sample_configs'))
        self.loader = plaster.get_loader('basic_app.ini')

    def teadDown(self):
        os.chdir(self.original_cwd)

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
        self.original_cwd = os.getcwd()
        os.chdir(os.path.join(here, '../sample_configs'))
        self.loader = plaster.get_loader('basic_app.ini#main')


class TestRelativeSchemeAndSectionedURI(TestRelativeURI):
    def setUp(self):
        self.original_cwd = os.getcwd()
        os.chdir(os.path.join(here, '../sample_configs'))
        self.loader = plaster.get_loader('config:basic_app.ini#main')
