"""
Company Research API Endpoints
Provides endpoints for company research functionality
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from fastapi.responses import StreamingResponse
import logging
from typing import Optional, Dict, Any
import json

from app.models.schemas.company_research import (
    CompanyResearchRequest, CompanyResearchResponse, ResearchProgress,
    ResearchCostEstimate
)
from app.services.company_research.company_research_orchestrator import CompanyResearchOrchestrator
from app.config.settings import settings

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize orchestrator
research_orchestrator = CompanyResearchOrchestrator()

@router.post("/research", response_model=CompanyResearchResponse)
async def research_company(request: CompanyResearchRequest):
    """
    Perform comprehensive company research
    
    This endpoint initiates research across multiple data sources including:
    - WHOIS domain analysis
    - Web search for company background
    - Google Knowledge Graph entity information
    - AI-powered analysis and insights
    """
    try:
        logger.info(f"Starting company research for: {request.company_name or request.company_domain}")
        
        # Perform research
        response = await research_orchestrator.research_company(request)
        
        logger.info(f"Company research completed for: {response.company_name}")
        return response
        
    except Exception as e:
        logger.error(f"Company research failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Research failed: {str(e)}")

@router.post("/research/async", response_model=Dict[str, str])
async def research_company_async(
    request: CompanyResearchRequest,
    background_tasks: BackgroundTasks
):
    """
    Initiate asynchronous company research
    
    Returns a request ID that can be used to track progress and retrieve results
    """
    try:
        # Generate request ID
        import uuid
        request_id = str(uuid.uuid4())
        
        # Add research task to background
        background_tasks.add_task(
            research_orchestrator.research_company,
            request
        )
        
        logger.info(f"Async research initiated with ID: {request_id}")
        
        return {
            "request_id": request_id,
            "status": "research_initiated",
            "message": "Research started in background. Use the request ID to track progress."
        }
        
    except Exception as e:
        logger.error(f"Async research initiation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to initiate research: {str(e)}")

@router.get("/research/progress/{request_id}", response_model=ResearchProgress)
async def get_research_progress(request_id: str):
    """
    Get research progress for a specific request
    
    Use this endpoint to track the progress of ongoing research
    """
    try:
        progress = await research_orchestrator.get_research_progress(request_id)
        
        if not progress:
            raise HTTPException(status_code=404, detail="Research request not found")
        
        return progress
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get research progress: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get progress: {str(e)}")

@router.delete("/research/cancel/{request_id}")
async def cancel_research(request_id: str):
    """
    Cancel ongoing research request
    
    This will stop the research process and clean up resources
    """
    try:
        success = await research_orchestrator.cancel_research(request_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Research request not found")
        
        return {"message": "Research cancelled successfully", "request_id": request_id}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to cancel research: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to cancel research: {str(e)}")

@router.get("/research/cost-estimate")
async def get_cost_estimate(research_depth: str = "standard"):
    """
    Get cost estimate for company research
    
    Provides cost breakdown and optimization tips for different research depths
    """
    try:
        cost_estimate = research_orchestrator.get_cost_estimate(research_depth)
        return cost_estimate
        
    except Exception as e:
        logger.error(f"Failed to get cost estimate: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get cost estimate: {str(e)}")

@router.get("/research/health")
async def get_service_health():
    """
    Get health status of all research services
    
    Useful for monitoring service availability and troubleshooting
    """
    try:
        health_status = research_orchestrator.get_service_health()
        return {
            "overall_status": "healthy" if all(
                service["is_healthy"] for service in health_status.values()
            ) else "degraded",
            "services": health_status,
            "active_sessions": research_orchestrator.get_active_sessions_count()
        }
        
    except Exception as e:
        logger.error(f"Failed to get service health: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get health status: {str(e)}")

@router.post("/research/test-services")
async def test_all_services():
    """
    Test all research services
    
    Performs connection tests to verify all services are working properly
    """
    try:
        test_results = await research_orchestrator.test_all_services()
        
        overall_status = "healthy" if all(test_results.values()) else "degraded"
        
        return {
            "overall_status": overall_status,
            "test_results": test_results,
            "timestamp": "2024-01-01T00:00:00Z"
        }
        
    except Exception as e:
        logger.error(f"Service testing failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Service testing failed: {str(e)}")

@router.get("/research/sources")
async def get_research_sources():
    """
    Get information about available research sources
    
    Provides details about each data source including costs and capabilities
    """
    try:
        source_info = research_orchestrator.get_research_source_info()
        return {
            "available_sources": source_info,
            "total_sources": len(source_info),
            "research_depths": research_orchestrator.get_available_research_depths()
        }
        
    except Exception as e:
        logger.error(f"Failed to get research sources: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get source info: {str(e)}")

@router.get("/research/stream/{request_id}")
async def stream_research_progress(request_id: str):
    """
    Stream research progress updates in real-time
    
    Returns Server-Sent Events stream for live progress updates
    """
    async def generate_progress_stream():
        """Generate SSE stream for research progress"""
        try:
            while True:
                progress = await research_orchestrator.get_research_progress(request_id)
                
                if not progress:
                    yield f"data: {json.dumps({'error': 'Request not found'})}\n\n"
                    break
                
                if progress.status in ["completed", "failed"]:
                    yield f"data: {json.dumps(progress.dict())}\n\n"
                    break
                
                # Send progress update
                yield f"data: {json.dumps(progress.dict())}\n\n"
                
                # Wait before next update
                await asyncio.sleep(2)
                
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return StreamingResponse(
        generate_progress_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*"
        }
    )

@router.get("/research/quick-check")
async def quick_company_check(
    company_name: Optional[str] = None,
    company_domain: Optional[str] = None
):
    """
    Quick company verification check
    
    Performs basic domain and web presence verification for quick company validation
    """
    if not company_name and not company_domain:
        raise HTTPException(status_code=400, detail="Either company_name or company_domain must be provided")
    
    try:
        # Create basic request for quick check
        request = CompanyResearchRequest(
            company_name=company_name,
            company_domain=company_domain,
            research_depth="basic",
            user_id="quick_check",
            is_premium=False
        )
        
        # Perform basic research
        response = await research_orchestrator.research_company(request)
        
        # Extract key verification info
        verification_info = {
            "company_name": response.company_name,
            "company_domain": response.company_domain,
            "domain_verified": response.whois_data is not None,
            "web_presence": response.web_search_results is not None and len(response.web_search_results) > 0,
            "basic_authenticity": "verified" if response.whois_data else "unknown",
            "research_status": response.research_status.value,
            "processing_time": response.total_processing_time
        }
        
        return verification_info
        
    except Exception as e:
        logger.error(f"Quick company check failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Quick check failed: {str(e)}")

# Import asyncio for the streaming endpoint
import asyncio

