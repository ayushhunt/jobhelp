"""
Simplified Authentication Middleware with Automatic Token Refresh
Handles role-based authentication with seamless token refresh
"""
from typing import Optional, List
from fastapi import HTTPException, status, Depends, Request, Response, Cookie
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.auth.jwt_service import jwt_service
from app.services.auth.auth_service import auth_service
from app.models.entities.user import User, UserRole
from app.config.settings import settings

# HTTP Bearer security scheme (optional)
security = HTTPBearer(auto_error=False)

class SimpleAuthMiddleware:
    """Simplified authentication middleware with automatic token refresh"""
    
    @staticmethod
    def _get_tokens_from_request(
        request: Request,
        access_token: Optional[str] = Cookie(None),
        refresh_token: Optional[str] = Cookie(None),
        authorization: Optional[HTTPAuthorizationCredentials] = Depends(security)
    ) -> tuple[Optional[str], Optional[str]]:
        """Extract access and refresh tokens from cookies or headers"""
        # Priority: Cookie > Authorization header
        access = access_token
        if not access and authorization:
            access = authorization.credentials
        
        return access, refresh_token
    
    @staticmethod
    def _set_access_token_cookie(response: Response, access_token: str) -> None:
        """Set access token in HTTP-only cookie"""
        response.set_cookie(
            key="access_token",
            value=access_token,
            max_age=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            httponly=True,
            secure=True,
            samesite="lax"
        )
    
    @staticmethod
    def _authenticate_with_refresh(
        access_token: Optional[str],
        refresh_token: Optional[str],
        response: Response,
        db: Session
    ) -> Optional[User]:
        """
        Authenticate user with automatic token refresh
        Returns user if authenticated, None if not
        """
        # Try access token first
        if access_token:
            payload = jwt_service.validate_access_token(access_token)
            if payload:
                user_id = int(payload.get("sub"))
                user = auth_service.get_user_by_id(user_id, db)
                if user and user.is_active:
                    return user
        
        # If access token is invalid/expired, try refresh token
        if refresh_token:
            payload = jwt_service.validate_refresh_token(refresh_token)
            if payload:
                user_id = int(payload.get("sub"))
                user = auth_service.get_user_by_id(user_id, db)
                if user and user.is_active:
                    # Generate new access token
                    new_access_token = jwt_service.create_access_token(user)
                    SimpleAuthMiddleware._set_access_token_cookie(response, new_access_token)
                    return user
        
        return None
    
    @staticmethod
    def create_auth_dependency(required_roles: Optional[List[UserRole]] = None, require_verified: bool = False):
        """
        Create authentication dependency for specific roles
        
        Args:
            required_roles: List of allowed roles (None = any authenticated user)
            require_verified: Whether email verification is required
        """
        def auth_dependency(
            request: Request,
            response: Response,
            db: Session = Depends(get_db),
            tokens: tuple = Depends(SimpleAuthMiddleware._get_tokens_from_request)
        ) -> User:
            access_token, refresh_token = tokens
            
            # Authenticate with automatic refresh
            user = SimpleAuthMiddleware._authenticate_with_refresh(
                access_token, refresh_token, response, db
            )
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            # Check if account is active
            if not user.is_active:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Account is deactivated"
                )
            
            # Check email verification if required
            if require_verified and not user.is_verified:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Email verification required"
                )
            
            # Check role permissions if specified
            if required_roles and user.role not in required_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions"
                )
            
            return user
        
        return auth_dependency

# Pre-configured authentication dependencies

# Basic authentication (any role)
require_auth = SimpleAuthMiddleware.create_auth_dependency()

# Role-specific authentication
require_admin = SimpleAuthMiddleware.create_auth_dependency([UserRole.ADMIN])
require_applicant = SimpleAuthMiddleware.create_auth_dependency([UserRole.APPLICANT])
require_recruiter = SimpleAuthMiddleware.create_auth_dependency([UserRole.RECRUITER])

# Multi-role authentication
require_applicant_or_recruiter = SimpleAuthMiddleware.create_auth_dependency([UserRole.APPLICANT, UserRole.RECRUITER])
require_admin_or_recruiter = SimpleAuthMiddleware.create_auth_dependency([UserRole.ADMIN, UserRole.RECRUITER])

# Verified user authentication
require_verified_user = SimpleAuthMiddleware.create_auth_dependency(require_verified=True)
require_verified_applicant = SimpleAuthMiddleware.create_auth_dependency([UserRole.APPLICANT], require_verified=True)
require_verified_recruiter = SimpleAuthMiddleware.create_auth_dependency([UserRole.RECRUITER], require_verified=True)

# Optional authentication (can return None)
def optional_auth(
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
    tokens: tuple = Depends(SimpleAuthMiddleware._get_tokens_from_request)
) -> Optional[User]:
    """Optional authentication - returns user if authenticated, None otherwise"""
    access_token, refresh_token = tokens
    
    try:
        return SimpleAuthMiddleware._authenticate_with_refresh(
            access_token, refresh_token, response, db
        )
    except Exception:
        return None
