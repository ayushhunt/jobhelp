'use client'

import { useEffect, useRef } from 'react'
import { Chart } from 'chart.js/auto'
import { CheckCircle, XCircle, TrendingUp, TrendingDown, Users, BookOpen, Briefcase, Zap, Target, Award, Sparkles } from 'lucide-react'
import WordCloud from './WordCloud'
import { AnalysisResponse } from '../services/api'

interface ResumeJobDashboardProps {
  data: AnalysisResponse
}

export default function ResumeJobDashboard({ data }: ResumeJobDashboardProps) {
  const skillsChartRef = useRef<HTMLCanvasElement>(null)
  const experienceChartRef = useRef<HTMLCanvasElement>(null)
  const coverageChartRef = useRef<HTMLCanvasElement>(null)
  
  const skillsChartInstance = useRef<Chart | null>(null)
  const experienceChartInstance = useRef<Chart | null>(null)
  const coverageChartInstance = useRef<Chart | null>(null)

  // Extract data from the new nested structure
  const basicAnalytics = data.basic_analytics
  const advancedAnalytics = data.advanced_analytics
  const experienceAnalysis = data.experience_analysis
  const aiInsights = data.ai_insights

  // Prepare word cloud data
  const resumeWords = Object.entries(basicAnalytics.resume_word_frequency)
    .map(([text, value]) => ({ text, value }))
    .sort((a, b) => b.value - a.value)
    .slice(0, 50)

  const jdWords = Object.entries(basicAnalytics.jd_word_frequency)
    .map(([text, value]) => ({ text, value }))
    .sort((a, b) => b.value - a.value)
    .slice(0, 50)

  // Calculate overall match percentage
  const overallMatch = Math.round((basicAnalytics.similarity_score + (advancedAnalytics?.semantic_similarity_score || 0) / 100) / 2 * 100)

  useEffect(() => {
    // Cleanup previous charts
    if (skillsChartInstance.current) skillsChartInstance.current.destroy()
    if (experienceChartInstance.current) experienceChartInstance.current.destroy()
    if (coverageChartInstance.current) coverageChartInstance.current.destroy()

    // Skills Chart
    if (skillsChartRef.current) {
      const ctx = skillsChartRef.current.getContext('2d')
      if (ctx) {
        // Use placeholder data for now since the new API structure is different
        const skillCategories = ['Technical', 'Soft Skills', 'Tools']
        const matchedCounts = [3, 2, 1] // Placeholder values
        const missingCounts = [1, 1, 2] // Placeholder values

        skillsChartInstance.current = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: skillCategories.map(cat => cat.replace('_', ' ').toUpperCase()),
            datasets: [
              {
                label: 'Matched Skills',
                data: matchedCounts,
                backgroundColor: 'rgba(34, 197, 94, 0.6)',
                borderColor: 'rgb(34, 197, 94)',
                borderWidth: 1
              },
              {
                label: 'Missing Skills',
                data: missingCounts,
                backgroundColor: 'rgba(239, 68, 68, 0.6)',
                borderColor: 'rgb(239, 68, 68)',
                borderWidth: 1
              }
            ]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                position: 'top'
              }
            },
            scales: {
              y: {
                beginAtZero: true
              }
            }
          }
        } as any)
      }
    }

    // Coverage Chart
    if (coverageChartRef.current) {
      const ctx = coverageChartRef.current.getContext('2d')
      if (ctx) {
        coverageChartInstance.current = new Chart(ctx, {
          type: 'doughnut',
          data: {
            labels: ['Responsibility Match', 'Requirement Match', 'Gap'],
            datasets: [{
              data: [
                75, // Placeholder responsibility coverage score
                80, // Placeholder requirement coverage score
                22.5 // Calculated gap
              ],
              backgroundColor: [
                'rgba(59, 130, 246, 0.6)',
                'rgba(147, 51, 234, 0.6)',
                'rgba(156, 163, 175, 0.6)'
              ],
              borderColor: [
                'rgb(59, 130, 246)',
                'rgb(147, 51, 234)',
                'rgb(156, 163, 175)'
              ],
              borderWidth: 1
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                position: 'bottom'
              }
            }
          }
        } as any)
      }
    }

    return () => {
      if (skillsChartInstance.current) skillsChartInstance.current.destroy()
      if (experienceChartInstance.current) experienceChartInstance.current.destroy()
      if (coverageChartInstance.current) coverageChartInstance.current.destroy()
    }
  }, [data])

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600 dark:text-green-400'
    if (score >= 60) return 'text-yellow-600 dark:text-yellow-400'
    return 'text-red-600 dark:text-red-400'
  }

  const getScoreBgColor = (score: number) => {
    if (score >= 80) return 'bg-green-500'
    if (score >= 60) return 'bg-yellow-500'
    return 'bg-red-500'
  }

  return (
    <div className="space-y-6">
      {/* AI Insights Summary */}
      <div className="bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20 p-6 rounded-lg border border-blue-200 dark:border-blue-800">
        <div className="flex items-start gap-3">
          <Zap className="w-6 h-6 text-blue-600 dark:text-blue-400 mt-1" />
          <div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">Analysis Summary</h3>
            <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
              {advancedAnalytics?.insights_summary || 'Analysis completed successfully.'}
            </p>
          </div>
        </div>
      </div>

      {/* Enhanced AI Insights */}
      {aiInsights && (
        <div className="bg-gradient-to-r from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20 p-6 rounded-lg border border-purple-200 dark:border-purple-800">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-purple-600 dark:text-purple-400" />
              AI-Powered Analysis
            </h3>
            <div className="flex items-center gap-2 text-xs text-gray-500 dark:text-gray-400">
              <span>AI Enabled: {aiInsights.ai_enabled ? 'Yes' : 'No'}</span>
            </div>
          </div>
          
          <div className="grid md:grid-cols-2 gap-6">
            {/* Match Analysis */}
            <div>
              <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-3">Match Analysis</h4>
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600 dark:text-gray-400">Overall Match</span>
                  <span className={`font-semibold ${getScoreColor(overallMatch)}`}>
                    {overallMatch}%
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600 dark:text-gray-400">Similarity Score</span>
                  <span className="font-medium text-gray-900 dark:text-gray-100">
                    {Math.round(basicAnalytics.similarity_score * 100)}%
                  </span>
                </div>
                {advancedAnalytics?.semantic_similarity_score && (
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600 dark:text-gray-400">Semantic Similarity</span>
                    <span className="font-medium text-gray-900 dark:text-gray-100">
                      {Math.round(advancedAnalytics.semantic_similarity_score * 100)}%
                    </span>
                  </div>
                )}
              </div>
            </div>

            {/* Skills Analysis */}
            <div>
              <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-3">Skills Analysis</h4>
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600 dark:text-gray-400">Matched Skills</span>
                  <span className="font-medium text-gray-900 dark:text-gray-100">
                    {advancedAnalytics?.matched_skills?.length || 0}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600 dark:text-gray-400">Missing Skills</span>
                  <span className="font-medium text-gray-900 dark:text-gray-100">
                    {advancedAnalytics?.missing_skills?.length || 0}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600 dark:text-gray-400">Extra Skills</span>
                  <span className="font-medium text-gray-900 dark:text-gray-100">
                    {advancedAnalytics?.extra_skills?.length || 0}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white dark:bg-gray-800 p-4 rounded-lg border border-gray-200 dark:border-gray-700">
          <div className="flex items-center">
            <div className={`w-3 h-3 rounded-full ${getScoreBgColor(overallMatch)} mr-3`}></div>
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-400">Overall Match</p>
              <p className={`text-2xl font-bold ${getScoreColor(overallMatch)}`}>{overallMatch}%</p>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 p-4 rounded-lg border border-gray-200 dark:border-gray-700">
          <div className="flex items-center">
            <div className="w-3 h-3 rounded-full bg-blue-500 mr-3"></div>
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-400">Common Keywords</p>
              <p className="text-2xl font-bold text-blue-600 dark:text-blue-400">{basicAnalytics.common_keywords.length}</p>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 p-4 rounded-lg border border-gray-200 dark:border-gray-700">
          <div className="flex items-center">
            <div className="w-3 h-3 rounded-full bg-red-500 mr-3"></div>
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-400">Missing Keywords</p>
              <p className="text-2xl font-bold text-red-600 dark:text-red-400">{basicAnalytics.missing_keywords.length}</p>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 p-4 rounded-lg border border-gray-200 dark:border-gray-700">
          <div className="flex items-center">
            <div className="w-3 h-3 rounded-full bg-green-500 mr-3"></div>
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-400">Processing Time</p>
              <p className="text-2xl font-bold text-green-600 dark:text-green-400">{data.processing_time}s</p>
            </div>
          </div>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white dark:bg-gray-800 p-4 rounded-lg border border-gray-200 dark:border-gray-700">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">Skills Analysis</h3>
          <div className="h-64">
            <canvas ref={skillsChartRef}></canvas>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 p-4 rounded-lg border border-gray-200 dark:border-gray-700">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">Coverage Analysis</h3>
          <div className="h-64">
            <canvas ref={coverageChartRef}></canvas>
          </div>
        </div>
      </div>

      {/* Word Clouds */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                 <div className="bg-white dark:bg-gray-800 p-4 rounded-lg border border-gray-200 dark:border-gray-700">
           <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">Resume Keywords</h3>
           <WordCloud words={resumeWords} type="resume" />
         </div>

         <div className="bg-white dark:bg-gray-800 p-4 rounded-lg border border-gray-200 dark:border-gray-700">
           <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">Job Description Keywords</h3>
           <WordCloud words={jdWords} type="jd" />
         </div>
      </div>

      {/* Analysis Details */}
      <div className="bg-white dark:bg-gray-800 p-6 rounded-lg border border-gray-200 dark:border-gray-700">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">Analysis Details</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-2">Resume Analysis</h4>
            <ul className="space-y-1 text-sm text-gray-600 dark:text-gray-400">
              <li>• Total words: {Object.keys(basicAnalytics.resume_word_frequency).length}</li>
              <li>• Readability: {advancedAnalytics?.resume_readability ? Math.round(advancedAnalytics.resume_readability) : 'N/A'}</li>
            </ul>
          </div>
          <div>
            <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-2">Job Description Analysis</h4>
            <ul className="space-y-1 text-sm text-gray-600 dark:text-gray-400">
              <li>• Total words: {Object.keys(basicAnalytics.jd_word_frequency).length}</li>
              <li>• Readability: {advancedAnalytics?.jd_readability ? Math.round(advancedAnalytics.jd_readability) : 'N/A'}</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}