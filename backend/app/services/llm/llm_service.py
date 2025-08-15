"""
LLM service for handling AI model interactions
"""
import logging
from typing import Dict, Any, Optional
from datetime import datetime, date
from app.core.exceptions.exceptions import LLMServiceError, InsufficientCredits
from app.config.settings import settings

logger = logging.getLogger(__name__)

class LLMService:
    """Service for managing LLM interactions and usage tracking"""
    
    def __init__(self):
        """Initialize LLM service"""
        self.usage_tracker = {}
        self.free_tier_daily_limit = settings.FREE_TIER_DAILY_LIMIT
        self.premium_tier_daily_limit = settings.PREMIUM_TIER_DAILY_LIMIT
        
        logger.info("LLM service initialized")
    
    async def can_use_ai(self, user_id: str, is_premium: bool = False) -> bool:
        """
        Check if user can use AI features
        
        Args:
            user_id: User identifier
            is_premium: Whether user has premium access
            
        Returns:
            True if user can use AI, False otherwise
        """
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
        user_id: str
    ) -> Dict[str, Any]:
        """
        Generate AI-powered insights
        
        Args:
            resume_content: Resume text content
            job_description_content: Job description text content
            user_id: User identifier
            
        Returns:
            AI-generated insights
        """
        try:
            # Increment usage counter
            self._increment_usage(user_id)
            
            # Generate insights using LLM
            insights = await self._call_llm_for_insights(resume_content, job_description_content)
            
            logger.info(f"AI insights generated for user {user_id}")
            return insights
            
        except Exception as e:
            logger.error(f"AI insights generation failed for user {user_id}: {str(e)}")
            raise LLMServiceError(f"Failed to generate AI insights: {str(e)}")
    
    def get_usage_stats(self, user_id: str) -> Dict[str, Any]:
        """
        Get usage statistics for a user
        
        Args:
            user_id: User identifier
            
        Returns:
            Usage statistics
        """
        try:
            today = f"{user_id}_{date.today()}"
            current_usage = self.usage_tracker.get(today, 0)
            
            return {
                "user_id": user_id,
                "daily_usage": current_usage,
                "daily_limit": self.free_tier_daily_limit,
                "remaining": max(0, self.free_tier_daily_limit - current_usage),
                "can_use_ai": current_usage < self.free_tier_daily_limit
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
    
    async def _call_llm_for_insights(
        self,
        resume_content: str,
        job_description_content: str
    ) -> Dict[str, Any]:
        """
        Call LLM to generate insights
        
        Args:
            resume_content: Resume text content
            job_description_content: Job description text content
            
        Returns:
            LLM-generated insights
        """
        try:
            # This is a placeholder for actual LLM integration
            # In production, you would integrate with your LLM provider here
            
            # For now, return mock insights
            insights = {
                "strength_analysis": "Resume shows strong technical skills and relevant experience",
                "improvement_suggestions": [
                    "Add more quantifiable achievements",
                    "Include specific project examples",
                    "Highlight leadership experience"
                ],
                "skill_gap_analysis": "Consider adding cloud computing experience",
                "overall_assessment": "Strong candidate with room for improvement in specific areas"
            }
            
            return insights
            
        except Exception as e:
            logger.error(f"LLM call failed: {str(e)}")
            raise LLMServiceError(f"LLM integration failed: {str(e)}")
    
    def reset_usage_tracking(self) -> None:
        """Reset usage tracking (useful for testing or daily resets)"""
        try:
            self.usage_tracker.clear()
            logger.info("Usage tracking reset")
            
        except Exception as e:
            logger.error(f"Usage tracking reset failed: {str(e)}")
    
    def get_available_models(self) -> Dict[str, Any]:
        """Get information about available AI models"""
        try:
            # This is a placeholder - implement based on your model registry
            models = {
                "gpt-4": {
                    "name": "GPT-4",
                    "provider": "OpenAI",
                    "cost_per_1k_tokens": 0.03,
                    "max_tokens": 8192,
                    "context_window": 8192,
                    "speed_tier": "medium",
                    "quality_tier": "excellent"
                },
                "gpt-3.5-turbo": {
                    "name": "GPT-3.5 Turbo",
                    "provider": "OpenAI",
                    "cost_per_1k_tokens": 0.002,
                    "max_tokens": 4096,
                    "context_window": 4096,
                    "speed_tier": "fast",
                    "quality_tier": "good"
                }
            }
            
            return {
                "available_models": models,
                "total_available": len(models),
                "recommended": {
                    "free_tier": "gpt-3.5-turbo",
                    "premium_tier": "gpt-4"
                }
            }
            
        except Exception as e:
            logger.error(f"Model information retrieval failed: {str(e)}")
            return {}
