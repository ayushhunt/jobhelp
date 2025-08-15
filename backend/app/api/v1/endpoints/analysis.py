"""
API endpoints for document analysis
"""
import logging
from typing import Optional
from fastapi import APIRouter, UploadFile, File, Form, Query, HTTPException, Depends
from app.services.analytics.analytics_service import AnalyticsService
from app.utils.file_handling.document_processor import DocumentProcessor
from app.models.schemas.analysis import (
    AnalysisRequest, AnalysisResponse, AnalysisType,
    AIUsageResponse, AvailableModelsResponse, CostComparisonResponse
)
from app.core.exceptions.exceptions import create_http_exception, JobHelpException
from app.core.logging.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()
analytics_service = AnalyticsService()
document_processor = DocumentProcessor()

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_documents(
    resume_file: Optional[UploadFile] = File(None),
    job_description_file: Optional[UploadFile] = File(None),
    resume_text: Optional[str] = Form(None),
    job_description_text: Optional[str] = Form(None),
    use_ai: bool = Query(False, description="Enable AI-powered insights"),
    user_id: str = Query("default", description="User identifier for usage tracking"),
    is_premium: bool = Query(False, description="Whether user has premium access"),
    analysis_type: AnalysisType = Query(AnalysisType.BASIC, description="Type of analysis to perform")
):
    """
    Analyze resume and job description with comprehensive analytics
    
    This endpoint supports both file uploads and direct text input.
    Choose the analysis type based on your needs:
    - BASIC: Simple keyword matching and similarity
    - ADVANCED: Enhanced text analysis with skills extraction
    - AI_ENHANCED: AI-powered insights and recommendations
    """
    try:
        logger.info(f"Analysis request received for user {user_id}, type: {analysis_type}")
        
        # Extract resume content
        resume_content = await _extract_content(
            resume_file, resume_text, "resume", user_id
        )
        
        # Extract job description content
        jd_content = await _extract_content(
            job_description_file, job_description_text, "job description", user_id
        )
        
        # Determine analysis type based on use_ai flag for backward compatibility
        if use_ai and analysis_type == AnalysisType.BASIC:
            analysis_type = AnalysisType.AI_ENHANCED
        
        # Perform analysis
        analysis_result = await analytics_service.analyze_documents(
            resume_content=resume_content,
            job_description_content=jd_content,
            analysis_type=analysis_type,
            user_id=user_id,
            is_premium=is_premium
        )
        
        logger.info(f"Analysis completed successfully for user {user_id}")
        return analysis_result
        
    except JobHelpException as e:
        logger.error(f"Analysis failed for user {user_id}: {e.message}")
        raise create_http_exception(e)
    except Exception as e:
        logger.error(f"Unexpected error in analysis for user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/ai-usage", response_model=AIUsageResponse)
async def get_ai_usage(user_id: str = Query("default", description="User identifier")):
    """Get AI usage statistics for a user"""
    try:
        logger.info(f"AI usage request for user {user_id}")
        
        usage_stats = analytics_service.llm_service.get_usage_stats(user_id)
        
        logger.info(f"AI usage stats retrieved for user {user_id}")
        return usage_stats
        
    except Exception as e:
        logger.error(f"AI usage retrieval failed for user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/ai-models", response_model=AvailableModelsResponse)
async def get_available_models():
    """Get information about available AI models"""
    try:
        logger.info("AI models information request")
        
        models_info = analytics_service.llm_service.get_available_models()
        
        logger.info("AI models information retrieved successfully")
        return models_info
        
    except Exception as e:
        logger.error(f"AI models information retrieval failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/ai-costs", response_model=CostComparisonResponse)
async def get_cost_comparison():
    """Get cost comparison between different models"""
    try:
        logger.info("AI cost comparison request")
        
        # This is a placeholder - implement based on your model registry
        cost_comparison = {
            "gpt-4": {
                "provider": "OpenAI",
                "cost_per_1k_tokens": "$0.0300",
                "sample_costs": {
                    "100_tokens": "$0.0030",
                    "500_tokens": "$0.0150",
                    "1000_tokens": "$0.0300",
                    "5000_tokens": "$0.1500"
                },
                "quality_tier": "excellent",
                "speed_tier": "medium"
            },
            "gpt-3.5-turbo": {
                "provider": "OpenAI",
                "cost_per_1k_tokens": "$0.0020",
                "sample_costs": {
                    "100_tokens": "$0.0002",
                    "500_tokens": "$0.0010",
                    "1000_tokens": "$0.0020",
                    "5000_tokens": "$0.0100"
                },
                "quality_tier": "good",
                "speed_tier": "fast"
            }
        }
        
        result = {
            "cost_comparison": cost_comparison,
            "note": "Costs shown are estimates. Actual costs may vary based on usage patterns."
        }
        
        logger.info("AI cost comparison retrieved successfully")
        return result
        
    except Exception as e:
        logger.error(f"AI cost comparison retrieval failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def _extract_content(
    file: Optional[UploadFile],
    text: Optional[str],
    content_type: str,
    user_id: str
) -> str:
    """
    Extract content from either file upload or direct text input
    
    Args:
        file: Uploaded file
        text: Direct text input
        content_type: Type of content (for logging)
        user_id: User identifier
        
    Returns:
        Extracted text content
        
    Raises:
        HTTPException: If content extraction fails
    """
    try:
        if file:
            # Process uploaded file
            logger.info(f"Processing {content_type} file: {file.filename} for user {user_id}")
            
            # Validate file size
            file_bytes = await file.read()
            if not document_processor.validate_file_size(file_bytes):
                raise HTTPException(
                    status_code=400,
                    detail=f"{content_type.title()} file size exceeds limit"
                )
            
            # Extract text from file
            content = document_processor.extract_text(file_bytes, file.filename)
            
            if not content.strip():
                raise HTTPException(
                    status_code=400,
                    detail=f"No readable text found in {content_type} file"
                )
            
            logger.info(f"Successfully extracted {len(content)} characters from {content_type} file")
            return content
            
        elif text:
            # Use direct text input
            if not text.strip():
                raise HTTPException(
                    status_code=400,
                    detail=f"{content_type.title()} text cannot be empty"
                )
            
            logger.info(f"Using direct {content_type} text input for user {user_id}")
            return text.strip()
            
        else:
            # Neither file nor text provided
            raise HTTPException(
                status_code=400,
                detail=f"Either {content_type} file or text must be provided"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Content extraction failed for {content_type}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process {content_type}: {str(e)}"
        )
