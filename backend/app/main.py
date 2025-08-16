"""
JobHelp AI API - Application Factory
Creates and configures the FastAPI application with all middleware and routes
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from contextlib import asynccontextmanager
import logging

from app.config.settings import settings
from app.core.logging.logger import setup_logging
from app.api.v1.api import api_router
from app.core.exceptions.handlers import setup_exception_handlers

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("🚀 Starting JobHelp AI API...")
    logger.info(f"Environment: {'Development' if settings.DEBUG else 'Production'}")
    logger.info(f"Log level: {settings.LOG_LEVEL}")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down JobHelp AI API...")

def create_app() -> FastAPI:
    """Create and configure the FastAPI application"""
    
    # Create FastAPI instance
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="AI-powered resume and job description analysis API",
        version=settings.VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan
    )
    
    # Add middleware
    _add_middleware(app)
    
    # Setup exception handlers
    setup_exception_handlers(app)
    
    # Include API routes
    app.include_router(api_router, prefix=settings.API_V1_STR)
    
    # Add health check endpoint
    _add_health_check(app)
    
    return app

def _add_middleware(app: FastAPI) -> None:
    """Add middleware to the application"""
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Gzip compression middleware
    app.add_middleware(GZipMiddleware, minimum_size=1000)

def _add_health_check(app: FastAPI) -> None:
    """Add health check endpoint"""
    
    @app.get("/health")
    async def health_check():
        """Health check endpoint"""
        return {
            "status": "healthy",
            "service": settings.PROJECT_NAME,
            "version": settings.VERSION,
            "timestamp": "2024-01-01T00:00:00Z"
        }

# Create the app instance for uvicorn to import
app = create_app()
