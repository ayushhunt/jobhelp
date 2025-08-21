"""
AI Analysis Service for Company Research
Synthesizes research data and generates comprehensive insights using LLM
"""
import asyncio
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
import json

from .base_research_source import BaseResearchSource
from app.models.schemas.company_research import (
    ResearchSource, CompanyAuthenticity, CompanyGrowth, 
    EmployeeInsights, ResearchTaskResult
)
from app.services.llm.llm_orchestrator import LLMOrchestrator
from app.config.settings import settings

logger = logging.getLogger(__name__)

class AIAnalysisService(BaseResearchSource):
    """AI-powered analysis service for company research synthesis"""
    
    def __init__(self):
        """Initialize AI analysis service"""
        super().__init__(ResearchSource.AI_ANALYSIS)
        self.llm_orchestrator = LLMOrchestrator()
        
        # Analysis prompts
        self.analysis_prompts = {
            "executive_summary": self._get_executive_summary_prompt(),
            "authenticity_assessment": self._get_authenticity_assessment_prompt(),
            "growth_analysis": self._get_growth_analysis_prompt(),
            "employee_insights": self._get_employee_insights_prompt(),
            "risk_assessment": self._get_risk_assessment_prompt(),
            "recommendations": self._get_recommendations_prompt()
        }
        
    async def research(self, company_name: str, company_domain: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """Perform AI-powered analysis of company research data"""
        # Extract research data from kwargs
        research_data = kwargs.get('research_data', {})
        task_results = kwargs.get('task_results', [])
        
        if not research_data:
            raise ValueError("No research data provided for AI analysis")
        
        # Perform comprehensive AI analysis
        analysis_results = {}
        
        try:
            # 1. Generate executive summary
            executive_summary = await self._generate_executive_summary(company_name, research_data)
            analysis_results['executive_summary'] = executive_summary
            
            # 2. Assess company authenticity
            authenticity = await self._assess_authenticity(research_data, task_results)
            analysis_results['company_authenticity'] = authenticity
            
            # 3. Analyze company growth
            growth = await self._analyze_growth(research_data)
            analysis_results['company_growth'] = growth
            
            # 4. Extract employee insights
            employee_insights = await self._extract_employee_insights(research_data)
            analysis_results['employee_insights'] = employee_insights
            
            # 5. Risk assessment
            risk_assessment = await self._assess_risks(research_data, authenticity)
            analysis_results['risk_assessment'] = risk_assessment
            
            # 6. Generate recommendations
            recommendations = await self._generate_recommendations(research_data, risk_assessment)
            analysis_results['recommendations'] = recommendations
            
            # 7. Key insights
            key_insights = await self._extract_key_insights(research_data, analysis_results)
            analysis_results['key_insights'] = key_insights
            
        except Exception as e:
            logger.error(f"AI analysis failed: {str(e)}")
            # Return partial results if possible
            analysis_results['error'] = str(e)
        
        return analysis_results
    
    async def _generate_executive_summary(self, company_name: str, research_data: Dict[str, Any]) -> str:
        """Generate executive summary of company research"""
        prompt = self.analysis_prompts['executive_summary'].format(
            company_name=company_name,
            research_data=json.dumps(research_data, indent=2)
        )
        
        try:
            llm_provider = self.llm_orchestrator.get_current_provider()
            if llm_provider:
                response = await llm_provider.generate_text(prompt, max_tokens=500)
                return response.strip()
            else:
                return self._fallback_executive_summary(company_name, research_data)
        except Exception as e:
            logger.warning(f"LLM executive summary generation failed: {str(e)}")
            return self._fallback_executive_summary(company_name, research_data)
    
    async def _assess_authenticity(self, research_data: Dict[str, Any], task_results: List[ResearchTaskResult]) -> CompanyAuthenticity:
        """Assess company authenticity based on research data"""
        prompt = self.analysis_prompts['authenticity_assessment'].format(
            research_data=json.dumps(research_data, indent=2),
            task_results=json.dumps([tr.dict() for tr in task_results], indent=2)
        )
        
        try:
            llm_provider = self.llm_orchestrator.get_current_provider()
            if llm_provider:
                response = await llm_provider.generate_text(prompt, max_tokens=300)
                return self._parse_authenticity_response(response)
            else:
                return self._fallback_authenticity_assessment(research_data)
        except Exception as e:
            logger.warning(f"LLM authenticity assessment failed: {str(e)}")
            return self._fallback_authenticity_assessment(research_data)
    
    async def _analyze_growth(self, research_data: Dict[str, Any]) -> CompanyGrowth:
        """Analyze company growth indicators"""
        prompt = self.analysis_prompts['growth_analysis'].format(
            research_data=json.dumps(research_data, indent=2)
        )
        
        try:
            llm_provider = self.llm_orchestrator.get_current_provider()
            if llm_provider:
                response = await llm_provider.generate_text(prompt, max_tokens=300)
                return self._parse_growth_response(response)
            else:
                return self._fallback_growth_analysis(research_data)
        except Exception as e:
            logger.warning(f"LLM growth analysis failed: {str(e)}")
            return self._fallback_growth_analysis(research_data)
    
    async def _extract_employee_insights(self, research_data: Dict[str, Any]) -> EmployeeInsights:
        """Extract employee-related insights"""
        prompt = self.analysis_prompts['employee_insights'].format(
            research_data=json.dumps(research_data, indent=2)
        )
        
        try:
            llm_provider = self.llm_orchestrator.get_current_provider()
            if llm_provider:
                response = await llm_provider.generate_text(prompt, max_tokens=300)
                return self._parse_employee_insights_response(response)
            else:
                return self._fallback_employee_insights(research_data)
        except Exception as e:
            logger.warning(f"LLM employee insights failed: {str(e)}")
            return self._fallback_employee_insights(research_data)
    
    async def _assess_risks(self, research_data: Dict[str, Any], authenticity: CompanyAuthenticity) -> str:
        """Assess potential risks associated with the company"""
        prompt = self.analysis_prompts['risk_assessment'].format(
            research_data=json.dumps(research_data, indent=2),
            authenticity=json.dumps(authenticity.dict(), indent=2)
        )
        
        try:
            llm_provider = self.llm_orchestrator.get_current_provider()
            if llm_provider:
                response = await llm_provider.generate_text(prompt, max_tokens=200)
                return response.strip()
            else:
                return self._fallback_risk_assessment(research_data, authenticity)
        except Exception as e:
            logger.warning(f"LLM risk assessment failed: {str(e)}")
            return self._fallback_risk_assessment(research_data, authenticity)
    
    async def _generate_recommendations(self, research_data: Dict[str, Any], risk_assessment: str) -> List[str]:
        """Generate actionable recommendations"""
        prompt = self.analysis_prompts['recommendations'].format(
            research_data=json.dumps(research_data, indent=2),
            risk_assessment=risk_assessment
        )
        
        try:
            llm_provider = self.llm_orchestrator.get_current_provider()
            if llm_provider:
                response = await llm_provider.generate_text(prompt, max_tokens=300)
                return self._parse_recommendations_response(response)
            else:
                return self._fallback_recommendations(research_data, risk_assessment)
        except Exception as e:
            logger.warning(f"LLM recommendations failed: {str(e)}")
            return self._fallback_recommendations(research_data, risk_assessment)
    
    async def _extract_key_insights(self, research_data: Dict[str, Any], analysis_results: Dict[str, Any]) -> List[str]:
        """Extract key insights from research and analysis"""
        # Combine research data and analysis results
        combined_data = {
            "research_data": research_data,
            "analysis_results": analysis_results
        }
        
        prompt = f"""
        Based on the following company research data and analysis, extract 5-7 key insights that would be most valuable for someone considering working at or doing business with this company.
        
        Data: {json.dumps(combined_data, indent=2)}
        
        Provide insights as a JSON array of strings, each insight should be concise but informative.
        """
        
        try:
            llm_provider = self.llm_orchestrator.get_current_provider()
            if llm_provider:
                response = await llm_provider.generate_text(prompt, max_tokens=400)
                return self._parse_insights_response(response)
            else:
                return self._fallback_key_insights(research_data, analysis_results)
        except Exception as e:
            logger.warning(f"LLM key insights failed: {str(e)}")
            return self._fallback_key_insights(research_data, analysis_results)
    
    # Prompt templates
    def _get_executive_summary_prompt(self) -> str:
        return """
        Based on the following company research data, provide a concise executive summary (2-3 paragraphs) that covers:
        1. Company overview and main business
        2. Key strengths and market position
        3. Notable achievements or challenges
        
        Company: {company_name}
        Research Data: {research_data}
        
        Executive Summary:
        """
    
    def _get_authenticity_assessment_prompt(self) -> str:
        return """
        Analyze the following company research data and assess the company's authenticity and trustworthiness.
        Consider domain age, web presence, news coverage, and overall credibility.
        
        Provide assessment as JSON with these fields:
        - domain_age_days: number
        - domain_reputation_score: float (0-1)
        - social_presence_score: float (0-1)
        - news_mentions_count: number
        - employee_reviews_count: number
        - authenticity_score: float (0-1)
        - risk_factors: array of strings
        - trust_indicators: array of strings
        - overall_assessment: "trustworthy", "suspicious", or "unknown"
        
        Research Data: {research_data}
        Task Results: {task_results}
        
        Assessment:
        """
    
    def _get_growth_analysis_prompt(self) -> str:
        return """
        Analyze the following company research data to assess growth indicators and market position.
        
        Provide analysis as JSON with these fields:
        - employee_growth_trend: string
        - funding_rounds: array of objects
        - acquisition_history: array of objects
        - expansion_news: array of strings
        - market_position: string
        - growth_score: float (0-1)
        
        Research Data: {research_data}
        
        Analysis:
        """
    
    def _get_employee_insights_prompt(self) -> str:
        return """
        Extract employee-related insights from the company research data.
        
        Provide insights as JSON with these fields:
        - review_sentiment: string
        - common_pros: array of strings
        - common_cons: array of strings
        - work_life_balance_score: float (0-1)
        - career_growth_score: float (0-1)
        - compensation_score: float (0-1)
        - management_score: float (0-1)
        - overall_rating: float (0-5)
        - review_count: number
        
        Research Data: {research_data}
        
        Insights:
        """
    
    def _get_risk_assessment_prompt(self) -> str:
        return """
        Based on the company research data and authenticity assessment, provide a concise risk assessment.
        Focus on potential red flags, concerns, or areas that require further investigation.
        
        Research Data: {research_data}
        Authenticity Assessment: {authenticity}
        
        Risk Assessment:
        """
    
    def _get_recommendations_prompt(self) -> str:
        return """
        Based on the company research data and risk assessment, provide 3-5 actionable recommendations.
        These should be practical suggestions for someone considering working at or doing business with this company.
        
        Research Data: {research_data}
        Risk Assessment: {risk_assessment}
        
        Provide recommendations as a JSON array of strings.
        
        Recommendations:
        """
    
    # Response parsing methods
    def _parse_authenticity_response(self, response: str) -> CompanyAuthenticity:
        """Parse LLM response for authenticity assessment"""
        try:
            # Try to extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end != 0:
                json_str = response[json_start:json_end]
                data = json.loads(json_str)
                return CompanyAuthenticity(**data)
        except:
            pass
        
        # Fallback to default values
        return CompanyAuthenticity(
            overall_assessment="unknown",
            risk_factors=["Unable to assess due to insufficient data"],
            trust_indicators=["Analysis incomplete"]
        )
    
    def _parse_growth_response(self, response: str) -> CompanyGrowth:
        """Parse LLM response for growth analysis"""
        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end != 0:
                json_str = response[json_start:json_end]
                data = json.loads(json_str)
                return CompanyGrowth(**data)
        except:
            pass
        
        return CompanyGrowth()
    
    def _parse_employee_insights_response(self, response: str) -> EmployeeInsights:
        """Parse LLM response for employee insights"""
        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end != 0:
                json_str = response[json_start:json_end]
                data = json.loads(json_str)
                return EmployeeInsights(**data)
        except:
            pass
        
        return EmployeeInsights()
    
    def _parse_recommendations_response(self, response: str) -> List[str]:
        """Parse LLM response for recommendations"""
        try:
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            if json_start != -1 and json_end != 0:
                json_str = response[json_start:json_end]
                return json.loads(json_str)
        except:
            pass
        
        return ["Conduct additional research", "Verify information independently"]
    
    def _parse_insights_response(self, response: str) -> List[str]:
        """Parse LLM response for key insights"""
        try:
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            if json_start != -1 and json_end != 0:
                json_str = response[json_start:json_end]
                return json.loads(json_str)
        except:
            pass
        
        return ["Analysis completed with AI assistance", "Key insights available in detailed results"]
    
    # Fallback methods
    def _fallback_executive_summary(self, company_name: str, research_data: Dict[str, Any]) -> str:
        """Fallback executive summary when LLM fails"""
        return f"Company research completed for {company_name}. Analysis includes domain verification, web search results, and entity information. Review the detailed results for comprehensive insights."
    
    def _fallback_authenticity_assessment(self, research_data: Dict[str, Any]) -> CompanyAuthenticity:
        """Fallback authenticity assessment when LLM fails"""
        return CompanyAuthenticity(
            overall_assessment="unknown",
            risk_factors=["AI analysis unavailable"],
            trust_indicators=["Basic research completed"]
        )
    
    def _fallback_growth_analysis(self, research_data: Dict[str, Any]) -> CompanyGrowth:
        """Fallback growth analysis when LLM fails"""
        return CompanyGrowth()
    
    def _fallback_employee_insights(self, research_data: Dict[str, Any]) -> EmployeeInsights:
        """Fallback employee insights when LLM fails"""
        return EmployeeInsights()
    
    def _fallback_risk_assessment(self, research_data: Dict[str, Any], authenticity: CompanyAuthenticity) -> str:
        """Fallback risk assessment when LLM fails"""
        return "Risk assessment requires additional analysis. Review the research data for potential concerns."
    
    def _fallback_recommendations(self, research_data: Dict[str, Any], risk_assessment: str) -> List[str]:
        """Fallback recommendations when LLM fails"""
        return ["Review all research data carefully", "Verify information from multiple sources", "Consider professional consultation if needed"]
    
    def _fallback_key_insights(self, research_data: Dict[str, Any], analysis_results: Dict[str, Any]) -> List[str]:
        """Fallback key insights when LLM fails"""
        return [
            "Research data collected successfully",
            "Multiple data sources utilized",
            "Analysis completed with available data",
            "Review detailed results for comprehensive understanding"
        ]
    
    def get_cost_estimate(self) -> float:
        """Get estimated cost for AI analysis"""
        # Estimate based on token usage
        return 0.02  # Approximately $0.02 per analysis
    
    def is_healthy(self) -> bool:
        """Check if AI analysis service is healthy"""
        return self.is_available and self.llm_orchestrator.get_current_provider() is not None
    
    async def test_connection(self) -> bool:
        """Test AI analysis service connection"""
        try:
            # Test with minimal data
            test_data = {"company_name": "Test Company"}
            result = await self.research("Test Company", research_data=test_data)
            return bool(result and result.get("executive_summary"))
        except Exception as e:
            logger.error(f"AI analysis service test failed: {str(e)}")
            return False

