import os
import plaster
import pytest

here = os.path.dirname(__file__)

test_config_path = 'sample_configs/test_config.ini'


class TestSimpleURI(object):
    config_uri = test_config_path

    @pytest.fixture(autouse=True)
    def loader(self, fake_packages, monkeypatch):
        monkeypatch.chdir(here)
        self.loader = plaster.get_loader(self.config_uri, protocols=['wsgi'])

    def test_get_wsgi_server_default(self):
        server = self.loader.get_wsgi_server()
        dummy_app = object()
        result = server(dummy_app)
        assert result is dummy_app
        assert server.settings['foo'] == 'main'

    def test_invalid_name(self):
        with pytest.raises(LookupError):
            self.loader.get_wsgi_server('invalid')


class TestSectionedURI(TestSimpleURI):
    config_uri = test_config_path + '#other'

    def test_get_wsgi_server_default(self):
        server = self.loader.get_wsgi_server()
        dummy_app = object()
        result = server(dummy_app)
        assert result is dummy_app
        assert server.settings['foo'] == 'other'


class TestSchemeAndSectionedURI(TestSectionedURI):
    config_uri = 'pastedeploy+ini:' + test_config_path + '#other'


class TestEggURI(object):
    config_uri = 'egg:FakeApp#fake'

    @pytest.fixture(autouse=True)
    def loader(self, fake_packages):
        self.loader = plaster.get_loader(self.config_uri, protocols=['wsgi'])

    def test_it(self):
        server = self.loader.get_wsgi_server()
        result = server('foo')
        assert result == 'foo'

    def test_it_override_name(self):
        server = self.loader.get_wsgi_server('fake')
        result = server('foo')
        assert result == 'foo'

    def test_invalid_name(self):
        with pytest.raises(LookupError):
            self.loader.get_wsgi_server('invalid')
