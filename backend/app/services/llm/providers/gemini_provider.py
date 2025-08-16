"""
Gemini LLM provider implementation
"""
import time
import google.generativeai as genai
from typing import Dict, Any
from .base_provider import BaseLLMProvider

class GeminiProvider(BaseLLMProvider):
    """Gemini LLM provider using Google's Generative AI"""
    
    def __init__(self, api_key: str, model_name: str = None):
        """
        Initialize Gemini provider
        
        Args:
            api_key: Google AI API key
            model_name: Specific Gemini model to use
        """
        super().__init__(api_key, model_name)
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        
        # Initialize the model
        try:
            self.model = genai.GenerativeModel(self.model_name)
            self.logger.info(f"Gemini model {self.model_name} initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize Gemini model {self.model_name}: {str(e)}")
            raise
    
    def get_default_model(self) -> str:
        """Get default Gemini model"""
        return "gemini-1.5-flash"
    
    async def generate_response(
        self, 
        prompt: str, 
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """
        Generate response using Gemini
        
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
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=max_tokens,
                    temperature=temperature,
                    top_p=0.8,
                    top_k=40
                )
            )
            
            processing_time = time.time() - start_time
            
            # Extract response content
            content = response.text if response.text else "No response generated"
            
            # Create response object
            result = {
                "content": content,
                "model": self.model_name,
                "provider": "gemini",
                "tokens_used": getattr(response, 'usage_metadata', {}).get('total_token_count', 'N/A'),
                "finish_reason": getattr(response, 'candidates', [{}])[0].get('finish_reason', 'unknown'),
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
                "provider": "gemini",
                "tokens_used": 0,
                "finish_reason": "error",
                "processing_time": processing_time,
                "success": False,
                "error": str(e)
            }
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current Gemini model"""
        return {
            "name": self.model_name,
            "provider": "gemini",
            "type": "generative",
            "capabilities": ["text-generation", "analysis", "insights"],
            "max_tokens": 8192,  # Gemini 1.5 Flash limit
            "context_window": 1000000,  # 1M tokens
            "cost_per_1k_tokens": 0.000075,  # $0.075 per 1M tokens
            "speed_tier": "fast",
            "quality_tier": "excellent"
        }
    
    def get_available_models(self) -> Dict[str, Any]:
        """Get list of available Gemini models"""
        return {
            "gemini-1.5-flash": {
                "name": "Gemini 1.5 Flash",
                "description": "Fast and efficient model for most tasks",
                "max_tokens": 8192,
                "context_window": 1000000,
                "cost_per_1k_tokens": 0.000075
            },
            "gemini-1.5-pro": {
                "name": "Gemini 1.5 Pro",
                "description": "Most capable model for complex tasks",
                "max_tokens": 8192,
                "context_window": 1000000,
                "cost_per_1k_tokens": 0.00375
            },
            "gemini-1.0-pro": {
                "name": "Gemini 1.0 Pro",
                "description": "Previous generation pro model",
                "max_tokens": 30720,
                "context_window": 30720,
                "cost_per_1k_tokens": 0.0005
            }
        }
