############################################################
# Apps
############################################################


def simple_app(response, environ, start_response):
    start_response("200 OK", [("Content-type", "text/html")])
    return ["This is ", response]


def basic_app(environ, start_response):
    return simple_app("basic app", environ, start_response)


def make_basic_app(global_conf, **conf):
    return basic_app


############################################################
# Filters
############################################################


def make_cap_filter(global_conf, method_to_call="upper"):
    def cap_filter(app):
        return CapFilter(app, global_conf, method_to_call)

    return cap_filter


class CapFilter:
    def __init__(self, app, global_conf, method_to_call="upper"):
        self.app = app
        self.method_to_call = method_to_call
        self.global_conf = global_conf

    def __call__(self, environ, start_response):
        app_iter = self.app(environ, start_response)
        for item in app_iter:
            yield getattr(item, self.method_to_call)()
        if hasattr(app_iter, "close"):
            app_iter.close()


############################################################
# Servers
############################################################


def make_fake_server(global_conf=None, **settings):
    return Server(global_conf, settings)


class Server:
    def __init__(self, global_conf, settings):
        self.global_conf = global_conf
        self.settings = settings

    def __call__(self, app):
        return app
