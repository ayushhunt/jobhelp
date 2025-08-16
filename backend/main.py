#!/usr/bin/env python3
"""
JobHelp AI API - Main Application Entry Point
A modular, production-ready FastAPI application for resume and job description analysis
"""
import uvicorn
from app.config.settings import settings

def main():
    """Main application entry point"""
    # Run the application with proper import string format
    uvicorn.run(
        "app.main:app",  # Import string format
        host="0.0.0.0",
        port=8000,
        reload=False,  # Disable reload for production
        log_level="info",
        access_log=True
    )

if __name__ == "__main__":
    main()
