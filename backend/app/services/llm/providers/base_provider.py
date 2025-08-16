"""
Base abstract class for LLM providers
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import logging

class BaseLLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    def __init__(self, api_key: str, model_name: str = None):
        """
        Initialize the LLM provider
        
        Args:
            api_key: API key for the provider
            model_name: Specific model to use
        """
        self.api_key = api_key
        self.model_name = model_name or self.get_default_model()
        self.provider_name = self.__class__.__name__.replace('Provider', '').lower()
        self.logger = logging.getLogger(__name__)
        
        self.logger.info(f"Initialized {self.provider_name} provider with model: {self.model_name}")
    
    @abstractmethod
    def get_default_model(self) -> str:
        """Get the default model name for this provider"""
        pass
    
    @abstractmethod
    async def generate_response(
        self, 
        prompt: str, 
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """
        Generate a response from the LLM
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            temperature: Creativity level (0.0 to 1.0)
            
        Returns:
            Response dictionary with content and metadata
        """
        pass
    
    @abstractmethod
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model"""
        pass
    
    def log_request(self, prompt: str, max_tokens: int, temperature: float) -> None:
        """Log LLM request details"""
        self.logger.info(
            f"LLM Request - Provider: {self.provider_name}, "
            f"Model: {self.model_name}, "
            f"Max Tokens: {max_tokens}, "
            f"Temperature: {temperature}, "
            f"Prompt Length: {len(prompt)} chars"
        )
    
    def log_response(self, response: Dict[str, Any], processing_time: float) -> None:
        """Log LLM response details"""
        self.logger.info(
            f"LLM Response - Provider: {self.provider_name}, "
            f"Model: {self.model_name}, "
            f"Processing Time: {processing_time:.3f}s, "
            f"Response Length: {len(response.get('content', ''))} chars, "
            f"Tokens Used: {response.get('tokens_used', 'N/A')}"
        )
    
    def log_error(self, error: Exception, context: str = "") -> None:
        """Log LLM error details"""
        self.logger.error(
            f"LLM Error - Provider: {self.provider_name}, "
            f"Model: {self.model_name}, "
            f"Context: {context}, "
            f"Error: {str(error)}"
        )
