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


def dict_copy(d):
    return d.copy()


def copy_copy(d):
    return copy.copy(d)


@pytest.mark.parametrize('copier',
                         [dict_copy, copy_copy],
                         ids=lambda f: f.__name__)
def test_copy(copier, loader):
    from plaster_pastedeploy import ConfigDict
    x = []
    global_conf = {}
    configdict = ConfigDict({'x': x}, global_conf, loader)

    duplicate = copier(configdict)

    assert duplicate.items() == configdict.items()
    # check that we got a shallow copy
    assert duplicate['x'] is x
    assert duplicate.global_conf is global_conf
    assert duplicate.loader is loader
