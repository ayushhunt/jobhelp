"""
Authentication endpoints
Handles user registration, login, logout, and token management
"""
from datetime import timedelta
from typing import Any, Dict
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request, Cookie
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.simple_auth_middleware import require_auth
from app.services.auth.auth_service import auth_service
from app.services.auth.oauth_service import oauth_service
from app.models.entities.user import User
from app.models.schemas.auth import (
    UserRegister, 
    UserLogin, 
    UserResponse, 
    TokenResponse, 
    AuthResponse,
    PasswordReset,
    PasswordResetConfirm,
    RefreshTokenRequest
)
from app.config.settings import settings

router = APIRouter()

@router.post("/register", response_model=AuthResponse)
async def register(
    user_data: UserRegister,
    response: Response,
    db: Session = Depends(get_db)
):
    """Register a new user with email/password"""
    try:
        # Create user
        user = auth_service.register_user(user_data, db)
        
        # Generate tokens
        tokens = auth_service.jwt_service.create_token_pair(user)
        
        # Set HTTP-only cookies
        _set_auth_cookies(response, tokens)
        
        return AuthResponse(
            message="Registration successful. Please verify your email.",
            user=UserResponse.from_orm(user)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )

@router.post("/login", response_model=AuthResponse)
async def login(
    credentials: UserLogin,
    response: Response,
    db: Session = Depends(get_db)
):
    """Login with email/password"""
    try:
        # Authenticate user
        user = auth_service.authenticate_user(credentials, db)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Generate tokens
        tokens = auth_service.jwt_service.create_token_pair(user)
        
        # Set HTTP-only cookies
        _set_auth_cookies(response, tokens)
        
        return AuthResponse(
            message="Login successful",
            user=UserResponse.from_orm(user)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )

@router.post("/logout")
async def logout(response: Response):
    """Logout user by clearing cookies"""
    response.delete_cookie(key="access_token", httponly=True, secure=True, samesite="lax")
    response.delete_cookie(key="refresh_token", httponly=True, secure=True, samesite="lax")
    return {"message": "Logged out successfully"}

@router.post("/refresh", response_model=Dict[str, Any])
async def refresh_token(
    response: Response,
    refresh_token: str = Cookie(None),
    db: Session = Depends(get_db)
):
    """Refresh access token using refresh token"""
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token required"
        )
    
    try:
        # Generate new access token
        new_tokens = auth_service.refresh_access_token(refresh_token, db)
        if not new_tokens:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token"
            )
        
        # Update access token cookie
        response.set_cookie(
            key="access_token",
            value=new_tokens["access_token"],
            max_age=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            httponly=True,
            secure=True,
            samesite="lax"
        )
        
        return new_tokens
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Token refresh failed: {str(e)}"
        )

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(require_auth)
):
    """Get current user information with automatic token refresh"""
    return UserResponse.from_orm(current_user)

@router.post("/forgot-password")
async def forgot_password(
    password_reset: PasswordReset,
    db: Session = Depends(get_db)
):
    """Initiate password reset process"""
    try:
        user = auth_service.initiate_password_reset(password_reset.email, db)
        
        # Always return success for security (don't reveal if email exists)
        return {
            "message": "If the email exists, a password reset link has been sent"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Password reset request failed"
        )

@router.post("/reset-password")
async def reset_password(
    reset_data: PasswordResetConfirm,
    db: Session = Depends(get_db)
):
    """Reset password with token"""
    try:
        user = auth_service.reset_password(
            reset_data.token, 
            reset_data.new_password, 
            db
        )
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset token"
            )
        
        return {"message": "Password reset successful"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Password reset failed"
        )

@router.post("/verify-email")
async def verify_email(
    token: str,
    db: Session = Depends(get_db)
):
    """Verify email with token"""
    try:
        user = auth_service.verify_email(token, db)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired verification token"
            )
        
        return {"message": "Email verified successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Email verification failed"
        )

@router.post("/resend-verification")
async def resend_verification(
    current_user: User = Depends(require_auth),
    db: Session = Depends(get_db)
):
    """Resend email verification"""
    if current_user.is_verified:
        return {"message": "Email is already verified"}
    
    try:
        # Generate new verification token
        verification_token = auth_service.jwt_service.generate_verification_token()
        current_user.verification_token = verification_token
        db.commit()
        
        # Send verification email
        try:
            from app.services.email_service import email_service
            if email_service:
                email_service.send_verification_email(
                    current_user.email, 
                    current_user.full_name or "User", 
                    verification_token
                )
        except Exception as e:
            print(f"Failed to send verification email: {str(e)}")
        
        return {"message": "Verification email sent"}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send verification email"
        )

def _set_auth_cookies(response: Response, tokens: Dict[str, Any]) -> None:
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

