#  Modified
import json
import os


class Settings:
    _config_location = 'config.json'

    def __init__(self):
        if os.path.exists(self._config_location):
            self.__dict__ = json.load(open(self._config_location))
        else:
            self.__dict__ = {
                # Default settings
                'ICAO_API_key': ''
            }

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        json.dump(self.__dict__, open(self._config_location, 'w'))

    def exit(self):
        json.dump(self.__dict__, open(self._config_location, 'w'))
