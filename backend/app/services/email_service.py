"""
Email Service using Resend API
Handles email verification, password reset, and other notifications
"""
import resend
from typing import Optional, Dict, Any
from fastapi import HTTPException
from app.config.settings import settings

class EmailService:
    """Email service using Resend API"""
    
    def __init__(self):
        if not settings.RESEND_API_KEY:
            raise ValueError("RESEND_API_KEY is required for email service")
        resend.api_key = settings.RESEND_API_KEY
    
    def send_verification_email(self, email: str, full_name: str, verification_token: str) -> bool:
        """Send email verification email"""
        try:
            verification_url = f"{settings.FRONTEND_URL}/auth/verify-email?token={verification_token}"
            
            params: resend.Emails.SendParams = {
                "from": settings.EMAIL_FROM,
                "to": [email],
                "subject": "Verify your email - JobHelp AI",
                "html": self._get_verification_email_html(full_name, verification_url)
            }
            
            email_response: resend.Email = resend.Emails.send(params)
            return True
            
        except Exception as e:
            print(f"Failed to send verification email: {str(e)}")
            return False
    
    def send_password_reset_email(self, email: str, full_name: str, reset_token: str) -> bool:
        """Send password reset email"""
        try:
            reset_url = f"{settings.FRONTEND_URL}/auth/reset-password?token={reset_token}"
            
            params: resend.Emails.SendParams = {
                "from": settings.EMAIL_FROM,
                "to": [email],
                "subject": "Reset your password - JobHelp AI",
                "html": self._get_password_reset_email_html(full_name, reset_url)
            }
            
            email_response: resend.Email = resend.Emails.send(params)
            return True
            
        except Exception as e:
            print(f"Failed to send password reset email: {str(e)}")
            return False
    
    def send_welcome_email(self, email: str, full_name: str) -> bool:
        """Send welcome email after successful verification"""
        try:
            params: resend.Emails.SendParams = {
                "from": settings.EMAIL_FROM,
                "to": [email],
                "subject": "Welcome to JobHelp AI!",
                "html": self._get_welcome_email_html(full_name)
            }
            
            email_response: resend.Email = resend.Emails.send(params)
            return True
            
        except Exception as e:
            print(f"Failed to send welcome email: {str(e)}")
            return False
    
    def _get_verification_email_html(self, full_name: str, verification_url: str) -> str:
        """Get HTML template for email verification"""
        return f"""
        <html>
            <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px;">
                    <h2 style="color: #333; text-align: center;">Welcome to JobHelp AI!</h2>
                    
                    <p>Hi {full_name or 'there'},</p>
                    
                    <p>Thank you for registering with JobHelp AI. To complete your registration and start using our platform, please verify your email address by clicking the button below:</p>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{verification_url}" 
                           style="background-color: #007bff; color: white; padding: 12px 30px; 
                                  text-decoration: none; border-radius: 5px; display: inline-block;">
                            Verify Email Address
                        </a>
                    </div>
                    
                    <p>If the button doesn't work, you can also copy and paste this link into your browser:</p>
                    <p style="word-break: break-all; color: #666;">{verification_url}</p>
                    
                    <p>This verification link will expire in 24 hours for security reasons.</p>
                    
                    <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
                    
                    <p style="color: #666; font-size: 14px;">
                        If you didn't create an account with JobHelp AI, please ignore this email.
                    </p>
                    
                    <p style="color: #666; font-size: 14px;">
                        Best regards,<br>
                        The JobHelp AI Team
                    </p>
                </div>
            </body>
        </html>
        """
    
    def _get_password_reset_email_html(self, full_name: str, reset_url: str) -> str:
        """Get HTML template for password reset"""
        return f"""
        <html>
            <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px;">
                    <h2 style="color: #333; text-align: center;">Reset Your Password</h2>
                    
                    <p>Hi {full_name or 'there'},</p>
                    
                    <p>We received a request to reset your password for your JobHelp AI account. Click the button below to create a new password:</p>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{reset_url}" 
                           style="background-color: #dc3545; color: white; padding: 12px 30px; 
                                  text-decoration: none; border-radius: 5px; display: inline-block;">
                            Reset Password
                        </a>
                    </div>
                    
                    <p>If the button doesn't work, you can also copy and paste this link into your browser:</p>
                    <p style="word-break: break-all; color: #666;">{reset_url}</p>
                    
                    <p>This password reset link will expire in 1 hour for security reasons.</p>
                    
                    <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
                    
                    <p style="color: #666; font-size: 14px;">
                        If you didn't request a password reset, please ignore this email. Your password will remain unchanged.
                    </p>
                    
                    <p style="color: #666; font-size: 14px;">
                        Best regards,<br>
                        The JobHelp AI Team
                    </p>
                </div>
            </body>
        </html>
        """
    
    def _get_welcome_email_html(self, full_name: str) -> str:
        """Get HTML template for welcome email"""
        return f"""
        <html>
            <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px;">
                    <h2 style="color: #333; text-align: center;">Welcome to JobHelp AI! 🎉</h2>
                    
                    <p>Hi {full_name or 'there'},</p>
                    
                    <p>Congratulations! Your email has been verified and your JobHelp AI account is now active.</p>
                    
                    <p>You can now access all features of our platform:</p>
                    <ul>
                        <li>AI-powered resume analysis</li>
                        <li>Company research tools</li>
                        <li>Job application tracking</li>
                        <li>Interview preparation assistance</li>
                    </ul>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{settings.FRONTEND_URL}/dashboard" 
                           style="background-color: #28a745; color: white; padding: 12px 30px; 
                                  text-decoration: none; border-radius: 5px; display: inline-block;">
                            Get Started
                        </a>
                    </div>
                    
                    <p>If you have any questions or need help getting started, feel free to reach out to our support team.</p>
                    
                    <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
                    
                    <p style="color: #666; font-size: 14px;">
                        Best regards,<br>
                        The JobHelp AI Team
                    </p>
                </div>
            </body>
        </html>
        """

# Global email service instance
try:
    email_service = EmailService()
except ValueError:
    # If RESEND_API_KEY is not set, email_service will be None
    email_service = None
