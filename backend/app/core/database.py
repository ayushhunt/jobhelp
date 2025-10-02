"""
Database configuration and connection management
Simple and clean database setup for JobHelp API
"""
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from typing import Generator

from app.config.settings import settings

logger = logging.getLogger(__name__)

def create_database_engine():
    """Create database engine with fallback to SQLite"""
    try:
        database_url = settings.get_database_url
        
        # Ensure the URL uses the correct PostgreSQL dialect
        if database_url.startswith('postgres://'):
            # Convert postgres:// to postgresql:// for compatibility
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        elif not database_url.startswith('postgresql://'):
            database_url = f"postgresql://{database_url}"
        
        logger.info(f"Attempting PostgreSQL connection to: {database_url}")
        
        engine = create_engine(
            database_url,
            pool_pre_ping=True,
            echo=settings.DEBUG,
            connect_args={"connect_timeout": 10}
        )
        
        logger.info(f"PostgreSQL engine created successfully for {database_url.split('@')[1] if '@' in database_url else 'database'}")
        return engine
        
    except Exception as e:
        logger.warning(f"PostgreSQL connection failed: {str(e)}")
        logger.info("Using SQLite fallback for testing")
        
        return create_engine(
            "sqlite:///:memory:",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
            echo=settings.DEBUG
        )

# Create engine and session factory
engine = create_database_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_database_connection() -> dict:
    """Test database connection and return status"""
    try:
        with engine.connect() as connection:
            # Test basic connection
            connection.execute(text("SELECT 1"))
            
            # Determine database type and get version info
            if engine.dialect.name == 'postgresql':
                version_result = connection.execute(text("SELECT version()"))
                version = version_result.fetchone()[0]
                database_type = "PostgreSQL"
            else:
                version = "SQLite (fallback)"
                database_type = "SQLite"
            
            return {
                "status": "success",
                "message": "Database connection successful",
                "version": version,
                "database_type": database_type
            }
            
    except Exception as e:
        logger.error(f"Database connection test failed: {str(e)}")
        return {
            "status": "error",
            "message": f"Database connection failed: {str(e)}"
        }
