"""
Pydantic schemas for analysis requests and responses
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from enum import Enum

class AnalysisType(str, Enum):
    """Types of analysis available"""
    BASIC = "basic"
    ADVANCED = "advanced"
    AI_ENHANCED = "ai_enhanced"

class AnalysisRequest(BaseModel):
    """Request model for document analysis"""
    resume_file: Optional[str] = Field(None, description="Resume file content (base64 encoded)")
    job_description_file: Optional[str] = Field(None, description="Job description file content (base64 encoded)")
    resume_text: Optional[str] = Field(None, description="Resume text content")
    job_description_text: Optional[str] = Field(None, description="Job description text content")
    use_ai: bool = Field(False, description="Enable AI-powered insights")
    user_id: str = Field("default", description="User identifier for usage tracking")
    is_premium: bool = Field(False, description="Whether user has premium access")
    analysis_type: AnalysisType = Field(AnalysisType.BASIC, description="Type of analysis to perform")
    
    @validator('resume_file', 'job_description_file', 'resume_text', 'job_description_text')
    def validate_content_provided(cls, v, values):
        """Ensure at least one content source is provided for each document"""
        if 'resume_file' in values or 'resume_text' in values:
            if not values.get('resume_file') and not values.get('resume_text'):
                raise ValueError("Either resume_file or resume_text must be provided")
        if 'job_description_file' in values or 'job_description_text' in values:
            if not values.get('job_description_file') and not values.get('job_description_text'):
                raise ValueError("Either job_description_file or job_description_text must be provided")
        return v

class BasicAnalytics(BaseModel):
    """Basic analytics results"""
    similarity_score: float = Field(..., description="Jaccard similarity score")
    resume_word_frequency: Dict[str, int] = Field(..., description="Word frequency in resume")
    jd_word_frequency: Dict[str, int] = Field(..., description="Word frequency in job description")
    common_keywords: List[str] = Field(..., description="Keywords present in both documents")
    missing_keywords: List[str] = Field(..., description="Keywords missing from resume")

class AdvancedAnalytics(BaseModel):
    """Advanced analytics results"""
    semantic_similarity_score: float = Field(..., description="Semantic similarity score")
    matched_skills: List[str] = Field(..., description="Skills that match between resume and JD")
    missing_skills: List[str] = Field(..., description="Skills required but missing from resume")
    extra_skills: List[str] = Field(..., description="Skills in resume but not required")
    resume_readability: float = Field(..., description="Resume readability score")
    jd_readability: float = Field(..., description="Job description readability score")
    insights_summary: str = Field(..., description="Summary of insights")
    
    # Optional fields that may not always be available
    years_experience_required: Optional[float] = Field(None, description="Years of experience required")
    years_experience_resume: Optional[float] = Field(None, description="Years of experience in resume")
    experience_gap: Optional[float] = Field(None, description="Gap between required and actual experience")
    responsibility_coverage_score: Optional[float] = Field(None, description="Coverage of responsibilities")
    requirement_coverage_score: Optional[float] = Field(None, description="Coverage of requirements")
    common_phrases: Optional[List[str]] = Field(None, description="Common phrases between documents")
    action_verb_analysis: Optional[Dict[str, Any]] = Field(None, description="Action verb analysis")
    keyword_density: Optional[Dict[str, float]] = Field(None, description="Keyword density analysis")
    education_match: Optional[Dict[str, Any]] = Field(None, description="Education matching results")
    missing_certifications: Optional[List[str]] = Field(None, description="Missing certifications")
    resume_sections: Optional[Dict[str, Any]] = Field(None, description="Resume section analysis")
    jd_sections: Optional[Dict[str, Any]] = Field(None, description="Job description section analysis")

class ExperienceAnalysis(BaseModel):
    """Experience analysis results"""
    experience_analysis: Optional[Dict[str, Any]] = Field(None, description="Detailed experience analysis")
    role_duration_mapping: Optional[Dict[str, Any]] = Field(None, description="Role duration mapping")
    career_progression: Optional[Dict[str, Any]] = Field(None, description="Career progression analysis")
    employment_gaps: Optional[List[Dict[str, Any]]] = Field(None, description="Employment gaps identified")
    experience_by_recency: Optional[Dict[str, Any]] = Field(None, description="Experience by recency")
    skill_experience_mapping: Optional[Dict[str, Any]] = Field(None, description="Skill to experience mapping")
    career_stability: Optional[float] = Field(None, description="Career stability score")

class AIInsights(BaseModel):
    """AI-generated insights"""
    ai_insights: Optional[Dict[str, Any]] = Field(None, description="AI-generated insights")
    ai_enabled: bool = Field(..., description="Whether AI was used for analysis")

class AnalysisResponse(BaseModel):
    """Complete analysis response"""
    # Basic analytics
    basic_analytics: BasicAnalytics
    
    # Advanced analytics (optional)
    advanced_analytics: Optional[AdvancedAnalytics] = None
    
    # Experience analysis (if available)
    experience_analysis: Optional[ExperienceAnalysis] = None
    
    # AI insights (if available)
    ai_insights: Optional[AIInsights] = None
    
    # Metadata
    analysis_type: AnalysisType
    processing_time: float = Field(..., description="Time taken for analysis in seconds")
    timestamp: str = Field(..., description="Timestamp of analysis")

class AIUsageResponse(BaseModel):
    """AI usage statistics response"""
    user_id: str
    daily_usage: int
    daily_limit: int
    remaining: int
    can_use_ai: bool

class ModelInfo(BaseModel):
    """AI model information"""
    id: str
    name: str
    provider: str
    cost_per_1k_tokens: str
    max_tokens: int
    context_window: int
    speed_tier: str
    quality_tier: str

class AvailableModelsResponse(BaseModel):
    """Available AI models response"""
    available_models: List[ModelInfo]
    total_available: int
    recommended: Dict[str, str]
    free_tier_preference: List[str]
    premium_tier_preference: List[str]

class CostComparisonResponse(BaseModel):
    """Cost comparison response"""
    cost_comparison: Dict[str, Dict[str, Any]]
    note: str
