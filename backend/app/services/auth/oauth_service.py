"""
OAuth Service
Handles OAuth authentication with Google and other providers
"""
from typing import Optional, Dict, Any
import httpx
from fastapi import HTTPException, status
from authlib.integrations.starlette_client import OAuth
from authlib.integrations.starlette_client import OAuthError

from app.config.settings import settings
from app.models.entities.user import AuthProvider
from app.models.schemas.auth import OAuthUserInfo

class OAuthService:
    """OAuth authentication service"""
    
    def __init__(self):
        self.oauth = OAuth()
        self._setup_providers()
    
    def _setup_providers(self):
        """Setup OAuth providers"""
        # Google OAuth
        if settings.GOOGLE_CLIENT_ID and settings.GOOGLE_CLIENT_SECRET:
            self.oauth.register(
                name='google',
                client_id=settings.GOOGLE_CLIENT_ID,
                client_secret=settings.GOOGLE_CLIENT_SECRET,
                server_metadata_url='https://accounts.google.com/.well-known/openid_configuration',
                client_kwargs={
                    'scope': 'openid email profile'
                }
            )
        
        # GitHub OAuth (for future implementation)
        if settings.GITHUB_CLIENT_ID and settings.GITHUB_CLIENT_SECRET:
            self.oauth.register(
                name='github',
                client_id=settings.GITHUB_CLIENT_ID,
                client_secret=settings.GITHUB_CLIENT_SECRET,
                access_token_url='https://github.com/login/oauth/access_token',
                access_token_params=None,
                authorize_url='https://github.com/login/oauth/authorize',
                authorize_params=None,
                api_base_url='https://api.github.com/',
                client_kwargs={'scope': 'user:email'},
            )
    
    async def get_google_login_url(self, request, redirect_uri: str):
        """Get Google OAuth login URL"""
        try:
            google = self.oauth.create_client('google')
            return await google.authorize_redirect(request, redirect_uri)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to generate Google login URL: {str(e)}"
            )
    
    async def handle_google_callback(self, request) -> OAuthUserInfo:
        """Handle Google OAuth callback"""
        try:
            google = self.oauth.create_client('google')
            token = await google.authorize_access_token(request)
            
            # Get user info from Google
            user_info = token.get('userinfo')
            if not user_info:
                # Fallback: fetch user info manually
                async with httpx.AsyncClient() as client:
                    response = await client.get(
                        'https://www.googleapis.com/oauth2/v2/userinfo',
                        headers={'Authorization': f'Bearer {token["access_token"]}'}
                    )
                    user_info = response.json()
            
            # Create OAuth user info
            oauth_user = OAuthUserInfo(
                email=user_info['email'],
                name=user_info.get('name'),
                provider=AuthProvider.GOOGLE,
                provider_id=user_info['id'],
                verified=user_info.get('verified_email', False)
            )
            
            return oauth_user
            
        except OAuthError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"OAuth authentication failed: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Authentication error: {str(e)}"
            )
    
    async def handle_github_callback(self, request) -> OAuthUserInfo:
        """Handle GitHub OAuth callback (for future implementation)"""
        try:
            github = self.oauth.create_client('github')
            token = await github.authorize_access_token(request)
            
            # Get user info from GitHub
            async with httpx.AsyncClient() as client:
                # Get user profile
                user_response = await client.get(
                    'https://api.github.com/user',
                    headers={'Authorization': f'token {token["access_token"]}'}
                )
                user_data = user_response.json()
                
                # Get user email (GitHub may not provide email in profile)
                email_response = await client.get(
                    'https://api.github.com/user/emails',
                    headers={'Authorization': f'token {token["access_token"]}'}
                )
                emails = email_response.json()
                
                # Find primary email
                primary_email = None
                for email_info in emails:
                    if email_info.get('primary', False):
                        primary_email = email_info['email']
                        break
                
                if not primary_email and emails:
                    primary_email = emails[0]['email']
            
            oauth_user = OAuthUserInfo(
                email=primary_email,
                name=user_data.get('name') or user_data.get('login'),
                provider=AuthProvider.GITHUB,
                provider_id=str(user_data['id']),
                verified=True  # GitHub emails are considered verified
            )
            
            return oauth_user
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"GitHub authentication error: {str(e)}"
            )

# Global OAuth service instance
oauth_service = OAuthService()
