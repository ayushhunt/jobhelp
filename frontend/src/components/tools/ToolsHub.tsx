'use client'

import { useState } from 'react'
import MainLayout from '@/components/layout/MainLayout'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'
import ResumeJobAnalyzer from './ResumeJobAnalyzer'
import CompanyResearchTool from './CompanyResearchTool'
import { 
  DocumentTextIcon, 
  BuildingOfficeIcon,
  ChartBarIcon,
  MagnifyingGlassIcon
} from '@heroicons/react/24/outline'

const ToolsHub = () => {
  const [activeTool, setActiveTool] = useState<string | null>(null)

  const tools = [
    {
      id: 'resume-analyzer',
      name: 'Resume & Job Description Analyzer',
      description: 'Compare your resume with job descriptions using AI to identify gaps and improve your match score.',
      icon: DocumentTextIcon,
      features: ['AI-powered analysis', 'Keyword matching', 'Skill gap identification', 'Match scoring'],
      component: ResumeJobAnalyzer
    },
    {
      id: 'company-research',
      name: 'Company Research Tool',
      description: 'Get comprehensive insights about companies including financial data, employee reviews, and market position.',
      icon: BuildingOfficeIcon,
      features: ['WHOIS lookup', 'Financial analysis', 'Employee reviews', 'Market insights'],
      component: CompanyResearchTool
    }
  ]

  if (activeTool) {
    const tool = tools.find(t => t.id === activeTool)
    if (tool) {
      const ToolComponent = tool.component
      return (
        <MainLayout>
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <div className="mb-6">
              <button
                onClick={() => setActiveTool(null)}
                className="text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300 mb-4"
              >
                ← Back to Tools
              </button>
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
                {tool.name}
              </h1>
              <p className="text-gray-600 dark:text-gray-400 mt-2">
                {tool.description}
              </p>
            </div>
            <ToolComponent />
          </div>
        </MainLayout>
      )
    }
  }

  return (
    <MainLayout>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
            Free Career Tools
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto">
            Powerful AI-driven tools to enhance your job search and career development. 
            All tools are completely free to use.
          </p>
        </div>

        {/* Tools Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
          {tools.map((tool) => (
            <Card key={tool.id} className="hover:shadow-lg transition-all duration-300 cursor-pointer group">
              <CardHeader>
                <div className="flex items-start space-x-4">
                  <div className="p-3 bg-blue-100 dark:bg-blue-900/20 rounded-lg group-hover:bg-blue-200 dark:group-hover:bg-blue-900/30 transition-colors">
                    <tool.icon className="h-8 w-8 text-blue-600 dark:text-blue-400" />
                  </div>
                  <div className="flex-1">
                    <CardTitle className="text-xl mb-2 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                      {tool.name}
                    </CardTitle>
                    <p className="text-gray-600 dark:text-gray-400 text-sm leading-relaxed">
                      {tool.description}
                    </p>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <h4 className="font-medium text-gray-900 dark:text-white mb-2">Features:</h4>
                    <ul className="space-y-1">
                      {tool.features.map((feature, index) => (
                        <li key={index} className="flex items-center text-sm text-gray-600 dark:text-gray-400">
                          <ChartBarIcon className="h-4 w-4 text-green-500 mr-2 flex-shrink-0" />
                          {feature}
                        </li>
                      ))}
                    </ul>
                  </div>
                  
                  <button
                    onClick={() => setActiveTool(tool.id)}
                    className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-4 rounded-lg transition-colors duration-200 flex items-center justify-center space-x-2"
                  >
                    <span>Use Tool</span>
                    <MagnifyingGlassIcon className="h-4 w-4" />
                  </button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Benefits Section */}
        <div className="bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 rounded-2xl p-8">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
              Why Use Our Tools?
            </h2>
            <p className="text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
              Our AI-powered tools are designed to give you a competitive edge in your job search
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <ChartBarIcon className="h-8 w-8 text-white" />
              </div>
              <h3 className="font-semibold text-gray-900 dark:text-white mb-2">AI-Powered Analysis</h3>
              <p className="text-gray-600 dark:text-gray-400 text-sm">
                Advanced algorithms provide deep insights and actionable recommendations
              </p>
            </div>
            
            <div className="text-center">
              <div className="w-16 h-16 bg-green-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <DocumentTextIcon className="h-8 w-8 text-white" />
              </div>
              <h3 className="font-semibold text-gray-900 dark:text-white mb-2">Completely Free</h3>
              <p className="text-gray-600 dark:text-gray-400 text-sm">
                All tools are free to use with no hidden costs or subscription requirements
              </p>
            </div>
            
            <div className="text-center">
              <div className="w-16 h-16 bg-purple-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <BuildingOfficeIcon className="h-8 w-8 text-white" />
              </div>
              <h3 className="font-semibold text-gray-900 dark:text-white mb-2">Instant Results</h3>
              <p className="text-gray-600 dark:text-gray-400 text-sm">
                Get immediate feedback and insights to improve your job applications
              </p>
            </div>
          </div>
        </div>
      </div>
    </MainLayout>
  )
}

export default ToolsHub


