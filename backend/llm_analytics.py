import os
import json
import asyncio
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import re
from llm_providers import model_registry, LLMResponse

@dataclass
class LLMConfig:
    """Configuration for LLM usage and limits"""
    free_tier_daily_limit: int = 3  # Max LLM calls per day for free users
    max_tokens_per_call: int = 500  # Token limit per request
    # Model preferences by tier
    free_tier_models: List[str] = None  # Will be set in __post_init__
    premium_tier_models: List[str] = None  # Will be set in __post_init__
    timeout_seconds: int = 15  # Request timeout
    
    def __post_init__(self):
        if self.free_tier_models is None:
            # Prioritize cost-effective models for free tier
            self.free_tier_models = [
                "llama-3.1-8b",  # Groq - super cheap and fast
                "mixtral-8x7b",  # Groq - good quality, still cheap
                "gpt-4o-mini",   # OpenAI - backup
                "claude-3-haiku", # Anthropic - backup
                "phi3",          # Ollama - free local fallback
            ]
        
        if self.premium_tier_models is None:
            # Prioritize quality models for premium tier
            self.premium_tier_models = [
                "llama-3.1-70b",    # Groq - excellent quality, fast
                "claude-3-sonnet",  # Anthropic - top quality
                "gpt-4o",          # OpenAI - top quality
                "llama-3.1-8b",    # Groq - fast fallback
                "gpt-4o-mini",     # OpenAI - backup
            ]

class TextSummarizer:
    """Efficiently summarize JD and Resume for LLM processing"""
    
    def __init__(self):
        # High-impact keywords for different categories
        self.skill_keywords = [
            'python', 'java', 'javascript', 'react', 'angular', 'vue', 'nodejs', 'django',
            'aws', 'azure', 'docker', 'kubernetes', 'sql', 'postgresql', 'mongodb',
            'machine learning', 'ai', 'data science', 'analytics', 'cloud', 'api',
            'microservices', 'devops', 'ci/cd', 'git', 'linux', 'tensorflow', 'pytorch'
        ]
        
        self.experience_patterns = [
            r'(\d+)\+?\s*years?\s*(?:of\s*)?(?:experience|exp)',
            r'(\d+)\+?\s*yrs?\s*(?:of\s*)?(?:experience|exp)',
            r'minimum\s*(?:of\s*)?(\d+)\+?\s*years?',
            r'at\s*least\s*(\d+)\+?\s*years?'
        ]
        
        self.responsibility_keywords = [
            'responsible for', 'manage', 'lead', 'develop', 'design', 'implement',
            'maintain', 'optimize', 'collaborate', 'coordinate', 'supervise'
        ]

    def extract_key_info(self, text: str, doc_type: str = "resume") -> Dict[str, Any]:
        """Extract key information from text in a structured format"""
        text_lower = text.lower()
        
        # Extract skills
        found_skills = []
        for skill in self.skill_keywords:
            if skill.lower() in text_lower:
                found_skills.append(skill)
        
        # Extract experience years
        experience_years = 0
        for pattern in self.experience_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                experience_years = max([int(match) for match in matches])
                break
        
        # Extract key responsibilities/requirements
        sentences = text.split('.')
        key_points = []
        for sentence in sentences[:10]:  # Limit to first 10 sentences
            sentence_lower = sentence.lower().strip()
            if any(keyword in sentence_lower for keyword in self.responsibility_keywords):
                if len(sentence.strip()) > 20 and len(sentence.strip()) < 150:
                    key_points.append(sentence.strip())
        
        # Extract job titles/roles
        title_patterns = [
            r'(software engineer|developer|data scientist|analyst|manager|lead|senior|junior)',
            r'(product manager|project manager|tech lead|architect|consultant)',
            r'(full stack|frontend|backend|devops|ml engineer)'
        ]
        
        titles = []
        for pattern in title_patterns:
            matches = re.findall(pattern, text_lower)
            titles.extend(matches)
        
        return {
            "skills": found_skills[:10],  # Top 10 skills
            "experience_years": experience_years,
            "key_points": key_points[:5],  # Top 5 key points
            "titles": list(set(titles))[:3],  # Top 3 unique titles
            "doc_type": doc_type
        }

    def create_summary(self, resume_text: str, jd_text: str) -> Tuple[Dict, Dict]:
        """Create optimized summaries for LLM processing"""
        resume_summary = self.extract_key_info(resume_text, "resume")
        jd_summary = self.extract_key_info(jd_text, "job_description")
        
        return resume_summary, jd_summary

class LLMAnalytics:
    """LLM-powered analytics with modular providers and cost optimization"""
    
    def __init__(self):
        self.config = LLMConfig()
        self.summarizer = TextSummarizer()
        self.model_registry = model_registry
        
        # Simple in-memory usage tracking (in production, use Redis/database)
        self.usage_tracker = {}
        
        # Log available models
        available_models = self.model_registry.get_available_models()
        if available_models:
            print(f"Available LLM models: {', '.join(available_models)}")
        else:
            print("Warning: No LLM models available. Please configure API keys.")

    def check_usage_limit(self, user_id: str = "default", is_premium: bool = False) -> bool:
        """Check if user has exceeded their daily LLM usage limit"""
        if is_premium:
            return True  # No limits for premium users
        
        today = datetime.now().date()
        user_key = f"{user_id}_{today}"
        
        current_usage = self.usage_tracker.get(user_key, 0)
        return current_usage < self.config.free_tier_daily_limit

    def increment_usage(self, user_id: str = "default"):
        """Increment user's daily usage counter"""
        today = datetime.now().date()
        user_key = f"{user_id}_{today}"
        
        self.usage_tracker[user_key] = self.usage_tracker.get(user_key, 0) + 1

    def create_structured_prompt(self, resume_summary: Dict, jd_summary: Dict) -> str:
        """Create a token-efficient, structured prompt for the LLM"""
        
        prompt = f"""You are an expert recruitment assistant. Analyze the following job-resume match and respond ONLY in valid JSON format.

Job Description Summary:
- Required Skills: {', '.join(jd_summary['skills'])}
- Experience Required: {jd_summary['experience_years']} years
- Key Requirements: {'; '.join(jd_summary['key_points'])}
- Target Roles: {', '.join(jd_summary['titles'])}

Resume Summary:
- Current Skills: {', '.join(resume_summary['skills'])}
- Experience: {resume_summary['experience_years']} years  
- Key Points: {'; '.join(resume_summary['key_points'])}
- Roles: {', '.join(resume_summary['titles'])}

Respond with this exact JSON structure:
{{
  "match_score": <0-100 integer>,
  "alignment_strength": "<excellent|good|moderate|weak>",
  "top_matched_skills": [<array of up to 5 strings>],
  "critical_missing_skills": [<array of up to 3 strings>],
  "experience_assessment": "<exceeds|meets|below> requirements",
  "improvement_priority": "<skills|experience|presentation>",
  "quick_wins": [<array of up to 3 actionable suggestions, each max 15 words>],
  "ats_optimization_tip": "<one specific tip for ATS systems, max 20 words>",
  "role_fit_reason": "<why this role fits/doesn't fit, max 25 words>"
}}

Respond ONLY with the JSON, no other text."""

        return prompt

    async def get_llm_insights(self, resume_text: str, jd_text: str, 
                              user_id: str = "default", is_premium: bool = False) -> Optional[Dict[str, Any]]:
        """Get AI-powered insights with usage limits and automatic model selection"""
        
        # Check if any LLM models are available
        available_models = self.model_registry.get_available_models()
        if not available_models:
            return {
                "error": "no_models_available",
                "message": "No LLM models configured. Please set up API keys for OpenAI, Anthropic, Groq, or Ollama.",
                "available_models": []
            }
        
        # Check usage limits
        if not self.check_usage_limit(user_id, is_premium):
            return {
                "error": "daily_limit_exceeded",
                "message": "Free tier daily limit reached. Upgrade to premium for unlimited AI insights.",
                "limit": self.config.free_tier_daily_limit,
                "available_models": available_models
            }
        
        try:
            # Create optimized summaries
            resume_summary, jd_summary = self.summarizer.create_summary(resume_text, jd_text)
            
            # Create structured prompt
            prompt = self.create_structured_prompt(resume_summary, jd_summary)
            
            # Choose models based on user tier
            preferred_models = (
                self.config.premium_tier_models if is_premium 
                else self.config.free_tier_models
            )
            
            # Filter to only available models
            available_preferred = [m for m in preferred_models if m in available_models]
            
            if not available_preferred:
                available_preferred = available_models  # Fallback to any available
            
            # Generate with automatic fallback
            response: LLMResponse = await self.model_registry.generate_with_fallback(
                prompt=prompt,
                preferred_models=available_preferred,
                max_tokens=self.config.max_tokens_per_call
            )
            
            if not response.success:
                return {
                    "error": "all_models_failed",
                    "message": f"All available models failed: {response.error}",
                    "attempted_models": available_preferred
                }
            
            # Parse response
            try:
                llm_insights = json.loads(response.content)
            except json.JSONDecodeError:
                # Try to extract JSON from response if it's wrapped in other text
                import re
                json_match = re.search(r'\{.*\}', response.content, re.DOTALL)
                if json_match:
                    llm_insights = json.loads(json_match.group())
                else:
                    raise json.JSONDecodeError("No valid JSON found", response.content, 0)
            
            # Increment usage counter
            self.increment_usage(user_id)
            
            # Add metadata
            llm_insights["tokens_used"] = response.tokens_used
            llm_insights["model_used"] = response.model_used
            llm_insights["provider"] = response.provider
            llm_insights["cost"] = response.cost
            llm_insights["response_time"] = response.response_time
            llm_insights["timestamp"] = datetime.now().isoformat()
            
            return llm_insights
            
        except json.JSONDecodeError as e:
            return {
                "error": "invalid_json_response",
                "message": "AI returned invalid JSON format. Basic analytics still available.",
                "raw_response": response.content[:200] if 'response' in locals() else "N/A"
            }
        except Exception as e:
            return {
                "error": "llm_error", 
                "message": f"AI analysis failed: {str(e)[:100]}",
                "fallback": True
            }

    def create_fallback_insights(self, analytics_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create basic AI-style insights from existing analytics when LLM fails"""
        
        similarity = analytics_data.get('similarity_score', 0) * 100
        matched_skills = analytics_data.get('matched_skills', {})
        missing_skills = analytics_data.get('missing_skills', {})
        
        # Generate fallback insights
        if similarity >= 80:
            alignment = "excellent"
            priority = "presentation"
        elif similarity >= 60:
            alignment = "good"
            priority = "skills"
        elif similarity >= 40:
            alignment = "moderate"
            priority = "skills"
        else:
            alignment = "weak"
            priority = "experience"
        
        # Extract top skills
        all_matched = []
        for category, skills in matched_skills.items():
            all_matched.extend(skills)
        
        all_missing = []
        for category, skills in missing_skills.items():
            all_missing.extend(skills[:2])  # Top 2 from each category
        
        return {
            "match_score": int(similarity),
            "alignment_strength": alignment,
            "top_matched_skills": all_matched[:5],
            "critical_missing_skills": all_missing[:3],
            "experience_assessment": "meets",
            "improvement_priority": priority,
            "quick_wins": [
                "Add missing keywords to resume",
                "Quantify achievements with numbers",
                "Optimize for ATS readability"
            ],
            "ats_optimization_tip": "Use exact keywords from job description",
            "role_fit_reason": f"Good technical match with {int(similarity)}% compatibility",
            "source": "fallback_analysis",
            "timestamp": datetime.now().isoformat()
        }

    async def enhanced_analysis(self, resume_text: str, jd_text: str, 
                               analytics_data: Dict[str, Any],
                               user_id: str = "default", 
                               is_premium: bool = False) -> Dict[str, Any]:
        """Combine existing analytics with LLM insights"""
        
        # Try to get LLM insights
        llm_insights = await self.get_llm_insights(resume_text, jd_text, user_id, is_premium)
        
        # If LLM failed or unavailable, use fallback
        if not llm_insights or "error" in llm_insights:
            fallback_insights = self.create_fallback_insights(analytics_data)
            
            # Merge with existing analytics
            enhanced_data = analytics_data.copy()
            enhanced_data["ai_insights"] = fallback_insights
            
            if llm_insights and "error" in llm_insights:
                enhanced_data["ai_insights"]["llm_status"] = llm_insights
            
            return enhanced_data
        
        # Successfully got LLM insights
        enhanced_data = analytics_data.copy()
        enhanced_data["ai_insights"] = llm_insights
        enhanced_data["ai_insights"]["llm_status"] = "success"
        
        return enhanced_data

# Usage tracking and management
class UsageManager:
    """Manage LLM usage limits and tracking"""
    
    def __init__(self):
        self.usage_data = {}
    
    def get_usage_stats(self, user_id: str = "default") -> Dict[str, Any]:
        """Get user's current usage statistics"""
        today = datetime.now().date()
        user_key = f"{user_id}_{today}"
        
        current_usage = self.usage_data.get(user_key, 0)
        
        return {
            "daily_usage": current_usage,
            "daily_limit": LLMConfig().free_tier_daily_limit,
            "remaining": max(0, LLMConfig().free_tier_daily_limit - current_usage),
            "reset_time": (datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)).isoformat()
        }
