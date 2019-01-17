# Copyright (C) 2019 Wanja Chresta
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Load configuration from given config file."""
import copy
import yaml

from yaml import YAMLError


DEFAULT_CONFIG="""
twitter:
    message: 'I own a file with checksum {checksum} (cotary)'
    # The following are twitter API keys. Get them from https://dev.twitter.com/apps
    consumer:
        key: null
        secret: null
    access_token:
        key: null
        secret: null
"""

class Config(dict):
    """Load and manage loading configuration files over a default set of config"""

    @staticmethod
    def default_config():
        """Return a dict which contains the default configuration"""
        return yaml.load(DEFAULT_CONFIG)

    def __init__(self, config_path):
        """
        Initialize the configuration by loading the given config file.
        """
        super().__init__()

        self.clear()
        self.load(config_path)

    def __getitem__(self, key):
        """Return the value to the key or split the key at . and get recursively."""
        try:
            return super().__getitem__(key)
        except KeyError as e:
            super_key_not_found_error = e

        key_parts = key.split('.')
        if len(key_parts) <= 1: # There are no . in the key, so there is nothing to split
            raise super_key_not_found_error

        current_value = self
        for part in key_parts:
            try:
                current_value = current_value[part]
            except KeyError as e:
                raise KeyError("Unknown config part {} in key {}".format(part, key)
                        ) from None
        return current_value

    def clear(self):
        """Reset the config to the global defaults."""
        super().clear()

        # We need to use deepcopy in case there is a nested structure in the defaults
        self.update(Config.default_config())

    def load(self, config_path):
        """
        Open the given path and load the YAML content into the config.

        Possible Exceptions:
            FileNotFoundError: Couldn't open file.
            YAMLError: Formatting problem in the config file.
        """

        stream = open(config_path) # Might raise FileNotFoundError
        content = yaml.safe_load(stream) # Might raise YAMLError

        self.deep_update(content)

    def deep_update(a, b):
        "Based on https://stackoverflow.com/questions/7204805/dictionaries-of-dictionaries-merge/7205107#7205107"
        for key in b:
            if key in a and isinstance(a[key], dict) and isinstance(b[key], dict):
                Config.deep_update(a[key], b[key])
            else:
                a[key] = b[key]

# Quick test
if __name__=="__main__":
    import os

    path = os.path.expanduser("~/.config/cotary/config.yaml")
    config = Config(path)
    for key in ["twitter.consumer.key","twitter.access_token.key"]:
        print("{}: {}".format(key, config[key]))

