"""
Mock LLM provider for testing and development
"""
import time
import logging
from typing import Dict, Any
from .base_provider import BaseLLMProvider
import asyncio

logger = logging.getLogger(__name__)

class MockProvider(BaseLLMProvider):
    """Mock LLM provider for testing and development"""
    
    def __init__(self, api_key: str = None, model_name: str = None):
        """
        Initialize Mock provider
        
        Args:
            api_key: Not used for mock provider
            model_name: Mock model name
        """
        super().__init__("mock_key", model_name)
        self.provider_name = "mock"
        logger.info("Mock LLM provider initialized for testing")
    
    def get_default_model(self) -> str:
        """Get default mock model name"""
        return "mock-model-v1"
    
    async def generate_response(
        self, 
        prompt: str, 
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """
        Generate mock response
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            temperature: Creativity level (0.0 to 1.0)
            
        Returns:
            Mock response dictionary
        """
        start_time = time.time()
        
        try:
            # Log the request
            self.log_request(prompt, max_tokens, temperature)
            
            # Simulate processing time
            await asyncio.sleep(0.5)
            
            # Generate mock insights based on the prompt
            if "resume" in prompt.lower() and "job description" in prompt.lower():
                mock_content = """
                {
                    "match_score": 75,
                    "alignment_strength": "moderate",
                    "top_matched_skills": ["python", "git", "agile"],
                    "critical_missing_skills": ["docker", "kubernetes"],
                    "experience_assessment": "Good technical foundation with room for growth",
                    "improvement_priority": "medium",
                    "quick_wins": ["Add cloud experience", "Include metrics in achievements"],
                    "ats_optimization_tip": "Use industry-standard keywords and quantify achievements",
                    "role_fit_reason": "Strong technical skills align well with the role requirements"
                }
                """
            else:
                mock_content = "This is a mock response for testing purposes. Please configure a real LLM provider for production use."
            
            processing_time = time.time() - start_time
            
            # Create response object
            result = {
                "content": mock_content,
                "model": self.model_name,
                "provider": "mock",
                "tokens_used": len(mock_content.split()),
                "finish_reason": "stop",
                "processing_time": processing_time,
                "success": True,
                "note": "This is a mock response - configure real API keys for production"
            }
            
            # Log the response
            self.log_response(result, processing_time)
            
            return result
            
        except Exception as e:
            processing_time = time.time() - start_time
            self.log_error(e, f"Mock response generation failed after {processing_time:.3f}s")
            
            return {
                "content": f"Mock error: {str(e)}",
                "model": self.model_name,
                "provider": "mock",
                "tokens_used": 0,
                "finish_reason": "error",
                "processing_time": processing_time,
                "success": False,
                "error": str(e)
            }
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the mock model"""
        return {
            "name": self.model_name,
            "provider": "mock",
            "type": "mock",
            "capabilities": ["text-generation", "analysis", "insights"],
            "max_tokens": 1000,
            "context_window": 1000,
            "cost_per_1k_tokens": 0.0,
            "speed_tier": "instant",
            "quality_tier": "mock",
            "note": "This is a mock model for testing - not suitable for production"
        }
    
    def get_available_models(self) -> Dict[str, Any]:
        """Get list of available mock models"""
        return {
            "mock-model-v1": {
                "name": "Mock Model v1",
                "description": "Mock model for testing and development",
                "max_tokens": 1000,
                "context_window": 1000,
                "cost_per_1k_tokens": 0.0,
                "note": "Not suitable for production use"
            }
        }
