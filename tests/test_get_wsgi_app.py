import os
import plaster
import pytest

here = os.path.dirname(__file__)

basic_app_relpath = 'sample_configs/basic_app.ini'
basic_app_path = os.path.abspath(os.path.join(here, basic_app_relpath))


class TestSimpleURI(object):
    config_uri = basic_app_path

    @pytest.fixture(autouse=True)
    def loader(self, fake_packages, monkeypatch):
        monkeypatch.chdir(here)
        self.loader = plaster.get_loader(self.config_uri, protocols=['wsgi'])

    def test_get_wsgi_app_with_relative(self):
        import fakeapp.apps
        app = self.loader.get_wsgi_app()
        assert app is fakeapp.apps.basic_app

    def test_get_wsgi_app_main(self):
        import fakeapp.apps
        app = self.loader.get_wsgi_app('main')
        assert app is fakeapp.apps.basic_app

        same_app = self.loader.get_wsgi_app()
        assert same_app is fakeapp.apps.basic_app


class TestSectionedURI(TestSimpleURI):
    config_uri = basic_app_path + '#main'


class TestSchemeAndSectionedURI(TestSimpleURI):
    config_uri = 'ini+pastedeploy:' + basic_app_path + '#main'


class TestRelativeURI(TestSimpleURI):
    config_uri = basic_app_relpath


class TestRelativeSectionedURI(TestSectionedURI, TestRelativeURI):
    config_uri = basic_app_relpath + '#main'


class TestRelativeSchemeAndSectionedURI(TestSchemeAndSectionedURI,
                                        TestRelativeURI):
    config_uri = 'ini+pastedeploy:' + basic_app_relpath + '#main'


def test_egg_scheme(fake_packages):
    import fakeapp.apps
    loader = plaster.get_loader('egg:FakeApp', protocols=['wsgi'])
    app = loader.get_wsgi_app('basic_app')
    assert app is fakeapp.apps.basic_app
