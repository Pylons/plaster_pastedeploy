import mock
import os
import plaster
import unittest

# Object Under Test
from plaster_pastedeploy import Loader


@mock.patch('plaster_pastedeploy.fileConfig')
class Test_setup_logging(unittest.TestCase):

    def setUp(self):
        uri = plaster.parse_uri('/abc.ini')
        self.loader = Loader(uri)

    def test_it_no_global_conf(self, file_config):

        with mock.patch.object(self.loader, 'get_sections', return_value=['loggers']):
            self.loader.setup_logging()

        filepath, options = file_config.call_args[0]  # args
        # os.path.abspath is a sop to Windows
        self.assertEqual(filepath, os.path.abspath('/abc.ini'))
        self.assertEqual(options['__file__'], os.path.abspath('/abc.ini'))
        self.assertEqual(options['here'], os.path.abspath('/'))

    def test_it_global_conf_empty(self, file_config):
        with mock.patch.object(self.loader, 'get_sections', return_value=['loggers']):
            self.loader.setup_logging(defaults={})

        filepath, options = file_config.call_args[0]  # args
        # os.path.abspath is a sop to Windows
        self.assertEqual(filepath, os.path.abspath('/abc.ini'))
        self.assertEqual(options['__file__'], os.path.abspath('/abc.ini'))
        self.assertEqual(options['here'], os.path.abspath('/'))

    def test_it_global_conf_not_empty(self, file_config):
        defaults = {'key': 'val'}
        with mock.patch.object(self.loader, 'get_sections', return_value=['loggers']):
            self.loader.setup_logging(defaults=defaults)

        filepath, options = file_config.call_args[0]  # args
        # os.path.abspath is a sop to Windows
        self.assertEqual(filepath, os.path.abspath('/abc.ini'))
        self.assertEqual(options['__file__'], os.path.abspath('/abc.ini'))
        self.assertEqual(options['here'], os.path.abspath('/'))
        self.assertEqual(options['key'], 'val')

    def test_no_logging_section(self, file_config):
        with mock.patch.object(self.loader, 'get_sections', return_value=[]):
            self.loader.setup_logging()

        self.assertIsNone(file_config.call_args)
