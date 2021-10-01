class StorageException(Exception):
    def __init__(self, reason: str = ""):
        self.message = reason


class ScreenshotException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(f"{message}")

