import os
import plaster
import pytest

here = os.path.dirname(__file__)

test_settings_relpath = 'sample_configs/test_settings.ini'
test_settings_path = os.path.abspath(os.path.join(here, test_settings_relpath))


class TestSimpleUri(object):
    config_uri = test_settings_path

    @pytest.fixture(autouse=True)
    def loader(self, fake_packages):
        self.loader = plaster.get_loader(self.config_uri)

    def test_sections(self):
        result = self.loader.get_sections()
        assert set(result) == {'section1', 'section2', 'section3'}

    def test_missing_section(self):
        result = self.loader.get_settings('missing', {'a': 'b'})
        assert result == {}

    def test_no_defaults_passed(self):
        result = self.loader.get_settings('section1')
        assert list(result.items()) == [
            ('a', 'a_val'),
            ('c', 'override_b'),
            ('b', 'default_b'),
        ]

        assert result.global_conf['default_a'] == 'default_a'
        assert result.global_conf['default_b'] == 'override_b'
        assert result.loader == self.loader

        with pytest.raises(Exception):
            self.loader.get_settings('section2')

    def test_defaults_passed(self):
        defaults = {'default_c': 'default_c'}
        result = self.loader.get_settings('section1', defaults=defaults)
        assert result['a'] == 'a_val'
        assert result['b'] == 'default_b'
        assert 'default_c' not in result

        assert result.global_conf['default_a'] == 'default_a'
        assert result.global_conf['default_b'] == 'override_b'
        assert result.global_conf['default_c'] == 'default_c'

        result = self.loader.get_settings('section2', defaults=defaults)
        assert result['a'] == 'a_val'
        assert result['b'] == 'b_val'
        assert result['c'] == 'default_c'

        assert result.global_conf['default_a'] == 'default_a'
        assert result.global_conf['default_b'] == 'default_b'
        assert result.global_conf['default_c'] == 'default_c'

    @pytest.mark.skipif('sys.version_info[0] == 2')
    def test_environ_passed_and_escaped(self, monkeypatch):
        monkeypatch.setenv('PLASTER_FOO', '%(foo)s')
        monkeypatch.setenv('PLASTER_BAR', '%bar')
        result = self.loader.get_settings('section3')

        assert result['foo'] == '%(foo)s'
        assert result.global_conf['ENV_PLASTER_FOO'] == '%(foo)s'

        assert result['bar'] == '%bar'
        assert result.global_conf['ENV_PLASTER_BAR'] == '%bar'

class TestSectionedURI(TestSimpleUri):
    config_uri = test_settings_path + '#section1'

    def test_no_section_name_passed(self):
        result = self.loader.get_settings()
        assert result['a'] == 'a_val'
        assert result['b'] == 'default_b'
        assert result['c'] == 'override_b'
        assert 'default_b' not in result


class TestFullURI(TestSectionedURI):
    config_uri = 'pastedeploy+ini:' + test_settings_path + '#section1'


class TestEggURI(object):
    config_uri = 'pastedeploy+egg:FakeApp#basic_app'

    @pytest.fixture(autouse=True)
    def loader(self, fake_packages):
        self.loader = plaster.get_loader(self.config_uri)

    def test_sections(self):
        result = self.loader.get_sections()
        assert result == []

    def test_settings(self):
        result = self.loader.get_settings()
        assert result == {}

    def test_named_settings(self):
        result = self.loader.get_settings('missing')
        assert result == {}
