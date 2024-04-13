import importlib
import os.path
import sys

import pytest


@pytest.fixture(scope="session")
def fake_packages():
    # We'd like to keep this scope more focused.  It proved really
    # difficult to fully monkeypatch pkg_resources and so we just
    # installed the packages for the duration of the test suite.
    # The scope was left as-is after switching from pkg_resources to
    # importlib.
    test_dir = os.path.dirname(__file__)
    info_dir = os.path.join(test_dir, "fake_packages", "FakeApp")
    sys.path.insert(0, info_dir)
    importlib.import_module("fakeapp")
