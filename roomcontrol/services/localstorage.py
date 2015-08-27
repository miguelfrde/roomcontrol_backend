import configparser
import os

from nameko.rpc import rpc


class LocalStorageService:
    name = 'localstorage_service'

    DEFAULT_FILE = os.path.expanduser('~/.roomcontrol/storage.cfg')

    def __init__(self):
        self.storage_file = os.getenv('ROOMCONTROL_STORAGE', self.DEFAULT_FILE)
        self.config = configparser.ConfigParser()
        self.set_storage_file(self.storage_file)

    def test(self):
        print("Yeah")

    def _save_changes(self):
        with open(self.storage_file, 'w') as configfile:
            self.config.write(configfile)

    @rpc
    def set_storage_file(self, filename):
        self.storage_file = filename
        if os.path.isfile(self.storage_file):
            self.config.read(self.storage_file)
        else:
            self.config = configparser.ConfigParser()
        os.environ['ROOMCONTROL_STORAGE'] = filename

    @rpc
    def set(self, kind, key, value):
        self.config[kind][key] = str(value)
        self._save_changes()

    @rpc
    def set_all(self, kind, mapping):
        m = {str(k): str(v) for k, v in mapping.items()}
        self.config[kind] = m
        self._save_changes()

    @rpc
    def get(self, kind, key):
        return self.config[kind][key]

    @rpc
    def get_all(self, kind):
        return self.config._sections[kind]
