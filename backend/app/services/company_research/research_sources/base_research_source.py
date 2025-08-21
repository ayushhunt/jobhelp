"""
Base Research Source Interface
Defines the contract that all research sources must implement
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from app.models.schemas.company_research import ResearchSource, ResearchStatus, ResearchTaskResult
import logging
import time
from datetime import datetime

logger = logging.getLogger(__name__)

class BaseResearchSource(ABC):
    """Abstract base class for all research sources"""
    
    def __init__(self, source_name: ResearchSource, api_key: Optional[str] = None):
        """Initialize the research source"""
        self.source_name = source_name
        self.api_key = api_key
        self.is_available = True
        self.last_used = None
        self.error_count = 0
        self.max_retries = 3
        self.retry_delay = 1  # seconds
        
    @abstractmethod
    async def research(self, company_name: str, company_domain: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """Perform research and return data"""
        pass
    
    @abstractmethod
    def get_cost_estimate(self) -> float:
        """Get estimated cost for this research source"""
        pass
    
    @abstractmethod
    def is_healthy(self) -> bool:
        """Check if the service is healthy and available"""
        pass
    
    async def execute_research(self, company_name: str, company_domain: Optional[str] = None, **kwargs) -> ResearchTaskResult:
        """Execute research with error handling and retries"""
        start_time = time.time()
        
        try:
            # Check if service is healthy
            if not self.is_healthy():
                return ResearchTaskResult(
                    source=self.source_name,
                    status=ResearchStatus.FAILED,
                    error_message="Service is not healthy",
                    processing_time=time.time() - start_time,
                    cost_estimate=self.get_cost_estimate()
                )
            
            # Attempt research with retries
            for attempt in range(self.max_retries):
                try:
                    data = await self.research(company_name, company_domain, **kwargs)
                    
                    # Success - update metrics
                    self.last_used = datetime.utcnow()
                    self.error_count = 0
                    
                    return ResearchTaskResult(
                        source=self.source_name,
                        status=ResearchStatus.COMPLETED,
                        data=data,
                        processing_time=time.time() - start_time,
                        cost_estimate=self.get_cost_estimate()
                    )
                    
                except Exception as e:
                    self.error_count += 1
                    logger.warning(f"Attempt {attempt + 1} failed for {self.source_name}: {str(e)}")
                    
                    if attempt < self.max_retries - 1:
                        await asyncio.sleep(self.retry_delay * (2 ** attempt))  # Exponential backoff
                    else:
                        # All retries exhausted
                        logger.error(f"All retries failed for {self.source_name}: {str(e)}")
                        return ResearchTaskResult(
                            source=self.source_name,
                            status=ResearchStatus.FAILED,
                            error_message=str(e),
                            processing_time=time.time() - start_time,
                            cost_estimate=self.get_cost_estimate()
                        )
                        
        except Exception as e:
            logger.error(f"Unexpected error in {self.source_name}: {str(e)}")
            return ResearchTaskResult(
                source=self.source_name,
                status=ResearchStatus.FAILED,
                error_message=f"Unexpected error: {str(e)}",
                processing_time=time.time() - start_time,
                cost_estimate=self.get_cost_estimate()
            )
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get detailed health status of the service"""
        return {
            "source": self.source_name,
            "is_available": self.is_available,
            "is_healthy": self.is_healthy(),
            "last_used": self.last_used,
            "error_count": self.error_count,
            "api_key_configured": bool(self.api_key)
        }
    
    def reset_health_metrics(self):
        """Reset health metrics (useful for testing)"""
        self.error_count = 0
        self.last_used = None
    
    def update_availability(self, is_available: bool):
        """Update service availability status"""
        self.is_available = is_available
        if not is_available:
            logger.warning(f"Service {self.source_name} marked as unavailable")
        else:
            logger.info(f"Service {self.source_name} marked as available")

# Import asyncio for the sleep function
import asyncio

