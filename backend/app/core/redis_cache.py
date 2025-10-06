"""
Redis caching service for JobHelp API
Simple and efficient caching with Redis
"""
import logging
import json
from typing import Any, Optional, Union
from datetime import datetime, date
from redis import Redis, ConnectionPool
from redis.exceptions import RedisError

from app.config.settings import settings

logger = logging.getLogger(__name__)

class DateTimeEncoder(json.JSONEncoder):
    """Custom JSON encoder to handle datetime objects"""
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return super().default(obj)

class RedisCache:
    """Redis caching service"""
    
    def __init__(self):
        """Initialize Redis connection"""
        try:
            redis_url = settings.get_redis_url
            logger.info(f"Attempting Redis connection to: {redis_url}")
            
            # Parse URL to get connection details for better error handling
            if redis_url.startswith('rediss://'):
                # SSL connection
                self.redis = Redis.from_url(
                    redis_url,
                    decode_responses=True,
                    socket_connect_timeout=10,
                    socket_timeout=10,
                    retry_on_timeout=True,
                    health_check_interval=30,
                    max_connections=10
                )
            else:
                # Non-SSL connection
                self.redis = Redis.from_url(
                    redis_url,
                    decode_responses=True,
                    socket_connect_timeout=10,
                    socket_timeout=10,
                    retry_on_timeout=True,
                    health_check_interval=30,
                    max_connections=10
                )
            
            # Test connection with ping
            self.redis.ping()
            logger.info(f"Redis connected successfully to {redis_url.split('@')[1] if '@' in redis_url else 'redis'}")
            self.connected = True
            
        except Exception as e:
            logger.warning(f"Redis connection failed: {str(e)}")
            logger.warning(f"Redis URL used: {settings.get_redis_url}")
            logger.warning("Redis caching will be disabled")
            self.redis = None
            self.connected = False
    
    def set(self, key: str, value: Any, expire: int = 3600) -> bool:
        """Set a key-value pair with expiration"""
        if not self.connected:
            logger.warning(f"Redis not connected - skipping cache set for key: {key}")
            return False
        
        try:
            if isinstance(value, (dict, list)):
                # Use custom encoder to handle datetime objects
                value = json.dumps(value, cls=DateTimeEncoder)
            self.redis.setex(key, expire, value)
            logger.debug(f"Redis SET successful - Key: {key}, Expire: {expire}s, Value size: {len(str(value))} chars")
            return True
        except (RedisError, TypeError) as e:
            logger.error(f"Redis set error for key {key}: {str(e)}")
            return False
    
    def get(self, key: str) -> Optional[Any]:
        """Get a value by key"""
        if not self.connected:
            logger.debug(f"Redis not connected - skipping cache get for key: {key}")
            return None
        
        try:
            value = self.redis.get(key)
            if value:
                try:
                    parsed_value = json.loads(value)
                    logger.debug(f"Redis GET successful - Key: {key}, Value size: {len(str(value))} chars")
                    return parsed_value
                except json.JSONDecodeError:
                    logger.debug(f"Redis GET successful (raw string) - Key: {key}, Value size: {len(str(value))} chars")
                    return value
            else:
                logger.debug(f"Redis GET miss - Key: {key} not found")
            return None
        except RedisError as e:
            logger.error(f"Redis get error for key {key}: {str(e)}")
            return None
    
    def delete(self, key: str) -> bool:
        """Delete a key"""
        if not self.connected:
            return False
        
        try:
            return bool(self.redis.delete(key))
        except RedisError as e:
            logger.error(f"Redis delete error: {str(e)}")
            return False
    
    def exists(self, key: str) -> bool:
        """Check if key exists"""
        if not self.connected:
            return False
        
        try:
            return bool(self.redis.exists(key))
        except RedisError as e:
            logger.error(f"Redis exists error: {str(e)}")
            return False
    
    def test_connection(self) -> dict:
        """Test Redis connection and return status"""
        if not self.connected:
            return {
                "status": "error",
                "message": "Redis not connected",
                "redis_type": "None"
            }
        
        try:
            # Test basic operations
            self.redis.ping()
            self.redis.set("test_key", "test_value", ex=10)
            test_value = self.redis.get("test_key")
            self.redis.delete("test_key")
            
            if test_value == "test_value":
                return {
                    "status": "success",
                    "message": "Redis connection and operations successful",
                    "redis_type": "Redis"
                }
            else:
                return {
                    "status": "error",
                    "message": "Redis operations test failed",
                    "redis_type": "Redis"
                }
                
        except Exception as e:
            return {
                "status": "error",
                "message": f"Redis test failed: {str(e)}",
                "redis_type": "Redis"
            }
    
    def test_connection_detailed(self) -> dict:
        """Test Redis connection with detailed error information"""
        if not self.connected:
            return {
                "status": "error",
                "message": "Redis not connected",
                "redis_type": "None",
                "details": "Redis connection was not established during initialization"
            }
        
        try:
            # Test ping
            self.redis.ping()
            
            # Test set operation
            self.redis.set("test_key", "test_value", ex=10)
            
            # Test get operation
            test_value = self.redis.get("test_key")
            
            # Test delete operation
            self.redis.delete("test_key")
            
            # Verify all operations worked
            if test_value == "test_value":
                return {
                    "status": "success",
                    "message": "Redis connection and operations successful",
                    "redis_type": "Redis",
                    "details": "All basic operations (ping, set, get, delete) completed successfully"
                }
            else:
                return {
                    "status": "error",
                    "message": "Redis operations test failed",
                    "redis_type": "Redis",
                    "details": f"Expected 'test_value', got '{test_value}'"
                }
                
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            return {
                "status": "error",
                "message": f"Redis test failed: {str(e)}",
                "redis_type": "Redis",
                "details": error_details
            }

# Global Redis instance
redis_cache = RedisCache()
