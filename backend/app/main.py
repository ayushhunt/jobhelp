"""
Main FastAPI application
"""
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from app.config.settings import settings
from app.core.logging.logger import setup_logging
from app.api.v1.api import api_router
from app.core.exceptions.exceptions import JobHelpException, create_http_exception

# Setup logging
setup_logging()

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting JobHelp AI API...")
    logger.info(f"Environment: {'Development' if settings.DEBUG else 'Production'}")
    logger.info(f"Log level: {settings.LOG_LEVEL}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down JobHelp AI API...")

def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.DESCRIPTION,
        version=settings.VERSION,
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
        openapi_url="/openapi.json" if settings.DEBUG else None,
        lifespan=lifespan
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"]
    )
    
    # Add trusted host middleware for production
    if not settings.DEBUG:
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=["*"]  # Configure based on your deployment
        )
    
    # Global exception handler
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
                "details": {"exception": str(exc)} if settings.DEBUG else {}
            }
        )
    
    # Include API router
    app.include_router(api_router, prefix=settings.API_V1_STR)
    
    # Health check endpoint
    @app.get("/health")
    async def health_check():
        """Health check endpoint"""
        return {
            "status": "healthy",
            "service": settings.PROJECT_NAME,
            "version": settings.VERSION,
            "timestamp": "2024-01-01T00:00:00Z"  # Replace with actual timestamp
        }
    
    # Root endpoint
    @app.get("/")
    async def root():
        """Root endpoint"""
        return {
            "message": f"{settings.PROJECT_NAME} is running",
            "version": settings.VERSION,
            "docs": "/docs" if settings.DEBUG else "Documentation disabled in production",
            "health": "/health"
        }
    
    logger.info("FastAPI application created successfully")
    return app

# Create application instance
app = create_app()

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
