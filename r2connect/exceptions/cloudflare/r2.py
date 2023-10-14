class BucketAlreadyExists(Exception):
    def __init__(self, message):
        super().__init__(message)


class BucketDoesNotExist(Exception):
    def __init__(self, message):
        super().__init__(message)


class BucketIsNotEmpty(Exception):
    def __init__(self, message):
        super().__init__(message)


class ObjectDoesNotExist(Exception):
    def __init__(self, message):
        super().__init__(message)


class ObjectAlreadyExists(Exception):
    def __init__(self, message):
        super().__init__(message)


class MissingConfig(Exception):
    def __init__(self, message):
        super().__init__(message)
