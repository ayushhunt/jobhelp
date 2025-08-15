from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import nltk
from collections import Counter
import PyPDF2
import docx
import io
import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string
from advanced_analytics import AdvancedAnalytics
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

# Initialize components
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()
analytics_engine = AdvancedAnalytics()  # Now uses modular provider system

app = FastAPI(title="JobHelp API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://192.168.1.7:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

def extract_text_from_pdf(file_bytes):
    """Extract text from PDF file"""
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(file_bytes):
    """Extract text from DOCX file"""
    doc = docx.Document(io.BytesIO(file_bytes))
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def preprocess_text(text: str) -> str:
    """Preprocess text by removing stopwords, punctuation, and lemmatizing"""
    # Convert to lowercase and remove punctuation
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    
    # Tokenize and remove stopwords
    tokens = word_tokenize(text)
    tokens = [token for token in tokens if token not in stop_words and token.isalpha()]
    
    # Lemmatize
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return " ".join(tokens)

def get_word_frequency(text: str) -> dict:
    """Get word frequency from text"""
    # Preprocess text
    processed_text = preprocess_text(text)
    words = word_tokenize(processed_text)
    return dict(Counter(words))

def calculate_similarity(text1: str, text2: str) -> float:
    """Calculate Jaccard similarity between two texts"""
    # Preprocess both texts
    set1 = set(preprocess_text(text1).split())
    set2 = set(preprocess_text(text2).split())
    
    # Calculate Jaccard similarity
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union > 0 else 0.0

@app.post("/analyze")
async def analyze_documents(
    resume_file: Optional[UploadFile] = File(None),
    job_description_file: Optional[UploadFile] = File(None),
    resume_text: Optional[str] = Form(None),
    job_description_text: Optional[str] = Form(None),
    use_ai: bool = Query(False, description="Enable AI-powered insights"),
    user_id: str = Query("default", description="User identifier for usage tracking"),
    is_premium: bool = Query(False, description="Whether user has premium access")
):
    """Analyze resume and job description with comprehensive analytics"""
    try:
        # Get resume text
        resume_content = ""
        if resume_file:
            file_bytes = await resume_file.read()
            if resume_file.filename.endswith('.pdf'):
                resume_content = extract_text_from_pdf(file_bytes)
            elif resume_file.filename.endswith('.docx'):
                resume_content = extract_text_from_docx(file_bytes)
            else:
                raise HTTPException(status_code=400, detail="Unsupported resume file format")
        elif resume_text:
            resume_content = resume_text
        else:
            raise HTTPException(status_code=400, detail="Resume content is required")

        # Get job description text
        jd_content = ""
        if job_description_file:
            file_bytes = await job_description_file.read()
            if job_description_file.filename.endswith('.pdf'):
                jd_content = extract_text_from_pdf(file_bytes)
            elif job_description_file.filename.endswith('.docx'):
                jd_content = extract_text_from_docx(file_bytes)
            else:
                raise HTTPException(status_code=400, detail="Unsupported job description file format")
        elif job_description_text:
            jd_content = job_description_text
        else:
            raise HTTPException(status_code=400, detail="Job description content is required")

        # Basic analytics (backward compatibility)
        resume_freq = get_word_frequency(resume_content)
        jd_freq = get_word_frequency(jd_content)
        similarity_score = calculate_similarity(resume_content, jd_content)

        # Find common and missing keywords
        jd_keywords = set(jd_freq.keys())
        resume_keywords = set(resume_freq.keys())
        common_keywords = jd_keywords.intersection(resume_keywords)
        missing_keywords = jd_keywords - resume_keywords

        # Advanced analytics - choose AI-enhanced or standard based on request
        if use_ai:
            advanced_analytics = await analytics_engine.comprehensive_analysis_with_ai(
                resume_content, jd_content, user_id, is_premium
            )
        else:
            advanced_analytics = analytics_engine.comprehensive_analysis(resume_content, jd_content)

        # Combine basic and advanced analytics
        result = {
            # Basic analytics (for backward compatibility)
            "similarity_score": similarity_score,
            "resume_word_frequency": resume_freq,
            "jd_word_frequency": jd_freq,
            "common_keywords": list(common_keywords),
            "missing_keywords": list(missing_keywords),
            
            # Advanced analytics
            "semantic_similarity_score": advanced_analytics["semantic_similarity_score"],
            "matched_skills": advanced_analytics["matched_skills"],
            "missing_skills": advanced_analytics["missing_skills"],
            "extra_skills": advanced_analytics["extra_skills"],
            "years_experience_required": advanced_analytics["years_experience_required"],
            "years_experience_resume": advanced_analytics["years_experience_resume"],
            "experience_gap": advanced_analytics["experience_gap"],
            "responsibility_coverage_score": advanced_analytics["responsibility_coverage_score"],
            "requirement_coverage_score": advanced_analytics["requirement_coverage_score"],
            "common_phrases": advanced_analytics["common_phrases"],
            "action_verb_analysis": advanced_analytics["action_verb_analysis"],
            "jd_readability": advanced_analytics["jd_readability"],
            "resume_readability": advanced_analytics["resume_readability"],
            "keyword_density": advanced_analytics["keyword_density"],
            "education_match": advanced_analytics["education_match"],
            "missing_certifications": advanced_analytics["missing_certifications"],
            "resume_sections": advanced_analytics["resume_sections"],
            "jd_sections": advanced_analytics["jd_sections"],
            "insights_summary": advanced_analytics["insights_summary"],
            
            # Enhanced experience analytics (if available)
            "experience_analysis": advanced_analytics.get("experience_analysis"),
            "role_duration_mapping": advanced_analytics.get("role_duration_mapping"),
            "career_progression": advanced_analytics.get("career_progression"),
            "employment_gaps": advanced_analytics.get("employment_gaps"),
            "experience_by_recency": advanced_analytics.get("experience_by_recency"),
            "skill_experience_mapping": advanced_analytics.get("skill_experience_mapping"),
            "career_stability": advanced_analytics.get("career_stability"),
            
            # AI insights (if available)
            "ai_insights": advanced_analytics.get("ai_insights"),
            "ai_enabled": use_ai
        }

        return result

    except Exception as e:
        print(f"Error in analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ai-usage")
async def get_ai_usage(user_id: str = Query("default", description="User identifier")):
    """Get AI usage statistics for a user"""
    try:
        usage_stats = analytics_engine.llm_analytics.usage_tracker
        today = f"{user_id}_{__import__('datetime').datetime.now().date()}"
        current_usage = usage_stats.get(today, 0)
        
        return {
            "user_id": user_id,
            "daily_usage": current_usage,
            "daily_limit": analytics_engine.llm_analytics.config.free_tier_daily_limit,
            "remaining": max(0, analytics_engine.llm_analytics.config.free_tier_daily_limit - current_usage),
            "can_use_ai": current_usage < analytics_engine.llm_analytics.config.free_tier_daily_limit
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ai-models")
async def get_available_models():
    """Get information about available AI models"""
    try:
        registry = analytics_engine.llm_analytics.model_registry
        available_models = registry.get_available_models()
        
        model_info = []
        for model_id in available_models:
            config = registry.models[model_id]
            model_info.append({
                "id": model_id,
                "name": config.name,
                "provider": config.provider,
                "cost_per_1k_tokens": config.cost_per_token,
                "max_tokens": config.max_tokens,
                "context_window": config.context_window,
                "speed_tier": config.speed_tier,
                "quality_tier": config.quality_tier
            })
        
        # Get optimal models for each tier
        optimal_free = registry.get_optimal_model("cost", "good")
        optimal_premium = registry.get_optimal_model("quality", "excellent")
        
        return {
            "available_models": model_info,
            "total_available": len(available_models),
            "recommended": {
                "free_tier": optimal_free,
                "premium_tier": optimal_premium
            },
            "free_tier_preference": analytics_engine.llm_analytics.config.free_tier_models,
            "premium_tier_preference": analytics_engine.llm_analytics.config.premium_tier_models
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ai-costs")
async def get_cost_comparison():
    """Get cost comparison between different models"""
    try:
        registry = analytics_engine.llm_analytics.model_registry
        available_models = registry.get_available_models()
        
        # Sample token counts for comparison
        sample_tokens = [100, 500, 1000, 5000]
        
        cost_comparison = {}
        for model_id in available_models:
            config = registry.models[model_id]
            costs = {}
            for tokens in sample_tokens:
                costs[f"{tokens}_tokens"] = f"${(tokens / 1000 * config.cost_per_token):.4f}"
            cost_comparison[model_id] = {
                "provider": config.provider,
                "cost_per_1k_tokens": f"${config.cost_per_token:.4f}",
                "sample_costs": costs,
                "quality_tier": config.quality_tier,
                "speed_tier": config.speed_tier
            }
        
        return {
            "cost_comparison": cost_comparison,
            "note": "Costs shown are estimates. Actual costs may vary based on usage patterns."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "JobHelp AI API is running", "version": "3.0.0", "features": ["NLP Analytics", "Experience Parser", "AI Insights"]}