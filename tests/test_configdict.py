""" Tests for plaster_pastedeploy.ConfigDict
"""
import copy                     # noqa: F401
import plaster
import pytest


@pytest.fixture
def loader():
    from plaster_pastedeploy import Loader
    uri = plaster.PlasterURL('pastedeploy+ini', 'development.ini')
    return Loader(uri)


@pytest.mark.parametrize('copy_method', [
    "configdict.copy()",
    "copy.copy(configdict)",
    ])
def test_copy(copy_method, loader):
    from plaster_pastedeploy import ConfigDict
    x = []
    global_conf = {}
    configdict = ConfigDict({'x': x}, global_conf, loader)

    duplicate = eval(copy_method)

    assert duplicate.items() == configdict.items()
    # check that we got a shallow copy
    assert duplicate['x'] is x
    assert duplicate.global_conf is global_conf
    assert duplicate.loader is loader
