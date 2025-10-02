"""
Configuration for Portfolio Research Service
"""
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class PortfolioResearchConfig:
    """Configuration for portfolio research service"""
    
    # Web scraping settings
    session_timeout: int = 30
    max_pages: int = 10
    max_content_length: int = 50000  # characters
    request_delay: float = 1.0  # seconds between requests
    
    # Content extraction settings
    min_text_length: int = 100  # minimum text length to consider valid
    max_title_length: int = 200  # maximum title length
    
    # NLP settings
    summary_sentences: int = 5
    keyphrase_ngram_range: tuple = (1, 3)
    max_keywords: int = 10
    min_keyword_score: float = 0.1
    
    # LLM settings
    max_tokens: int = 1000
    temperature: float = 0.3
    
    # Portfolio keywords for URL discovery
    portfolio_keywords: List[str] = None
    
    # Technology patterns for extraction
    technology_patterns: List[str] = None
    
    # Industry keywords
    industry_keywords: List[str] = None
    
    def __post_init__(self):
        """Set default values for lists"""
        if self.portfolio_keywords is None:
            self.portfolio_keywords = [
                "portfolio", "projects", "work", "case studies", "clients", "services",
                "products", "solutions", "industries", "sectors", "technologies",
                "achievements", "results", "impact", "experience", "expertise",
                "showcase", "gallery", "examples", "success stories", "testimonials"
            ]
        
        if self.technology_patterns is None:
            self.technology_patterns = [
                # Programming languages
                r'\b(?:python|javascript|java|c\+\+|c#|php|ruby|go|rust|swift|kotlin|scala|r|matlab|perl|bash|powershell)\b',
                # Web technologies
                r'\b(?:react|angular|vue|node\.js|django|flask|spring|laravel|rails|express|asp\.net|jquery|bootstrap|tailwind|sass|less)\b',
                # Cloud and DevOps
                r'\b(?:aws|azure|gcp|docker|kubernetes|terraform|jenkins|git|github|gitlab|bitbucket|jira|confluence|slack|zoom|teams|trello)\b',
                # Databases and data
                r'\b(?:sql|mongodb|postgresql|mysql|redis|elasticsearch|kafka|rabbitmq|cassandra|dynamodb|firebase|supabase)\b',
                # Infrastructure
                r'\b(?:nginx|apache|iis|tomcat|wildfly|glassfish|nginx|haproxy|varnish|cdn|load\s*balancer)\b'
            ]
        
        if self.industry_keywords is None:
            self.industry_keywords = [
                "healthcare", "finance", "education", "retail", "manufacturing", "technology",
                "consulting", "real estate", "transportation", "energy", "media", "entertainment",
                "government", "nonprofit", "startup", "enterprise", "sme", "ecommerce",
                "saas", "b2b", "b2c", "fintech", "healthtech", "edtech", "proptech"
            ]

# Default configuration
DEFAULT_CONFIG = PortfolioResearchConfig()

# Configuration presets
CONFIG_PRESETS = {
    "fast": PortfolioResearchConfig(
        max_pages=5,
        max_content_length=25000,
        summary_sentences=3,
        max_keywords=5
    ),
    "thorough": PortfolioResearchConfig(
        max_pages=15,
        max_content_length=75000,
        summary_sentences=7,
        max_keywords=15,
        request_delay=2.0
    ),
    "cost_optimized": PortfolioResearchConfig(
        max_pages=8,
        max_content_length=40000,
        summary_sentences=4,
        max_keywords=8,
        session_timeout=20
    )
}

