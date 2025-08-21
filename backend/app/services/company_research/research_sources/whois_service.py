"""
WHOIS Service for Company Research
Provides domain registration and ownership information using python-whois library
"""
import asyncio
import logging
from typing import Dict, Any, Optional
from datetime import datetime
import re
from urllib.parse import urlparse
import whois

from .base_research_source import BaseResearchSource
from app.models.schemas.company_research import ResearchSource, WHOISData
from app.config.settings import settings

logger = logging.getLogger(__name__)

class WHOISService(BaseResearchSource):
    """WHOIS domain lookup service using python-whois library"""
    
    def __init__(self):
        """Initialize WHOIS service"""
        super().__init__(ResearchSource.WHOIS)
        
    async def research(self, company_name: str, company_domain: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """Perform WHOIS lookup for company domain using python-whois"""
        if not company_domain:
            # Try to extract domain from company name or search for it
            company_domain = await self._find_company_domain(company_name)
        
        if not company_domain:
            raise ValueError("No domain found for company research")
        
        # Clean domain (remove protocol, www, etc.)
        clean_domain = self._clean_domain(company_domain)
        
        try:
            # Use python-whois library for lookup
            result = await self._query_whois_library(clean_domain)
            if result:
                return self._parse_whois_response(result, clean_domain)
        except Exception as e:
            logger.warning(f"WHOIS lookup failed: {str(e)}")
        
        # Fallback to basic domain validation
        return self._create_basic_domain_info(clean_domain)
    
    async def _find_company_domain(self, company_name: str) -> Optional[str]:
        """Try to find company domain from company name"""
        # Common domain patterns
        common_tlds = ['.com', '.org', '.net', '.co', '.io', '.ai', '.tech']
        
        # Clean company name
        clean_name = re.sub(r'[^\w\s]', '', company_name.lower())
        words = clean_name.split()
        
        # Try different domain combinations
        potential_domains = []
        
        # Full company name
        potential_domains.append(f"{clean_name.replace(' ', '')}.com")
        
        # First word + common TLDs
        if words:
            first_word = words[0]
            for tld in common_tlds:
                potential_domains.append(f"{first_word}{tld}")
        
        # Check if any of these domains exist (basic check)
        for domain in potential_domains:
            if await self._check_domain_exists(domain):
                return domain
        
        return None
    
    async def _check_domain_exists(self, domain: str) -> bool:
        """Basic check if domain exists"""
        try:
            # Use python-whois to check if domain exists
            result = await self._query_whois_library(domain)
            return result is not None
        except:
            return False
    
    def _clean_domain(self, domain: str) -> str:
        """Clean domain string"""
        # Remove protocol
        if domain.startswith(('http://', 'https://')):
            domain = domain.split('://', 1)[1]
        
        # Remove www
        if domain.startswith('www.'):
            domain = domain[4:]
        
        # Remove path and query parameters
        domain = domain.split('/')[0]
        
        return domain.lower()
    
    async def _query_whois_library(self, domain: str) -> Optional[Any]:
        """Query WHOIS using python-whois library"""
        try:
            # Run the whois query in a thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(None, whois.whois, domain)
            return result
        except Exception as e:
            logger.error(f"WHOIS lookup failed for {domain}: {str(e)}")
            return None
    
    def _parse_whois_response(self, whois_result: Any, domain: str) -> Dict[str, Any]:
        """Parse WHOIS library response"""
        try:
            # Extract relevant information from python-whois result
            whois_data = {
                "domain": domain,
                "registrar": getattr(whois_result, 'registrar', None),
                "creation_date": self._parse_date_field(whois_result.creation_date),
                "expiration_date": self._parse_date_field(whois_result.expiration_date),
                "updated_date": self._parse_date_field(whois_result.updated_date),
                "status": self._parse_status_field(whois_result.status),
                "name_servers": self._parse_name_servers(whois_result.name_servers),
                "registrant_organization": getattr(whois_result, 'org', None),
                "registrant_country": getattr(whois_result, 'country', None),
                "admin_contact": self._extract_contact_info(whois_result, 'admin'),
                "tech_contact": self._extract_contact_info(whois_result, 'tech'),
                "dnssec": getattr(whois_result, 'dnssec', None),
                "last_checked": datetime.utcnow(),
                "raw_text": getattr(whois_result, 'text', None)
            }
            
            return whois_data
            
        except Exception as e:
            logger.error(f"Error parsing WHOIS response: {str(e)}")
            return self._create_basic_domain_info(domain)
    
    def _parse_date_field(self, date_field: Any) -> Optional[datetime]:
        """Parse date field from python-whois result"""
        if not date_field:
            return None
        
        try:
            # python-whois returns dates as datetime objects or lists
            if isinstance(date_field, list):
                # Take the first date if it's a list
                date_field = date_field[0] if date_field else None
            
            if isinstance(date_field, datetime):
                return date_field
            elif isinstance(date_field, str):
                # Try to parse string dates
                for fmt in ['%Y-%m-%dT%H:%M:%SZ', '%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%d']:
                    try:
                        return datetime.strptime(date_field, fmt)
                    except ValueError:
                        continue
            
            return None
        except Exception as e:
            logger.warning(f"Failed to parse date field: {str(e)}")
            return None
    
    def _parse_status_field(self, status_field: Any) -> list:
        """Parse status field from python-whois result"""
        if not status_field:
            return []
        
        try:
            if isinstance(status_field, list):
                return status_field
            elif isinstance(status_field, str):
                return [status_field]
            else:
                return [str(status_field)]
        except:
            return []
    
    def _parse_name_servers(self, ns_field: Any) -> list:
        """Parse name servers field from python-whois result"""
        if not ns_field:
            return []
        
        try:
            if isinstance(ns_field, list):
                return ns_field
            elif isinstance(ns_field, str):
                return [ns_field]
            else:
                return [str(ns_field)]
        except:
            return []
    
    def _extract_contact_info(self, whois_result: Any, contact_type: str) -> Optional[Dict[str, str]]:
        """Extract contact information from python-whois result"""
        try:
            # Try to get contact info based on contact type
            if contact_type == 'admin':
                email = getattr(whois_result, 'admin_email', None)
                name = getattr(whois_result, 'admin_name', None)
                org = getattr(whois_result, 'admin_org', None)
            elif contact_type == 'tech':
                email = getattr(whois_result, 'tech_email', None)
                name = getattr(whois_result, 'tech_name', None)
                org = getattr(whois_result, 'tech_org', None)
            else:
                return None
            
            if email or name or org:
                return {
                    "name": name,
                    "email": email,
                    "organization": org
                }
            
            return None
        except:
            return None
    
    def _create_basic_domain_info(self, domain: str) -> Dict[str, Any]:
        """Create basic domain information when detailed lookup fails"""
        return {
            "domain": domain,
            "last_checked": datetime.utcnow(),
            "note": "Basic domain validation only - detailed WHOIS lookup failed"
        }
    
    def get_cost_estimate(self) -> float:
        """Get estimated cost for WHOIS lookup"""
        return 0.0  # python-whois library is free to use
    
    def is_healthy(self) -> bool:
        """Check if WHOIS service is healthy"""
        return self.is_available
    
    async def test_connection(self) -> bool:
        """Test WHOIS service connection"""
        try:
            test_domain = "google.com"
            result = await self.research("Google", test_domain)
            return bool(result and result.get("domain"))
        except Exception as e:
            logger.error(f"WHOIS service test failed: {str(e)}")
            return False

