'use client'

import { useState } from 'react'
import MainLayout from '@/components/layout/MainLayout'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'
import Button from '@/components/ui/Button'

interface CompanyProfileProps {
  companyId: string
}

const CompanyProfile = ({ companyId }: CompanyProfileProps) => {
  const [activeTab, setActiveTab] = useState('overview')

  // Mock data - in real app, this would be fetched based on companyId
  const company = {
    name: 'TechCorp Inc.',
    logo: '🏢',
    industry: 'Technology',
    size: '1000-5000 employees',
    location: 'San Francisco, CA',
    founded: '2010',
    website: 'https://techcorp.com',
    description: 'TechCorp is a leading technology company focused on building innovative solutions that transform how businesses operate in the digital age.',
    openJobs: 25,
    benefits: ['Health Insurance', 'Remote Work', '401k Matching', 'Flexible PTO'],
    culture: ['Innovation', 'Collaboration', 'Work-Life Balance', 'Diversity & Inclusion'],
  }

  const tabs = [
    { id: 'overview', label: 'Overview' },
    { id: 'jobs', label: `Jobs (${company.openJobs})` },
    { id: 'culture', label: 'Culture' },
    { id: 'benefits', label: 'Benefits' },
  ]

  return (
    <MainLayout>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Company Header */}
        <Card className="mb-8">
          <CardContent className="pt-6">
            <div className="flex items-start space-x-6">
              <div className="text-6xl">{company.logo}</div>
              <div className="flex-1">
                <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
                  {company.name}
                </h1>
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-sm text-gray-600 dark:text-gray-400">
                  <div>
                    <span className="font-medium">Industry:</span> {company.industry}
                  </div>
                  <div>
                    <span className="font-medium">Size:</span> {company.size}
                  </div>
                  <div>
                    <span className="font-medium">Location:</span> {company.location}
                  </div>
                  <div>
                    <span className="font-medium">Founded:</span> {company.founded}
                  </div>
                </div>
                <p className="mt-4 text-gray-600 dark:text-gray-300">
                  {company.description}
                </p>
              </div>
              <div className="flex space-x-2">
                <Button variant="outline">
                  Visit Website
                </Button>
                <Button>
                  View Jobs ({company.openJobs})
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Tabs */}
        <div className="border-b border-gray-200 dark:border-gray-700 mb-6">
          <nav className="-mb-px flex space-x-8">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                    : 'border-transparent text-gray-500 hover:text-gray-700 dark:hover:text-gray-300'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </nav>
        </div>

        {/* Tab Content */}
        <div>
          {activeTab === 'overview' && (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="lg:col-span-2">
                <Card>
                  <CardHeader>
                    <CardTitle>About {company.name}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                      {company.description} We are committed to fostering an inclusive 
                      environment where innovation thrives and employees can grow their careers 
                      while making a meaningful impact on the world.
                    </p>
                  </CardContent>
                </Card>
              </div>
              
              <div className="space-y-6">
                <Card>
                  <CardHeader>
                    <CardTitle>Quick Stats</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-gray-600 dark:text-gray-400">Open Jobs</span>
                      <span className="font-semibold">{company.openJobs}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600 dark:text-gray-400">Employees</span>
                      <span className="font-semibold">{company.size.split(' ')[0]}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600 dark:text-gray-400">Founded</span>
                      <span className="font-semibold">{company.founded}</span>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </div>
          )}

          {activeTab === 'jobs' && (
            <Card>
              <CardHeader>
                <CardTitle>Open Positions</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600 dark:text-gray-400 text-center py-8">
                  Job listings will be displayed here. Currently showing {company.openJobs} available positions.
                </p>
              </CardContent>
            </Card>
          )}

          {activeTab === 'culture' && (
            <Card>
              <CardHeader>
                <CardTitle>Company Culture</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  {company.culture.map((value, index) => (
                    <div key={index} className="text-center p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                      <div className="text-2xl mb-2">⭐</div>
                      <p className="font-medium text-gray-900 dark:text-white">{value}</p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {activeTab === 'benefits' && (
            <Card>
              <CardHeader>
                <CardTitle>Benefits & Perks</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {company.benefits.map((benefit, index) => (
                    <div key={index} className="flex items-center space-x-3 p-3 bg-green-50 dark:bg-green-900/20 rounded-lg">
                      <div className="text-green-600">✓</div>
                      <span className="font-medium text-gray-900 dark:text-white">{benefit}</span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </MainLayout>
  )
}

export default CompanyProfile


