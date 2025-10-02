"""
Database Management Script for JobHelp AI API
==============================================
This script provides comprehensive database management functionality including
table creation, data reset, enum management, and database health checks.

Usage:
    python3 manage_database.py [command]

Commands:
    create      - Create all database tables
    reset       - Reset database (drop and recreate all tables)
    check       - Check database connection and status
    migrate     - Run database migrations (enum fixes, etc.)
    help        - Show this help message

Examples:
    python3 manage_database.py create
    python3 manage_database.py reset
    python3 manage_database.py check
"""
import sys
import os
from typing import Dict, Any, Optional
import argparse

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text
from app.core.database import engine, Base, test_database_connection
from app.models.entities.user import User
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DatabaseManager:
    """Database management utility class"""
    
    def __init__(self):
        self.engine = engine
        self.base = Base
    
    def check_connection(self) -> Dict[str, Any]:
        """Check database connection and return detailed status"""
        logger.info("🔍 Checking database connection...")
        return test_database_connection()
    
    def create_enum_types(self) -> bool:
        """Create required enum types in the database"""
        try:
            logger.info("🔧 Creating enum types...")
            
            with self.engine.connect() as conn:
                trans = conn.begin()
                
                try:
                    # Create UserRole enum if it doesn't exist
                    conn.execute(text("""
                        DO $$ BEGIN
                            CREATE TYPE userrole AS ENUM ('admin', 'applicant', 'recruiter');
                        EXCEPTION
                            WHEN duplicate_object THEN null;
                        END $$;
                    """))
                    
                    # Create AuthProvider enum if it doesn't exist
                    conn.execute(text("""
                        DO $$ BEGIN
                            CREATE TYPE authprovider AS ENUM ('local', 'google', 'github');
                        EXCEPTION
                            WHEN duplicate_object THEN null;
                        END $$;
                    """))
                    
                    trans.commit()
                    logger.info("✅ Enum types created/verified successfully")
                    return True
                    
                except Exception as e:
                    trans.rollback()
                    logger.error(f"❌ Failed to create enum types: {str(e)}")
                    return False
                    
        except Exception as e:
            logger.error(f"❌ Database connection failed: {str(e)}")
            return False
    
    def create_tables(self) -> bool:
        """Create all database tables"""
        try:
            # First check connection
            db_status = self.check_connection()
            if db_status["status"] != "success":
                return False
            
            # Create enum types first
            if not self.create_enum_types():
                return False
            
            # Create all tables
            logger.info("🏗️  Creating database tables...")
            self.base.metadata.create_all(bind=self.engine)
            
            # List created tables
            logger.info("✅ Database tables created successfully!")
            logger.info("📋 Tables:")
            for table_name in self.base.metadata.tables.keys():
                logger.info(f"   - {table_name}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to create tables: {str(e)}")
            return False
    
    def reset_database(self) -> bool:
        """Reset database by dropping and recreating all tables"""
        try:
            logger.warning("⚠️  RESETTING DATABASE - ALL DATA WILL BE LOST!")
            
            # Confirm action
            if not self._confirm_reset():
                logger.info("❌ Database reset cancelled by user")
                return False
            
            logger.info("🗑️  Dropping all tables and enum types...")
            
            with self.engine.connect() as conn:
                trans = conn.begin()
                
                try:
                    # Drop tables first
                    self.base.metadata.drop_all(bind=self.engine)
                    
                    # Drop enum types
                    conn.execute(text("DROP TYPE IF EXISTS userrole CASCADE"))
                    conn.execute(text("DROP TYPE IF EXISTS authprovider CASCADE"))
                    
                    trans.commit()
                    logger.info("✅ Database cleared successfully")
                    
                except Exception as e:
                    trans.rollback()
                    logger.error(f"❌ Failed to drop tables: {str(e)}")
                    return False
            
            # Recreate everything
            logger.info("🔄 Recreating database structure...")
            return self.create_tables()
            
        except Exception as e:
            logger.error(f"❌ Database reset failed: {str(e)}")
            return False
    
    def migrate_enums(self) -> bool:
        """Fix enum types and update existing data"""
        try:
            logger.info("🔄 Running enum migration...")
            
            with self.engine.connect() as conn:
                trans = conn.begin()
                
                try:
                    # Check if enum types exist and have correct values
                    result = conn.execute(text("""
                        SELECT t.typname, array_agg(e.enumlabel ORDER BY e.enumlabel) as labels
                        FROM pg_type t
                        JOIN pg_enum e ON t.oid = e.enumtypid
                        WHERE t.typname IN ('userrole', 'authprovider')
                        GROUP BY t.typname
                    """))
                    
                    existing_enums = {row[0]: row[1] for row in result.fetchall()}
                    
                    # Expected enum values
                    expected_enums = {
                        'userrole': ['admin', 'applicant', 'recruiter'],
                        'authprovider': ['local', 'google', 'github']
                    }
                    
                    for enum_name, expected_values in expected_enums.items():
                        if enum_name not in existing_enums:
                            logger.info(f"Creating missing enum: {enum_name}")
                            values_str = "', '".join(expected_values)
                            conn.execute(text(f"CREATE TYPE {enum_name} AS ENUM ('{values_str}')"))
                        elif set(existing_enums[enum_name]) != set(expected_values):
                            logger.warning(f"Enum {enum_name} has unexpected values: {existing_enums[enum_name]}")
                            logger.info(f"Expected: {expected_values}")
                    
                    trans.commit()
                    logger.info("✅ Enum migration completed")
                    return True
                    
                except Exception as e:
                    trans.rollback()
                    logger.error(f"❌ Enum migration failed: {str(e)}")
                    return False
                    
        except Exception as e:
            logger.error(f"❌ Migration failed: {str(e)}")
            return False
    
    def _confirm_reset(self) -> bool:
        """Confirm database reset action"""
        try:
            response = input("Are you sure you want to reset the database? This will delete ALL data! (yes/no): ")
            return response.lower() in ['yes', 'y']
        except KeyboardInterrupt:
            return False

def main():
    """Main execution function with command line interface"""
    parser = argparse.ArgumentParser(
        description="Database Management Script for JobHelp AI API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 manage_database.py create    # Create all tables
  python3 manage_database.py reset     # Reset database (careful!)
  python3 manage_database.py check     # Check database status
  python3 manage_database.py migrate   # Run migrations
        """
    )
    
    parser.add_argument(
        'command',
        choices=['create', 'reset', 'check', 'migrate', 'help'],
        help='Database management command to execute'
    )
    
    args = parser.parse_args()
    
    # Create database manager
    db_manager = DatabaseManager()
    
    print("=" * 60)
    print("JobHelp AI - Database Management Script")
    print("=" * 60)
    
    success = True
    
    if args.command == 'create':
        print("📝 Creating database tables...")
        success = db_manager.create_tables()
    
    elif args.command == 'reset':
        print("🔄 Resetting database...")
        success = db_manager.reset_database()
    
    elif args.command == 'check':
        print("🔍 Checking database status...")
        status = db_manager.check_connection()
        if status["status"] == "success":
            print(f"✅ Database: {status['database_type']}")
            print(f"📊 Version: {status['version']}")
            print(f"🏠 Host: {status.get('host', 'Unknown')}")
            success = True
        else:
            print(f"❌ Database connection failed: {status['message']}")
            success = False
    
    elif args.command == 'migrate':
        print("🔄 Running database migrations...")
        success = db_manager.migrate_enums()
    
    elif args.command == 'help':
        parser.print_help()
        return
    
    print("=" * 60)
    if success:
        print("✅ Operation completed successfully!")
    else:
        print("❌ Operation failed! Check logs for details.")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Usage: python3 manage_database.py [command]")
        print("Run 'python3 manage_database.py help' for more information.")
        sys.exit(1)
    
    main()
