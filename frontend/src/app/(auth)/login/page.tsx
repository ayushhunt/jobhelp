'use client'

import React, { useState, useEffect } from 'react'
import Link from 'next/link'
import { useRouter, useSearchParams } from 'next/navigation'
import AuthLayout from '@/components/auth/AuthLayout'
import { InputField, PasswordField, SubmitButton, SocialButton } from '@/components/auth/FormComponents'
import AuthService, { LoginRequest, ApiError } from '@/services/auth'

export default function LoginPage() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  })
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [loading, setLoading] = useState(false)
  const [successMessage, setSuccessMessage] = useState('')

  // Check for registration success message
  useEffect(() => {
    if (searchParams.get('registered') === 'true') {
      setSuccessMessage('Registration successful! Please check your email for verification.')
    }
  }, [searchParams])

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {}

    // Email validation
    if (!AuthService.validateEmail(formData.email)) {
      newErrors.email = 'Please enter a valid email address'
    }

    // Password validation (basic check for login)
    if (!formData.password || formData.password.length < 1) {
      newErrors.password = 'Password is required'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!validateForm()) return

    setLoading(true)
    setErrors({})
    setSuccessMessage('')

    try {
      const loginData: LoginRequest = {
        email: formData.email,
        password: formData.password
      }

      const response = await AuthService.login(loginData)
      
      // Redirect to dashboard or home page after successful login
      router.push('/dashboard')

    } catch (error) {
      const apiError = error as ApiError
      
      // Handle specific error cases
      if (apiError.status === 403 && apiError.detail.includes('verification')) {
        setErrors({ submit: 'Please verify your email before logging in. Check your inbox for the verification link.' })
      } else if (apiError.status === 401) {
        setErrors({ submit: 'Invalid email or password. Please try again.' })
      } else {
        setErrors({ submit: apiError.detail })
      }
    } finally {
      setLoading(false)
    }
  }

  const handleSocialLogin = {
    google: () => AuthService.googleLogin(),
    github: () => AuthService.githubLogin(),
    linkedin: () => AuthService.linkedinLogin()
  }

  return (
    <AuthLayout
      title="Welcome Back"
      subtitle="Sign in to your JobHelp AI account"
    >
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Success Message */}
        {successMessage && (
          <div className="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-4">
            <p className="text-green-800 dark:text-green-200 text-sm">{successMessage}</p>
          </div>
        )}

        {/* Error Message */}
        {errors.submit && (
          <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
            <p className="text-red-800 dark:text-red-200 text-sm">{errors.submit}</p>
            {errors.submit.includes('verification') && (
              <div className="mt-2">
                <button
                  type="button"
                  onClick={async () => {
                    try {
                      await AuthService.resendVerification()
                      setSuccessMessage('Verification email sent! Please check your inbox.')
                      setErrors({})
                    } catch (error) {
                      console.error('Failed to resend verification:', error)
                    }
                  }}
                  className="text-sm text-blue-600 dark:text-blue-400 hover:underline"
                >
                  Resend verification email
                </button>
              </div>
            )}
          </div>
        )}

        {/* Email */}
        <InputField
          label="Email Address"
          type="email"
          value={formData.email}
          onChange={(value) => setFormData({ ...formData, email: value })}
          error={errors.email}
          placeholder="Enter your email address"
          required
          disabled={loading}
        />

        {/* Password */}
        <PasswordField
          label="Password"
          value={formData.password}
          onChange={(value) => setFormData({ ...formData, password: value })}
          error={errors.password}
          placeholder="Enter your password"
          required
          disabled={loading}
        />

        {/* Forgot Password Link */}
        <div className="flex justify-end">
          <Link 
            href="/forgot-password" 
            className="text-sm text-black dark:text-white hover:underline"
          >
            Forgot your password?
          </Link>
        </div>

        {/* Submit Button */}
        <SubmitButton loading={loading} disabled={loading}>
          Sign In
        </SubmitButton>

        {/* Divider */}
        <div className="relative">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-gray-300 dark:border-gray-600" />
          </div>
          <div className="relative flex justify-center text-sm">
            <span className="px-2 bg-white dark:bg-gray-800 text-gray-500 dark:text-gray-400">
              Or continue with
            </span>
          </div>
        </div>

        {/* Social Login Buttons */}
        <div className="space-y-3">
          <SocialButton 
            provider="google" 
            onClick={handleSocialLogin.google}
            disabled={loading}
          />
          <SocialButton 
            provider="github" 
            onClick={handleSocialLogin.github}
            disabled={loading}
          />
          <SocialButton 
            provider="linkedin" 
            onClick={handleSocialLogin.linkedin}
            disabled={loading}
          />
        </div>

        {/* Register Link */}
        <div className="text-center">
          <p className="text-sm text-gray-600 dark:text-gray-400">
            Don't have an account?{' '}
            <Link 
              href="/register" 
              className="font-medium text-black dark:text-white hover:underline"
            >
              Create one here
            </Link>
          </p>
        </div>
      </form>
    </AuthLayout>
  )
}
