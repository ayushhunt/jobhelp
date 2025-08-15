"""
Analytics service for orchestrating different types of analysis
"""
import logging
import time
from typing import Dict, Any, Optional
from datetime import datetime
from app.utils.text_processing.text_analyzer import TextAnalyzer
from app.services.llm.llm_service import LLMService
from app.services.parsing.experience_parser_service import ExperienceParserService
from app.core.exceptions.exceptions import AnalyticsError
from app.models.schemas.analysis import AnalysisType

logger = logging.getLogger(__name__)

class AnalyticsService:
    """Main analytics service that orchestrates different analysis types"""
    
    def __init__(self):
        """Initialize analytics service with required components"""
        self.text_analyzer = TextAnalyzer()
        self.llm_service = LLMService()
        self.experience_parser = ExperienceParserService()
        
        logger.info("Analytics service initialized")
    
    async def analyze_documents(
        self,
        resume_content: str,
        job_description_content: str,
        analysis_type: AnalysisType = AnalysisType.BASIC,
        user_id: str = "default",
        is_premium: bool = False
    ) -> Dict[str, Any]:
        """
        Analyze resume and job description based on requested type
        
        Args:
            resume_content: Resume text content
            job_description_content: Job description text content
            analysis_type: Type of analysis to perform
            user_id: User identifier for tracking
            is_premium: Whether user has premium access
            
        Returns:
            Complete analysis results
        """
        start_time = time.time()
        
        try:
            logger.info(f"Starting {analysis_type.value} analysis for user {user_id}")
            
            # Basic analytics (always performed)
            basic_analytics = self._perform_basic_analysis(resume_content, job_description_content)
            
            # Advanced analytics (for advanced and AI-enhanced)
            advanced_analytics = None
            if analysis_type in [AnalysisType.ADVANCED, AnalysisType.AI_ENHANCED]:
                advanced_analytics = self._perform_advanced_analysis(resume_content, job_description_content)
            
            # AI-enhanced analytics (only for AI-enhanced type)
            ai_insights = None
            if analysis_type == AnalysisType.AI_ENHANCED:
                ai_insights = await self._perform_ai_enhanced_analysis(
                    resume_content, job_description_content, user_id, is_premium
                )
            
            # Experience analysis (if available)
            experience_analysis = self._perform_experience_analysis(resume_content)
            
            processing_time = time.time() - start_time
            
            # Compile results
            result = {
                "basic_analytics": basic_analytics,
                "advanced_analytics": advanced_analytics,
                "experience_analysis": experience_analysis,
                "ai_insights": ai_insights,
                "analysis_type": analysis_type,
                "processing_time": round(processing_time, 3),
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"Analysis completed in {processing_time:.3f}s for user {user_id}")
            return result
            
        except Exception as e:
            logger.error(f"Analysis failed for user {user_id}: {str(e)}")
            raise AnalyticsError(
                f"Document analysis failed: {str(e)}",
                error_code="ANALYSIS_FAILED",
                details={"user_id": user_id, "analysis_type": analysis_type.value}
            )
    
    def _perform_basic_analysis(self, resume_content: str, jd_content: str) -> Dict[str, Any]:
        """Perform basic text analysis"""
        try:
            # Word frequency analysis
            resume_freq = self.text_analyzer.get_word_frequency(resume_content)
            jd_freq = self.text_analyzer.get_word_frequency(jd_content)
            
            # Similarity calculation
            similarity_score = self.text_analyzer.calculate_similarity(resume_content, jd_content)
            
            # Keyword analysis
            jd_keywords = set(jd_freq.keys())
            resume_keywords = set(resume_freq.keys())
            common_keywords = list(jd_keywords.intersection(resume_keywords))
            missing_keywords = list(jd_keywords - resume_keywords)
            
            return {
                "similarity_score": similarity_score,
                "resume_word_frequency": resume_freq,
                "jd_word_frequency": jd_freq,
                "common_keywords": common_keywords,
                "missing_keywords": missing_keywords
            }
            
        except Exception as e:
            logger.error(f"Basic analysis failed: {str(e)}")
            raise AnalyticsError(f"Basic analysis failed: {str(e)}")
    
    def _perform_advanced_analysis(self, resume_content: str, jd_content: str) -> Dict[str, Any]:
        """Perform advanced text analysis"""
        try:
            # Skills extraction
            resume_skills = self.text_analyzer.extract_skills(resume_content)
            jd_skills = self.text_analyzer.extract_skills(jd_content)
            
            # Text statistics
            resume_stats = self.text_analyzer.get_text_statistics(resume_content)
            jd_stats = self.text_analyzer.get_text_statistics(jd_content)
            
            # Advanced similarity
            semantic_similarity = self.text_analyzer.calculate_similarity(
                resume_content, jd_content, method="cosine"
            )
            
            # Skills matching
            matched_skills = list(
                set(resume_skills['hard_skills']).intersection(set(jd_skills['hard_skills']))
            )
            missing_skills = list(
                set(jd_skills['hard_skills']) - set(resume_skills['hard_skills'])
            )
            extra_skills = list(
                set(resume_skills['hard_skills']) - set(jd_skills['hard_skills'])
            )
            
            return {
                "semantic_similarity_score": semantic_similarity,
                "matched_skills": matched_skills,
                "missing_skills": missing_skills,
                "extra_skills": extra_skills,
                "resume_readability": resume_stats.get('readability_score', 0),
                "jd_readability": jd_stats.get('readability_score', 0),
                "resume_sections": resume_stats,
                "jd_sections": jd_stats,
                "insights_summary": self._generate_insights_summary(
                    matched_skills, missing_skills, extra_skills, semantic_similarity
                )
            }
            
        except Exception as e:
            logger.error(f"Advanced analysis failed: {str(e)}")
            raise AnalyticsError(f"Advanced analysis failed: {str(e)}")
    
    async def _perform_ai_enhanced_analysis(
        self,
        resume_content: str,
        jd_content: str,
        user_id: str,
        is_premium: bool
    ) -> Dict[str, Any]:
        """Perform AI-enhanced analysis"""
        try:
            # Check if user can use AI
            if not await self.llm_service.can_use_ai(user_id, is_premium):
                raise AnalyticsError(
                    "AI usage limit exceeded",
                    error_code="AI_LIMIT_EXCEEDED"
                )
            
            # Generate AI insights
            ai_insights = await self.llm_service.generate_insights(
                resume_content, jd_content, user_id
            )
            
            return {
                "ai_insights": ai_insights,
                "ai_enabled": True
            }
            
        except Exception as e:
            logger.error(f"AI-enhanced analysis failed: {str(e)}")
            raise AnalyticsError(f"AI-enhanced analysis failed: {str(e)}")
    
    def _perform_experience_analysis(self, resume_content: str) -> Optional[Dict[str, Any]]:
        """Perform experience analysis if possible"""
        try:
            experience_data = self.experience_parser.parse_experience(resume_content)
            if experience_data:
                return {
                    "experience_analysis": experience_data,
                    "career_stability": self._calculate_career_stability(experience_data)
                }
            return None
            
        except Exception as e:
            logger.warning(f"Experience analysis failed: {str(e)}")
            return None
    
    def _generate_insights_summary(
        self,
        matched_skills: list,
        missing_skills: list,
        extra_skills: list,
        similarity_score: float
    ) -> str:
        """Generate insights summary"""
        try:
            summary_parts = []
            
            if similarity_score > 0.7:
                summary_parts.append("Strong alignment between resume and job requirements.")
            elif similarity_score > 0.4:
                summary_parts.append("Moderate alignment with room for improvement.")
            else:
                summary_parts.append("Limited alignment - significant improvements needed.")
            
            if matched_skills:
                summary_parts.append(f"Strong match on {len(matched_skills)} key skills.")
            
            if missing_skills:
                summary_parts.append(f"Consider adding {len(missing_skills)} missing skills.")
            
            if extra_skills:
                summary_parts.append(f"Resume includes {len(extra_skills)} additional valuable skills.")
            
            return " ".join(summary_parts)
            
        except Exception as e:
            logger.error(f"Insights summary generation failed: {str(e)}")
            return "Analysis completed successfully."
    
    def _calculate_career_stability(self, experience_data: Dict[str, Any]) -> float:
        """Calculate career stability score"""
        try:
            # Simple stability calculation based on employment gaps
            # This is a placeholder - implement based on your experience parser output
            return 0.8  # Placeholder score
            
        except Exception as e:
            logger.error(f"Career stability calculation failed: {str(e)}")
            return 0.0
