"""
Custom exceptions for FastWindX.
"""


class FastWindXException(Exception):
    """
    Base exception class for FastWindX.

    This class can be used to catch any FastWindX-specific exceptions.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class DatabaseException(FastWindXException):
    """
    Exception raised for database-related errors.
    """

    pass


class AuthenticationException(FastWindXException):
    """
    Exception raised for authentication-related errors.
    """

    pass


class ValidationException(FastWindXException):
    """
    Exception raised for data validation errors.
    """

    pass


class NotFoundException(FastWindXException):
    """
    Exception raised when a requested resource is not found.
    """

    pass
