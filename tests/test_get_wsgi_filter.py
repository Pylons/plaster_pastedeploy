import os
import plaster
import pytest

here = os.path.dirname(__file__)

test_filter_path = 'sample_configs/test_filter.ini'


class TestSimpleURI(object):
    config_uri = test_filter_path

    @pytest.fixture(autouse=True)
    def loader(self, fake_packages, monkeypatch):
        monkeypatch.chdir(here)
        self.loader = plaster.get_loader(self.config_uri, protocols=['wsgi'])

    def test_get_wsgi_app_main(self):
        import fakeapp.apps
        app_filter_factory = self.loader.get_wsgi_filter('filt')

        other_loader = plaster.get_loader(
            'sample_configs/basic_app.ini', protocols=['wsgi'])
        app = other_loader.get_wsgi_app()
        app_filter = app_filter_factory(app)

        assert isinstance(app_filter, fakeapp.apps.CapFilter)
        assert app_filter.method_to_call == 'lower'
        assert app_filter.app is fakeapp.apps.basic_app


class TestSectionedURI(TestSimpleURI):
    config_uri = test_filter_path + '#filt'

    def test_get_wsgi_filter(self):
        import fakeapp.apps
        app_filter_factory = self.loader.get_wsgi_filter()

        other_loader = plaster.get_loader(
            'ini+pastedeploy:sample_configs/basic_app.ini#main')
        app = other_loader.get_wsgi_app()
        app_filter = app_filter_factory(app)

        assert isinstance(app_filter, fakeapp.apps.CapFilter)
        assert app_filter.method_to_call == 'lower'
        assert app_filter.app is fakeapp.apps.basic_app


class TestSchemeAndSectionedURI(TestSectionedURI):
    config_uri = 'ini+pastedeploy:' + test_filter_path + '#filt'
