import os
import plaster
import unittest

# Testing Utilities

# # Manipulates sys.path. Must be before fakeapp.apps import
# from tests.fixture import *
#
# import fakeapp.apps

# Class under test
from plaster_pastedeploy import Loader

# Testing Constants
here = os.path.dirname(__file__)


class TestSimpleUri(unittest.TestCase):
    def setUp(self):
        os.chdir(here)
        uri = plaster.parse_uri('../sample_configs/test_settings.ini')
        self.loader = Loader(uri)

    def test_no_defaults_passed(self):
        result = self.loader.get_settings('section1')
        self.assertEqual(result['a'], 'default_a')
        self.assertEqual(result['b'], 'default_b')
        self.assertEqual(result['c'], 'default_a')

        result = self.loader.get_settings('section2')
        self.assertEqual(result['a'], 'default_a')
        self.assertEqual(result['b'], 'b_val')
        self.assertRaises(KeyError, lambda: result['c'])

    def test_defaults_passed(self):
        result = self.loader.get_settings('section1',
                                          defaults={'c': 'c_val', 'd': '%(b)s'})
        self.assertEqual(result['a'], 'default_a')
        self.assertEqual(result['b'], 'default_b')
        self.assertEqual(result['c'], 'default_a')
        self.assertEqual(result['d'], 'default_b')

        result = self.loader.get_settings('section2',
                                          defaults={'c': 'c_val', 'd': '%(b)s'})
        self.assertEqual(result['a'], 'default_a')
        self.assertEqual(result['b'], 'b_val')
        self.assertEqual(result['c'], 'c_val')
        self.assertEqual(result['d'], 'b_val')


class TestSectionedURI(TestSimpleUri):
    def setUp(self):
        os.chdir(here)
        uri = plaster.parse_uri('../sample_configs/test_settings.ini#section1')
        self.loader = Loader(uri)

    def test_no_section_name_passed(self):
        result = self.loader.get_settings()
        self.assertEqual(result['a'], 'default_a')
        self.assertEqual(result['b'], 'default_b')
        self.assertEqual(result['c'], 'default_a')

        result = self.loader.get_settings(defaults={'c': 'c_val', 'd': '%(b)s'})
        self.assertEqual(result['a'], 'default_a')
        self.assertEqual(result['b'], 'default_b')
        self.assertEqual(result['c'], 'default_a')
        self.assertEqual(result['d'], 'default_b')


class TestFullURI(TestSectionedURI):
    def setUp(self):
        os.chdir(here)
        uri = plaster.parse_uri('config:../sample_configs/test_settings.ini#section1')
        self.loader = Loader(uri)
