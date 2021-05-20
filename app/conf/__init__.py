from importlib.util import module_from_spec, spec_from_file_location
from os import environ

SETTINGS_MODULE = environ.get("SETTINGS_MODULE")

spec = spec_from_file_location("settings", SETTINGS_MODULE)

settings = module_from_spec(spec)
spec.loader.exec_module(settings)
