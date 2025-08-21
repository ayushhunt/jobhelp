"""
Google Knowledge Graph Service for Company Research
Provides company entity information from Google's Knowledge Graph
"""
import asyncio
import aiohttp
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
import json
import re

from .base_research_source import BaseResearchSource
from app.models.schemas.company_research import ResearchSource, KnowledgeGraphData
from app.config.settings import settings

logger = logging.getLogger(__name__)

class KnowledgeGraphService(BaseResearchSource):
    """Google Knowledge Graph service for company entity lookup"""
    
    def __init__(self):
        """Initialize Knowledge Graph service"""
        super().__init__(ResearchSource.KNOWLEDGE_GRAPH)
        self.api_key = getattr(settings, 'GOOGLE_KNOWLEDGE_GRAPH_API_KEY', None)
        self.base_url = "https://kgsearch.googleapis.com/v1/entities:search"
        
        # Entity types for companies
        self.company_types = [
            "Organization",
            "Corporation",
            "Company",
            "Business",
            "TechnologyCompany",
            "SoftwareCompany"
        ]
        
    async def research(self, company_name: str, company_domain: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """Search for company information in Google Knowledge Graph"""
        if not self.api_key:
            raise ValueError("Google Knowledge Graph API key not configured")
        
        # Try different search strategies
        search_results = []
        
        # Strategy 1: Direct company name search
        try:
            result = await self._search_entity(company_name)
            if result:
                search_results.extend(result)
        except Exception as e:
            logger.warning(f"Direct company search failed: {str(e)}")
        
        # Strategy 2: Search with company type
        try:
            for entity_type in self.company_types:
                result = await self._search_entity(f"{company_name} {entity_type}")
                if result:
                    search_results.extend(result)
                    break  # Stop after first successful type search
        except Exception as e:
            logger.warning(f"Typed company search failed: {str(e)}")
        
        # Strategy 3: Domain-based search if available
        if company_domain:
            try:
                clean_domain = self._clean_domain(company_domain)
                result = await self._search_entity(clean_domain)
                if result:
                    search_results.extend(result)
            except Exception as e:
                logger.warning(f"Domain-based search failed: {str(e)}")
        
        # Process and rank results
        if search_results:
            # Remove duplicates
            unique_results = self._deduplicate_results(search_results)
            # Rank by relevance
            ranked_results = self._rank_results(unique_results, company_name)
            # Take the best result
            best_result = ranked_results[0] if ranked_results else None
            
            if best_result:
                return self._parse_entity_data(best_result)
        
        # Return empty result if no matches found
        return self._create_empty_result(company_name)
    
    async def _search_entity(self, query: str) -> List[Dict[str, Any]]:
        """Search for entities in Knowledge Graph"""
        params = {
            "query": query,
            "key": self.api_key,
            "limit": 10,
            "indent": True,
            "types": "Organization",
            "languages": "en"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url, params=params, timeout=30) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("itemListElement", [])
                else:
                    logger.error(f"Knowledge Graph API error: {response.status}")
                    return []
    
    def _parse_entity_data(self, entity: Dict[str, Any]) -> Dict[str, Any]:
        """Parse Knowledge Graph entity data"""
        try:
            # Extract basic entity info
            entity_data = entity.get("result", {})
            
            # Extract detailed properties
            properties = entity_data.get("detailedDescription", {})
            if not properties:
                properties = entity_data.get("description", {})
            
            # Extract image
            image = entity_data.get("image", {})
            
            # Extract additional properties
            additional_properties = {}
            if "additionalProperty" in entity_data:
                for prop in entity_data["additionalProperty"]:
                    if isinstance(prop, dict) and "name" in prop and "value" in prop:
                        additional_properties[prop["name"]] = prop["value"]
            
            # Build knowledge graph data
            kg_data = {
                "entity_id": entity_data.get("@id"),
                "name": entity_data.get("name", ""),
                "description": properties.get("articleBody") if isinstance(properties, dict) else str(properties),
                "entity_type": self._extract_entity_type(entity_data),
                "industry": self._extract_industry(entity_data),
                "founded_date": self._extract_founded_date(entity_data),
                "headquarters": self._extract_headquarters(entity_data),
                "ceo": self._extract_ceo(entity_data),
                "employees": self._extract_employees(entity_data),
                "revenue": self._extract_revenue(entity_data),
                "website": self._extract_website(entity_data),
                "social_media": self._extract_social_media(entity_data),
                "subsidiaries": self._extract_subsidiaries(entity_data),
                "competitors": self._extract_competitors(entity_data),
                "image_url": image.get("contentUrl") if isinstance(image, dict) else None,
                "additional_properties": additional_properties
            }
            
            return kg_data
            
        except Exception as e:
            logger.error(f"Error parsing Knowledge Graph entity: {str(e)}")
            return self._create_empty_result("Unknown")
    
    def _extract_entity_type(self, entity_data: Dict[str, Any]) -> Optional[str]:
        """Extract entity type from Knowledge Graph data"""
        types = entity_data.get("@type", [])
        if isinstance(types, list):
            # Look for company-related types
            for entity_type in types:
                if any(company_type in entity_type for company_type in self.company_types):
                    return entity_type
            return types[0] if types else None
        return types
    
    def _extract_industry(self, entity_data: Dict[str, Any]) -> Optional[str]:
        """Extract industry information"""
        # Look for industry in various properties
        industry_sources = [
            entity_data.get("industry"),
            entity_data.get("sector"),
            entity_data.get("businessCategory")
        ]
        
        for source in industry_sources:
            if source:
                return source
        return None
    
    def _extract_founded_date(self, entity_data: Dict[str, Any]) -> Optional[str]:
        """Extract company founding date"""
        # Look for founding date in various properties
        date_sources = [
            entity_data.get("foundingDate"),
            entity_data.get("dateFounded"),
            entity_data.get("established")
        ]
        
        for source in date_sources:
            if source:
                return source
        return None
    
    def _extract_headquarters(self, entity_data: Dict[str, Any]) -> Optional[str]:
        """Extract company headquarters location"""
        # Look for headquarters in various properties
        location_sources = [
            entity_data.get("location", {}).get("name") if isinstance(entity_data.get("location"), dict) else None,
            entity_data.get("headquarters"),
            entity_data.get("addressLocality"),
            entity_data.get("addressCountry")
        ]
        
        for source in location_sources:
            if source:
                return source
        return None
    
    def _extract_ceo(self, entity_data: Dict[str, Any]) -> Optional[str]:
        """Extract CEO information"""
        # Look for CEO in various properties
        ceo_sources = [
            entity_data.get("ceo"),
            entity_data.get("founder"),
            entity_data.get("executive")
        ]
        
        for source in ceo_sources:
            if source:
                if isinstance(source, dict):
                    return source.get("name", str(source))
                return str(source)
        return None
    
    def _extract_employees(self, entity_data: Dict[str, Any]) -> Optional[str]:
        """Extract employee count information"""
        # Look for employee count in various properties
        employee_sources = [
            entity_data.get("numberOfEmployees"),
            entity_data.get("employeeCount"),
            entity_data.get("staffCount")
        ]
        
        for source in employee_sources:
            if source:
                return str(source)
        return None
    
    def _extract_revenue(self, entity_data: Dict[str, Any]) -> Optional[str]:
        """Extract revenue information"""
        # Look for revenue in various properties
        revenue_sources = [
            entity_data.get("revenue"),
            entity_data.get("annualRevenue"),
            entity_data.get("turnover")
        ]
        
        for source in revenue_sources:
            if source:
                return str(source)
        return None
    
    def _extract_website(self, entity_data: Dict[str, Any]) -> Optional[str]:
        """Extract company website"""
        # Look for website in various properties
        website_sources = [
            entity_data.get("url"),
            entity_data.get("website"),
            entity_data.get("homepage")
        ]
        
        for source in website_sources:
            if source:
                return source
        return None
    
    def _extract_social_media(self, entity_data: Dict[str, Any]) -> Optional[Dict[str, str]]:
        """Extract social media profiles"""
        # Look for social media in various properties
        social_media = {}
        
        # Check for common social media properties
        social_platforms = ["facebook", "twitter", "linkedin", "instagram", "youtube"]
        for platform in social_platforms:
            if platform in entity_data:
                social_media[platform] = entity_data[platform]
        
        return social_media if social_media else None
    
    def _extract_subsidiaries(self, entity_data: Dict[str, Any]) -> Optional[List[str]]:
        """Extract subsidiary companies"""
        subsidiaries = entity_data.get("subsidiary", [])
        if isinstance(subsidiaries, list):
            return [sub.get("name", str(sub)) if isinstance(sub, dict) else str(sub) for sub in subsidiaries]
        elif subsidiaries:
            return [str(subsidiaries)]
        return None
    
    def _extract_competitors(self, entity_data: Dict[str, Any]) -> Optional[List[str]]:
        """Extract competitor companies"""
        competitors = entity_data.get("competitor", [])
        if isinstance(competitors, list):
            return [comp.get("name", str(comp)) if isinstance(comp, dict) else str(comp) for comp in competitors]
        elif competitors:
            return [str(competitors)]
        return None
    
    def _deduplicate_results(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate search results"""
        seen_ids = set()
        unique_results = []
        
        for result in results:
            entity_id = result.get("result", {}).get("@id")
            if entity_id not in seen_ids:
                seen_ids.add(entity_id)
                unique_results.append(result)
        
        return unique_results
    
    def _rank_results(self, results: List[Dict[str, Any]], company_name: str) -> List[Dict[str, Any]]:
        """Rank search results by relevance"""
        def calculate_score(result: Dict[str, Any]) -> float:
            score = 0.0
            entity_data = result.get("result", {})
            
            # Name similarity
            entity_name = entity_data.get("name", "").lower()
            company_lower = company_name.lower()
            if company_lower in entity_name or entity_name in company_lower:
                score += 10
            
            # Entity type relevance
            entity_type = entity_data.get("@type", "")
            if any(company_type in str(entity_type) for company_type in self.company_types):
                score += 5
            
            # Description quality
            if entity_data.get("detailedDescription"):
                score += 3
            
            # Image availability
            if entity_data.get("image"):
                score += 1
            
            # Result score from API
            result_score = result.get("resultScore", 0)
            if isinstance(result_score, (int, float)):
                score += result_score
            
            return score
        
        # Sort by calculated score
        ranked_results = sorted(results, key=calculate_score, reverse=True)
        return ranked_results
    
    def _clean_domain(self, domain: str) -> str:
        """Clean domain string"""
        if domain.startswith(('http://', 'https://')):
            domain = domain.split('://', 1)[1]
        if domain.startswith('www.'):
            domain = domain[4:]
        return domain.lower()
    
    def _create_empty_result(self, company_name: str) -> Dict[str, Any]:
        """Create empty result when no entity is found"""
        return {
            "entity_id": None,
            "name": company_name,
            "description": None,
            "entity_type": None,
            "industry": None,
            "founded_date": None,
            "headquarters": None,
            "ceo": None,
            "employees": None,
            "revenue": None,
            "website": None,
            "social_media": None,
            "subsidiaries": None,
            "competitors": None,
            "note": "No entity found in Google Knowledge Graph"
        }
    
    def get_cost_estimate(self) -> float:
        """Get estimated cost for Knowledge Graph lookup"""
        return 0.0  # Google Knowledge Graph API is free for basic usage
    
    def is_healthy(self) -> bool:
        """Check if Knowledge Graph service is healthy"""
        return self.is_available and self.api_key is not None
    
    async def test_connection(self) -> bool:
        """Test Knowledge Graph service connection"""
        try:
            result = await self.research("Google")
            return bool(result and result.get("name"))
        except Exception as e:
            logger.error(f"Knowledge Graph service test failed: {str(e)}")
            return False

