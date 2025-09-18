import { apiClient } from './api';

// Auth request/response types
export interface RegisterRequest {
  email: string;
  password: string;
  full_name: string;
  role: 'admin' | 'applicant' | 'recruiter';
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface ForgotPasswordRequest {
  email: string;
}

export interface ResetPasswordRequest {
  token: string;
  new_password: string;
}

export interface User {
  id: number;
  email: string;
  full_name: string;
  role: 'admin' | 'applicant' | 'recruiter';
  auth_provider: 'local' | 'google' | 'github';
  is_active: boolean;
  is_verified: boolean;
  created_at: string;
  last_login?: string;
}

export interface AuthResponse {
  message: string;
  user: User;
}

export interface ApiError {
  detail: string;
  status?: number;
}

// Auth service class
export class AuthService {
  // Register new user
  static async register(data: RegisterRequest): Promise<AuthResponse> {
    try {
      const response = await apiClient.post('/auth/register', data);
      return response.data;
    } catch (error: any) {
      throw this.handleAuthError(error);
    }
  }

  // Login user
  static async login(data: LoginRequest): Promise<AuthResponse> {
    try {
      const response = await apiClient.post('/auth/login', data);
      return response.data;
    } catch (error: any) {
      throw this.handleAuthError(error);
    }
  }

  // Logout user
  static async logout(): Promise<{ message: string }> {
    try {
      const response = await apiClient.post('/auth/logout');
      return response.data;
    } catch (error: any) {
      throw this.handleAuthError(error);
    }
  }

  // Get current user
  static async getCurrentUser(): Promise<User> {
    try {
      const response = await apiClient.get('/auth/me');
      return response.data;
    } catch (error: any) {
      throw this.handleAuthError(error);
    }
  }

  // Forgot password
  static async forgotPassword(data: ForgotPasswordRequest): Promise<{ message: string }> {
    try {
      const response = await apiClient.post('/auth/forgot-password', data);
      return response.data;
    } catch (error: any) {
      throw this.handleAuthError(error);
    }
  }

  // Reset password
  static async resetPassword(data: ResetPasswordRequest): Promise<{ message: string }> {
    try {
      const response = await apiClient.post('/auth/reset-password', data);
      return response.data;
    } catch (error: any) {
      throw this.handleAuthError(error);
    }
  }

  // Verify email
  static async verifyEmail(token: string): Promise<{ message: string }> {
    try {
      const response = await apiClient.post(`/auth/verify-email?token=${encodeURIComponent(token)}`);
      return response.data;
    } catch (error: any) {
      throw this.handleAuthError(error);
    }
  }

  // Resend verification email
  static async resendVerification(): Promise<{ message: string }> {
    try {
      const response = await apiClient.post('/auth/resend-verification');
      return response.data;
    } catch (error: any) {
      throw this.handleAuthError(error);
    }
  }

  // Refresh token
  static async refreshToken(): Promise<any> {
    try {
      const response = await apiClient.post('/auth/refresh');
      return response.data;
    } catch (error: any) {
      throw this.handleAuthError(error);
    }
  }

  // Social login stubs (for future implementation)
  static async googleLogin(): Promise<void> {
    // TODO: Implement Google OAuth flow
    console.log('Google login clicked - implement OAuth flow');
    // window.location.href = `${process.env.NEXT_PUBLIC_API_URL}/api/v1/auth/google`;
  }

  static async githubLogin(): Promise<void> {
    // TODO: Implement GitHub OAuth flow
    console.log('GitHub login clicked - implement OAuth flow');
    // window.location.href = `${process.env.NEXT_PUBLIC_API_URL}/api/v1/auth/github`;
  }

  static async linkedinLogin(): Promise<void> {
    // TODO: Implement LinkedIn OAuth flow
    console.log('LinkedIn login clicked - implement OAuth flow');
    // Note: LinkedIn OAuth would need to be implemented in backend first
  }

  // Handle authentication errors
  private static handleAuthError(error: any): ApiError {
    if (error.response) {
      // Server responded with error status
      const status = error.response.status;
      const message = error.response.data?.detail || error.response.data?.message || 'Authentication failed';
      
      return {
        detail: message,
        status: status
      };
    } else if (error.request) {
      // Request was made but no response received
      return {
        detail: 'Network error. Please check your connection and try again.',
        status: 0
      };
    } else {
      // Something else happened
      return {
        detail: error.message || 'An unexpected error occurred',
        status: 0
      };
    }
  }

  // Utility functions for form validation
  static validateEmail(email: string): boolean {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }

  static validatePassword(password: string): {
    isValid: boolean;
    errors: string[];
  } {
    const errors: string[] = [];
    
    if (password.length < 8) {
      errors.push('Password must be at least 8 characters long');
    }
    
    if (!/[A-Z]/.test(password)) {
      errors.push('Password must contain at least one uppercase letter');
    }
    
    if (!/[a-z]/.test(password)) {
      errors.push('Password must contain at least one lowercase letter');
    }
    
    if (!/[0-9]/.test(password)) {
      errors.push('Password must contain at least one number');
    }
    
    return {
      isValid: errors.length === 0,
      errors
    };
  }

  static validatePasswordMatch(password: string, confirmPassword: string): boolean {
    return password === confirmPassword;
  }

  static validateFullName(fullName: string): boolean {
    return fullName.trim().length >= 2;
  }
}

export default AuthService;
