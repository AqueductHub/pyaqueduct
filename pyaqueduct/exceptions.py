"""Aqueduct exceptions."""


class AqueductException(Exception):
    """Aqueduct Exception base class."""

    message: str

    def __init__(self, message: str):
        Exception.__init__(self, message)
        self.message = message


class FileNotFoundException(AqueductException):
    """File Not Found Exception."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = "File was not found on the server."


class InterruptedUploadException(AqueductException):
    """Interrupted Upload Exception."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = "Upload failed as upload was interrupted."


class InterruptedDownloadException(AqueductException):
    """Interrupted Download Exception"""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = "Download failed as download was interrupted."
