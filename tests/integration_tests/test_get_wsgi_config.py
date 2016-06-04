from collections import OrderedDict
import os
import unittest

# Test Utilities
from tests.fixture import *  # Manipulates sys.path. Must be before fakeapp.apps import
import fakeapp.apps
from plaster_pastedeploy import loadwsgi

# Object under test
from plaster_pastedeploy import Loader

# Test Constants
ini_file = 'config:../sample_configs/test_config.ini'
here = os.path.dirname(__file__)
config_path = os.path.join(here, '../sample_configs')
config_filename = os.path.join(config_path, 'test_config.ini')

class TestSimpleURI(unittest.TestCase):

    def setUp(self):
        self.loader = Loader('config:../sample_configs/test_config.ini')

    def test_get_wsgi_app_config(self):
        conf = self.loader.get_wsgi_app_config('test_get', relative_to=here)
        assert conf == {
            'def1': 'a',
            'def2': 'TEST',
            'basepath': os.path.join(here, 'sample_configs'),
            'here': config_path,
            '__file__': config_filename,
            'foo': 'TEST'}
        assert conf.local_conf == {
            'def1': 'a',
            'foo': 'TEST'}
        assert conf.global_conf == {
            'def1': 'a',
            'def2': 'TEST',
            'basepath': os.path.join(here, 'sample_configs'),
            'here': config_path,
            '__file__': config_filename}

        assert isinstance(conf, OrderedDict)
        assert isinstance(conf, loadwsgi.AttrDict)

class TestSimpleURI(unittest.TestCase):
    def setUp(self):
        self.loader = Loader('test_filter_with.ini')

    def test_get_wsgi_app_config(self):
        conf = self.loader.get_wsgi_app_config(relative_to=config_path)
        assert conf['example'] == 'test'
