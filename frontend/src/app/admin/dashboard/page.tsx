'use client'

import React, { useEffect } from 'react'
import { useSelector } from 'react-redux'
import { RootState } from '@/redux/store'
import { AuthGuard } from '@/components/auth/AuthGuard'
import { Card } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'

export default function AdminDashboardPage() {
  const { user } = useSelector((state: RootState) => state.auth)

  const adminFeatures = [
    {
      title: 'User Management',
      description: 'Manage users, roles, and permissions',
      icon: '👥',
      href: '/admin/users',
      color: 'from-blue-500 to-purple-600'
    },
    {
      title: 'System Analytics',
      description: 'View system-wide analytics and insights',
      icon: '📊',
      href: '/admin/analytics',
      color: 'from-green-500 to-Teal-600'
    },
    {
      title: 'Company Oversight',
      description: 'Monitor all companies and recruitment activities',
      icon: '🏢',
      href: '/admin/companies',
      color: 'from-orange-500 to-red-600'
    },
    {
      title: 'System Settings',
      description: 'Configure system-wide settings and preferences',
      icon: '⚙️',
      href: '/admin/settings',
      color: 'from-purple-500 to-pink-600'
    }
  ]

  return (
    <AuthGuard requiredRole="admin">
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
        {/* Header */}
        <header className="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center py-4">
              <div className="flex items-center">
                <div className="w-8 h-8 bg-red-600 dark:bg-red-500 rounded-lg flex items-center justify-center mr-3">
                  <span className="text-white font-bold">A</span>
                </div>
                <h1 className="text-xl font-bold text-gray-900 dark:text-white">
                  Admin Dashboard
                </h1>
              </div>
              <div className="flex items-center space-x-4">
                <span className="text-sm text-gray-600 dark:text-gray-400">
                  Admin: {user?.full_name}
                </span>
              </div>
            </div>
          </div>
        </header>

        {/* Welcome Section */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="mb-8">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
              Admin Panel 🔒
            </h2>
            <p className="text-gray-600 dark:text-gray-400">
              System administration and oversight tools.
            </p>
          </div>

          {/* System Stats */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <Card className="p-6">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="w-8 h-8 bg-blue-100 dark:bg-blue-900/20 rounded-full flex items-center justify-center">
                    <span className="text-blue-600 dark:text-blue-400 text-sm font-medium">👥</span>
                  </div>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Total Users</p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">--</p>
                </div>
              </div>
            </Card>
            
            <Card className="p-6">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="w-8 h-8 bg-green-100 dark:bg-green-900/20 rounded-full flex items-center justify-center">
                    <span className="text-green-600 dark:text-green-400 text-sm font-medium">🏢</span>
                  </div>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Companies</p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">--</p>
                </div>
              </div>
            </Card>
            
            <Card className="p-6">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="w-8 h-8 bg-purple-100 dark:bg-purple-900/20 rounded-full flex items-center justify-center">
                    <span className="text-purple-600 dark:text-purple-400 text-sm font-medium">📊</span>
                  </div>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Admin Features</p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">{adminFeatures.length}</p>
                </div>
              </div>
            </Card>
            
            <Card className="p-6">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="w-8 h-8 bg-orange-100 dark:bg-orange-900/20 rounded-full flex items-center justify-center">
                    <span className="text-orange-600 dark:text-orange-400 text-sm font-medium">⚙️</span>
                  </div>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600 dark:text-gray-400">System Status</p>
                  <p className="text-sm font-bold text-green-600 dark:text-green-400">Healthy</p>
                </div>
              </div>
            </Card>
          </div>

          {/* Admin Tools */}
          <div>
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-6">
              Administrator Tools
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {adminFeatures.map((feature, index) => (
                <>
                  <Card key={index} className="group hover:shadow-lg transition-shadow duration-200 border-red-200 dark:border-red-800">
                    <div className="p-6">
                      <div className={`w-12 h-12 bg-gradient-to-r ${feature.color} rounded-lg flex items-center justify-center mb-4`}>
                        <span className="text-2xl text-white">{feature.icon}</span>
                      </div>
                      <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                        {feature.title}
                      </h4>
                      <p className="text-gray-600 dark:text-gray-400 text-sm mb-4">
                        {feature.description}
                      </p>
                      <Button 
                        variant="outline" 
                        className="w-full text-sm bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 hover:bg-red-100 dark:hover:bg-red-900/30"
                        disabled
                      >
                        Coming Soon
                      </Button>
                    </div>
                  </Card>
                </>
              ))}
            </div>
          </div>

          {/* Admin Notice */}
          <div className="mt-8">
            <Card className="p-6 bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <span className="text-red-600 dark:text-red-400 text-2xl">⚠️</span>
                </div>
                <div className="ml-4">
                  <h3 className="text-lg font-semibold text-red-800 dark:text-red-200">
                    Admin Panel - Development Mode
                  </h3>
                  <p className="text-red-700 dark:text-red-300 mt-1">
                    This is a placeholder admin dashboard. Full admin features will be implemented in future versions.
                  </p>
                </div>
              </div>
            </Card>
          </div>
        </div>
      </div>
    </AuthGuard>
  )
}
