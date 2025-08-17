"""
Parallel AI LLM provider implementation using OpenAI SDK compatibility
"""
import time
from typing import Dict, Any
from openai import OpenAI
from .base_provider import BaseLLMProvider

class ParallelProvider(BaseLLMProvider):
    """Parallel AI LLM provider using OpenAI SDK compatibility"""
    
    def __init__(self, api_key: str, model_name: str = None):
        """
        Initialize Parallel AI provider
        
        Args:
            api_key: Parallel AI API key
            model_name: Specific Parallel AI model to use
        """
        super().__init__(api_key, model_name)
        
        # Configure Parallel AI client using OpenAI SDK compatibility
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.parallel.ai"  # Parallel's API beta endpoint
        )
        
        self.logger.info(f"Parallel AI provider initialized with model: {self.model_name}")
    
    def get_default_model(self) -> str:
        """Get default Parallel AI model"""
        return "speed"  # Parallel's optimized model for low latency
    
    async def generate_response(
        self, 
        prompt: str, 
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """
        Generate response using Parallel AI
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            temperature: Creativity level (0.0 to 1.0)
            
        Returns:
            Response dictionary with content and metadata
        """
        start_time = time.time()
        
        try:
            # Log the request
            self.log_request(prompt, max_tokens, temperature)
            
            # Generate response using Parallel AI's "speed" model
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are an expert HR analyst and career coach."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=0.8,
                stream=False
            )
            
            processing_time = time.time() - start_time
            
            # Extract response content
            content = response.choices[0].message.content if response.choices else "No response generated"
            
            # Create response object
            result = {
                "content": content,
                "model": self.model_name,
                "provider": "parallel",
                "tokens_used": response.usage.total_tokens if response.usage else 'N/A',
                "finish_reason": response.choices[0].finish_reason if response.choices else 'unknown',
                "processing_time": processing_time,
                "success": True
            }
            
            # Log the response
            self.log_response(result, processing_time)
            
            return result
            
        except Exception as e:
            processing_time = time.time() - start_time
            self.log_error(e, f"Response generation failed after {processing_time:.3f}s")
            
            return {
                "content": f"Error generating response: {str(e)}",
                "model": self.model_name,
                "provider": "parallel",
                "tokens_used": 0,
                "finish_reason": "error",
                "processing_time": processing_time,
                "success": False,
                "error": str(e)
            }
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current Parallel AI model"""
        return {
            "name": self.model_name,
            "provider": "parallel",
            "type": "generative",
            "capabilities": ["text-generation", "analysis", "insights", "web-research"],
            "max_tokens": 4096,
            "context_window": 4096,
            "cost_per_1k_tokens": "Contact Parallel AI for pricing",
            "speed_tier": "ultra-fast",  # Parallel AI is optimized for low latency
            "quality_tier": "excellent",
            "special_features": ["web-research", "low-latency", "streaming-support"]
        }
    
    def get_available_models(self) -> Dict[str, Any]:
        """Get list of available Parallel AI models"""
        return {
            "speed": {
                "name": "Speed",
                "description": "Parallel AI's optimized model for low latency responses",
                "max_tokens": 4096,
                "context_window": 4096,
                "special_features": [
                    "3 second p50 TTFT (median time to first token)",
                    "Web research capabilities",
                    "OpenAI SDK compatibility",
                    "Streaming support"
                ],
                "use_cases": ["Chat interfaces", "Interactive tools", "Real-time applications"]
            }
        }
    
    def get_provider_features(self) -> Dict[str, Any]:
        """Get Parallel AI specific features and capabilities"""
        return {
            "web_research": True,
            "low_latency": True,
            "streaming": True,
            "openai_compatibility": True,
            "rate_limit": "300 requests per minute (default)",
            "beta_status": True,
            "documentation": "https://docs.parallel.ai/chat-api/chat-quickstart"
        }
