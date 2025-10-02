"""
JWT Authentication Service
Handles token creation, validation, and refresh functionality
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
import secrets

from app.config.settings import settings
from app.models.entities.user import User

class JWTService:
    """JWT token management service"""
    
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.secret_key = settings.JWT_SECRET_KEY
        self.algorithm = settings.JWT_ALGORITHM
        self.access_token_expire_minutes = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        self.refresh_token_expire_days = settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS
    
    def hash_password(self, password: str) -> str:
        """Hash a password"""
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def create_access_token(self, user: User) -> str:
        """Create JWT access token"""
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        payload = {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role.value,
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "access"
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def create_refresh_token(self, user: User) -> str:
        """Create JWT refresh token"""
        expire = datetime.utcnow() + timedelta(days=self.refresh_token_expire_days)
        payload = {
            "sub": str(user.id),
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "refresh",
            "jti": secrets.token_urlsafe(32)  # Unique token ID
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def create_token_pair(self, user: User) -> Dict[str, Any]:
        """Create access and refresh token pair"""
        access_token = self.create_access_token(user)
        refresh_token = self.create_refresh_token(user)
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": self.access_token_expire_minutes * 60
        }
    
    def decode_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Decode and validate JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            return None
    
    def validate_access_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Validate access token and return payload"""
        payload = self.decode_token(token)
        if payload and payload.get("type") == "access":
            return payload
        return None
    
    def validate_refresh_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Validate refresh token and return payload"""
        payload = self.decode_token(token)
        if payload and payload.get("type") == "refresh":
            return payload
        return None
    
    def generate_password_reset_token(self) -> str:
        """Generate secure password reset token"""
        return secrets.token_urlsafe(32)
    
    def generate_verification_token(self) -> str:
        """Generate email verification token"""
        return secrets.token_urlsafe(32)

# Global JWT service instance
jwt_service = JWTService()

