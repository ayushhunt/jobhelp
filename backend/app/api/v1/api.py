"""
Main API router for v1 endpoints
"""
from fastapi import APIRouter
from app.api.v1.endpoints import analysis, llm, company_research, auth, oauth

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
api_router.include_router(llm.router, prefix="/llm", tags=["llm"])
api_router.include_router(company_research.router, prefix="/company-research", tags=["company-research"])

# Authentication endpoints
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(oauth.router, prefix="/auth", tags=["oauth"])
