"""
Main API router for v1 endpoints
"""
from fastapi import APIRouter
from app.api.v1.endpoints import analysis

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])

# Add more endpoint routers here as needed
# api_router.include_router(users.router, prefix="/users", tags=["users"])
# api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
