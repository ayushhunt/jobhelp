"""
Company Research Orchestrator
Coordinates multiple research sources and manages the research pipeline
"""
import asyncio
import logging
import time
from typing import Dict, Any, Optional, List
from datetime import datetime
import uuid

from app.models.schemas.company_research import (
    CompanyResearchRequest, CompanyResearchResponse, ResearchSource, 
    ResearchStatus, ResearchTaskResult, ResearchProgress, ResearchCostEstimate
)
from .research_sources.whois_service import WHOISService
from .research_sources.web_search_service import WebSearchService
from .research_sources.knowledge_graph_service import KnowledgeGraphService
from .research_sources.ai_analysis_service import AIAnalysisService

logger = logging.getLogger(__name__)

class CompanyResearchOrchestrator:
    """Orchestrates company research across multiple data sources"""
    
    def __init__(self):
        """Initialize the research orchestrator"""
        self.research_sources = {
            ResearchSource.WHOIS: WHOISService(),
            ResearchSource.WEB_SEARCH: WebSearchService(),
            ResearchSource.KNOWLEDGE_GRAPH: KnowledgeGraphService(),
            ResearchSource.AI_ANALYSIS: AIAnalysisService()
        }
        
        # Research pipeline configuration
        self.pipeline_config = {
            "basic": [ResearchSource.WEB_SEARCH],
            "standard": [ResearchSource.WHOIS, ResearchSource.WEB_SEARCH, ResearchSource.KNOWLEDGE_GRAPH],
            "comprehensive": [ResearchSource.WHOIS, ResearchSource.WEB_SEARCH, ResearchSource.KNOWLEDGE_GRAPH, ResearchSource.AI_ANALYSIS]
        }
        
        # Active research sessions
        self.active_research_sessions: Dict[str, ResearchProgress] = {}
        
    async def research_company(self, request: CompanyResearchRequest) -> CompanyResearchResponse:
        """Perform comprehensive company research"""
        start_time = time.time()
        request_id = str(uuid.uuid4())
        
        # Initialize research progress
        progress = ResearchProgress(
            request_id=request_id,
            company_name=request.company_name or request.company_domain or "Unknown Company",
            overall_progress=0.0,
            status=ResearchStatus.IN_PROGRESS
        )
        self.active_research_sessions[request_id] = progress
        
        try:
            # Determine research sources based on depth
            research_sources = self.pipeline_config.get(request.research_depth, self.pipeline_config["standard"])
            
            # Execute research tasks in parallel
            task_results = await self._execute_research_pipeline(
                request, research_sources, progress
            )
            
            # Aggregate research data
            research_data = self._aggregate_research_data(task_results)
            
            # Perform AI analysis if available
            if ResearchSource.AI_ANALYSIS in research_sources:
                ai_analysis = await self._perform_ai_analysis(request, research_data, task_results)
                research_data.update(ai_analysis)
            
            # Build final response
            response = self._build_research_response(request, research_data, task_results, start_time)
            
            # Update progress
            progress.overall_progress = 100.0
            progress.status = ResearchStatus.COMPLETED
            progress.completed_tasks = research_sources
            
            return response
            
        except Exception as e:
            logger.error(f"Company research failed: {str(e)}")
            # Update progress
            progress.status = ResearchStatus.FAILED
            progress.overall_progress = 0.0
            
            # Return partial response if possible
            return self._build_error_response(request, str(e), start_time)
        
        finally:
            # Clean up active session after some time
            asyncio.create_task(self._cleanup_session(request_id))
    
    async def _execute_research_pipeline(
        self, 
        request: CompanyResearchRequest, 
        research_sources: List[ResearchSource],
        progress: ResearchProgress
    ) -> List[ResearchTaskResult]:
        """Execute research pipeline with parallel processing"""
        task_results = []
        total_sources = len(research_sources)
        
        # Create research tasks
        research_tasks = []
        for source in research_sources:
            if source in self.research_sources:
                task = self._execute_research_task(request, source)
                research_tasks.append(task)
        
        # Execute tasks with progress tracking
        for i, task in enumerate(asyncio.as_completed(research_tasks)):
            try:
                result = await task
                task_results.append(result)
                
                # Update progress
                progress.overall_progress = ((i + 1) / total_sources) * 100
                progress.completed_tasks.append(result.source)
                
                if result.status == ResearchStatus.FAILED:
                    progress.failed_tasks.append(result.source)
                
            except Exception as e:
                logger.error(f"Research task failed: {str(e)}")
                # Create failed result
                failed_result = ResearchTaskResult(
                    source=research_sources[i] if i < len(research_sources) else ResearchSource.WHOIS,
                    status=ResearchStatus.FAILED,
                    error_message=str(e),
                    processing_time=0.0,
                    cost_estimate=0.0
                )
                task_results.append(failed_result)
                progress.failed_tasks.append(failed_result.source)
        
        return task_results
    
    async def _execute_research_task(
        self, 
        request: CompanyResearchRequest, 
        source: ResearchSource
    ) -> ResearchTaskResult:
        """Execute a single research task"""
        research_service = self.research_sources.get(source)
        if not research_service:
            raise ValueError(f"Research source {source} not available")
        
        try:
            # Execute research with service-specific parameters
            if source == ResearchSource.AI_ANALYSIS:
                # AI analysis needs aggregated data from other sources
                return await research_service.execute_research(
                    request.company_name or "",
                    request.company_domain,
                    research_data={},  # Will be populated later
                    task_results=[]     # Will be populated later
                )
            else:
                return await research_service.execute_research(
                    request.company_name or "",
                    request.company_domain
                )
                
        except Exception as e:
            logger.error(f"Research task {source} failed: {str(e)}")
            return ResearchTaskResult(
                source=source,
                status=ResearchStatus.FAILED,
                error_message=str(e),
                processing_time=0.0,
                cost_estimate=0.0
            )
    
    def _aggregate_research_data(self, task_results: List[ResearchTaskResult]) -> Dict[str, Any]:
        """Aggregate research data from all sources"""
        aggregated_data = {}
        
        for result in task_results:
            if result.status == ResearchStatus.COMPLETED and result.data:
                source_name = result.source.value
                aggregated_data[source_name] = result.data
        
        return aggregated_data
    
    async def _perform_ai_analysis(
        self, 
        request: CompanyResearchRequest, 
        research_data: Dict[str, Any],
        task_results: List[ResearchTaskResult]
    ) -> Dict[str, Any]:
        """Perform AI analysis on aggregated research data"""
        try:
            ai_service = self.research_sources.get(ResearchSource.AI_ANALYSIS)
            if ai_service:
                ai_result = await ai_service.research(
                    request.company_name or "",
                    request.company_domain,
                    research_data=research_data,
                    task_results=task_results
                )
                return ai_result
        except Exception as e:
            logger.error(f"AI analysis failed: {str(e)}")
        
        return {}
    
    def _build_research_response(
        self, 
        request: CompanyResearchRequest, 
        research_data: Dict[str, Any],
        task_results: List[ResearchTaskResult],
        start_time: float
    ) -> CompanyResearchResponse:
        """Build the final research response"""
        # Extract data by source
        whois_data = research_data.get("whois", {})
        web_search_results = research_data.get("web_search", {}).get("search_results", [])
        knowledge_graph_data = research_data.get("knowledge_graph", {})
        
        # Extract AI analysis results
        ai_results = research_data.get("ai_analysis", {})
        executive_summary = ai_results.get("executive_summary", "Analysis completed successfully.")
        key_insights = ai_results.get("key_insights", ["Research completed with available data"])
        risk_assessment = ai_results.get("risk_assessment", "Risk assessment completed")
        recommendations = ai_results.get("recommendations", ["Review all data carefully"])
        
        # Build response
        response = CompanyResearchResponse(
            company_name=request.company_name or request.company_domain or "Unknown Company",
            company_domain=request.company_domain,
            whois_data=whois_data if whois_data else None,
            web_search_results=web_search_results if web_search_results else None,
            knowledge_graph_data=knowledge_graph_data if knowledge_graph_data else None,
            company_authenticity=ai_results.get("company_authenticity"),
            company_growth=ai_results.get("company_growth"),
            employee_insights=ai_results.get("employee_insights"),
            executive_summary=executive_summary,
            key_insights=key_insights,
            risk_assessment=risk_assessment,
            recommendations=recommendations,
            research_depth=request.research_depth,
            research_status=ResearchStatus.COMPLETED,
            total_processing_time=time.time() - start_time,
            total_cost=self._calculate_total_cost(task_results),
            sources_used=[result.source for result in task_results if result.status == ResearchStatus.COMPLETED],
            failed_sources=[result.source for result in task_results if result.status == ResearchStatus.FAILED],
            task_results=task_results
        )
        
        return response
    
    def _build_error_response(
        self, 
        request: CompanyResearchRequest, 
        error_message: str,
        start_time: float
    ) -> CompanyResearchResponse:
        """Build error response when research fails"""
        return CompanyResearchResponse(
            company_name=request.company_name or request.company_domain or "Unknown Company",
            company_domain=request.company_domain,
            executive_summary=f"Research failed: {error_message}",
            key_insights=["Research could not be completed"],
            risk_assessment="Unable to assess risks due to research failure",
            recommendations=["Try again later", "Verify company information manually"],
            research_depth=request.research_depth,
            research_status=ResearchStatus.FAILED,
            total_processing_time=time.time() - start_time,
            total_cost=0.0,
            sources_used=[],
            failed_sources=[],
            task_results=[]
        )
    
    def _calculate_total_cost(self, task_results: List[ResearchTaskResult]) -> float:
        """Calculate total cost of research"""
        total_cost = 0.0
        for result in task_results:
            if result.cost_estimate:
                total_cost += result.cost_estimate
        return total_cost
    
    async def get_research_progress(self, request_id: str) -> Optional[ResearchProgress]:
        """Get research progress for a specific request"""
        return self.active_research_sessions.get(request_id)
    
    async def cancel_research(self, request_id: str) -> bool:
        """Cancel ongoing research"""
        if request_id in self.active_research_sessions:
            progress = self.active_research_sessions[request_id]
            progress.status = ResearchStatus.FAILED
            progress.overall_progress = 0.0
            return True
        return False
    
    def get_cost_estimate(self, research_depth: str = "standard") -> ResearchCostEstimate:
        """Get cost estimate for research"""
        sources = self.pipeline_config.get(research_depth, [])
        cost_breakdown = {}
        total_cost = 0.0
        
        for source in sources:
            if source in self.research_sources:
                cost = self.research_sources[source].get_cost_estimate()
                cost_breakdown[source.value] = cost
                total_cost += cost
        
        # Cost optimization tips
        optimization_tips = []
        if total_cost > 0.10:  # More than $0.10
            optimization_tips.append("Consider using 'basic' research depth for cost savings")
        if ResearchSource.AI_ANALYSIS in sources:
            optimization_tips.append("AI analysis adds cost but provides valuable insights")
        
        # Alternative options
        alternative_options = [
            {
                "depth": "basic",
                "cost": self._calculate_depth_cost("basic"),
                "description": "Basic domain and web search only"
            },
            {
                "depth": "standard", 
                "cost": self._calculate_depth_cost("standard"),
                "description": "Standard research with knowledge graph"
            }
        ]
        
        return ResearchCostEstimate(
            estimated_total_cost=total_cost,
            cost_breakdown=cost_breakdown,
            cost_optimization_tips=optimization_tips,
            alternative_research_options=alternative_options
        )
    
    def _calculate_depth_cost(self, depth: str) -> float:
        """Calculate cost for specific research depth"""
        sources = self.pipeline_config.get(depth, [])
        total_cost = 0.0
        
        for source in sources:
            if source in self.research_sources:
                total_cost += self.research_sources[source].get_cost_estimate()
        
        return total_cost
    
    def get_service_health(self) -> Dict[str, Any]:
        """Get health status of all research services"""
        health_status = {}
        
        for source, service in self.research_sources.items():
            health_status[source.value] = service.get_health_status()
        
        return health_status
    
    async def test_all_services(self) -> Dict[str, bool]:
        """Test all research services"""
        test_results = {}
        
        for source, service in self.research_sources.items():
            try:
                result = await service.test_connection()
                test_results[source.value] = result
            except Exception as e:
                logger.error(f"Service test failed for {source}: {str(e)}")
                test_results[source.value] = False
        
        return test_results
    
    async def _cleanup_session(self, request_id: str, delay_seconds: int = 300):
        """Clean up research session after delay"""
        await asyncio.sleep(delay_seconds)
        if request_id in self.active_research_sessions:
            del self.active_research_sessions[request_id]
            logger.info(f"Cleaned up research session: {request_id}")
    
    def get_active_sessions_count(self) -> int:
        """Get count of active research sessions"""
        return len(self.active_research_sessions)
    
    def get_available_research_depths(self) -> List[str]:
        """Get available research depth options"""
        return list(self.pipeline_config.keys())
    
    def get_research_source_info(self) -> Dict[str, Any]:
        """Get information about available research sources"""
        source_info = {}
        
        for source, service in self.research_sources.items():
            source_info[source.value] = {
                "name": source.value,
                "description": service.__class__.__doc__ or "No description available",
                "cost_per_request": service.get_cost_estimate(),
                "is_healthy": service.is_healthy(),
                "is_available": service.is_available
            }
        
        return source_info

