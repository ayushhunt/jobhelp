"""
Cache decorator for easy function result caching
"""
import functools
from typing import Any, Callable
from app.core.redis_cache import redis_cache

def cache_result(expire: int = 3600, key_prefix: str = ""):
    """
    Decorator to cache function results in Redis
    
    Args:
        expire: Cache expiration time in seconds (default: 1 hour)
        key_prefix: Prefix for cache key (default: empty)
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = f"{key_prefix}:{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            # Try to get from cache
            cached_result = redis_cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Execute function and cache result
            result = await func(*args, **kwargs)
            redis_cache.set(cache_key, result, expire)
            return result
        
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = f"{key_prefix}:{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            # Try to get from cache
            cached_result = redis_cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            redis_cache.set(cache_key, result, expire)
            return result
        
        # Return appropriate wrapper based on function type
        if func.__code__.co_flags & 0x80:  # Check if function is async
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator
