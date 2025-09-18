"""
User entity model for authentication and authorization
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Enum
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class UserRole(str, enum.Enum):
    """User roles for authorization"""
    ADMIN = "admin"
    APPLICANT = "applicant"
    RECRUITER = "recruiter"

class AuthProvider(str, enum.Enum):
    """Authentication providers"""
    LOCAL = "local"
    GOOGLE = "google"
    GITHUB = "github"

class User(Base):
    """User entity model with authentication support"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=True)
    
    # Authentication fields
    hashed_password = Column(String(255), nullable=True)  # Nullable for OAuth users
    auth_provider = Column(Enum(AuthProvider, values_callable=lambda obj: [e.value for e in obj]), default=AuthProvider.LOCAL, nullable=False)
    provider_id = Column(String(255), nullable=True, index=True)  # External provider ID
    
    # Authorization and status
    role = Column(Enum(UserRole, values_callable=lambda obj: [e.value for e in obj]), default=UserRole.APPLICANT, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    
    # Security fields
    password_reset_token = Column(String(255), nullable=True)
    password_reset_expires = Column(DateTime(timezone=True), nullable=True)
    verification_token = Column(String(255), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', role='{self.role}')>"
