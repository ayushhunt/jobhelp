"""
Pydantic schemas for company research requests and responses
"""
from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, Field, model_validator
from enum import Enum
from datetime import datetime

class ResearchSource(str, Enum):
    """Available research data sources"""
    WHOIS = "whois"
    WEB_SEARCH = "web_search"
    KNOWLEDGE_GRAPH = "knowledge_graph"
    AI_ANALYSIS = "ai_analysis"
    LOCATION_VERIFICATION = "location_verification"
    PORTFOLIO_RESEARCH = "portfolio_research"

class ResearchStatus(str, Enum):
    """Research task status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIAL = "partial"

class CompanyResearchRequest(BaseModel):
    """Request model for company research"""
    company_name: Optional[str] = Field(None, description="Company name to research")
    company_domain: Optional[str] = Field(None, description="Company domain to research")
    research_depth: str = Field("standard", description="Research depth: basic, standard, comprehensive")
    include_employee_reviews: bool = Field(False, description="Include employee review analysis")
    include_financial_data: bool = Field(False, description="Include financial data analysis")
    user_id: str = Field("default", description="User identifier for usage tracking")
    is_premium: bool = Field(False, description="Whether user has premium access")
    
    @model_validator(mode='after')
    def validate_input_provided(self):
        """Ensure at least one input is provided"""
        if not self.company_name and not self.company_domain:
            raise ValueError("Either company_name or company_domain must be provided")
        return self

class WHOISData(BaseModel):
    """WHOIS domain registration data"""
    domain: str
    registrar: Optional[str] = None
    creation_date: Optional[datetime] = None
    expiration_date: Optional[datetime] = None
    updated_date: Optional[datetime] = None
    status: List[str] = []
    name_servers: List[str] = []
    registrant_organization: Optional[str] = None
    registrant_country: Optional[str] = None
    admin_contact: Optional[Dict[str, str]] = None
    tech_contact: Optional[Dict[str, str]] = None
    dnssec: Optional[str] = None
    last_checked: datetime = Field(default_factory=datetime.utcnow)

class WebSearchResult(BaseModel):
    """Web search result data"""
    title: str
    url: str
    snippet: str
    source: str
    published_date: Optional[datetime] = None
    relevance_score: Optional[float] = None
    content_type: str = "web_page"  # web_page, news, social_media, etc.

class KnowledgeGraphData(BaseModel):
    """Google Knowledge Graph entity data"""
    entity_id: Optional[str] = None
    name: str
    description: Optional[str] = None
    entity_type: Optional[str] = None
    industry: Optional[str] = None
    founded_date: Optional[str] = None
    headquarters: Optional[str] = None
    ceo: Optional[str] = None
    employees: Optional[str] = None
    revenue: Optional[str] = None
    website: Optional[str] = None
    social_media: Optional[Dict[str, str]] = None
    subsidiaries: Optional[List[str]] = None
    competitors: Optional[List[str]] = None

class CompanyAuthenticity(BaseModel):
    """Company authenticity assessment"""
    domain_age_days: Optional[int] = None
    domain_reputation_score: Optional[float] = None
    social_presence_score: Optional[float] = None
    news_mentions_count: Optional[int] = None
    employee_reviews_count: Optional[int] = None
    authenticity_score: Optional[float] = None
    risk_factors: List[str] = []
    trust_indicators: List[str] = []
    overall_assessment: str = "unknown"  # trustworthy, suspicious, unknown

class CompanyGrowth(BaseModel):
    """Company growth indicators"""
    employee_growth_trend: Optional[str] = None
    funding_rounds: Optional[List[Dict[str, Any]]] = None

class PortfolioPageData(BaseModel):
    """Data from a single portfolio page"""
    url: str
    title: str
    text: str
    scraped_at: datetime

class PortfolioSummary(BaseModel):
    """Portfolio summary data"""
    summary: str
    method: str  # "llm" or "nlp"
    model_used: Optional[str] = None
    key_phrases: Optional[List[str]] = None
    entities: Optional[Dict[str, List[str]]] = None
    techniques_used: Optional[List[str]] = None
    error: Optional[str] = None
    generated_at: datetime

class PortfolioData(BaseModel):
    """Complete portfolio research data"""
    domain: str
    pages: List[PortfolioPageData]
    raw_text: str
    portfolio_urls: List[str]
    technologies: List[str]
    industries: List[str]
    projects: List[str]
    scraped_at: datetime
    total_pages_scraped: int
    total_content_length: int
    llm_summary: PortfolioSummary
    nlp_summary: PortfolioSummary
    acquisition_history: Optional[List[Dict[str, Any]]] = None
    expansion_news: Optional[List[str]] = None
    market_position: Optional[str] = None
    growth_score: Optional[float] = None

class EmployeeInsights(BaseModel):
    """Employee-related insights"""
    review_sentiment: Optional[str] = None
    common_pros: List[str] = []
    common_cons: List[str] = []
    work_life_balance_score: Optional[float] = None
    career_growth_score: Optional[float] = None
    compensation_score: Optional[float] = None
    management_score: Optional[float] = None
    overall_rating: Optional[float] = None
    review_count: Optional[int] = None

class LocationData(BaseModel):
    """Location information from a single source"""
    source: str  # "google_places" or "nominatim_osm"
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    formatted_address: Optional[str] = None
    place_id: Optional[str] = None
    confidence_score: Optional[float] = None
    last_updated: datetime = Field(default_factory=datetime.utcnow)

class LocationComparison(BaseModel):
    """Comparison results between location sources"""
    address_similarity_score: float = Field(0.0, description="Address similarity score (0-1)")
    coordinate_distance_km: Optional[float] = Field(None, description="Distance between coordinates in km")
    city_match: bool = Field(False, description="Whether cities match")
    state_match: bool = Field(False, description="Whether states match")
    country_match: bool = Field(False, description="Whether countries match")
    postal_code_match: bool = Field(False, description="Whether postal codes match")
    overall_location_confidence: float = Field(0.0, description="Overall location confidence score (0-1)")

class LocationVerificationData(BaseModel):
    """Complete location verification data"""
    company_name: str
    search_query: str
    google_places_data: Optional[LocationData] = None
    nominatim_osm_data: Optional[LocationData] = None
    comparison: Optional[LocationComparison] = None
    authenticity_score: float = Field(0.0, description="Location authenticity score (0-1)")
    verification_status: str = Field("unknown", description="verified, suspicious, unknown")
    risk_factors: List[str] = []
    trust_indicators: List[str] = []
    last_verified: datetime = Field(default_factory=datetime.utcnow)

class ResearchTaskResult(BaseModel):
    """Individual research task result"""
    source: ResearchSource
    status: ResearchStatus
    data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    processing_time: float
    cost_estimate: Optional[float] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class CompanyResearchResponse(BaseModel):
    """Complete company research response"""
    # Request identification
    request_id: str
    
    # Company identification
    company_name: str
    company_domain: Optional[str] = None
    
    # Research results by source
    whois_data: Optional[WHOISData] = None
    web_search_results: Optional[List[WebSearchResult]] = None
    knowledge_graph_data: Optional[KnowledgeGraphData] = None
    location_verification_data: Optional[LocationVerificationData] = None
    
    # Synthesized insights
    company_authenticity: Optional[CompanyAuthenticity] = None
    company_growth: Optional[CompanyGrowth] = None
    employee_insights: Optional[EmployeeInsights] = None
    portfolio_data: Optional[PortfolioData] = None
    
    # AI-generated summary
    executive_summary: str
    key_insights: List[str]
    risk_assessment: str
    recommendations: List[str]
    
    # Research metadata
    research_depth: str
    research_status: ResearchStatus
    total_processing_time: float
    total_cost: Optional[float] = None
    sources_used: List[ResearchSource]
    failed_sources: List[ResearchSource]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    # Authenticity scoring
    authenticity_score: float = Field(0.0, description="Overall company authenticity score (0-100)")
    
    # Task-level results
    task_results: List[ResearchTaskResult]

class ResearchProgress(BaseModel):
    """Research progress tracking"""
    request_id: str
    company_name: str
    overall_progress: float = Field(..., ge=0, le=100)
    completed_tasks: List[ResearchSource] = []
    failed_tasks: List[ResearchSource] = []
    current_task: Optional[ResearchSource] = None
    estimated_completion_time: Optional[float] = None
    status: ResearchStatus = ResearchStatus.PENDING

class ResearchCostEstimate(BaseModel):
    """Cost estimation for research"""
    estimated_total_cost: float
    cost_breakdown: Dict[ResearchSource, float]
    cost_optimization_tips: List[str]
    alternative_research_options: List[Dict[str, Any]]
