"""
Factory for creating and managing LLM providers
"""
import logging
from typing import Dict, Any, Optional
from app.config.settings import settings
from .providers.base_provider import BaseLLMProvider

logger = logging.getLogger(__name__)

class LLMProviderFactory:
    """Factory for creating LLM provider instances"""
    
    def __init__(self):
        """Initialize the provider factory"""
        self.providers = {}
        self.current_provider = None
        self._initialize_providers()
    
    def _initialize_providers(self) -> None:
        """Initialize available LLM providers"""
        try:
            # Initialize Groq provider (recommended for speed)
            if settings.GROQ_API_KEY and settings.GROQ_API_KEY != "your_groq_api_key_here":
                try:
                    from .providers.groq_provider import GroqProvider
                    self.providers['groq'] = GroqProvider(settings.GROQ_API_KEY)
                    logger.info("Groq provider initialized successfully")
                except Exception as e:
                    logger.error(f"Failed to initialize Groq provider: {str(e)}")
            else:
                logger.warning("Groq API key not found or not configured - provider not available")
            
            # Initialize Gemini provider
            if settings.GEMINI_API_KEY and settings.GEMINI_API_KEY != "your_gemini_api_key_here":
                try:
                    from .providers.gemini_provider import GeminiProvider
                    self.providers['gemini'] = GeminiProvider(settings.GEMINI_API_KEY)
                    logger.info("Gemini provider initialized successfully")
                except Exception as e:
                    logger.error(f"Failed to initialize Gemini provider: {str(e)}")
            else:
                logger.warning("Gemini API key not found or not configured - provider not available")
            
            # Initialize OpenAI provider
            if settings.OPENAI_API_KEY and settings.OPENAI_API_KEY != "your_openai_api_key_here":
                try:
                    from .providers.openai_provider import OpenAIProvider
                    self.providers['openai'] = OpenAIProvider(settings.OPENAI_API_KEY)
                    logger.info("OpenAI provider initialized successfully")
                except Exception as e:
                    logger.error(f"Failed to initialize OpenAI provider: {str(e)}")
            else:
                logger.warning("OpenAI API key not found or not configured - provider not available")
            
            # Initialize Parallel AI provider
            if settings.PARALLEL_API_KEY and settings.PARALLEL_API_KEY != "your_parallel_api_key_here":
                try:
                    from .providers.parallel_provider import ParallelProvider
                    self.providers['parallel'] = ParallelProvider(settings.PARALLEL_API_KEY)
                    logger.info("Parallel AI provider initialized successfully")
                except Exception as e:
                    logger.error(f"Failed to initialize Parallel AI provider: {str(e)}")
            else:
                logger.warning("Parallel AI API key not found or not configured - provider not available")
            
            # Log available providers
            if self.providers:
                logger.info(f"Available LLM providers: {list(self.providers.keys())}")
                # Auto-select the first available provider (prefer groq for speed)
                preferred_order = [ 'parallel','groq', 'gemini', 'openai', 'mock']
                for provider_name in preferred_order:
                    if provider_name in self.providers:
                        self.current_provider = self.providers[provider_name]
                        logger.info(f"Auto-selected {provider_name} provider as default")
                        break
                
                if not self.current_provider:
                    # Fallback to first available provider
                    first_provider = list(self.providers.keys())[0]
                    self.current_provider = self.providers[first_provider]
                    logger.info(f"Auto-selected {first_provider} provider as fallback")
                
                logger.info(f"Current provider: {self.current_provider.provider_name}")
            else:
                # No real providers available, use mock provider for testing
                try:
                    from .providers.mock_provider import MockProvider
                    self.providers['mock'] = MockProvider()
                    logger.warning("No real LLM providers available - using mock provider for testing")
                    logger.info("Mock provider will generate sample responses - not suitable for production")
                except Exception as e:
                    logger.error(f"Failed to initialize mock provider: {str(e)}")
                    logger.error("No LLM providers available! Please configure API keys in your .env file")
                    logger.info("Available providers to configure:")
                    logger.info("- GROQ_API_KEY for Groq (recommended for speed)")
                    logger.info("- GEMINI_API_KEY for Google Gemini")
                    logger.info("- OPENAI_API_KEY for OpenAI GPT models")
                    logger.info("- PARALLEL_API_KEY for Parallel AI (ultra-fast web research)")
                    logger.info("- ANTHROPIC_API_KEY for Anthropic Claude")
                    logger.info("Note: Provider will be auto-selected based on availability and preference")
                
        except Exception as e:
            logger.error(f"Failed to initialize LLM providers: {str(e)}")
    
    def get_provider(self, provider_name: str = None) -> Optional[BaseLLMProvider]:
        """
        Get a specific LLM provider
        
        Args:
            provider_name: Name of the provider to get
            
        Returns:
            LLM provider instance or None if not found
        """
        if provider_name:
            provider = self.providers.get(provider_name.lower())
            if provider:
                logger.info(f"Using LLM provider: {provider_name}")
                return provider
            else:
                logger.warning(f"Provider {provider_name} not found")
                return None
        
        # Return current provider if set, otherwise None
        if self.current_provider:
            return self.current_provider
        else:
            logger.warning("No provider selected. Use switch_provider() to select a provider first.")
            return None
    
    def get_current_provider(self) -> Optional[BaseLLMProvider]:
        """Get the current selected LLM provider"""
        return self.current_provider
    
    def switch_provider(self, provider_name: str) -> bool:
        """
        Switch to a different LLM provider
        
        Args:
            provider_name: Name of the provider to switch to
            
        Returns:
            True if successful, False otherwise
        """
        provider = self.providers.get(provider_name.lower())
        if provider:
            self.current_provider = provider
            logger.info(f"Successfully switched to {provider_name} provider")
            return True
        else:
            logger.error(f"Cannot switch to provider {provider_name} - not available")
            logger.info(f"Available providers: {list(self.providers.keys())}")
            return False
    
    def get_available_providers(self) -> Dict[str, Any]:
        """Get information about all available providers"""
        provider_info = {}
        
        for name, provider in self.providers.items():
            try:
                provider_info[name] = {
                    "name": name,
                    "model": provider.model_name,
                    "status": "available",
                    "model_info": provider.get_model_info(),
                    "is_current": provider == self.current_provider
                }
            except Exception as e:
                logger.error(f"Failed to get info for provider {name}: {str(e)}")
                provider_info[name] = {
                    "name": name,
                    "status": "error",
                    "error": str(e)
                }
        
        return {
            "available_providers": provider_info,
            "current_provider": self.current_provider.provider_name if self.current_provider else None,
            "total_providers": len(self.providers),
            "note": "Provider auto-selected. Use switch_provider() method to change provider."
        }
    
    async def test_provider(self, provider_name: str) -> Dict[str, Any]:
        """
        Test a specific LLM provider
        
        Args:
            provider_name: Name of the provider to test
            
        Returns:
            Test results
        """
        provider = self.providers.get(provider_name.lower())
        if not provider:
            return {
                "success": False,
                "error": f"Provider {provider_name} not found"
            }
        
        try:
            # Simple test prompt
            test_prompt = "Hello, this is a test. Please respond with 'Test successful'."
            
            logger.info(f"Testing LLM provider: {provider_name}")
            response = await provider.generate_response(test_prompt, max_tokens=50, temperature=0.1)
            
            if response.get('success') and 'test successful' in response.get('content', '').lower():
                return {
                    "success": True,
                    "provider": provider_name,
                    "model": provider.model_name,
                    "response_time": response.get('processing_time', 0),
                    "message": "Provider test successful"
                }
            else:
                return {
                    "success": False,
                    "provider": provider_name,
                    "error": "Unexpected response format",
                    "response": response
                }
                
        except Exception as e:
            logger.error(f"Provider test failed for {provider_name}: {str(e)}")
            return {
                "success": False,
                "provider": provider_name,
                "error": str(e)
            }
    
    def get_provider_status(self) -> Dict[str, Any]:
        """Get overall status of all providers"""
        return {
            "total_providers": len(self.providers),
            "current_provider": self.current_provider.provider_name if self.current_provider else None,
            "available_providers": list(self.providers.keys()),
            "status": "ready" if self.providers else "no_providers",
            "message": "Use switch_provider() to select a provider" if self.providers else "Configure API keys to enable providers"
        }
