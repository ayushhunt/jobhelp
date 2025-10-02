'use client'

import { useState } from 'react'
import FileUpload from '@/components/FileUpload'
import ResumeJobDashboard from '@/components/ResumeJobDashboard'
import { AnalysisResponse } from '@/services/api'

const ResumeJobAnalyzer = () => {
  const [analysisData, setAnalysisData] = useState<AnalysisResponse | null>(null)

  const handleAnalysisComplete = (data: AnalysisResponse) => {
    setAnalysisData(data)
  }

  return (
    <div className="space-y-6">
      <FileUpload onAnalysisComplete={handleAnalysisComplete} />
      {analysisData && <ResumeJobDashboard data={analysisData} />}
    </div>
  )
}

export default ResumeJobAnalyzer


