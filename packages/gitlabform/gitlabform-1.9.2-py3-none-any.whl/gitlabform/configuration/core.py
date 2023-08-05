import os
import logging
import yaml
from pathlib import Path


class ConfigurationCore:

    config_from_file = None
    config_dir = None

    def __init__(self, config_path=None):
        try:
            # using this env var should be considered unofficial, we need this temporarily for backwards compatibility.
            # support for it may be removed without notice, do not use it!
            if 'APP_HOME' in os.environ:
                config_path = os.path.join(os.environ['APP_HOME'], 'config.yml')
            # this case is only meant for using gitlabform as a library
            elif not config_path:
                config_path = os.path.join(str(Path.home()), '.gitlabform', 'config.yml')
            elif config_path in [os.path.join('.', 'config.yml'), 'config.yml']:
                config_path = os.path.join(os.getcwd(), 'config.yml')

            logging.info("Reading config from: {}".format(config_path))

            with open(config_path, 'r') as ymlfile:
                self.config_from_file = yaml.safe_load(ymlfile)

            # we need config path for accessing files for relative paths
            self.config_dir = os.path.dirname(config_path)

        except Exception as e:
            raise ConfigFileNotFoundException(config_path)

    def get(self, path, default=None):
        """
        :param path: "path" to given element in YAML file, for example for:

        group_settings:
          sddc:
            deploy_keys:
              qa_puppet:
                key: some key...
                title: some title...
                can_push: false

        ..a path to a single element array ['qa_puppet'] will be: "group_settings|sddc|deploy_keys".

        To get the dict under it use: get("group_settings|sddc|deploy_keys")

        :return: element from YAML file (dict, array, string...)
        """
        tokens = path.split('|')
        current = self.config_from_file

        try:
            for token in tokens:
                current = current[token]
        except:
            if default is not None:
                return default
            else:
                raise KeyNotFoundException

        return current


class ConfigFileNotFoundException(Exception):
    pass


class KeyNotFoundException(Exception):
    pass
