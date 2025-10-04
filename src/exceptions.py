

class CustomException(Exception):  # pragma: no cover
    """Custom exception base class."""

    key = "CUSTOM_GENERIC_EXCEPTION"

    def __init__(self, message: str):
        super(CustomException, self).__init__(message)

        self.details: dict = dict(message=message)


class DirectoryCreationError(CustomException):  # pragma: no cover
    """Raised when a directory cannot be created."""

    key = "DIRECTORY_CREATION_ERROR"

    def __init__(self, directory_path: str, error: str):
        message = f"Failed to create directory at '{directory_path}'. {error=}"
        super(DirectoryCreationError, self).__init__(message)
        self.details = dict(directory_path=directory_path, error=str(error))
