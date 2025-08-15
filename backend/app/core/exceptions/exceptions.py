"""
Custom exception classes for the application
"""
from typing import Any, Dict, Optional
from fastapi import HTTPException, status

class JobHelpException(Exception):
    """Base exception for JobHelp application"""
    
    def __init__(
        self,
        message: str,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)

class FileProcessingError(JobHelpException):
    """Raised when file processing fails"""
    pass

class TextExtractionError(JobHelpException):
    """Raised when text extraction from files fails"""
    pass

class LLMServiceError(JobHelpException):
    """Raised when LLM service encounters an error"""
    pass

class AnalyticsError(JobHelpException):
    """Raised when analytics processing fails"""
    pass

class ValidationError(JobHelpException):
    """Raised when input validation fails"""
    pass

class RateLimitExceeded(JobHelpException):
    """Raised when rate limit is exceeded"""
    pass

class InsufficientCredits(JobHelpException):
    """Raised when user doesn't have enough credits for AI features"""
    pass

def create_http_exception(
    exc: JobHelpException,
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
) -> HTTPException:
    """Convert JobHelpException to HTTPException"""
    return HTTPException(
        status_code=status_code,
        detail={
            "message": exc.message,
            "error_code": exc.error_code,
            "details": exc.details
        }
    )
