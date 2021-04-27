from importlib import import_module

from starlette.routing import Mount, Route

from . import views


def include(urlconf_module):
    urlconf_module = import_module(urlconf_module)
    sub_routes = getattr(urlconf_module, "routes", [])
    return sub_routes


routes = [
    Route("/", views.root),
    Mount("/auth", routes=include("app.auth.urls")),
    Mount("/core", routes=include("app.core.urls")),
]
