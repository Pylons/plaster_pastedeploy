import os

import plaster
import pytest

here = os.path.dirname(__file__)

test_filter_path = "sample_configs/test_filter.ini"


class TestSimpleURI:
    config_uri = test_filter_path

    @pytest.fixture(autouse=True)
    def loader(self, fake_packages, monkeypatch):
        monkeypatch.chdir(here)
        self.loader = plaster.get_loader(self.config_uri, protocols=["wsgi"])

    def test_get_wsgi_filter(self):
        import fakeapp.apps

        app_filter_factory = self.loader.get_wsgi_filter("filt")

        other_loader = plaster.get_loader(
            "sample_configs/basic_app.ini", protocols=["wsgi"]
        )
        app = other_loader.get_wsgi_app()
        app_filter = app_filter_factory(app)

        assert isinstance(app_filter, fakeapp.apps.CapFilter)
        assert app_filter.method_to_call == "lower"
        assert app_filter.app is fakeapp.apps.basic_app

    def test_invalid_name(self):
        with pytest.raises(LookupError):
            self.loader.get_wsgi_filter("invalid")


class TestSectionedURI(TestSimpleURI):
    config_uri = test_filter_path + "#filt"

    def test_get_wsgi_filter(self):
        import fakeapp.apps

        app_filter_factory = self.loader.get_wsgi_filter()

        other_loader = plaster.get_loader(
            "pastedeploy+ini:sample_configs/basic_app.ini#main",
            protocols=["wsgi"],
        )
        app = other_loader.get_wsgi_app()
        app_filter = app_filter_factory(app)

        assert isinstance(app_filter, fakeapp.apps.CapFilter)
        assert app_filter.method_to_call == "lower"
        assert app_filter.app is fakeapp.apps.basic_app


class TestSchemeAndSectionedURI(TestSectionedURI):
    config_uri = "pastedeploy+ini:" + test_filter_path + "#filt"


class TestEggURI:
    config_uri = "egg:FakeApp#caps"

    @pytest.fixture(autouse=True)
    def loader(self, fake_packages):
        self.loader = plaster.get_loader(self.config_uri, protocols=["wsgi"])

    def test_it(self):
        import fakeapp.apps

        filter = self.loader.get_wsgi_filter()
        filtered_app = filter("foo")
        assert isinstance(filtered_app, fakeapp.apps.CapFilter)

    def test_it_override_name(self):
        import fakeapp.apps

        filter = self.loader.get_wsgi_filter("caps")
        filtered_app = filter("foo")
        assert isinstance(filtered_app, fakeapp.apps.CapFilter)

    def test_invalid_name(self):
        with pytest.raises(LookupError):
            self.loader.get_wsgi_filter("invalid")
