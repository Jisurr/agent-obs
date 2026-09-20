"""Exceptions raised by the compensation middleware."""


class CompensationError(Exception):
    """Base class for compensation middleware errors."""


class NoCompensationRegisteredError(CompensationError):
    """Raised when an action fails but has no registered compensation."""


class CompensationExecutionError(CompensationError):
    """Raised when a compensation step itself fails during rollback."""
