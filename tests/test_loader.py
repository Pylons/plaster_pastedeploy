import plaster

def test___repr__():
    from plaster_pastedeploy import Loader
    uri = plaster.PlasterURL('pastedeploy+ini', 'development.ini')
    loader = Loader(uri)
    assert str(loader) == (
        'plaster_pastedeploy.Loader(uri="pastedeploy+ini://development.ini")'
    )
