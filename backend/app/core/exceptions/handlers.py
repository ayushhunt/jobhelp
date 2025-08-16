"""
Exception handlers for the JobHelp AI API
Centralized exception handling for better error management
"""
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions.exceptions import JobHelpException, create_http_exception

logger = logging.getLogger(__name__)

def setup_exception_handlers(app: FastAPI) -> None:
    """Setup exception handlers for the application"""
    
    @app.exception_handler(JobHelpException)
    async def jobhelp_exception_handler(request: Request, exc: JobHelpException):
        """Handle custom JobHelp exceptions"""
        logger.error(f"JobHelp exception: {exc.message}", extra={
            "error_code": exc.error_code,
            "details": exc.details,
            "path": request.url.path
        })
        return create_http_exception(exc)
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle general exceptions"""
        logger.error(f"Unhandled exception: {str(exc)}", extra={
            "path": request.url.path,
            "exception_type": type(exc).__name__
        })
        return JSONResponse(
            status_code=500,
            content={
                "message": "Internal server error",
                "error_code": "INTERNAL_ERROR",
                "details": {"exception": str(exc)} if app.debug else {}
            }
        )
