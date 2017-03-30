import plaster

def test___repr__():
    from plaster_pastedeploy import Loader
    uri = plaster.PlasterURL('ini+pastedeploy', 'development.ini')
    loader = Loader(uri)
    assert str(loader) == (
        'plaster_pastedeploy.Loader(uri="ini+pastedeploy://development.ini")'
    )
