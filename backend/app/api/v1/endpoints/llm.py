"""
LLM provider management endpoints
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any
from app.services.llm.llm_service import LLMService
from app.core.redis_cache import redis_cache

router = APIRouter()
llm_service = LLMService()

@router.get("/status")
async def get_llm_status() -> Dict[str, Any]:
    """Get overall status of LLM services"""
    try:
        # Try to get from cache first
        cache_key = "llm:status"
        cached_result = redis_cache.get(cache_key)
        if cached_result:
            return cached_result
        
        # Get fresh data and cache it
        result = llm_service.get_provider_status()
        redis_cache.set(cache_key, result, expire=300)  # Cache for 5 minutes
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get LLM status: {str(e)}")

@router.post("/switch-provider")
async def switch_provider(provider_name: str = Query(..., description="Name of the provider to switch to")) -> Dict[str, Any]:
    """Switch to a different LLM provider"""
    try:
        success = llm_service.switch_provider(provider_name)
        if success:
            # Clear related caches when provider changes
            redis_cache.delete("llm:status")
            redis_cache.delete("llm:current_provider")
            
            result = {
                "success": True,
                "message": f"Successfully switched to {provider_name} provider",
                "current_provider": llm_service.get_current_provider_info()
            }
            return result
        else:
            raise HTTPException(status_code=400, detail=f"Failed to switch to provider {provider_name}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Provider switch failed: {str(e)}")

@router.get("/current-provider")
async def get_current_provider() -> Dict[str, Any]:
    """Get information about the current LLM provider"""
    try:
        # Try to get from cache first
        cache_key = "llm:current_provider"
        cached_result = redis_cache.get(cache_key)
        if cached_result:
            return cached_result
        
        # Get fresh data and cache it
        result = llm_service.get_current_provider_info()
        redis_cache.set(cache_key, result, expire=600)  # Cache for 10 minutes
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get current provider: {str(e)}")

@router.get("/providers")
async def get_available_providers() -> Dict[str, Any]:
    """Get information about available LLM providers"""
    try:
        # Try to get from cache first
        cache_key = "llm:available_providers"
        cached_result = redis_cache.get(cache_key)
        if cached_result:
            return cached_result
        
        # Get fresh data and cache it
        result = llm_service.get_available_providers()
        redis_cache.set(cache_key, result, expire=1800)  # Cache for 30 minutes
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get providers: {str(e)}")

@router.post("/test-provider")
async def test_provider(provider_name: str = Query(..., description="Name of the provider to test")) -> Dict[str, Any]:
    """Test a specific LLM provider"""
    try:
        result = await llm_service.test_provider(provider_name)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Provider test failed: {str(e)}")

@router.get("/health")
async def llm_health_check() -> Dict[str, Any]:
    """Check the health of LLM services"""
    try:
        # Try to get from cache first
        cache_key = "llm:health"
        cached_result = redis_cache.get(cache_key)
        if cached_result:
            return cached_result
        
        current_provider = llm_service.get_current_provider_info()
        available_providers = llm_service.get_available_providers()
        
        result = {
            "status": "healthy",
            "current_provider": current_provider,
            "total_providers": available_providers.get("total_providers", 0),
            "timestamp": "2025-08-27T19:50:00Z"
        }
        
        # Cache the health check result
        redis_cache.set(cache_key, result, expire=60)  # Cache for 1 minute
        return result
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": "2025-08-27T19:50:00Z"
        }
