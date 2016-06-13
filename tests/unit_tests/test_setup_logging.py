import mock
import os
import plaster
import unittest

# Object Under Test
from plaster_pastedeploy import Loader


@mock.patch('plaster_pastedeploy.fileConfig')
@mock.patch('plaster_pastedeploy.compat.configparser.ConfigParser')
class Test_setup_logging(unittest.TestCase):

    def setUp(self):
        uri = plaster.parse_uri('/abc.ini')
        self.loader = Loader(uri)

    def test_it_no_global_conf(self, config_parser, file_config):
        self.loader.setup_logging()

        initial_defaults = config_parser.call_args[1]['defaults']  # kwargs
        self.assertEquals(initial_defaults, None)

        filepath, options = file_config.call_args[0]  # args
        # os.path.abspath is a sop to Windows
        self.assertEqual(filepath, os.path.abspath('/abc.ini'))
        self.assertEqual(options['__file__'], os.path.abspath('/abc.ini'))
        self.assertEqual(options['here'], os.path.abspath('/'))

    def test_it_global_conf_empty(self, config_parser, file_config):
        self.loader.setup_logging(defaults={})

        initial_defaults = config_parser.call_args[1]['defaults']  # kwargs
        self.assertEquals(initial_defaults, {})

        filepath, options = file_config.call_args[0]  # args
        # os.path.abspath is a sop to Windows
        self.assertEqual(filepath, os.path.abspath('/abc.ini'))
        self.assertEqual(options['__file__'], os.path.abspath('/abc.ini'))
        self.assertEqual(options['here'], os.path.abspath('/'))

    def test_it_global_conf_not_empty(self, config_parser, file_config):
        defaults = {'key': 'val'}
        self.loader.setup_logging(defaults=defaults)
        initial_defaults = config_parser.call_args[1]['defaults']  # kwargs
        self.assertEquals(initial_defaults, defaults)

        filepath, options = file_config.call_args[0]  # args
        # os.path.abspath is a sop to Windows
        self.assertEqual(filepath, os.path.abspath('/abc.ini'))
        self.assertEqual(options['__file__'], os.path.abspath('/abc.ini'))
        self.assertEqual(options['here'], os.path.abspath('/'))
        self.assertEqual(options['key'], 'val')

    def test_no_logging_section(self, config_parser, file_config):
        config_parser.return_value.has_section.return_value = False
        self.loader.setup_logging()

        self.assertIsNone(file_config.call_args)
