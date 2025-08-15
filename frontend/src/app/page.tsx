'use client'

import { useState } from 'react'
import Layout from '@/components/Layout'
import FileUpload from '@/components/FileUpload'
import AnalyticsDashboard from '@/components/AnalyticsDashboard'

interface AnalysisData {
  similarity_score: number
  semantic_similarity_score: number
  resume_word_frequency: Record<string, number>
  jd_word_frequency: Record<string, number>
  common_keywords: string[]
  missing_keywords: string[]
  matched_skills: Record<string, string[]>
  missing_skills: Record<string, string[]>
  extra_skills: Record<string, string[]>
  years_experience_required: number
  years_experience_resume: number
  experience_gap: number
  responsibility_coverage_score: number
  requirement_coverage_score: number
  common_phrases: string[]
  action_verb_analysis: {
    action_verbs: string[]
    verb_count: number
    verb_density: number
    strong_verb_score: number
  }
  jd_readability: {
    flesch_reading_ease: number
    readability_level: string
  }
  resume_readability: {
    flesch_reading_ease: number
    readability_level: string
  }
  keyword_density: Record<string, number>
  education_match: boolean
  missing_certifications: string[]
  insights_summary: string
  // Enhanced experience analytics
  experience_analysis?: {
    total_experience: {
      total_years: number
      total_months: number
      positions: any[]
      employment_gaps: any[]
      career_progression: any[]
    }
    role_mappings: Record<string, any>
    experience_by_recency: {
      recent_years: number
      mid_term_years: number
      older_years: number
    }
    skill_experience_mapping: Record<string, number>
    career_stability: {
      average_job_duration: number
      number_of_job_changes: number
      longest_tenure: number
    }
  }
  role_duration_mapping?: Record<string, any>
  career_progression?: any[]
  employment_gaps?: any[]
  experience_by_recency?: {
    recent_years: number
    mid_term_years: number
    older_years: number
  }
  skill_experience_mapping?: Record<string, number>
  career_stability?: {
    average_job_duration: number
    number_of_job_changes: number
    longest_tenure: number
  }
  // AI insights
  ai_insights?: {
    match_score: number
    alignment_strength: string
    top_matched_skills: string[]
    critical_missing_skills: string[]
    experience_assessment: string
    improvement_priority: string
    quick_wins: string[]
    ats_optimization_tip: string
    role_fit_reason: string
    tokens_used?: number
    model_used?: string
    llm_status?: string | any
  }
  ai_enabled?: boolean
}

export default function Home() {
  const [analysisData, setAnalysisData] = useState<AnalysisData | null>(null)

  const handleAnalysisComplete = (data: AnalysisData) => {
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