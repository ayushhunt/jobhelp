"""
Modular LLM Provider System for Cost Optimization
Supports multiple providers: OpenAI, Anthropic, Groq, Ollama, etc.
"""

import os
import json
import asyncio
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ModelConfig:
    """Configuration for a specific model"""
    name: str
    provider: str
    cost_per_token: float  # Cost per 1000 tokens
    max_tokens: int
    context_window: int
    speed_tier: str  # "fast", "medium", "slow"
    quality_tier: str  # "basic", "good", "excellent"
    api_key_env: str  # Environment variable name for API key

@dataclass
class LLMResponse:
    """Standardized response from any LLM provider"""
    content: str
    tokens_used: int
    cost: float
    model_used: str
    provider: str
    response_time: float
    success: bool
    error: Optional[str] = None

class BaseLLMProvider(ABC):
    """Abstract base class for all LLM providers"""
    
    def __init__(self, config: ModelConfig):
        self.config = config
        self.api_key = os.getenv(config.api_key_env)
        
    @abstractmethod
    async def generate(self, prompt: str, max_tokens: int = 500) -> LLMResponse:
        """Generate response from the model"""
        pass
    
    def calculate_cost(self, tokens: int) -> float:
        """Calculate cost based on token usage"""
        return (tokens / 1000) * self.config.cost_per_token
    
    def is_available(self) -> bool:
        """Check if the provider is available (has API key)"""
        return self.api_key is not None

class OpenAIProvider(BaseLLMProvider):
    """OpenAI GPT models provider"""
    
    def __init__(self, config: ModelConfig):
        super().__init__(config)
        if self.api_key:
            from openai import AsyncOpenAI
            self.client = AsyncOpenAI(api_key=self.api_key)
        else:
            self.client = None
    
    async def generate(self, prompt: str, max_tokens: int = 500) -> LLMResponse:
        start_time = datetime.now()
        
        if not self.client:
            return LLMResponse(
                content="", tokens_used=0, cost=0.0, model_used=self.config.name,
                provider=self.config.provider, response_time=0.0, success=False,
                error="OpenAI API key not configured"
            )
        
        try:
            response = await asyncio.wait_for(
                self.client.chat.completions.create(
                    model=self.config.name,
                    messages=[
                        {"role": "system", "content": "You are a helpful recruitment assistant that responds only in valid JSON format."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=min(max_tokens, self.config.max_tokens),
                    temperature=0.3,
                    response_format={"type": "json_object"}
                ),
                timeout=15.0
            )
            
            content = response.choices[0].message.content
            tokens_used = response.usage.total_tokens if response.usage else 0
            cost = self.calculate_cost(tokens_used)
            response_time = (datetime.now() - start_time).total_seconds()
            
            return LLMResponse(
                content=content, tokens_used=tokens_used, cost=cost,
                model_used=self.config.name, provider=self.config.provider,
                response_time=response_time, success=True
            )
            
        except asyncio.TimeoutError:
            return LLMResponse(
                content="", tokens_used=0, cost=0.0, model_used=self.config.name,
                provider=self.config.provider, response_time=15.0, success=False,
                error="Request timed out"
            )
        except Exception as e:
            response_time = (datetime.now() - start_time).total_seconds()
            return LLMResponse(
                content="", tokens_used=0, cost=0.0, model_used=self.config.name,
                provider=self.config.provider, response_time=response_time,
                success=False, error=str(e)
            )

class AnthropicProvider(BaseLLMProvider):
    """Anthropic Claude models provider"""
    
    def __init__(self, config: ModelConfig):
        super().__init__(config)
        if self.api_key:
            try:
                import anthropic
                self.client = anthropic.AsyncAnthropic(api_key=self.api_key)
            except ImportError:
                logger.warning("Anthropic library not installed. Install with: pip install anthropic")
                self.client = None
        else:
            self.client = None
    
    async def generate(self, prompt: str, max_tokens: int = 500) -> LLMResponse:
        start_time = datetime.now()
        
        if not self.client:
            return LLMResponse(
                content="", tokens_used=0, cost=0.0, model_used=self.config.name,
                provider=self.config.provider, response_time=0.0, success=False,
                error="Anthropic API key not configured or library not installed"
            )
        
        try:
            response = await asyncio.wait_for(
                self.client.messages.create(
                    model=self.config.name,
                    max_tokens=min(max_tokens, self.config.max_tokens),
                    temperature=0.3,
                    messages=[
                        {"role": "user", "content": f"Respond only in valid JSON format. {prompt}"}
                    ]
                ),
                timeout=15.0
            )
            
            content = response.content[0].text
            tokens_used = response.usage.input_tokens + response.usage.output_tokens
            cost = self.calculate_cost(tokens_used)
            response_time = (datetime.now() - start_time).total_seconds()
            
            return LLMResponse(
                content=content, tokens_used=tokens_used, cost=cost,
                model_used=self.config.name, provider=self.config.provider,
                response_time=response_time, success=True
            )
            
        except Exception as e:
            response_time = (datetime.now() - start_time).total_seconds()
            return LLMResponse(
                content="", tokens_used=0, cost=0.0, model_used=self.config.name,
                provider=self.config.provider, response_time=response_time,
                success=False, error=str(e)
            )

class GroqProvider(BaseLLMProvider):
    """Groq fast inference provider"""
    
    def __init__(self, config: ModelConfig):
        super().__init__(config)
        if self.api_key:
            try:
                from groq import AsyncGroq
                self.client = AsyncGroq(api_key=self.api_key)
            except ImportError:
                logger.warning("Groq library not installed. Install with: pip install groq")
                self.client = None
        else:
            self.client = None
    
    async def generate(self, prompt: str, max_tokens: int = 500) -> LLMResponse:
        start_time = datetime.now()
        
        if not self.client:
            return LLMResponse(
                content="", tokens_used=0, cost=0.0, model_used=self.config.name,
                provider=self.config.provider, response_time=0.0, success=False,
                error="Groq API key not configured or library not installed"
            )
        
        try:
            response = await asyncio.wait_for(
                self.client.chat.completions.create(
                    model=self.config.name,
                    messages=[
                        {"role": "system", "content": "You are a helpful recruitment assistant. Respond only in valid JSON format."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=min(max_tokens, self.config.max_tokens),
                    temperature=0.3
                ),
                timeout=10.0  # Groq is faster
            )
            
            content = response.choices[0].message.content
            tokens_used = response.usage.total_tokens if response.usage else 0
            cost = self.calculate_cost(tokens_used)
            response_time = (datetime.now() - start_time).total_seconds()
            
            return LLMResponse(
                content=content, tokens_used=tokens_used, cost=cost,
                model_used=self.config.name, provider=self.config.provider,
                response_time=response_time, success=True
            )
            
        except Exception as e:
            response_time = (datetime.now() - start_time).total_seconds()
            return LLMResponse(
                content="", tokens_used=0, cost=0.0, model_used=self.config.name,
                provider=self.config.provider, response_time=response_time,
                success=False, error=str(e)
            )

class OllamaProvider(BaseLLMProvider):
    """Ollama local models provider (free but requires local setup)"""
    
    def __init__(self, config: ModelConfig):
        super().__init__(config)
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    
    async def generate(self, prompt: str, max_tokens: int = 500) -> LLMResponse:
        start_time = datetime.now()
        
        try:
            import aiohttp
            
            async with aiohttp.ClientSession() as session:
                payload = {
                    "model": self.config.name,
                    "prompt": f"Respond only in valid JSON format. {prompt}",
                    "stream": False,
                    "options": {
                        "temperature": 0.3,
                        "num_predict": min(max_tokens, self.config.max_tokens)
                    }
                }
                
                async with session.post(
                    f"{self.base_url}/api/generate",
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30.0)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        content = result.get("response", "")
                        
                        # Estimate tokens (Ollama doesn't provide exact count)
                        tokens_used = len(content.split()) * 1.3  # Rough estimation
                        cost = 0.0  # Ollama is free
                        response_time = (datetime.now() - start_time).total_seconds()
                        
                        return LLMResponse(
                            content=content, tokens_used=int(tokens_used), cost=cost,
                            model_used=self.config.name, provider=self.config.provider,
                            response_time=response_time, success=True
                        )
                    else:
                        raise Exception(f"Ollama API error: {response.status}")
                        
        except Exception as e:
            response_time = (datetime.now() - start_time).total_seconds()
            return LLMResponse(
                content="", tokens_used=0, cost=0.0, model_used=self.config.name,
                provider=self.config.provider, response_time=response_time,
                success=False, error=str(e)
            )

class LLMModelRegistry:
    """Registry of available models with cost optimization"""
    
    def __init__(self):
        self.models = self._initialize_models()
        self.providers = self._initialize_providers()
        
    def _initialize_models(self) -> Dict[str, ModelConfig]:
        """Initialize all available models"""
        return {
            # OpenAI Models
            "gpt-4o-mini": ModelConfig(
                name="gpt-4o-mini", provider="openai", cost_per_token=0.00015,
                max_tokens=16384, context_window=128000, speed_tier="fast",
                quality_tier="good", api_key_env="OPENAI_API_KEY"
            ),
            "gpt-4o": ModelConfig(
                name="gpt-4o", provider="openai", cost_per_token=0.005,
                max_tokens=4096, context_window=128000, speed_tier="medium",
                quality_tier="excellent", api_key_env="OPENAI_API_KEY"
            ),
            "gpt-3.5-turbo": ModelConfig(
                name="gpt-3.5-turbo", provider="openai", cost_per_token=0.0005,
                max_tokens=4096, context_window=16385, speed_tier="fast",
                quality_tier="good", api_key_env="OPENAI_API_KEY"
            ),
            
            # Anthropic Models
            "claude-3-haiku": ModelConfig(
                name="claude-3-haiku-20240307", provider="anthropic", cost_per_token=0.00025,
                max_tokens=4096, context_window=200000, speed_tier="fast",
                quality_tier="good", api_key_env="ANTHROPIC_API_KEY"
            ),
            "claude-3-sonnet": ModelConfig(
                name="claude-3-sonnet-20240229", provider="anthropic", cost_per_token=0.003,
                max_tokens=4096, context_window=200000, speed_tier="medium",
                quality_tier="excellent", api_key_env="ANTHROPIC_API_KEY"
            ),
            
            # Groq Models (Super fast, low cost)
            "llama-3.1-8b": ModelConfig(
                name="llama-3.1-8b-instant", provider="groq", cost_per_token=0.00005,
                max_tokens=8192, context_window=131072, speed_tier="fast",
                quality_tier="good", api_key_env="GROQ_API_KEY"
            ),
            "llama-3.1-70b": ModelConfig(
                name="llama-3.1-70b-versatile", provider="groq", cost_per_token=0.00059,
                max_tokens=8192, context_window=131072, speed_tier="fast",
                quality_tier="excellent", api_key_env="GROQ_API_KEY"
            ),
            "mixtral-8x7b": ModelConfig(
                name="mixtral-8x7b-32768", provider="groq", cost_per_token=0.00024,
                max_tokens=32768, context_window=32768, speed_tier="fast",
                quality_tier="good", api_key_env="GROQ_API_KEY"
            ),
            
            # Ollama Models (Free, local)
            "llama3.1": ModelConfig(
                name="llama3.1", provider="ollama", cost_per_token=0.0,
                max_tokens=8192, context_window=131072, speed_tier="medium",
                quality_tier="good", api_key_env=""
            ),
            "phi3": ModelConfig(
                name="phi3", provider="ollama", cost_per_token=0.0,
                max_tokens=4096, context_window=128000, speed_tier="fast",
                quality_tier="basic", api_key_env=""
            )
        }
    
    def _initialize_providers(self) -> Dict[str, BaseLLMProvider]:
        """Initialize provider instances"""
        providers = {}
        
        for model_id, config in self.models.items():
            if config.provider == "openai":
                providers[model_id] = OpenAIProvider(config)
            elif config.provider == "anthropic":
                providers[model_id] = AnthropicProvider(config)
            elif config.provider == "groq":
                providers[model_id] = GroqProvider(config)
            elif config.provider == "ollama":
                providers[model_id] = OllamaProvider(config)
        
        return providers
    
    def get_available_models(self) -> List[str]:
        """Get list of models with available API keys"""
        return [
            model_id for model_id, provider in self.providers.items()
            if provider.is_available()
        ]
    
    def get_optimal_model(self, priority: str = "cost", quality_requirement: str = "good") -> str:
        """Get the optimal model based on priority and quality requirement"""
        available_models = self.get_available_models()
        
        if not available_models:
            return None
        
        # Filter by quality requirement
        quality_filtered = [
            model_id for model_id in available_models
            if self._quality_meets_requirement(self.models[model_id].quality_tier, quality_requirement)
        ]
        
        if not quality_filtered:
            quality_filtered = available_models  # Fallback to any available
        
        if priority == "cost":
            # Sort by cost (ascending)
            return min(quality_filtered, key=lambda x: self.models[x].cost_per_token)
        elif priority == "speed":
            # Prefer fast models, then by cost
            fast_models = [m for m in quality_filtered if self.models[m].speed_tier == "fast"]
            if fast_models:
                return min(fast_models, key=lambda x: self.models[x].cost_per_token)
            return min(quality_filtered, key=lambda x: self.models[x].cost_per_token)
        elif priority == "quality":
            # Sort by quality, then by cost
            excellent_models = [m for m in quality_filtered if self.models[m].quality_tier == "excellent"]
            if excellent_models:
                return min(excellent_models, key=lambda x: self.models[x].cost_per_token)
            return min(quality_filtered, key=lambda x: self.models[x].cost_per_token)
        
        return quality_filtered[0]  # Default fallback
    
    def _quality_meets_requirement(self, model_quality: str, required_quality: str) -> bool:
        """Check if model quality meets requirement"""
        quality_levels = {"basic": 1, "good": 2, "excellent": 3}
        return quality_levels.get(model_quality, 0) >= quality_levels.get(required_quality, 0)
    
    async def generate_with_fallback(self, prompt: str, 
                                   preferred_models: List[str] = None,
                                   max_tokens: int = 500) -> LLMResponse:
        """Generate response with automatic fallback to other models"""
        
        if not preferred_models:
            # Default preference: cost-optimized with good quality
            preferred_models = [
                self.get_optimal_model("cost", "good"),
                self.get_optimal_model("speed", "basic")
            ]
            # Remove None values
            preferred_models = [m for m in preferred_models if m]
        
        # Add all available models as ultimate fallback
        all_available = self.get_available_models()
        preferred_models.extend([m for m in all_available if m not in preferred_models])
        
        last_error = None
        
        for model_id in preferred_models:
            if model_id in self.providers:
                provider = self.providers[model_id]
                logger.info(f"Trying model: {model_id}")
                
                response = await provider.generate(prompt, max_tokens)
                
                if response.success:
                    logger.info(f"Success with {model_id}: {response.tokens_used} tokens, ${response.cost:.4f}")
                    return response
                else:
                    logger.warning(f"Failed with {model_id}: {response.error}")
                    last_error = response.error
        
        # All models failed
        return LLMResponse(
            content="", tokens_used=0, cost=0.0, model_used="none",
            provider="none", response_time=0.0, success=False,
            error=f"All models failed. Last error: {last_error}"
        )

# Global instance
model_registry = LLMModelRegistry()
