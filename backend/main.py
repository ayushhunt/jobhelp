#!/usr/bin/env python3
"""
JobHelp AI API - Main Application Entry Point
==============================================
Production-ready FastAPI application for AI-powered resume analysis and job matching.

Features:
- Resume and job description analysis with multiple LLM providers
- Company research tools with web scraping and knowledge graphs
- User authentication with JWT and role-based access control
- Email integration for notifications and verification
- Redis caching for performance optimization

Usage:
    python3 main.py                    # Production server
    python3 main.py --dev              # Development with auto-reload
    python3 main.py --port 8080        # Custom port
    python3 main.py --help             # Show help

Environment:
    Ensure .env file is configured with required variables:
    - DATABASE_URL
    - JWT_SECRET_KEY
    - RESEND_API_KEY (for emails)
    - REDIS_URL (for caching)
"""
import argparse
import sys
import uvicorn
from app.config.settings import settings

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="JobHelp AI API Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 main.py                    # Start production server
  python3 main.py --dev              # Development mode with auto-reload
  python3 main.py --port 8080        # Start on custom port
  python3 main.py --workers 4        # Production with 4 workers
        """
    )
    
    parser.add_argument(
        "--dev",
        action="store_true",
        help="Run in development mode with auto-reload"
    )
    
    parser.add_argument(
        "--port",
        type=int,
        default=settings.PORT,
        help=f"Port to run the server on (default: {settings.PORT})"
    )
    
    parser.add_argument(
        "--host",
        default=settings.HOST,
        help=f"Host to bind the server to (default: {settings.HOST})"
    )
    
    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="Number of worker processes (production only)"
    )
    
    parser.add_argument(
        "--log-level",
        choices=["debug", "info", "warning", "error", "critical"],
        default="info",
        help="Logging level (default: info)"
    )
    
    return parser.parse_args()

def main():
    """Main application entry point with enhanced configuration"""
    args = parse_arguments()
    
    print("=" * 60)
    print("🚀 Starting JobHelp AI API Server")
    print("=" * 60)
    print(f"📍 Host: {args.host}:{args.port}")
    print(f"🔧 Mode: {'Development' if args.dev else 'Production'}")
    print(f"📊 Log Level: {args.log_level.upper()}")
    
    if args.dev:
        print("🔄 Auto-reload: Enabled")
        print("⚠️  Development mode - not suitable for production!")
    else:
        print(f"👥 Workers: {args.workers}")
        print("🔒 Production mode")
    
    print("=" * 60)
    
    # Configure uvicorn settings
    uvicorn_config = {
        "app": "app.main:app",
        "host": args.host,
        "port": args.port,
        "log_level": args.log_level,
        "access_log": True,
        "server_header": False,  # Don't expose server info
        "date_header": False,    # Don't expose date header
    }
    
    if args.dev:
        # Development configuration
        uvicorn_config.update({
            "reload": True,
            "reload_dirs": ["app"],
            "reload_excludes": ["*.pyc", "__pycache__"],
        })
    else:
        # Production configuration
        uvicorn_config.update({
            "workers": args.workers,
            "reload": False,
        })
    
    try:
        # Start the server
        uvicorn.run(**uvicorn_config)
    except KeyboardInterrupt:
        print("\n🛑 Server shutdown requested by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Server startup failed: {e}")
        print("\n💡 Troubleshooting tips:")
        print("   1. Check that the port is not already in use")
        print("   2. Verify database connection in .env file")
        print("   3. Ensure all required environment variables are set")
        print("   4. Run 'python3 test_db_connection.py' to test database")
        sys.exit(1)

if __name__ == "__main__":
    main()
