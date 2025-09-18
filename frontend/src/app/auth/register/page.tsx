'use client'

import React, { useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import AuthLayout from '@/components/auth/AuthLayout'
import { InputField, PasswordField, PasswordMatch, SubmitButton, SocialButton } from '@/components/auth/FormComponents'
import AuthService, { RegisterRequest, ApiError } from '@/services/auth'

export default function RegisterPage() {
  const router = useRouter()
  const [formData, setFormData] = useState({
    fullName: '',
    email: '',
    password: '',
    confirmPassword: '',
    role: 'applicant' as 'admin' | 'applicant' | 'recruiter'
  })
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [loading, setLoading] = useState(false)
  const [successMessage, setSuccessMessage] = useState('')

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {}

    // Full name validation
    if (!AuthService.validateFullName(formData.fullName)) {
      newErrors.fullName = 'Full name must be at least 2 characters long'
    }

    // Email validation
    if (!AuthService.validateEmail(formData.email)) {
      newErrors.email = 'Please enter a valid email address'
    }

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
    
    if (!validateForm()) return

    setLoading(true)
    setErrors({})
    setSuccessMessage('')

    try {
      const registerData: RegisterRequest = {
        email: formData.email,
        password: formData.password,
        full_name: formData.fullName,
        role: formData.role
      }

      const response = await AuthService.register(registerData)
      
      setSuccessMessage(response.message)
      
      // Redirect to login after successful registration
      setTimeout(() => {
        router.push('/auth/login?registered=true')
      }, 2000)

    } catch (error) {
      const apiError = error as ApiError
      setErrors({ submit: apiError.detail })
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
      title="Create Your Account"
      subtitle="Join JobHelp AI to supercharge your career"
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
          </div>
        )}

        {/* Full Name */}
        <InputField
          label="Full Name"
          value={formData.fullName}
          onChange={(value) => setFormData({ ...formData, fullName: value })}
          error={errors.fullName}
          placeholder="Enter your full name"
          required
          disabled={loading}
        />

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

        {/* Role Selection */}
        <div className="space-y-2">
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
            I am a <span className="text-red-500">*</span>
          </label>
          <div className="grid grid-cols-3 gap-3">
            {[
              { value: 'applicant', label: 'Job Seeker' },
              { value: 'recruiter', label: 'Recruiter' },
              { value: 'admin', label: 'Admin' }
            ].map((option) => (
              <button
                key={option.value}
                type="button"
                onClick={() => setFormData({ ...formData, role: option.value as any })}
                disabled={loading}
                className={`p-3 rounded-lg border transition-colors text-sm font-medium ${
                  formData.role === option.value
                    ? 'border-black dark:border-white bg-black dark:bg-white text-white dark:text-black'
                    : 'border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:border-gray-400 dark:hover:border-gray-500'
                } disabled:opacity-50 disabled:cursor-not-allowed`}
              >
                {option.label}
              </button>
            ))}
          </div>
        </div>

        {/* Password */}
        <PasswordField
          label="Password"
          value={formData.password}
          onChange={(value) => setFormData({ ...formData, password: value })}
          error={errors.password}
          placeholder="Create a strong password"
          required
          disabled={loading}
          showStrength
        />

        {/* Confirm Password */}
        <div className="space-y-2">
          <PasswordField
            label="Confirm Password"
            value={formData.confirmPassword}
            onChange={(value) => setFormData({ ...formData, confirmPassword: value })}
            error={errors.confirmPassword}
            placeholder="Confirm your password"
            required
            disabled={loading}
          />
          <PasswordMatch 
            password={formData.password} 
            confirmPassword={formData.confirmPassword}
            showMatch={formData.password.length >= 8 && formData.confirmPassword.length > 0}
          />
        </div>

        {/* Submit Button */}
        <SubmitButton loading={loading} disabled={loading}>
          Create Account
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

        {/* Login Link */}
        <div className="text-center">
          <p className="text-sm text-gray-600 dark:text-gray-400">
            Already have an account?{' '}
            <Link 
              href="/auth/login" 
              className="font-medium text-black dark:text-white hover:underline"
            >
              Sign in here
            </Link>
          </p>
        </div>
      </form>
    </AuthLayout>
  )
}
