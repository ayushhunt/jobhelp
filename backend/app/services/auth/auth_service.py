"""
Authentication Service
Handles user authentication, registration, and session management
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.models.entities.user import User, UserRole, AuthProvider
from app.models.schemas.auth import UserRegister, UserLogin, OAuthUserInfo
from app.services.auth.jwt_service import jwt_service
from app.core.database import get_db

class AuthService:
    """Authentication service for user management"""
    
    def __init__(self):
        self.jwt_service = jwt_service
    
    def register_user(self, user_data: UserRegister, db: Session) -> User:
        """Register a new user with email/password"""
        try:
            # Check if user already exists
            existing_user = db.query(User).filter(User.email == user_data.email).first()
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User with this email already exists"
                )
            
            # Create new user
            hashed_password = self.jwt_service.hash_password(user_data.password)
            verification_token = self.jwt_service.generate_verification_token()
            
            user = User(
                email=user_data.email,
                full_name=user_data.full_name,
                hashed_password=hashed_password,
                auth_provider=AuthProvider.LOCAL,
                verification_token=verification_token,
                role=user_data.role
            )
            
            db.add(user)
            db.commit()
            db.refresh(user)
            
            # Send verification email
            try:
                from app.services.email_service import email_service
                if email_service:
                    email_service.send_verification_email(
                        user.email, 
                        user.full_name or "User", 
                        verification_token
                    )
            except Exception as e:
                # Log error but don't fail registration
                print(f"Failed to send verification email: {str(e)}")
            
            return user
            
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )
    
    def authenticate_user(self, credentials: UserLogin, db: Session) -> Optional[User]:
        """Authenticate user with email/password"""
        user = db.query(User).filter(
            User.email == credentials.email,
            User.auth_provider == AuthProvider.LOCAL
        ).first()
        
        if not user:
            return None
        
        if not user.hashed_password:
            return None
        
        if not self.jwt_service.verify_password(credentials.password, user.hashed_password):
            return None
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is deactivated"
            )
        
        # Update last login
        user.last_login = datetime.utcnow()
        db.commit()
        
        return user
    
    def create_oauth_user(self, oauth_info: OAuthUserInfo, db: Session) -> User:
        """Create or update user from OAuth provider"""
        try:
            # Check if user exists by email
            existing_user = db.query(User).filter(User.email == oauth_info.email).first()
            
            if existing_user:
                # Update existing user with OAuth info
                if existing_user.auth_provider != oauth_info.provider:
                    # User exists with different provider - link accounts
                    existing_user.provider_id = oauth_info.provider_id
                    existing_user.is_verified = oauth_info.verified
                else:
                    # Update provider info
                    existing_user.provider_id = oauth_info.provider_id
                
                existing_user.last_login = datetime.utcnow()
                db.commit()
                return existing_user
            
            # Create new OAuth user
            user = User(
                email=oauth_info.email,
                full_name=oauth_info.name,
                auth_provider=oauth_info.provider,
                provider_id=oauth_info.provider_id,
                is_verified=oauth_info.verified,
                role=UserRole.APPLICANT,
                last_login=datetime.utcnow()
            )
            
            db.add(user)
            db.commit()
            db.refresh(user)
            
            return user
            
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error creating user account"
            )
    
    def get_user_by_id(self, user_id: int, db: Session) -> Optional[User]:
        """Get user by ID"""
        return db.query(User).filter(User.id == user_id, User.is_active == True).first()
    
    def get_user_by_email(self, email: str, db: Session) -> Optional[User]:
        """Get user by email"""
        return db.query(User).filter(User.email == email, User.is_active == True).first()
    
    def refresh_access_token(self, refresh_token: str, db: Session) -> Optional[Dict[str, Any]]:
        """Generate new access token from refresh token"""
        payload = self.jwt_service.validate_refresh_token(refresh_token)
        if not payload:
            return None
        
        user_id = int(payload.get("sub"))
        user = self.get_user_by_id(user_id, db)
        
        if not user:
            return None
        
        # Generate new access token
        access_token = self.jwt_service.create_access_token(user)
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": self.jwt_service.access_token_expire_minutes * 60
        }
    
    def initiate_password_reset(self, email: str, db: Session) -> Optional[User]:
        """Initiate password reset process"""
        user = self.get_user_by_email(email, db)
        if not user or user.auth_provider != AuthProvider.LOCAL:
            return None
        
        # Generate reset token
        reset_token = self.jwt_service.generate_password_reset_token()
        reset_expires = datetime.utcnow() + timedelta(hours=1)  # 1 hour expiry
        
        user.password_reset_token = reset_token
        user.password_reset_expires = reset_expires
        
        db.commit()
        
        # Send password reset email
        try:
            from app.services.email_service import email_service
            if email_service:
                email_service.send_password_reset_email(
                    user.email, 
                    user.full_name or "User", 
                    reset_token
                )
        except Exception as e:
            # Log error but don't fail reset request
            print(f"Failed to send password reset email: {str(e)}")
        
        return user
    
    def reset_password(self, token: str, new_password: str, db: Session) -> Optional[User]:
        """Reset user password with token"""
        user = db.query(User).filter(
            User.password_reset_token == token,
            User.password_reset_expires > datetime.utcnow()
        ).first()
        
        if not user:
            return None
        
        # Update password and clear reset token
        user.hashed_password = self.jwt_service.hash_password(new_password)
        user.password_reset_token = None
        user.password_reset_expires = None
        
        db.commit()
        return user
    
    def verify_email(self, token: str, db: Session) -> Optional[User]:
        """Verify user email with token"""
        user = db.query(User).filter(User.verification_token == token).first()
        
        if not user:
            return None
        
        user.is_verified = True
        user.verification_token = None
        
        db.commit()
        
        # Send welcome email
        try:
            from app.services.email_service import email_service
            if email_service:
                email_service.send_welcome_email(
                    user.email, 
                    user.full_name or "User"
                )
        except Exception as e:
            # Log error but don't fail verification
            print(f"Failed to send welcome email: {str(e)}")
        
        return user

# Global auth service instance
auth_service = AuthService()

