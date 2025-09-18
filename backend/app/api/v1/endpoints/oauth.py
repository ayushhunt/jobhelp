"""
OAuth endpoints for Google and GitHub authentication
"""
from fastapi import APIRouter, Request, HTTPException, status, Response, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.auth.auth_service import auth_service
from app.services.auth.oauth_service import oauth_service
from app.models.schemas.auth import UserResponse, TokenResponse, AuthResponse
from app.config.settings import settings

router = APIRouter()

@router.get("/google/login")
async def google_login(request: Request):
    """Initiate Google OAuth login"""
    try:
        if not settings.GOOGLE_CLIENT_ID or not settings.GOOGLE_CLIENT_SECRET:
            raise HTTPException(
                status_code=status.HTTP_501_NOT_IMPLEMENTED,
                detail="Google OAuth not configured"
            )
        
        # Generate redirect URI
        redirect_uri = f"{request.url_for('google_callback')}"
        
        # Get Google OAuth client
        google = oauth_service.oauth.create_client('google')
        
        # Redirect to Google OAuth
        return await google.authorize_redirect(request, redirect_uri)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to initiate Google login: {str(e)}"
        )

@router.get("/google/callback")
async def google_callback(
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    """Handle Google OAuth callback"""
    try:
        # Handle OAuth callback
        oauth_user_info = await oauth_service.handle_google_callback(request)
        
        # Create or get user
        user = auth_service.create_oauth_user(oauth_user_info, db)
        
        # Generate tokens
        tokens = auth_service.jwt_service.create_token_pair(user)
        
        # Set HTTP-only cookies
        _set_auth_cookies(response, tokens)
        
        # Redirect to frontend with success
        frontend_url = f"{settings.FRONTEND_URL}/auth/success"
        return RedirectResponse(url=frontend_url, status_code=302)
        
    except HTTPException:
        # Redirect to frontend with error
        frontend_url = f"{settings.FRONTEND_URL}/auth/error"
        return RedirectResponse(url=frontend_url, status_code=302)
    except Exception as e:
        # Redirect to frontend with error
        frontend_url = f"{settings.FRONTEND_URL}/auth/error"
        return RedirectResponse(url=frontend_url, status_code=302)

@router.get("/github/login")
async def github_login(request: Request):
    """Initiate GitHub OAuth login"""
    try:
        if not settings.GITHUB_CLIENT_ID or not settings.GITHUB_CLIENT_SECRET:
            raise HTTPException(
                status_code=status.HTTP_501_NOT_IMPLEMENTED,
                detail="GitHub OAuth not configured"
            )
        
        # Generate redirect URI
        redirect_uri = f"{request.url_for('github_callback')}"
        
        # Get GitHub OAuth client
        github = oauth_service.oauth.create_client('github')
        
        # Redirect to GitHub OAuth
        return await github.authorize_redirect(request, redirect_uri)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to initiate GitHub login: {str(e)}"
        )

@router.get("/github/callback")
async def github_callback(
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    """Handle GitHub OAuth callback"""
    try:
        # Handle OAuth callback
        oauth_user_info = await oauth_service.handle_github_callback(request)
        
        # Create or get user
        user = auth_service.create_oauth_user(oauth_user_info, db)
        
        # Generate tokens
        tokens = auth_service.jwt_service.create_token_pair(user)
        
        # Set HTTP-only cookies
        _set_auth_cookies(response, tokens)
        
        # Redirect to frontend with success
        frontend_url = f"{settings.FRONTEND_URL}/auth/success"
        return RedirectResponse(url=frontend_url, status_code=302)
        
    except HTTPException:
        # Redirect to frontend with error
        frontend_url = f"{settings.FRONTEND_URL}/auth/error"
        return RedirectResponse(url=frontend_url, status_code=302)
    except Exception as e:
        # Redirect to frontend with error
        frontend_url = f"{settings.FRONTEND_URL}/auth/error"
        return RedirectResponse(url=frontend_url, status_code=302)

def _set_auth_cookies(response: Response, tokens: dict) -> None:
    """Set authentication cookies"""
    # Access token cookie (30 minutes)
    response.set_cookie(
        key="access_token",
        value=tokens["access_token"],
        max_age=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        httponly=True,
        secure=True,  # HTTPS only in production
        samesite="lax"
    )
    
    # Refresh token cookie (7 days)
    response.set_cookie(
        key="refresh_token",
        value=tokens["refresh_token"],
        max_age=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        httponly=True,
        secure=True,  # HTTPS only in production
        samesite="lax"
    )

