import os

import plaster
import pytest

here = os.path.dirname(__file__)

test_settings_relpath = "sample_configs/test_settings.ini"
test_settings_path = os.path.abspath(os.path.join(here, test_settings_relpath))


class TestSimpleUri:
    config_uri = test_settings_path

    @pytest.fixture(autouse=True)
    def loader(self, fake_packages):
        self.loader = plaster.get_loader(self.config_uri)

    def test_sections(self):
        result = self.loader.get_sections()
        assert set(result) == {"section1", "section2"}

    def test_missing_section(self):
        result = self.loader.get_settings("missing", {"a": "b"})
        assert result == {}

    @pytest.mark.parametrize("raw", [False, True])
    def test_no_defaults_passed(self, raw):
        result = self.loader.get_settings("section1", raw=raw)
        if raw:
            assert list(result.items()) == [
                ("a", "a_val"),
                ("get c", "default_b"),
                ("b", "%(default_b)s"),
                ("set default_b", "override_b"),
            ]
        else:
            assert list(result.items()) == [
                ("a", "a_val"),
                ("c", "override_b"),
                ("b", "default_b"),
            ]

        if raw:
            assert result.global_conf is None
        else:
            assert result.global_conf["default_a"] == "default_a"
            assert result.global_conf["default_b"] == "override_b"
        assert result.loader == self.loader

        if not raw:
            with pytest.raises(Exception, match="default_c"):
                self.loader.get_settings("section2", raw=raw)

    @pytest.mark.parametrize("raw", [False, True])
    def test_defaults_passed(self, raw):
        defaults = {"default_c": "default_c"}
        result = self.loader.get_settings("section1", defaults=defaults, raw=raw)
        assert result["a"] == "a_val"
        if raw:
            assert result["b"] == "%(default_b)s"
        else:
            assert result["b"] == "default_b"
        assert "default_c" not in result

        if raw:
            assert result.global_conf is None
        else:
            assert result.global_conf["default_a"] == "default_a"
            assert result.global_conf["default_b"] == "override_b"
            assert result.global_conf["default_c"] == "default_c"

        result = self.loader.get_settings("section2", defaults=defaults, raw=raw)
        assert result["a"] == "a_val"
        assert result["b"] == "b_val"
        if raw:
            assert result["c"] == "%(default_c)s"
        else:
            assert result["c"] == "default_c"

        if raw:
            assert result.global_conf is None
        else:
            assert result.global_conf["default_a"] == "default_a"
            assert result.global_conf["default_b"] == "default_b"
            assert result.global_conf["default_c"] == "default_c"


class TestSectionedURI(TestSimpleUri):
    config_uri = test_settings_path + "#section1"

    @pytest.mark.parametrize("raw", [False, True])
    def test_no_section_name_passed(self, raw):
        result = self.loader.get_settings(raw=raw)
        assert result["a"] == "a_val"
        if raw:
            assert result["b"] == "%(default_b)s"
            assert "c" not in result
        else:
            assert result["b"] == "default_b"
            assert result["c"] == "override_b"
        assert "default_b" not in result


class TestFullURI(TestSectionedURI):
    config_uri = "pastedeploy+ini:" + test_settings_path + "#section1"


class TestEggURI:
    config_uri = "pastedeploy+egg:FakeApp#basic_app"

    @pytest.fixture(autouse=True)
    def loader(self, fake_packages):
        self.loader = plaster.get_loader(self.config_uri)

    def test_sections(self):
        result = self.loader.get_sections()
        assert result == []

    @pytest.mark.parametrize("raw", [False, True])
    def test_settings(self, raw):
        result = self.loader.get_settings(raw=raw)
        assert result == {}

    @pytest.mark.parametrize("raw", [False, True])
    def test_named_settings(self, raw):
        result = self.loader.get_settings("missing", raw=raw)
        assert result == {}
