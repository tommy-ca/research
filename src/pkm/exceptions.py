"""
PKM System Exceptions
Custom exception classes for PKM operations
"""


class PkmError(Exception):
    """Base exception for PKM system errors"""
    pass


class CaptureError(PkmError):
    """Exception raised during note capture operations"""
    pass


class ProcessingError(PkmError):
    """Exception raised during note processing operations"""
    pass


class ValidationError(PkmError):
    """Exception raised during validation operations"""
    pass


class NetworkError(PkmError):
    """Exception raised during network operations"""
    pass