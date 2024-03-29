import os.path
import sys

import pkg_resources
import pytest


@pytest.fixture(scope="session")
def fake_packages():
    # we'd like to keep this scope more focused but it's proven really
    # difficult to fully monkeypatch pkg_resources and so for now we just
    # install the packages for the duration of the test suite
    test_dir = os.path.dirname(__file__)
    info_dir = os.path.join(test_dir, "fake_packages", "FakeApp")
    sys.path.insert(0, info_dir)
    pkg_resources.working_set.add_entry(info_dir)
