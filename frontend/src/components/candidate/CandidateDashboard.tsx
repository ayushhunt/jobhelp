'use client'

import React from 'react'
import Link from 'next/link'
import { useSelector } from 'react-redux'
import { RootState } from '@/redux/store'
import  Button  from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'

export default function CandidateDashboard() {
  const { user } = useSelector((state: RootState) => state.auth)

  if (!user) return null

  const candidateFeatures = [
    {
      title: 'Resume Analysis',
      description: 'Upload your resume for AI-powered analysis and personalized insights',
      icon: '📄',
      href: '/tools/resume-analyzer',
      color: 'from-blue-500 to-purple-600'
    },
    {
      title: 'Company Research',
      description: 'Research potential employers and get detailed company insights',
      icon: '🏢',
      href: '/company-research',
      color: 'from-green-500 to-teal-600'
    },
    {
      title: 'Job Matching',
      description: 'Find jobs that match your skills and preferences',
      icon: '💼',
      href: '/jobs',
      color: 'from-orange-500 to-red-600'
    },
    {
      title: 'Interview Prep',
      description: 'Practice with AI-powered interview questions',
      icon: '🎯',
      href: '/tools/interview-prep',
      color: 'from-purple-500 to-pink-600'
    },
    {
      title: 'Career Analytics',
      description: 'Track your job search progress and insights',
      icon: '📊',
      href: '/dashboard/analytics',
      color: 'from-indigo-500 to-blue-600'
    },
    {
      title: 'Profile Management',
      description: 'Update your profile and preferences',
      icon: '👤',
      href: '/profile',
      color: 'from-cyan-500 to-blue-600'
    }
  ]

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <header className="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center">
              <div className="w-8 h-8 bg-black dark:bg-white rounded-lg flex items-center justify-center mr-3">
                <span className="text-white dark:text-black font-bold">J</span>
              </div>
              <h1 className="text-xl font-bold text-gray-900 dark:text-white">
                Candidate Dashboard
              </h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-600 dark:text-gray-400">
                Welcome, {user.full_name}
              </span>
              <Link href="/profile">
                <Button variant="outline" size="sm">
                  Profile
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </header>

      {/* Welcome Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            Welcome back, {user.full_name?.split(' ')[0]} 👋
          </h2>
          <p className="text-gray-600 dark:text-gray-400">
            Ready to take your job search to the next level? Let's get started with these powerful tools.
          </p>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card className="p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="w-8 h-8 bg-blue-100 dark:bg-blue-900/20 rounded-full flex items-center justify-center">
                  <span className="text-blue-600 dark:text-blue-400 text-sm font-medium">📄</span>
                </div>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Applications</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">0</p>
              </div>
            </div>
          </Card>
          
          <Card className="p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="w-8 h-8 bg-green-100 dark:bg-green-900/20 rounded-full flex items-center justify-center">
                  <span className="text-green-600 dark:text-green-400 text-sm font-medium">✅</span>
                </div>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Interviews</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">0</p>
              </div>
            </div>
          </Card>
          
          <Card className="p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="w-8 h-8 bg-purple-100 dark:bg-purple-900/20 rounded-full flex items-center justify-center">
                  <span className="text-purple-600 dark:text-purple-400 text-sm font-medium">🎯</span>
                </div>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Match Score</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">--</p>
              </div>
            </div>
          </Card>
          
          <Card className="p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="w-8 h-8 bg-orange-100 dark:bg-orange-900/20 rounded-full flex items-center justify-center">
                  <span className="text-orange-600 dark:text-orange-400 text-sm font-medium">⚡</span>
                </div>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">This Week</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">0</p>
              </div>
            </div>
          </Card>
        </div>

        {/* Features Grid */}
        <div>
          <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-6">
            Available Features
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {candidateFeatures.map((feature, index) => (
              <Card key={index} className="group hover:shadow-lg transition-shadow duration-200">
                <Link href={feature.href}>
                  <div className="p-6">
                    <div className={`w-12 h-12 bg-gradient-to-r ${feature.color} rounded-lg flex items-center justify-center mb-4`}>
                      <span className="text-2xl text-white">{feature.icon}</span>
                    </div>
                    <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-2 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                      {feature.title}
                    </h4>
                    <p className="text-gray-600 dark:text-gray-400 text-sm mb-4">
                      {feature.description}
                    </p>
                    <div className="flex items-center text-blue-600 dark:text-blue-400 font-medium text-sm">
                      Get Started
                      <svg className="w-4 h-4 ml-1 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                      </svg>
                    </div>
                  </div>
                </Link>
              </Card>
            ))}
          </div>
        </div>

        {/* Recent Activity */}
        <div className="mt-8">
          <Card className="p-6">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Recent Activity
            </h3>
            <div className="text-center py-8">
              <div className="w-16 h-16 bg-gray-100 dark:bg-gray-700 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl text-gray-400 dark:text-gray-600">📭</span>
              </div>
              <p className="text-gray-500 dark:text-gray-400 mb-2">No recent activity yet</p>
              <p className="text-sm text-gray-400 dark:text-gray-500">
                Start by uploading your resume or researching companies!
              </p>
            </div>
          </Card>
        </div>
      </div>
    </div>
  )
}
