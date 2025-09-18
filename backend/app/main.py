"""
JobHelp AI API - Main Application
Simple and clean FastAPI application with integrated health checks
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.config.settings import settings
from app.core.logging.logger import setup_logging
from app.api.v1.api import api_router
from app.core.database import test_database_connection
from app.core.redis_cache import redis_cache

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("🚀 Starting JobHelp AI API...")
    logger.info(f"Environment: {'Development' if settings.DEBUG else 'Production'}")
    logger.info(f"Log level: {settings.LOG_LEVEL}")
    
    yield
    
    logger.info("🛑 Shutting down JobHelp AI API...")

def create_app() -> FastAPI:
    """Create and configure the FastAPI application"""
    
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="AI-powered resume and job description analysis API",
        version=settings.VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include API routes
    app.include_router(api_router, prefix=settings.API_V1_STR)
    
    # Add integrated health check endpoint
    @app.get("/health")
    async def health_check():
        """Comprehensive health check including database and Redis status"""
        try:
            # Test database connection
            db_status = test_database_connection()
            
            # Test Redis connection
            redis_status = redis_cache.test_connection()
            
            # Determine overall status
            if db_status["status"] == "success" and redis_status["status"] == "success":
                overall_status = "healthy"
            elif db_status["status"] == "success" or redis_status["status"] == "success":
                overall_status = "degraded"
            else:
                overall_status = "unhealthy"
            
            return {
                "status": overall_status,
                "service": settings.PROJECT_NAME,
                "version": settings.VERSION,
                "database": {
                    "status": "connected" if db_status["status"] == "success" else "disconnected",
                    "type": db_status.get("database_type", "Unknown"),
                    "message": db_status.get("message", "Unknown error")
                },
                "redis": {
                    "status": "connected" if redis_status["status"] == "success" else "disconnected",
                    "type": redis_status.get("redis_type", "Unknown"),
                    "message": redis_status.get("message", "Unknown error")
                },
                "timestamp": "2025-08-27T19:50:00Z"
            }
                
        except Exception as e:
            return {
                "status": "unhealthy",
                "service": settings.PROJECT_NAME,
                "version": settings.VERSION,
                "database": {
                    "status": "error",
                    "error": str(e)
                },
                "redis": {
                    "status": "error",
                    "error": str(e)
                },
                "timestamp": "2025-08-27T19:50:00Z"
            }
    
    return app

# Create the app instance for uvicorn to import
app = create_app()
