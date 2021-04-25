from importlib import import_module
from os import environ

SETTINGS_MODULE = environ.get("SETTINGS_MODULE")

settings = import_module(SETTINGS_MODULE)
