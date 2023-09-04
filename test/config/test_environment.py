from unittest import TestCase

from config.environment import EnvironmentConfig
from exceptions.environment import ConfigNotFound, ConfigAlreadyExists


class TestEnvironment(TestCase):
    config = EnvironmentConfig(environment="test")

    def test_get(self):
        self.assertEqual("TEST", self.config.get("ENVIRONMENT"))

    def test_get_exception(self):
        expected_exception = ConfigNotFound("The following config does not exist: UNITTEST")

        with self.assertRaises(ConfigNotFound) as actual_exception:
            self.config.get("UNITTEST")

            self.assertEqual(expected_exception, actual_exception)

        print(actual_exception.exception)
