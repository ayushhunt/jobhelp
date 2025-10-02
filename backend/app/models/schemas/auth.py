"""
Authentication and authorization schemas
"""
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime
from app.models.entities.user import UserRole, AuthProvider

# Request schemas
class UserRegister(BaseModel):
    """User registration schema"""
    email: EmailStr
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")
    full_name: str = Field(..., description="Full name is required")
    role: UserRole = Field(default=UserRole.APPLICANT, description="User role")
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v

class UserLogin(BaseModel):
    """User login schema"""
    email: EmailStr
    password: str

class PasswordReset(BaseModel):
    """Password reset request schema"""
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    """Password reset confirmation schema"""
    token: str
    new_password: str = Field(..., min_length=8)

class PasswordChange(BaseModel):
    """Password change schema"""
    current_password: str
    new_password: str = Field(..., min_length=8)

# Response schemas
class UserResponse(BaseModel):
    """User response schema"""
    id: int
    email: str
    full_name: Optional[str]
    role: UserRole
    auth_provider: AuthProvider
    is_active: bool
    is_verified: bool
    created_at: datetime
    last_login: Optional[datetime]
    
    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    """Token response schema"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse

class AuthResponse(BaseModel):
    """Authentication response schema"""
    message: str
    user: UserResponse

class RefreshTokenRequest(BaseModel):
    """Refresh token request schema"""
    refresh_token: str

# OAuth schemas
class OAuthUserInfo(BaseModel):
    """OAuth user information schema"""
    email: str
    name: Optional[str] = None
    provider: AuthProvider
    provider_id: str
    verified: bool = False

