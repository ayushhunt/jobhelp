'use client'

import { useState } from 'react'
import CompanyResearchForm from '@/components/CompanyResearch/CompanyResearchForm'
import ResearchResults from '@/components/CompanyResearch/ResearchResults'
import { CompanyResearchRequest, CompanyResearchAPIService, CompanyResearchResponse } from '@/services/companyResearchApi'

const CompanyResearchTool = () => {
  const [isLoading, setIsLoading] = useState(false)
  const [researchData, setResearchData] = useState<CompanyResearchResponse | null>(null)
  const [error, setError] = useState<string>('')

  const handleResearchSubmit = async (request: CompanyResearchRequest) => {
    setIsLoading(true)
    try {
      setError('')
      const result = await CompanyResearchAPIService.researchCompany(request)
      setResearchData(result)
    } catch (err: any) {
      console.error('Research failed:', err)
      setError(err?.message || 'Failed to perform company research')
      setResearchData(null)
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

      {error && (
        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
          <p className="text-red-800 dark:text-red-200 text-sm">{error}</p>
        </div>
      )}
      
      {researchData && <ResearchResults results={researchData} />}
    </div>
  )
}

export default CompanyResearchTool


