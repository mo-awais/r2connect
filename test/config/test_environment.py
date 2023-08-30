from unittest import TestCase

from config.environment import EnvironmentConfig
from exceptions.environment import ConfigNotFound, ConfigAlreadyExists


class TestEnvironment(TestCase):
    config = EnvironmentConfig()

    def test_get(self):
        self.assertEquals("TEST", self.config.get("ENVIRONMENT"))

    def test_get_exception(self):
        expected_exception = ConfigNotFound("The following config does not exist: UNITTEST")

        with self.assertRaises(ConfigNotFound) as actual_exception:
            self.config.get("UNITTEST")

        print(actual_exception.exception)
