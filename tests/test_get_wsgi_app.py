import os

import plaster
import pytest

here = os.path.dirname(__file__)

basic_app_relpath = "sample_configs/basic_app.ini"
basic_app_path = os.path.abspath(os.path.join(here, basic_app_relpath))


class TestSimpleURI:
    config_uri = basic_app_path

    @pytest.fixture(autouse=True)
    def loader(self, fake_packages, monkeypatch):
        monkeypatch.chdir(here)
        self.loader = plaster.get_loader(self.config_uri, protocols=["wsgi"])

    def test_get_wsgi_app_with_relative(self):
        import fakeapp.apps

        app = self.loader.get_wsgi_app()
        assert app is fakeapp.apps.basic_app

    def test_get_wsgi_app_main(self):
        import fakeapp.apps

        app = self.loader.get_wsgi_app("main")
        assert app is fakeapp.apps.basic_app

        same_app = self.loader.get_wsgi_app()
        assert same_app is fakeapp.apps.basic_app

    def test_invalid_name(self):
        with pytest.raises(LookupError):
            self.loader.get_wsgi_app("invalid")


class TestSectionedURI(TestSimpleURI):
    config_uri = basic_app_path + "#main"


class TestSchemeAndSectionedURI(TestSimpleURI):
    config_uri = "pastedeploy+ini:" + basic_app_path + "#main"


class TestRelativeURI(TestSimpleURI):
    config_uri = basic_app_relpath


class TestRelativeSectionedURI(TestSectionedURI, TestRelativeURI):
    config_uri = basic_app_relpath + "#main"


class TestRelativeSchemeAndSectionedURI(TestSchemeAndSectionedURI, TestRelativeURI):
    config_uri = "pastedeploy+ini:" + basic_app_relpath + "#main"


class TestEggURI:
    config_uri = "egg:FakeApp#basic_app"

    @pytest.fixture(autouse=True)
    def loader(self, fake_packages):
        self.loader = plaster.get_loader(self.config_uri, protocols=["wsgi"])

    def test_it(self):
        import fakeapp.apps

        app = self.loader.get_wsgi_app()
        assert app is fakeapp.apps.basic_app

    def test_it_override_name(self):
        import fakeapp.configapps

        app = self.loader.get_wsgi_app("configed")
        assert isinstance(app, fakeapp.configapps.SimpleApp)

    def test_invalid_name(self):
        with pytest.raises(LookupError):
            self.loader.get_wsgi_app("invalid")
