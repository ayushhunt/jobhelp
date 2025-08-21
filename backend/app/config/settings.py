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
    VERSION: str = "3.0.0"
    DESCRIPTION: str = "AI-powered resume and job description analysis"
    
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
    
    # LLM Provider Selection
    DEFAULT_LLM_PROVIDER: str = "gemini"  # gemini, openai, anthropic, groq
    FALLBACK_LLM_PROVIDER: str = "openai"
    
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
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"  # Allow extra fields from environment variables

# Global settings instance
settings = Settings()
