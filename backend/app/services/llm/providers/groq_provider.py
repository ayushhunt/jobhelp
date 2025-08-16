"""
Groq LLM provider implementation
"""
import time
from typing import Dict, Any
from groq import Groq
from .base_provider import BaseLLMProvider

class GroqProvider(BaseLLMProvider):
    """Groq LLM provider using Groq's fast inference API"""
    
    def __init__(self, api_key: str, model_name: str = None):
        """
        Initialize Groq provider
        
        Args:
            api_key: Groq API key
            model_name: Specific Groq model to use
        """
        super().__init__(api_key, model_name)
        
        # Configure Groq client
        self.client = Groq(api_key=self.api_key)
        
        self.logger.info(f"Groq provider initialized with model: {self.model_name}")
    
    def get_default_model(self) -> str:
        """Get default Groq model"""
        return "llama3-8b-8192"
    
    async def generate_response(
        self, 
        prompt: str, 
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """
        Generate response using Groq
        
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
                "provider": "groq",
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
                "provider": "groq",
                "tokens_used": 0,
                "finish_reason": "error",
                "processing_time": processing_time,
                "success": False,
                "error": str(e)
            }
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current Groq model"""
        return {
            "name": self.model_name,
            "provider": "groq",
            "type": "fast-inference",
            "capabilities": ["text-generation", "analysis", "insights"],
            "max_tokens": 8192,
            "context_window": 8192,
            "cost_per_1k_tokens": 0.00005,  # $0.05 per 1M tokens
            "speed_tier": "ultra-fast",
            "quality_tier": "excellent"
        }
    
    def get_available_models(self) -> Dict[str, Any]:
        """Get list of available Groq models"""
        return {
            "llama3-8b-8192": {
                "name": "Llama 3.1 8B",
                "description": "Fast and efficient 8B parameter model",
                "max_tokens": 8192,
                "context_window": 8192,
                "cost_per_1k_tokens": 0.00005
            },
            "llama3-70b-8192": {
                "name": "Llama 3.1 70B",
                "description": "High-quality 70B parameter model",
                "max_tokens": 8192,
                "context_window": 8192,
                "cost_per_1k_tokens": 0.0007
            },
            "mixtral-8x7b-32768": {
                "name": "Mixtral 8x7B",
                "description": "Powerful mixture-of-experts model",
                "max_tokens": 32768,
                "context_window": 32768,
                "cost_per_1k_tokens": 0.00024
            },
            "gemma2-9b-it": {
                "name": "Gemma 2 9B",
                "description": "Google's efficient Gemma model",
                "max_tokens": 8192,
                "context_window": 8192,
                "cost_per_1k_tokens": 0.00005
            }
        }
