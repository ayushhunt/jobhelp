"""
Web Search Service for Company Research
Provides web search capabilities for company background research
"""
import asyncio
import aiohttp
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
import json
import re

from .base_research_source import BaseResearchSource
from app.models.schemas.company_research import ResearchSource, WebSearchResult
from app.config.settings import settings

logger = logging.getLogger(__name__)

class WebSearchService(BaseResearchSource):
    """Web search service using Parallel AI and fallback options"""
    
    def __init__(self):
        """Initialize web search service"""
        super().__init__(ResearchSource.WEB_SEARCH)
        self.parallel_api_key = getattr(settings, 'PARALLEL_API_KEY', None)
        self.google_api_key = getattr(settings, 'GOOGLE_SEARCH_API_KEY', None)
        self.search_engine_id = getattr(settings, 'GOOGLE_SEARCH_ENGINE_ID', None)
        
        # Search strategies
        self.search_queries = [
            "{company} company overview",
            "{company} about us",
            "{company} company profile",
            "{company} business model",
            "{company} industry sector",
            "{company} company news",
            "{company} leadership team",
            "{company} company culture"
        ]
        
    async def research(self, company_name: str, company_domain: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """Perform comprehensive web search for company information"""
        search_results = []
        
        # Generate search queries
        queries = self._generate_search_queries(company_name, company_domain)
        
        # Execute searches in parallel
        search_tasks = []
        for query in queries:
            task = self._execute_search(query)
            search_tasks.append(task)
        
        # Wait for all searches to complete
        results = await asyncio.gather(*search_tasks, return_exceptions=True)
        
        # Process results
        for result in results:
            if isinstance(result, Exception):
                logger.warning(f"Search failed: {str(result)}")
                continue
            if result:
                search_results.extend(result)
        
        # Remove duplicates and rank results
        unique_results = self._deduplicate_results(search_results)
        ranked_results = self._rank_results(unique_results, company_name)
        
        return {
            "search_results": ranked_results,
            "total_results": len(ranked_results),
            "search_queries": queries,
            "search_timestamp": datetime.utcnow()
        }
    
    def _generate_search_queries(self, company_name: str, company_domain: Optional[str] = None) -> List[str]:
        """Generate search queries for company research"""
        queries = []
        
        # Basic company queries
        for template in self.search_queries:
            queries.append(template.format(company=company_name))
        
        # Domain-specific queries if available
        if company_domain:
            clean_domain = self._clean_domain(company_domain)
            queries.extend([
                f"site:{clean_domain} about us",
                f"site:{clean_domain} company profile",
                f"site:{clean_domain} leadership team"
            ])
        
        # Industry-specific queries
        industry_queries = [
            f"{company_name} competitors",
            f"{company_name} market position",
            f"{company_name} company reviews",
            f"{company_name} employee reviews",
            f"{company_name} company culture",
            f"{company_name} funding rounds",
            f"{company_name} acquisitions"
        ]
        queries.extend(industry_queries)
        
        return queries[:10]  # Limit to top 10 queries
    
    async def _execute_search(self, query: str) -> List[WebSearchResult]:
        """Execute a single search query"""
        # Try Parallel AI first
        if self.parallel_api_key:
            try:
                result = await self._search_parallel_ai(query)
                if result:
                    return result
            except Exception as e:
                logger.warning(f"Parallel AI search failed: {str(e)}")
        
        # Fallback to Google Custom Search
        if self.google_api_key and self.search_engine_id:
            try:
                result = await self._search_google(query)
                if result:
                    return result
            except Exception as e:
                logger.warning(f"Google search failed: {str(e)}")
        
        # Last resort - basic web scraping
        try:
            result = await self._basic_web_search(query)
            if result:
                return result
        except Exception as e:
            logger.warning(f"Basic web search failed: {str(e)}")
        
        return []
    
    async def _search_parallel_ai(self, query: str) -> List[WebSearchResult]:
        """Search using Parallel AI"""
        url = "https://api.parallel.ai/v1/search"
        headers = {
            "Authorization": f"Bearer {self.parallel_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "query": query,
            "max_results": 10,
            "search_type": "web",
            "include_domains": [],
            "exclude_domains": [],
            "time_period": "any"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload, timeout=30) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._parse_parallel_response(data, query)
                else:
                    logger.error(f"Parallel AI search error: {response.status}")
                    return []
    
    async def _search_google(self, query: str) -> List[WebSearchResult]:
        """Search using Google Custom Search API"""
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": self.google_api_key,
            "cx": self.search_engine_id,
            "q": query,
            "num": 10
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=30) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._parse_google_response(data, query)
                else:
                    logger.error(f"Google search error: {response.status}")
                    return []
    
    async def _basic_web_search(self, query: str) -> List[WebSearchResult]:
        """Basic web search using DuckDuckGo or similar"""
        # This is a simplified implementation
        # In production, you might use DuckDuckGo Instant Answer API or similar
        return []
    
    def _parse_parallel_response(self, data: Dict[str, Any], query: str) -> List[WebSearchResult]:
        """Parse Parallel AI search response"""
        results = []
        
        try:
            search_results = data.get("results", [])
            for item in search_results:
                result = WebSearchResult(
                    title=item.get("title", ""),
                    url=item.get("url", ""),
                    snippet=item.get("snippet", ""),
                    source=item.get("source", "web"),
                    published_date=self._parse_date(item.get("published_date")),
                    relevance_score=item.get("relevance_score"),
                    content_type=item.get("content_type", "web_page")
                )
                results.append(result)
        except Exception as e:
            logger.error(f"Error parsing Parallel AI response: {str(e)}")
        
        return results
    
    def _parse_google_response(self, data: Dict[str, Any], query: str) -> List[WebSearchResult]:
        """Parse Google Custom Search response"""
        results = []
        
        try:
            search_results = data.get("items", [])
            for item in search_results:
                result = WebSearchResult(
                    title=item.get("title", ""),
                    url=item.get("link", ""),
                    snippet=item.get("snippet", ""),
                    source="google",
                    published_date=self._parse_date(item.get("pagemap", {}).get("metatags", [{}])[0].get("article:published_time")),
                    content_type="web_page"
                )
                results.append(result)
        except Exception as e:
            logger.error(f"Error parsing Google response: {str(e)}")
        
        return results
    
    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        """Parse date string to datetime object"""
        if not date_str:
            return None
            
        try:
            # Try common date formats
            for fmt in ['%Y-%m-%dT%H:%M:%SZ', '%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%d']:
                try:
                    return datetime.strptime(date_str, fmt)
                except ValueError:
                    continue
            return None
        except:
            return None
    
    def _deduplicate_results(self, results: List[WebSearchResult]) -> List[WebSearchResult]:
        """Remove duplicate search results"""
        seen_urls = set()
        unique_results = []
        
        for result in results:
            if result.url not in seen_urls:
                seen_urls.add(result.url)
                unique_results.append(result)
        
        return unique_results
    
    def _rank_results(self, results: List[WebSearchResult], company_name: str) -> List[WebSearchResult]:
        """Rank search results by relevance"""
        def calculate_score(result: WebSearchResult) -> float:
            score = 0.0
            
            # Title relevance
            title_lower = result.title.lower()
            company_lower = company_name.lower()
            if company_lower in title_lower:
                score += 10
            
            # URL relevance
            if company_lower.replace(" ", "") in result.url.lower():
                score += 5
            
            # Source quality
            if result.source in ["official_website", "linkedin", "crunchbase"]:
                score += 3
            
            # Content type
            if result.content_type == "news":
                score += 2
            
            # Relevance score from API
            if result.relevance_score:
                score += result.relevance_score
            
            return score
        
        # Sort by calculated score
        ranked_results = sorted(results, key=calculate_score, reverse=True)
        return ranked_results[:20]  # Return top 20 results
    
    def _clean_domain(self, domain: str) -> str:
        """Clean domain string"""
        if domain.startswith(('http://', 'https://')):
            domain = domain.split('://', 1)[1]
        if domain.startswith('www.'):
            domain = domain[4:]
        return domain.lower()
    
    def get_cost_estimate(self) -> float:
        """Get estimated cost for web search"""
        if self.parallel_api_key:
            return 0.05  # Parallel AI typically costs ~$0.05 per search
        elif self.google_api_key:
            return 0.01  # Google Custom Search costs ~$0.01 per search
        return 0.0  # Free fallback
    
    def is_healthy(self) -> bool:
        """Check if web search service is healthy"""
        return self.is_available and (
            self.parallel_api_key is not None or 
            (self.google_api_key is not None and self.search_engine_id is not None)
        )
    
    async def test_connection(self) -> bool:
        """Test web search service connection"""
        try:
            result = await self.research("Google", "google.com")
            return bool(result and result.get("search_results"))
        except Exception as e:
            logger.error(f"Web search service test failed: {str(e)}")
            return False

