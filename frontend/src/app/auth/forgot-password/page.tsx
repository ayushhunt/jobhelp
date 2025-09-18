'use client'

import React, { useState } from 'react'
import Link from 'next/link'
import AuthLayout from '@/components/auth/AuthLayout'
import { InputField, SubmitButton } from '@/components/auth/FormComponents'
import AuthService, { ForgotPasswordRequest, ApiError } from '@/services/auth'
import { EnvelopeIcon, ArrowLeftIcon } from '@heroicons/react/24/outline'

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState('')
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [loading, setLoading] = useState(false)
  const [successMessage, setSuccessMessage] = useState('')
  const [isSubmitted, setIsSubmitted] = useState(false)

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {}

    // Email validation
    if (!AuthService.validateEmail(email)) {
      newErrors.email = 'Please enter a valid email address'
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
      const forgotPasswordData: ForgotPasswordRequest = {
        email: email
      }

      const response = await AuthService.forgotPassword(forgotPasswordData)
      
      setSuccessMessage(response.message)
      setIsSubmitted(true)

    } catch (error) {
      const apiError = error as ApiError
      setErrors({ submit: apiError.detail })
    } finally {
      setLoading(false)
    }
  }

  const handleResend = async () => {
    setLoading(true)
    setErrors({})
    
    try {
      const response = await AuthService.forgotPassword({ email })
      setSuccessMessage('Password reset email sent again. Please check your inbox.')
    } catch (error) {
      const apiError = error as ApiError
      setErrors({ submit: apiError.detail })
    } finally {
      setLoading(false)
    }
  }

  return (
    <AuthLayout
      title="Forgot Password"
      subtitle="Enter your email to receive a password reset link"
      showBackToHome={false}
    >
      {!isSubmitted ? (
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Error Message */}
          {errors.submit && (
            <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
              <p className="text-red-800 dark:text-red-200 text-sm">{errors.submit}</p>
            </div>
          )}

          {/* Email */}
          <InputField
            label="Email Address"
            type="email"
            value={email}
            onChange={setEmail}
            error={errors.email}
            placeholder="Enter your registered email address"
            required
            disabled={loading}
          />

          {/* Submit Button */}
          <SubmitButton loading={loading} disabled={loading}>
            Send Reset Link
          </SubmitButton>

          {/* Back to Login Link */}
          <div className="text-center">
            <Link 
              href="/auth/login" 
              className="inline-flex items-center text-sm text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors"
            >
              <ArrowLeftIcon className="w-4 h-4 mr-2" />
              Back to Sign In
            </Link>
          </div>
        </form>
      ) : (
        <div className="text-center space-y-6">
          {/* Success Icon */}
          <div className="mx-auto w-16 h-16 bg-green-100 dark:bg-green-900/20 rounded-full flex items-center justify-center">
            <EnvelopeIcon className="w-8 h-8 text-green-600 dark:text-green-400" />
          </div>

          {/* Success Message */}
          <div className="space-y-2">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
              Check Your Email
            </h2>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              {successMessage || 'We\'ve sent a password reset link to your email address.'}
            </p>
            <p className="text-xs text-gray-500 dark:text-gray-500">
              Email sent to: <span className="font-medium">{email}</span>
            </p>
          </div>

          {/* Instructions */}
          <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
            <p className="text-sm text-blue-800 dark:text-blue-200">
              <strong>Next steps:</strong>
            </p>
            <ul className="text-sm text-blue-700 dark:text-blue-300 mt-2 space-y-1">
              <li>• Check your inbox for the reset email</li>
              <li>• Click the reset link in the email</li>
              <li>• Create your new password</li>
              <li>• Sign in with your new password</li>
            </ul>
          </div>

          {/* Resend and Back Links */}
          <div className="space-y-3">
            <button
              onClick={handleResend}
              disabled={loading}
              className="text-sm text-black dark:text-white hover:underline disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Sending...' : 'Didn\'t receive the email? Send again'}
            </button>
            
            <div>
              <Link 
                href="/auth/login" 
                className="inline-flex items-center text-sm text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors"
              >
                <ArrowLeftIcon className="w-4 h-4 mr-2" />
                Back to Sign In
              </Link>
            </div>
          </div>
        </div>
      )}
    </AuthLayout>
  )
}
