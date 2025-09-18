'use client'

import React, { useState, useEffect } from 'react'
import Link from 'next/link'
import { useRouter, useSearchParams } from 'next/navigation'
import AuthLayout from '@/components/auth/AuthLayout'
import { PasswordField, PasswordMatch, SubmitButton } from '@/components/auth/FormComponents'
import AuthService, { ResetPasswordRequest, ApiError } from '@/services/auth'
import { CheckCircleIcon, XCircleIcon } from '@heroicons/react/24/outline'

export default function ResetPasswordPage() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const [formData, setFormData] = useState({
    password: '',
    confirmPassword: ''
  })
  const [token, setToken] = useState('')
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [loading, setLoading] = useState(false)
  const [isSubmitted, setIsSubmitted] = useState(false)
  const [tokenError, setTokenError] = useState('')

  // Extract token from URL params
  useEffect(() => {
    const tokenParam = searchParams.get('token')
    if (!tokenParam) {
      setTokenError('Invalid or missing reset token. Please request a new password reset.')
    } else {
      setToken(tokenParam)
    }
  }, [searchParams])

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {}

    // Password validation
    const passwordValidation = AuthService.validatePassword(formData.password)
    if (!passwordValidation.isValid) {
      newErrors.password = passwordValidation.errors[0]
    }

    // Password match validation
    if (!AuthService.validatePasswordMatch(formData.password, formData.confirmPassword)) {
      newErrors.confirmPassword = 'Passwords do not match'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!validateForm() || !token) return

    setLoading(true)
    setErrors({})

    try {
      const resetData: ResetPasswordRequest = {
        token: token,
        new_password: formData.password
      }

      const response = await AuthService.resetPassword(resetData)
      setIsSubmitted(true)

    } catch (error) {
      const apiError = error as ApiError
      
      if (apiError.status === 400 && apiError.detail.includes('token')) {
        setTokenError('This reset link has expired or is invalid. Please request a new password reset.')
      } else {
        setErrors({ submit: apiError.detail })
      }
    } finally {
      setLoading(false)
    }
  }

  // Show token error state
  if (tokenError) {
    return (
      <AuthLayout
        title="Invalid Reset Link"
        subtitle="This password reset link is no longer valid"
        showBackToHome={false}
      >
        <div className="text-center space-y-6">
          {/* Error Icon */}
          <div className="mx-auto w-16 h-16 bg-red-100 dark:bg-red-900/20 rounded-full flex items-center justify-center">
            <XCircleIcon className="w-8 h-8 text-red-600 dark:text-red-400" />
          </div>

          {/* Error Message */}
          <div className="space-y-2">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
              Link Expired
            </h2>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              {tokenError}
            </p>
          </div>

          {/* Actions */}
          <div className="space-y-3">
            <Link href="/auth/forgot-password">
              <SubmitButton type="button">
                Request New Reset Link
              </SubmitButton>
            </Link>
            
            <div>
              <Link 
                href="/auth/login" 
                className="text-sm text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors"
              >
                Back to Sign In
              </Link>
            </div>
          </div>
        </div>
      </AuthLayout>
    )
  }

  // Show success state
  if (isSubmitted) {
    return (
      <AuthLayout
        title="Password Reset Successful"
        subtitle="Your password has been updated"
        showBackToHome={false}
      >
        <div className="text-center space-y-6">
          {/* Success Icon */}
          <div className="mx-auto w-16 h-16 bg-green-100 dark:bg-green-900/20 rounded-full flex items-center justify-center">
            <CheckCircleIcon className="w-8 h-8 text-green-600 dark:text-green-400" />
          </div>

          {/* Success Message */}
          <div className="space-y-2">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
              All Set!
            </h2>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Your password has been successfully updated. You can now sign in with your new password.
            </p>
          </div>

          {/* Sign In Button */}
          <Link href="/auth/login">
            <SubmitButton type="button">
              Sign In Now
            </SubmitButton>
          </Link>
        </div>
      </AuthLayout>
    )
  }

  // Show reset form
  return (
    <AuthLayout
      title="Reset Your Password"
      subtitle="Enter your new password below"
      showBackToHome={false}
    >
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Error Message */}
        {errors.submit && (
          <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
            <p className="text-red-800 dark:text-red-200 text-sm">{errors.submit}</p>
          </div>
        )}

        {/* New Password */}
        <PasswordField
          label="New Password"
          value={formData.password}
          onChange={(value) => setFormData({ ...formData, password: value })}
          error={errors.password}
          placeholder="Enter your new password"
          required
          disabled={loading}
          showStrength
        />

        {/* Confirm New Password */}
        <div className="space-y-2">
          <PasswordField
            label="Confirm New Password"
            value={formData.confirmPassword}
            onChange={(value) => setFormData({ ...formData, confirmPassword: value })}
            error={errors.confirmPassword}
            placeholder="Confirm your new password"
            required
            disabled={loading}
          />
          <PasswordMatch 
            password={formData.password} 
            confirmPassword={formData.confirmPassword}
            showMatch={formData.password.length >= 8 && formData.confirmPassword.length > 0}
          />
        </div>

        {/* Password Requirements */}
        <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
          <p className="text-sm text-blue-800 dark:text-blue-200 font-medium mb-2">
            Password Requirements:
          </p>
          <ul className="text-sm text-blue-700 dark:text-blue-300 space-y-1">
            <li className={`flex items-center ${formData.password.length >= 8 ? 'text-green-600 dark:text-green-400' : ''}`}>
              <span className="mr-2">{formData.password.length >= 8 ? '✓' : '•'}</span>
              At least 8 characters long
            </li>
            <li className={`flex items-center ${/[A-Z]/.test(formData.password) ? 'text-green-600 dark:text-green-400' : ''}`}>
              <span className="mr-2">{/[A-Z]/.test(formData.password) ? '✓' : '•'}</span>
              One uppercase letter
            </li>
            <li className={`flex items-center ${/[a-z]/.test(formData.password) ? 'text-green-600 dark:text-green-400' : ''}`}>
              <span className="mr-2">{/[a-z]/.test(formData.password) ? '✓' : '•'}</span>
              One lowercase letter
            </li>
            <li className={`flex items-center ${/[0-9]/.test(formData.password) ? 'text-green-600 dark:text-green-400' : ''}`}>
              <span className="mr-2">{/[0-9]/.test(formData.password) ? '✓' : '•'}</span>
              One number
            </li>
          </ul>
        </div>

        {/* Submit Button */}
        <SubmitButton loading={loading} disabled={loading}>
          Update Password
        </SubmitButton>

        {/* Back to Login Link */}
        <div className="text-center">
          <Link 
            href="/auth/login" 
            className="text-sm text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors"
          >
            Remember your password? Sign in
          </Link>
        </div>
      </form>
    </AuthLayout>
  )
}
