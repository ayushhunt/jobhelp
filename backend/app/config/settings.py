"""
Application configuration settings
"""
import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "JobHelp AI API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "jobhelp"
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    
    # CORS Configuration
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://192.168.1.7:3000"
    ]
    
    # Database Configuration
    DATABASE_URL: Optional[str] = None
    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: int = 5432
    DATABASE_NAME: str = "jobhelp"
    DATABASE_USER: str = "postgres"
    DATABASE_PASSWORD: str = ""
    
    # Redis Configuration
    REDIS_URL: Optional[str] = None
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = None
    REDIS_DB: int = 0
    REDIS_SSL: bool = True  # Upstash uses SSL
    
    # LLM Configuration
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    PARALLEL_API_KEY: Optional[str] = None
    
    # Google Services Configuration
    GOOGLE_KNOWLEDGE_GRAPH_API_KEY: Optional[str] = None
    GOOGLE_SEARCH_API_KEY: Optional[str] = None
    GOOGLE_SEARCH_ENGINE_ID: Optional[str] = None
    GOOGLE_PLACES_API_KEY: Optional[str] = None
    
    # LLM Provider Selection
    DEFAULT_LLM_PROVIDER: str = "gemini"  # gemini, openai, anthropic, groq
    FALLBACK_LLM_PROVIDER: str = "openai"
    
    # Google API Configuration
    GOOGLE_KNOWLEDGE_GRAPH_API_KEY: Optional[str] = None
    GOOGLE_SEARCH_API_KEY: Optional[str] = None
    GOOGLE_SEARCH_ENGINE_ID: Optional[str] = None
    GOOGLE_PLACES_API_KEY: Optional[str] = None
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # File Upload
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_TYPES: List[str] = [".pdf", ".docx", ".txt"]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE: Optional[str] = "logs/app.log"
    
    # NLTK Data
    NLTK_DATA_PATH: str = "nltk_data"
    
    # AI Usage Limits
    FREE_TIER_DAILY_LIMIT: int = 10
    PREMIUM_TIER_DAILY_LIMIT: int = 100
    
    # JWT Configuration
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 1
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # OAuth Configuration
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None
    GITHUB_CLIENT_ID: Optional[str] = None
    GITHUB_CLIENT_SECRET: Optional[str] = None
    
    # Frontend URLs
    FRONTEND_URL: str = "http://localhost:3000"
    AUTH_REDIRECT_URL: str = "http://localhost:3000/auth/callback"
    
    # Email Configuration - Resend API
    RESEND_API_KEY: Optional[str] = None
    EMAIL_FROM: str = "noreply@jobhelp.ai"
    
    # Legacy SMTP Configuration (kept for compatibility)
    # SMTP_HOST: Optional[str] = None
    # SMTP_PORT: int = 587
    # SMTP_USERNAME: Optional[str] = None
    # SMTP_PASSWORD: Optional[str] = None
    # SMTP_USE_TLS: bool = True
    
    @property
    def get_database_url(self) -> str:
        """Get database URL from environment or construct from components"""
        if self.DATABASE_URL:
            return self.DATABASE_URL
        
        return f"postgresql://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
    
    @property
    def get_redis_url(self) -> str:
        """Get Redis URL from environment or construct from components"""
        if self.REDIS_URL:
            return self.REDIS_URL
        
        # Construct Redis URL with SSL for Upstash
        protocol = "rediss://" if self.REDIS_SSL else "redis://"
        auth = f":{self.REDIS_PASSWORD}@" if self.REDIS_PASSWORD else ""
        return f"{protocol}{auth}{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"  # Allow extra fields from environment variables

# Global settings instance
settings = Settings()
