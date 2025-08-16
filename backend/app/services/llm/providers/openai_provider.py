"""
OpenAI LLM provider implementation
"""
import time
from typing import Dict, Any
from openai import OpenAI
from .base_provider import BaseLLMProvider

class OpenAIProvider(BaseLLMProvider):
    """OpenAI LLM provider using OpenAI's API"""
    
    def __init__(self, api_key: str, model_name: str = None):
        """
        Initialize OpenAI provider
        
        Args:
            api_key: OpenAI API key
            model_name: Specific OpenAI model to use
        """
        super().__init__(api_key, model_name)
        
        # Configure OpenAI client
        self.client = OpenAI(api_key=self.api_key)
        
        self.logger.info(f"OpenAI provider initialized with model: {self.model_name}")
    
    def get_default_model(self) -> str:
        """Get default OpenAI model"""
        return "gpt-3.5-turbo"
    
    async def generate_response(
        self, 
        prompt: str, 
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """
        Generate response using OpenAI
        
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
            
            # Generate response
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
                "provider": "openai",
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
                "provider": "openai",
                "tokens_used": 0,
                "finish_reason": "error",
                "processing_time": processing_time,
                "success": False,
                "error": str(e)
            }
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current OpenAI model"""
        return {
            "name": self.model_name,
            "provider": "openai",
            "type": "generative",
            "capabilities": ["text-generation", "analysis", "insights"],
            "max_tokens": 4096,
            "context_window": 4096,
            "cost_per_1k_tokens": 0.002,
            "speed_tier": "fast",
            "quality_tier": "excellent"
        }
    
    def get_available_models(self) -> Dict[str, Any]:
        """Get list of available OpenAI models"""
        return {
            "gpt-4": {
                "name": "GPT-4",
                "description": "Most capable GPT model",
                "max_tokens": 8192,
                "context_window": 8192,
                "cost_per_1k_tokens": 0.03
            },
            "gpt-4-turbo": {
                "name": "GPT-4 Turbo",
                "description": "Latest GPT-4 model with improved performance",
                "max_tokens": 4096,
                "context_window": 4096,
                "cost_per_1k_tokens": 0.01
            },
            "gpt-3.5-turbo": {
                "name": "GPT-3.5 Turbo",
                "description": "Fast and efficient model for most tasks",
                "max_tokens": 4096,
                "context_window": 4096,
                "cost_per_1k_tokens": 0.002
            },
            "gpt-3.5-turbo-16k": {
                "name": "GPT-3.5 Turbo 16K",
                "description": "GPT-3.5 with extended context",
                "max_tokens": 16384,
                "context_window": 16384,
                "cost_per_1k_tokens": 0.004
            }
        }
