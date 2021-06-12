class StorageException(Exception):
    def __init__(self, reason: str = ""):
        self.message = reason
