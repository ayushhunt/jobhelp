"""
LLM Service - Business Logic Layer
Handles AI insights generation and usage tracking
"""
import logging
import time
from typing import Dict, Any, Optional
from datetime import date
from app.core.exceptions.exceptions import LLMServiceError, InsufficientCredits
from app.config.settings import settings
from .llm_orchestrator import LLMOrchestrator

logger = logging.getLogger(__name__)

class LLMService:
    """Service for managing LLM interactions and usage tracking"""
    
    def __init__(self):
        """Initialize LLM service"""
        self.usage_tracker = {}
        self.free_tier_daily_limit = settings.FREE_TIER_DAILY_LIMIT
        self.premium_tier_daily_limit = settings.PREMIUM_TIER_DAILY_LIMIT
        
        # Initialize orchestrator
        self.orchestrator = LLMOrchestrator()
        
        logger.info("LLM service initialized with orchestrator")
    
    async def can_use_ai(self, user_id: str, is_premium: bool = False) -> bool:
        """Check if user can use AI features"""
        try:
            daily_limit = self.premium_tier_daily_limit if is_premium else self.free_tier_daily_limit
            today = f"{user_id}_{date.today()}"
            
            current_usage = self.usage_tracker.get(today, 0)
            can_use = current_usage < daily_limit
            
            logger.info(f"AI usage check for user {user_id}: {current_usage}/{daily_limit} - Can use: {can_use}")
            return can_use
            
        except Exception as e:
            logger.error(f"AI usage check failed for user {user_id}: {str(e)}")
            return False
    
    async def generate_insights(
        self,
        resume_content: str,
        job_description_content: str,
        user_id: str,
        provider_name: str = None
    ) -> Dict[str, Any]:
        """Generate AI-powered insights"""
        start_time = time.time()
        
        try:
            # Check if user can use AI
            if not await self.can_use_ai(user_id):
                raise InsufficientCredits("Daily AI usage limit reached")
            
            # Get or auto-select LLM provider
            provider = self._get_or_select_provider(provider_name)
            
            logger.info(f"Generating AI insights for user {user_id} using {provider.provider_name} provider ({provider.model_name})")
            
            # Create the prompt for analysis
            prompt = self._create_analysis_prompt(resume_content, job_description_content)
            
            # Generate insights using LLM
            llm_response = await provider.generate_response(
                prompt=prompt,
                max_tokens=1500,
                temperature=0.7
            )
            
            # Increment usage counter
            self._increment_usage(user_id)
            
            # Process and format the response
            insights = self._process_llm_response(llm_response)
            
            total_time = time.time() - start_time
            
            logger.info(
                f"AI insights generated successfully for user {user_id} "
                f"using {provider.provider_name} ({provider.model_name}) "
                f"in {total_time:.3f}s"
            )
            
            return insights
            
        except Exception as e:
            total_time = time.time() - start_time
            logger.error(
                f"AI insights generation failed for user {user_id} "
                f"after {total_time:.3f}s: {str(e)}"
            )
            raise LLMServiceError(f"Failed to generate AI insights: {str(e)}")
    
    def _get_or_select_provider(self, provider_name: str = None):
        """Get a provider, auto-selecting if none is available"""
        # Try to get the specified provider
        provider = self.orchestrator.get_provider(provider_name)
        if provider:
            return provider
        
        # Try to get current provider
        current_provider = self.orchestrator.get_current_provider()
        if current_provider:
            return current_provider
        
        # Auto-select a provider
        if self.orchestrator.auto_select_provider():
            provider = self.orchestrator.get_current_provider()
            if provider:
                return provider
        
        # If still no provider, raise error
        available_providers = self.orchestrator.get_available_providers()
        available_names = list(available_providers.get('available_providers', {}).keys())
        
        raise LLMServiceError(
            f"No LLM provider available or selected. "
            f"Available providers: {available_names}. "
            f"Use switch_provider() to select one or configure API keys."
        )
    
    def _create_analysis_prompt(self, resume_content: str, job_description_content: str) -> str:
        """Create a structured prompt for resume analysis"""
        prompt = f"""
        You are an expert HR analyst and career coach. Analyze the following resume against the job description and provide insights.

        RESUME:
        {resume_content[:2000]}...

        JOB DESCRIPTION:
        {job_description_content[:2000]}...

        Please provide a comprehensive analysis in the following JSON format:
        {{
            "match_score": <0-100 score>,
            "alignment_strength": "<weak/moderate/strong>",
            "top_matched_skills": ["skill1", "skill2", "skill3"],
            "critical_missing_skills": ["skill1", "skill2"],
            "experience_assessment": "<brief assessment>",
            "improvement_priority": "<high/medium/low>",
            "quick_wins": ["improvement1", "improvement2"],
            "ats_optimization_tip": "<tip for ATS optimization>",
            "role_fit_reason": "<why they fit or don't fit>"
        }}

        Focus on actionable insights and specific recommendations.
        """
        return prompt
    
    def _process_llm_response(self, llm_response: Dict[str, Any]) -> Dict[str, Any]:
        """Process and format the LLM response"""
        try:
            if not llm_response.get('success'):
                logger.warning(f"LLM response indicates failure: {llm_response.get('error', 'Unknown error')}")
                return {
                    "ai_insights": {
                        "error": "Failed to generate insights",
                        "fallback_message": "Analysis completed with basic analytics only"
                    },
                    "ai_enabled": False
                }
            
            # Extract content
            content = llm_response.get('content', '')
            
            insights = {
                "ai_insights": {
                    "raw_response": content,
                    "model_used": llm_response.get('model', 'Unknown'),
                    "provider": llm_response.get('provider', 'Unknown'),
                    "tokens_used": llm_response.get('tokens_used', 'N/A'),
                    "processing_time": llm_response.get('processing_time', 0),
                    "success": True
                },
                "ai_enabled": True
            }
            
            return insights
            
        except Exception as e:
            logger.error(f"Failed to process LLM response: {str(e)}")
            return {
                "ai_insights": {
                    "error": f"Response processing failed: {str(e)}",
                    "fallback_message": "Analysis completed with basic analytics only"
                },
                "ai_enabled": False
            }
    
    # Provider management methods (delegated to orchestrator)
    def switch_provider(self, provider_name: str) -> bool:
        """Switch to a different LLM provider"""
        return self.orchestrator.switch_provider(provider_name)
    
    def get_provider_status(self) -> Dict[str, Any]:
        """Get overall status of all providers"""
        return self.orchestrator.get_provider_status()
    
    def get_available_providers(self) -> Dict[str, Any]:
        """Get information about available AI models and providers"""
        return self.orchestrator.get_available_providers()
    
    def get_current_provider_info(self) -> Dict[str, Any]:
        """Get information about the current LLM provider"""
        return self.orchestrator.get_current_provider_info()
    
    async def test_provider(self, provider_name: str) -> Dict[str, Any]:
        """Test a specific LLM provider"""
        return await self.orchestrator.test_provider(provider_name)
    
    # Usage tracking methods
    def get_usage_stats(self, user_id: str) -> Dict[str, Any]:
        """Get usage statistics for a user"""
        try:
            today = f"{user_id}_{date.today()}"
            current_usage = self.usage_tracker.get(today, 0)
            daily_limit = self.free_tier_daily_limit
            
            return {
                "user_id": user_id,
                "daily_usage": current_usage,
                "daily_limit": daily_limit,
                "remaining": max(0, daily_limit - current_usage),
                "can_use_ai": current_usage < daily_limit
            }
            
        except Exception as e:
            logger.error(f"Usage stats retrieval failed for user {user_id}: {str(e)}")
            return {}
    
    def _increment_usage(self, user_id: str) -> None:
        """Increment usage counter for a user"""
        try:
            today = f"{user_id}_{date.today()}"
            self.usage_tracker[today] = self.usage_tracker.get(today, 0) + 1
            
            logger.debug(f"Usage incremented for user {user_id}: {self.usage_tracker[today]}")
            
        except Exception as e:
            logger.error(f"Usage increment failed for user {user_id}: {str(e)}")
    
    def reset_usage_tracking(self) -> None:
        """Reset usage tracking (useful for testing or daily resets)"""
        try:
            self.usage_tracker.clear()
            logger.info("Usage tracking reset")
            
        except Exception as e:
            logger.error(f"Usage tracking reset failed: {str(e)}")
