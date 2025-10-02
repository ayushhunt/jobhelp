'use client'

import React from 'react'
import Link from 'next/link'

interface AuthLayoutProps {
  children: React.ReactNode
  title: string
  subtitle?: string
  showBackToHome?: boolean
}

export default function AuthLayout({ 
  children, 
  title, 
  subtitle,
  showBackToHome = true 
}: AuthLayoutProps) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-white to-gray-50 dark:from-gray-900 dark:to-black flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center mb-6">
            <div className="w-12 h-12 bg-black dark:bg-white rounded-lg flex items-center justify-center">
              <span className="text-white dark:text-black font-bold text-xl">J</span>
            </div>
          </div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
            {title}
          </h1>
          {subtitle && (
            <p className="text-gray-600 dark:text-gray-400 text-sm">
              {subtitle}
            </p>
          )}
        </div>

        {/* Main Content */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl border border-gray-200 dark:border-gray-700 p-8">
          {children}
        </div>

        {/* Footer */}
        <div className="text-center mt-6">
          {showBackToHome && (
            <Link 
              href="/" 
              className="text-sm text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors"
            >
              ← Back to Home
            </Link>
          )}
          <p className="text-xs text-gray-500 dark:text-gray-500 mt-4">
            © 2024 JobHelp AI. All rights reserved.
          </p>
        </div>
      </div>
    </div>
  )
}
