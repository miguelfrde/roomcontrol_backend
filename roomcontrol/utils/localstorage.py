import configparser
import os.path
from functools import wraps


class LocalStorage:
    def __init__(self, filename):
        self._filename = filename
        self._config = configparser.ConfigParser()
        if os.path.isfile(filename):
            self._config.read(filename)

    def persist_changes(f):
        @wraps(f)
        def wrapper(self, *args, **kwargs):
            f(self, *args, **kwargs)
            with open(self._filename, 'w') as configfile:
                self._config.write(configfile)
        return wrapper

    @persist_changes
    def set(self, kind, key, value=None):
        self._config[kind][key] = str(value)

    @persist_changes
    def set_all(self, kind, mapping):
        m = {str(k): str(v) for k, v in mapping.items()}
        self._config[kind] = m

    def get(self, kind, key):
        return self._config[kind][key]

    def get_all(self, kind):
        return self._config[kind]
