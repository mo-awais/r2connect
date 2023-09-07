class BucketAlreadyExists(Exception):
    def __init__(self, message):
        super().__init__(message)


class BucketDoesNotExist(Exception):
    def __init__(self, message):
        super().__init__(message)


class BucketIsNotEmpty(Exception):
    def __init__(self, message):
        super().__init__(message)
