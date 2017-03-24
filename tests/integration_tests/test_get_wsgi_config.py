from collections import OrderedDict
import os
import plaster
import unittest

# Test Utilities

# Manipulates sys.path. Must be before fakeapp.apps import
from tests.fixture import *

import fakeapp.apps
from plaster_pastedeploy import loadwsgi

# Object under test
from plaster_pastedeploy import Loader, ConfigDict

# Test Constants
ini_file = 'config:../../sample_configs/test_config.ini'
here = os.path.dirname(__file__)
config_path = os.path.join(here, '../sample_configs')
config_filename = os.path.join(config_path, 'test_config.ini')


class TestFullURI(unittest.TestCase):
    def setUp(self):
        self.loader = plaster.get_loader(
            'config:../sample_configs/test_config.ini')

    def test_get_wsgi_app_config(self):
        conf = self.loader.get_wsgi_app_config('test_get', relative_to=here)

        assert conf == {
            'def1': 'a',
            'def2': 'TEST',
            'basepath': os.path.abspath(config_path),
            'here': os.path.abspath(config_path),
            '__file__': os.path.abspath(config_filename),
            'foo': 'TEST'}

        assert conf.local_conf == {
            'def1': 'a',
            'foo': 'TEST'}
        assert conf.global_conf == {
            'def1': 'a',
            'def2': 'TEST',
            'basepath': os.path.abspath(config_path),
            'here': os.path.abspath(config_path),
            '__file__': os.path.abspath(config_filename),
        }

        assert isinstance(conf, OrderedDict)
        assert isinstance(conf, loadwsgi.AttrDict)


class TestSimpleURI(unittest.TestCase):
    def setUp(self):
        self.loader = plaster.get_loader('test_filter_with.ini')

    def test_get_wsgi_app_config(self):
        conf = self.loader.get_wsgi_app_config(relative_to=config_path)
        assert conf['example'] == 'test'
