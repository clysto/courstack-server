from importlib import import_module

from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles

from app.conf import settings

from . import views

UPLOAD_FOLDER = settings.UPLOAD_FOLDER
DEBUG = settings.DEBUG


def include(urlconf_module):
    urlconf_module = import_module(urlconf_module)
    sub_routes = getattr(urlconf_module, "routes", [])
    return sub_routes


routes = [
    Route("/", views.root),
    Mount("/auth", routes=include("app.auth.urls")),
    Mount("/core", routes=include("app.core.urls")),
]

# 调试模式下使用 starlette 服务静态文件
if DEBUG:
    routes.append(Mount("/files", app=StaticFiles(directory=UPLOAD_FOLDER)))
