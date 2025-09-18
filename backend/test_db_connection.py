#!/usr/bin/env python3
"""
Comprehensive database connection test script
Tests both PostgreSQL and Redis connections with detailed debugging
"""
import os
import sys
import logging

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.core.database import test_database_connection
from app.core.redis_cache import redis_cache
from app.config.settings import settings

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_postgresql_connection():
    """Test PostgreSQL connection"""
    try:
        logger.info("🔍 Testing PostgreSQL connection...")
        logger.info(f"Database URL: {settings.get_database_url}")
        
        result = test_database_connection()
        
        if result["status"] == "success":
            logger.info("✅ PostgreSQL connection successful!")
            logger.info(f"Database Type: {result.get('database_type', 'Unknown')}")
            logger.info(f"Version: {result.get('version', 'Unknown')}")
            return True
        else:
            logger.error("❌ PostgreSQL connection failed!")
            logger.error(f"Error: {result.get('message', 'Unknown error')}")
            return False
            
    except Exception as e:
        logger.error(f"❌ PostgreSQL test failed with exception: {str(e)}")
        return False

def test_redis_connection():
    """Test Redis connection"""
    try:
        logger.info("🔍 Testing Redis connection...")
        logger.info(f"Redis URL: {settings.get_redis_url}")
        
        # Test the Redis connection with detailed information
        result = redis_cache.test_connection_detailed()
        
        if result["status"] == "success":
            logger.info("✅ Redis connection successful!")
            logger.info(f"Redis Type: {result.get('redis_type', 'Unknown')}")
            logger.info(f"Message: {result.get('message', 'Unknown')}")
            if result.get('details'):
                logger.info(f"Details: {result.get('details')}")
            return True
        else:
            logger.error("❌ Redis connection failed!")
            logger.error(f"Error: {result.get('message', 'Unknown error')}")
            if result.get('details'):
                logger.error(f"Details: {result.get('details')}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Redis test failed with exception: {str(e)}")
        return False

def debug_connection_issues():
    """Debug connection issues by checking configuration"""
    logger.info("🔧 Debugging connection configuration...")
    
    # Check environment variables
    logger.info("Environment Variables:")
    logger.info(f"  DATABASE_URL: {'Set' if settings.DATABASE_URL else 'Not set'}")
    logger.info(f"  REDIS_URL: {'Set' if settings.REDIS_URL else 'Not set'}")
    
    if not settings.DATABASE_URL:
        logger.info("  DATABASE_HOST: " + settings.DATABASE_HOST)
        logger.info("  DATABASE_PORT: " + str(settings.DATABASE_PORT))
        logger.info("  DATABASE_NAME: " + settings.DATABASE_NAME)
        logger.info("  DATABASE_USER: " + settings.DATABASE_USER)
        logger.info("  DATABASE_PASSWORD: " + ("Set" if settings.DATABASE_PASSWORD else "Not set"))
    
    if not settings.REDIS_URL:
        logger.info("  REDIS_HOST: " + settings.REDIS_HOST)
        logger.info("  REDIS_PORT: " + str(settings.REDIS_PORT))
        logger.info("  REDIS_PASSWORD: " + ("Set" if settings.REDIS_PASSWORD else "Not set"))
        logger.info("  REDIS_DB: " + str(settings.REDIS_DB))
        logger.info("  REDIS_SSL: " + str(settings.REDIS_SSL))
    
    # Check constructed URLs
    logger.info("Constructed URLs:")
    logger.info(f"  Database: {settings.get_database_url}")
    logger.info(f"  Redis: {settings.get_redis_url}")

def test_basic_redis_operations():
    """Test basic Redis operations if connection is available"""
    if not redis_cache.connected:
        logger.warning("⚠️  Skipping Redis operations test - not connected")
        return False
    
    try:
        logger.info("🧪 Testing basic Redis operations...")
        
        # Test set operation
        test_key = "test:connection:key"
        test_value = "test_value_123"
        
        success = redis_cache.set(test_key, test_value, expire=60)
        if not success:
            logger.error("❌ Redis SET operation failed")
            return False
        
        # Test get operation
        retrieved_value = redis_cache.get(test_key)
        if retrieved_value != test_value:
            logger.error(f"❌ Redis GET operation failed. Expected: {test_value}, Got: {retrieved_value}")
            return False
        
        # Test delete operation
        delete_success = redis_cache.delete(test_key)
        if not delete_success:
            logger.error("❌ Redis DELETE operation failed")
            return False
        
        # Verify deletion
        if redis_cache.exists(test_key):
            logger.error("❌ Redis key still exists after deletion")
            return False
        
        logger.info("✅ All Redis operations successful!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Redis operations test failed: {str(e)}")
        return False

def main():
    """Main function"""
    logger.info("🚀 Starting comprehensive database connection test...")
    logger.info("=" * 60)
    
    # Debug configuration first
    debug_connection_issues()
    logger.info("=" * 60)
    
    # Test PostgreSQL
    postgres_success = test_postgresql_connection()
    logger.info("=" * 60)
    
    # Test Redis
    redis_success = test_redis_connection()
    logger.info("=" * 60)
    
    # Test Redis operations if connected
    redis_ops_success = False
    if redis_success:
        redis_ops_success = test_basic_redis_operations()
        logger.info("=" * 60)
    
    # Summary
    logger.info("📊 TEST SUMMARY:")
    logger.info(f"  PostgreSQL: {'✅ PASS' if postgres_success else '❌ FAIL'}")
    logger.info(f"  Redis Connection: {'✅ PASS' if redis_success else '❌ FAIL'}")
    logger.info(f"  Redis Operations: {'✅ PASS' if redis_ops_success else '❌ FAIL'}")
    
    if postgres_success and redis_success and redis_ops_success:
        logger.info("🎉 All tests passed! Both databases are working correctly.")
        sys.exit(0)
    else:
        logger.error("💥 Some tests failed. Check the configuration and connection details above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
