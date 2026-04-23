class StudentManagementError(Exception):
    """Base exception for the application."""


class AuthenticationError(StudentManagementError):
    """Raised when admin authentication fails."""


class ValidationError(StudentManagementError):
    """Raised when user input is invalid."""


class StudentNotFoundError(StudentManagementError):
    """Raised when a student record cannot be found."""
