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
        from collections import OrderedDict
        from paste.deploy import loadwsgi
        from plaster_pastedeploy import ConfigDict

        conf = self.loader.get_wsgi_app_settings('test_get')

        assert conf == {
            'def1': 'a',
            'def2': 'TEST',
            'basepath': os.path.dirname(test_config_path),
            'here': os.path.dirname(test_config_path),
            '__file__': test_config_path,
            'foo': 'TEST'}

        assert conf.local_conf == {
            'def1': 'a',
            'foo': 'TEST'}
        assert conf.global_conf == {
            'def1': 'a',
            'def2': 'TEST',
            'basepath': os.path.dirname(test_config_path),
            'here': os.path.dirname(test_config_path),
            '__file__': test_config_path,
        }

        assert isinstance(conf, OrderedDict)
        assert isinstance(conf, loadwsgi.AttrDict)
        assert isinstance(conf, ConfigDict)

    def test_invalid_name(self):
        with pytest.raises(LookupError):
            self.loader.get_wsgi_app_settings('invalid')


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
        assert conf.global_conf['here'] == os.getcwd()

    def test_invalid_name(self):
        with pytest.raises(LookupError):
            self.loader.get_wsgi_app_settings('invalid')
