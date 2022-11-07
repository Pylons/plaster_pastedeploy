from setuptools import find_packages, setup

setup(
    name="FakeApp",
    version="1.0",
    packages=find_packages(),
    entry_points={
        "paste.app_factory": """
        basic_app=fakeapp.apps:make_basic_app
        other=fakeapp.apps:make_basic_app2
        configed=fakeapp.configapps:SimpleApp.make_app
        """,
        "paste.filter_factory": """
        caps=fakeapp.apps:make_cap_filter
        """,
        "paste.server_factory": """
        fake=fakeapp.apps:make_fake_server
        """,
    },
)
