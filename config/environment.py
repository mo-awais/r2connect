from os import environ
from dotenv import load_dotenv

from exceptions.environment import ConfigNotFound, ConfigAlreadyExists


class EnvironmentConfig:
    def __init__(self, environment: str = "production"):
        load_dotenv(f'{environment}.env')

    @staticmethod
    def __exists(config_key: str) -> bool:
        """
        Check if a config key exists in the environment variables.

        :param config_key: A key to check against in the environment variables
        :type config_key: str
        :returns: True or False depending on if the config key exists
        """

        if config_key in environ:
            return True
        else:
            return False

    def get(self, config_key: str) -> str:
        """
        Returns a string corresponding to the key provided, from the system environment.

        :param config_key: A key to check against in the environment variables
        :type config_key: str
        :returns: A corresponding string value in the environment variables linked to the supplied key
        :rtype: str
        :raises ConfigNotFound: If supplied key does not exist in the environment variables
        """

        if self.__exists(config_key):
            return environ.get(config_key)
        else:
            raise ConfigNotFound(f"The following config does not exist: {config_key}")

    def set_new(self, config_key: str, config_value: str) -> None:
        """
        Set a new system variable corresponding to the key provided.

        :param config_key: A new key to set a value for in the environment variables
        :type config_key: str
        :param config_value: A new value to set to the new key in the environment variables
        :type config_value: str
        :returns: None
        :raises ConfigAlreadyExists: If key exists in the environment variables
        """

        if self.__exists(config_key):
            raise ConfigAlreadyExists(f"The following config key already exists: {config_key}, please overwrite this key")
        else:
            environ[config_key] = config_value

    def set_existing(self, config_key: str, config_value: str) -> None:
        """
        Overwrite an existing key in the environment variable with the supplied value.

        :param config_key: An existing key to overwrite
        :type config_key: str
        :param config_value: A value to overwrite the existing key with
        :type config_value: str
        :returns: None
        :raises ConfigNotFound: If key does not exist in the environment variables
        """

        if self.__exists(config_key):
            environ.pop(config_key)
            environ[config_key] = config_value
        else:
            raise ConfigNotFound(f"The following config does not exist: {config_key}")
