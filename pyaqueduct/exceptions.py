"""Aqueduct exceptions."""


class PyAqueductError(Exception):
    """Aqueduct exception base class."""


class RemoteOperationError(PyAqueductError):
    """Remote operation error."""


class ForbiddenError(PyAqueductError):
    """Operation forbidden error."""


class UnAuthorizedError(PyAqueductError):
    """Unauthorized operation error."""


class FileToUploadNotFoundError(PyAqueductError):
    """File not found error."""


class FileUploadError(PyAqueductError):
    """Interrupted upload error."""


class FileDownloadError(PyAqueductError):
    """Interrupted download error."""
