'use client'

import React, { useState, useEffect } from 'react'
import Link from 'next/link'
import { useSearchParams } from 'next/navigation'
import AuthLayout from '@/components/auth/AuthLayout'
import { SubmitButton } from '@/components/auth/FormComponents'
import AuthService, { ApiError } from '@/services/auth'
import { CheckCircleIcon, XCircleIcon, EnvelopeIcon } from '@heroicons/react/24/outline'

export default function VerifyEmailPage() {
  const searchParams = useSearchParams()
  const [token, setToken] = useState('')
  const [loading, setLoading] = useState(true)
  const [isVerified, setIsVerified] = useState(false)
  const [error, setError] = useState('')
  const [resendLoading, setResendLoading] = useState(false)
  const [resendMessage, setResendMessage] = useState('')

  // Extract token from URL params and verify
  useEffect(() => {
    const tokenParam = searchParams.get('token')
    if (!tokenParam) {
      setError('Invalid or missing verification token.')
      setLoading(false)
      return
    }

    setToken(tokenParam)
    verifyEmail(tokenParam)
  }, [searchParams])

  const verifyEmail = async (verificationToken: string) => {
    try {
      setLoading(true)
      const response = await AuthService.verifyEmail(verificationToken)
      setIsVerified(true)
    } catch (error) {
      const apiError = error as ApiError
      if (apiError.status === 400 && apiError.detail.includes('token')) {
        setError('This verification link has expired or is invalid.')
      } else {
        setError(apiError.detail || 'Email verification failed.')
      }
    } finally {
      setLoading(false)
    }
  }

  const handleResendVerification = async () => {
    try {
      setResendLoading(true)
      setResendMessage('')
      const response = await AuthService.resendVerification()
      setResendMessage('Verification email sent! Please check your inbox.')
    } catch (error) {
      const apiError = error as ApiError
      setResendMessage(`Failed to resend email: ${apiError.detail}`)
    } finally {
      setResendLoading(false)
    }
  }

  // Loading state
  if (loading) {
    return (
      <AuthLayout
        title="Verifying Email"
        subtitle="Please wait while we verify your email address"
        showBackToHome={false}
      >
        <div className="text-center space-y-6">
          {/* Loading Spinner */}
          <div className="mx-auto w-16 h-16 bg-blue-100 dark:bg-blue-900/20 rounded-full flex items-center justify-center">
            <div className="animate-spin rounded-full h-8 w-8 border-2 border-blue-600 dark:border-blue-400 border-t-transparent"></div>
          </div>

          <div className="space-y-2">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
              Verifying...
            </h2>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              We're verifying your email address. This should only take a moment.
            </p>
          </div>
        </div>
      </AuthLayout>
    )
  }

  // Success state
  if (isVerified) {
    return (
      <AuthLayout
        title="Email Verified!"
        subtitle="Your account has been successfully verified"
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
              Welcome to JobHelp AI!
            </h2>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Your email has been successfully verified. You can now access all features of your account.
            </p>
          </div>

          {/* Welcome Benefits */}
          <div className="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-4">
            <p className="text-sm text-green-800 dark:text-green-200 font-medium mb-2">
              What's next?
            </p>
            <ul className="text-sm text-green-700 dark:text-green-300 space-y-1 text-left">
              <li>• Upload your resume for AI-powered analysis</li>
              <li>• Research companies and job opportunities</li>
              <li>• Get personalized career insights</li>
              <li>• Track your job applications</li>
            </ul>
          </div>

          {/* Sign In Button */}
          <div className="space-y-3">
            <Link href="/login">
              <SubmitButton type="button">
                Sign In to Your Account
              </SubmitButton>
            </Link>
            
            <Link 
              href="#" 
              className="block text-sm text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors"
            >
              Or go to Dashboard
            </Link>
          </div>
        </div>
      </AuthLayout>
    )
  }

  // Error state
  return (
    <AuthLayout
      title="Verification Failed"
      subtitle="We couldn't verify your email address"
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
            Verification Failed
          </h2>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            {error}
          </p>
        </div>

        {/* Resend Section */}
        <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
          <div className="flex items-center justify-center mb-3">
            <EnvelopeIcon className="w-6 h-6 text-blue-600 dark:text-blue-400" />
          </div>
          <p className="text-sm text-blue-800 dark:text-blue-200 mb-3">
            Need a new verification link?
          </p>
          
          {resendMessage && (
            <div className={`mb-3 p-2 rounded text-sm ${
              resendMessage.includes('sent') 
                ? 'bg-green-100 dark:bg-green-900/20 text-green-800 dark:text-green-200'
                : 'bg-red-100 dark:bg-red-900/20 text-red-800 dark:text-red-200'
            }`}>
              {resendMessage}
            </div>
          )}
          
          <button
            onClick={handleResendVerification}
            disabled={resendLoading}
            className="w-full bg-blue-600 dark:bg-blue-500 text-white py-2 px-4 rounded-lg font-medium hover:bg-blue-700 dark:hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {resendLoading ? (
              <div className="flex items-center justify-center">
                <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent mr-2"></div>
                Sending...
              </div>
            ) : (
              'Send New Verification Email'
            )}
          </button>
        </div>

        {/* Alternative Actions */}
        <div className="space-y-3">
          <div className="text-sm text-gray-600 dark:text-gray-400">
            <p>Already verified?</p>
            <Link 
              href="/login" 
              className="text-black dark:text-white hover:underline font-medium"
            >
              Sign in to your account
            </Link>
          </div>
          
          <div className="text-sm text-gray-600 dark:text-gray-400">
            <p>Need help?</p>
            <Link 
              href="/contact" 
              className="text-black dark:text-white hover:underline font-medium"
            >
              Contact our support team
            </Link>
          </div>
        </div>
      </div>
    </AuthLayout>
  )
}
