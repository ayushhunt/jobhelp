'use client'

import { useState } from 'react'
import CompanyResearchForm from '@/components/CompanyResearch/CompanyResearchForm'
import { CompanyResearchRequest } from '@/services/companyResearchApi'

const CompanyResearchTool = () => {
  const [isLoading, setIsLoading] = useState(false)
  const [researchData, setResearchData] = useState<any>(null)

  const handleResearchSubmit = async (request: CompanyResearchRequest) => {
    setIsLoading(true)
    try {
      // TODO: Implement actual API call to your company research service
      console.log('Research request:', request)
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 2000))
      
      // Mock response data
      const mockData = {
        company_name: request.company_name,
        domain: request.company_domain,
        research_depth: request.research_depth,
        findings: {
          basic_info: {
            name: request.company_name,
            domain: request.company_domain,
            industry: 'Technology',
            founded: '2010',
            employees: '1000-5000'
          },
          financial_data: request.include_financial_data ? {
            revenue: '$100M - $500M',
            funding_rounds: 3,
            last_funding: '2023',
            valuation: '$1B+'
          } : null,
          employee_reviews: request.include_employee_reviews ? {
            rating: 4.2,
            total_reviews: 1250,
            pros: ['Great work-life balance', 'Innovative projects', 'Good benefits'],
            cons: ['Fast-paced environment', 'Limited remote work']
          } : null
        }
      }
      
      setResearchData(mockData)
    } catch (error) {
      console.error('Research failed:', error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="space-y-8">
      <CompanyResearchForm 
        onSubmit={handleResearchSubmit} 
        isLoading={isLoading} 
      />
      
      {researchData && (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
          <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
            Research Results for {researchData.company_name}
          </h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Basic Info */}
            <div className="space-y-4">
              <h4 className="font-medium text-gray-900 dark:text-white">Basic Information</h4>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-600 dark:text-gray-400">Domain:</span>
                  <span className="text-gray-900 dark:text-white">{researchData.findings.basic_info.domain}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600 dark:text-gray-400">Industry:</span>
                  <span className="text-gray-900 dark:text-white">{researchData.findings.basic_info.industry}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600 dark:text-gray-400">Founded:</span>
                  <span className="text-gray-900 dark:text-white">{researchData.findings.basic_info.founded}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600 dark:text-gray-400">Employees:</span>
                  <span className="text-gray-900 dark:text-white">{researchData.findings.basic_info.employees}</span>
                </div>
              </div>
            </div>

            {/* Financial Data */}
            {researchData.findings.financial_data && (
              <div className="space-y-4">
                <h4 className="font-medium text-gray-900 dark:text-white">Financial Information</h4>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-600 dark:text-gray-400">Revenue:</span>
                    <span className="text-gray-900 dark:text-white">{researchData.findings.financial_data.revenue}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600 dark:text-gray-400">Funding Rounds:</span>
                    <span className="text-gray-900 dark:text-white">{researchData.findings.financial_data.funding_rounds}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600 dark:text-gray-400">Last Funding:</span>
                    <span className="text-gray-900 dark:text-white">{researchData.findings.financial_data.last_funding}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600 dark:text-gray-400">Valuation:</span>
                    <span className="text-gray-900 dark:text-white">{researchData.findings.financial_data.valuation}</span>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Employee Reviews */}
          {researchData.findings.employee_reviews && (
            <div className="mt-6 space-y-4">
              <h4 className="font-medium text-gray-900 dark:text-white">Employee Reviews</h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h5 className="text-sm font-medium text-gray-900 dark:text-white mb-2">Pros</h5>
                  <ul className="space-y-1">
                    {researchData.findings.employee_reviews.pros.map((pro: string, index: number) => (
                      <li key={index} className="text-sm text-green-600 dark:text-green-400 flex items-center">
                        <span className="mr-2">+</span>
                        {pro}
                      </li>
                    ))}
                  </ul>
                </div>
                <div>
                  <h5 className="text-sm font-medium text-gray-900 dark:text-white mb-2">Cons</h5>
                  <ul className="space-y-1">
                    {researchData.findings.employee_reviews.cons.map((con: string, index: number) => (
                      <li key={index} className="text-sm text-red-600 dark:text-red-400 flex items-center">
                        <span className="mr-2">-</span>
                        {con}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
              <div className="flex items-center space-x-4 text-sm">
                <span className="text-gray-600 dark:text-gray-400">Overall Rating:</span>
                <span className="font-medium text-yellow-600">{researchData.findings.employee_reviews.rating}/5</span>
                <span className="text-gray-600 dark:text-gray-400">({researchData.findings.employee_reviews.total_reviews} reviews)</span>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default CompanyResearchTool


