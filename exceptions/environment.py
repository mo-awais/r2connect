class ConfigNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)


class ConfigAlreadyExists(Exception):
    def __init__(self, message):
        super().__init__(message)
