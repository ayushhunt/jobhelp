"""
LLM provider management endpoints
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any
from app.services.llm.llm_service import LLMService

router = APIRouter()
llm_service = LLMService()

@router.get("/status")
async def get_llm_status() -> Dict[str, Any]:
    """Get overall status of LLM services"""
    try:
        return llm_service.get_provider_status()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get LLM status: {str(e)}")

@router.post("/switch-provider")
async def switch_provider(provider_name: str = Query(..., description="Name of the provider to switch to")) -> Dict[str, Any]:
    """Switch to a different LLM provider"""
    try:
        success = llm_service.switch_provider(provider_name)
        if success:
            return {
                "success": True,
                "message": f"Successfully switched to {provider_name} provider",
                "current_provider": llm_service.get_current_provider_info()
            }
        else:
            raise HTTPException(status_code=400, detail=f"Failed to switch to provider {provider_name}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Provider switch failed: {str(e)}")

@router.get("/current-provider")
async def get_current_provider() -> Dict[str, Any]:
    """Get information about the current LLM provider"""
    try:
        return llm_service.get_current_provider_info()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get current provider: {str(e)}")

@router.get("/providers")
async def get_available_providers() -> Dict[str, Any]:
    """Get information about available LLM providers"""
    try:
        return llm_service.get_available_providers()
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
        current_provider = llm_service.get_current_provider_info()
        available_providers = llm_service.get_available_providers()
        
        return {
            "status": "healthy",
            "current_provider": current_provider,
            "total_providers": available_providers.get("total_providers", 0),
            "timestamp": "2024-01-01T00:00:00Z"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": "2024-01-01T00:00:00Z"
        }
