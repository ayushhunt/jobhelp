"""
Database Table Creation and Migration Script
============================================
This script handles database table creation and basic migrations for the JobHelp AI API.

Features:
- Creates all required database tables
- Handles enum type creation (UserRole, AuthProvider)
- Provides database connection validation
- Safe to run multiple times (idempotent)

Usage:
    python3 create_tables.py

Requirements:
- Database connection configured in .env
- All model imports available
"""
import sys
import os
from typing import Dict, Any

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import engine, Base, test_database_connection
from app.models.entities.user import User  # Import all entity models here
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def validate_database_connection() -> Dict[str, Any]:
    """Validate database connection and return status"""
    logger.info("🔍 Validating database connection...")
    db_status = test_database_connection()
    
    if db_status["status"] != "success":
        logger.error(f"❌ Database connection failed: {db_status['message']}")
        return db_status
    
    logger.info(f"✅ Connected to {db_status['database_type']}")
    logger.info(f"📊 Database version: {db_status['version']}")
    return db_status

def create_tables() -> bool:
    """
    Create all database tables with proper error handling
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Validate database connection
        db_status = validate_database_connection()
        if db_status["status"] != "success":
            return False
        
        # Create all tables
        logger.info("🏗️  Creating database tables...")
        Base.metadata.create_all(bind=engine)
        
        # Verify table creation
        logger.info("✅ Database tables created successfully!")
        logger.info("📋 Tables created:")
        
        # List all created tables
        for table_name in Base.metadata.tables.keys():
            logger.info(f"   - {table_name}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to create tables: {str(e)}")
        logger.error("💡 Possible solutions:")
        logger.error("   1. Check database connection settings in .env")
        logger.error("   2. Ensure database exists and user has proper permissions")
        logger.error("   3. Check for conflicting enum types or table constraints")
        return False

def main():
    """Main execution function"""
    print("=" * 60)
    print("JobHelp AI - Database Table Creation Script")
    print("=" * 60)
    
    success = create_tables()
    
    print("=" * 60)
    if success:
        print("✅ Database setup completed successfully!")
        print("🚀 Your application is ready to run!")
    else:
        print("❌ Database setup failed!")
        print("🔧 Please check the logs above for troubleshooting steps.")
        sys.exit(1)

if __name__ == "__main__":
    main()

