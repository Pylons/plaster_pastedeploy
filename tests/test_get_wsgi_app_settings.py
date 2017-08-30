import os
import plaster
import pytest

here = os.path.dirname(__file__)
test_config_relpath = 'sample_configs/test_config.ini'
test_config_path = os.path.abspath(os.path.join(here, test_config_relpath))


class TestFullURI(object):
    @pytest.fixture(autouse=True)
    def loader(self, fake_packages, monkeypatch):
        monkeypatch.chdir(here)
        self.loader = plaster.get_loader(
            test_config_relpath, protocols=['wsgi'])

    def test_get_wsgi_app_settings(self):
        result = self.loader.get_wsgi_app_settings('test_get')
        assert result == {'def1': 'a', 'foo': 'TEST'}
        assert result.global_conf['def1'] == 'a'
        assert result.global_conf['def2'] == 'TEST'
        assert 'basepath' in result.global_conf

    def test_invalid_name(self):
        with pytest.raises(LookupError):
            self.loader.get_wsgi_app_settings('invalid')

    def test_foreign_config(self):
        result = self.loader.get_wsgi_app_settings('test_foreign_config')
        assert result == {'another': 'FOO', 'bob': 'your uncle'}
        assert result.global_conf['def1'] == 'a'
        # NOTE this is actually different on pastedeploy tip but unreleased
        assert result.global_conf['def2'] == 'from include'
        assert result.global_conf['def3'] == 'c'
        assert result.global_conf['glob'] == 'override'
        assert 'basepath' in result.global_conf


class TestSimpleURI(object):
    @pytest.fixture(autouse=True)
    def loader(self, fake_packages, monkeypatch):
        monkeypatch.chdir(here)
        self.loader = plaster.get_loader(
            'sample_configs/test_filter_with.ini', protocols=['wsgi'])

    def test_get_wsgi_app_settings(self):
        conf = self.loader.get_wsgi_app_settings()
        assert conf['example'] == 'test'


class TestEggURI(object):
    config_uri = 'egg:FakeApp#configed'

    @pytest.fixture(autouse=True)
    def loader(self, fake_packages):
        self.loader = plaster.get_loader(self.config_uri, protocols=['wsgi'])

    def test_it(self):
        conf = self.loader.get_wsgi_app_settings()
        assert conf == {}

    def test_invalid_name(self):
        with pytest.raises(LookupError):
            self.loader.get_wsgi_app_settings('invalid')
