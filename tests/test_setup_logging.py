import os

import plaster
import pytest

here = os.path.dirname(__file__)

test_config_relpath = "sample_configs/test_config.ini"
test_config_path = os.path.abspath(os.path.join(here, test_config_relpath))


class Test_setup_logging:
    @pytest.fixture(autouse=True)
    def logging(self, fake_packages, monkeypatch):
        self.basicConfig = DummyFileConfig()
        self.fileConfig = DummyFileConfig()
        monkeypatch.setattr("logging.basicConfig", self.basicConfig)
        monkeypatch.setattr("plaster_pastedeploy.fileConfig", self.fileConfig)
        monkeypatch.chdir(here)

    def _makeOne(self, uri=None):
        if uri is None:
            uri = test_config_relpath
        return plaster.get_loader(uri)

    def test_it_no_global_conf(self):
        loader = self._makeOne()
        loader.setup_logging()
        assert self.fileConfig.called

        path, defaults = self.fileConfig.args
        assert path == test_config_relpath
        assert defaults["__file__"] == test_config_path
        assert defaults["here"] == os.path.dirname(test_config_path)

    def test_it_global_conf_empty(self):
        loader = self._makeOne()
        loader.setup_logging(defaults={})
        assert self.fileConfig.called

        path, defaults = self.fileConfig.args
        assert path == test_config_relpath
        assert defaults["__file__"] == test_config_path
        assert defaults["here"] == os.path.dirname(test_config_path)

    def test_it_global_conf_not_empty(self):
        defaults = {"key": "val"}
        loader = self._makeOne()
        loader.setup_logging(defaults=defaults)
        assert self.fileConfig.called

        path, defaults = self.fileConfig.args
        assert path == test_config_relpath
        assert defaults["__file__"] == test_config_path
        assert defaults["here"] == os.path.dirname(test_config_path)
        assert defaults["key"] == "val"

    def test_no_logging_section(self):
        loader = self._makeOne()
        loader.get_sections = lambda *args: []
        loader.setup_logging()
        assert self.basicConfig.called
        assert self.basicConfig.args == ()
        assert self.basicConfig.kwargs == {}

    def test_egg_uri(self):
        loader = self._makeOne("egg:FakeApp#fake")
        loader.setup_logging()
        assert self.basicConfig.called
        assert self.basicConfig.args == ()
        assert self.basicConfig.kwargs == {}

    def test_it_keeps_existing_loggers(self):
        loader = self._makeOne()
        loader.setup_logging()
        assert self.fileConfig.called
        assert self.fileConfig.kwargs["disable_existing_loggers"] is False


class DummyFileConfig:
    called = False
    args = None
    kwargs = None

    def __call__(self, *args, **kwargs):
        self.called = True
        self.args = args
        self.kwargs = kwargs
