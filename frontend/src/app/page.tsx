'use client'

import { useState } from 'react'
import Layout from '@/components/Layout'
import FileUpload from '@/components/FileUpload'
import AnalyticsDashboard from '@/components/AnalyticsDashboard'
import { AnalysisResponse } from '@/services/api'

export default function Home() {
  const [analysisData, setAnalysisData] = useState<AnalysisResponse | null>(null)

  const handleAnalysisComplete = (data: AnalysisResponse) => {
    setAnalysisData(data)
  }

  return (
    <Layout>
      <div className="space-y-6 sm:space-y-8">
        <FileUpload onAnalysisComplete={handleAnalysisComplete} />
        {analysisData && <AnalyticsDashboard data={analysisData} />}
      </div>
    </Layout>
  )
}