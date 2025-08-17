"""
LLM Orchestrator Service
Manages LLM provider selection, switching, and orchestration
"""
import logging
from typing import Dict, Any, Optional
from .provider_factory import LLMProviderFactory

logger = logging.getLogger(__name__)

class LLMOrchestrator:
    """Orchestrates LLM provider operations and management"""
    
    def __init__(self):
        """Initialize the LLM orchestrator"""
        self.provider_factory = LLMProviderFactory()
        logger.info("LLM orchestrator initialized")
    
    def get_provider(self, provider_name: str = None) -> Optional[Any]:
        """Get a specific or current LLM provider"""
        return self.provider_factory.get_provider(provider_name)
    
    def get_current_provider(self) -> Optional[Any]:
        """Get the current selected LLM provider"""
        return self.provider_factory.get_current_provider()
    
    def switch_provider(self, provider_name: str) -> bool:
        """Switch to a different LLM provider"""
        return self.provider_factory.switch_provider(provider_name)
    
    def get_provider_status(self) -> Dict[str, Any]:
        """Get overall status of all providers"""
        return self.provider_factory.get_provider_status()
    
    def get_available_providers(self) -> Dict[str, Any]:
        """Get information about available AI models and providers"""
        return self.provider_factory.get_available_providers()
    
    def get_current_provider_info(self) -> Dict[str, Any]:
        """Get information about the current LLM provider"""
        try:
            current_provider = self.provider_factory.get_current_provider()
            if current_provider:
                return {
                    "provider": current_provider.provider_name,
                    "model": current_provider.model_name,
                    "model_info": current_provider.get_model_info()
                }
            else:
                return {"error": "No provider available"}
                
        except Exception as e:
            logger.error(f"Current provider info retrieval failed: {str(e)}")
            return {"error": str(e)}
    
    async def test_provider(self, provider_name: str) -> Dict[str, Any]:
        """Test a specific LLM provider"""
        try:
            return await self.provider_factory.test_provider(provider_name)
        except Exception as e:
            logger.error(f"Provider test failed: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def auto_select_provider(self) -> bool:
        """Automatically select the best available provider"""
        try:
            available_providers = self.get_available_providers()
            available_names = list(available_providers.get('available_providers', {}).keys())
            
            if not available_names:
                logger.warning("No providers available for auto-selection")
                return False
            
            # Prefer Groq for speed, then Parallel AI for web research, then fall back to others
            preferred_order = ['groq', 'parallel', 'gemini', 'openai', 'mock']
            
            for provider_name in preferred_order:
                if provider_name in available_names:
                    success = self.switch_provider(provider_name)
                    if success:
                        logger.info(f"Auto-selected {provider_name} provider")
                        return True
            
            # If preferred providers failed, try any available
            if available_names:
                success = self.switch_provider(available_names[0])
                if success:
                    logger.info(f"Auto-selected {available_names[0]} provider as fallback")
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Auto-provider selection failed: {str(e)}")
            return False
