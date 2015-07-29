import configparser
import os
from functools import wraps


def _open_config(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        config = configparser.ConfigParser()
        filename = os.getenv('ROOMCONTROL_STORAGE', 'storage.cfg')
        if os.path.isfile(filename):
            config.read(filename)
        return f(config, *args, **kwargs)
    return wrapper


def _persist_changes(f):
    @wraps(f)
    @_open_config
    def wrapper(config, *args, **kwargs):
        filename = os.getenv('ROOMCONTROL_STORAGE', 'storage.cfg')
        f(config, *args, **kwargs)
        with open(filename, 'w') as configfile:
            config.write(configfile)
    return wrapper


@_persist_changes
def set(config, kind, key, value):
    config[kind][key] = str(value)


@_persist_changes
def set_all(config, kind, mapping):
    m = {str(k): str(v) for k, v in mapping.items()}
    config[kind] = m


@_open_config
def get(config, kind, key):
    return config[kind][key]


@_open_config
def get_all(config, kind):
    return config[kind]
