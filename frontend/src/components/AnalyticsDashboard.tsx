'use client'

import { useEffect, useRef } from 'react'
import { Chart } from 'chart.js/auto'
import { CheckCircle, XCircle, TrendingUp, TrendingDown, Users, BookOpen, Briefcase, Zap, Target, Award, Sparkles } from 'lucide-react'
import WordCloud from './WordCloud'

interface AnalyticsData {
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

interface AnalyticsDashboardProps {
  data: AnalyticsData
}

export default function AnalyticsDashboard({ data }: AnalyticsDashboardProps) {
  const skillsChartRef = useRef<HTMLCanvasElement>(null)
  const experienceChartRef = useRef<HTMLCanvasElement>(null)
  const coverageChartRef = useRef<HTMLCanvasElement>(null)
  const skillsChartInstance = useRef<Chart | null>(null)
  const experienceChartInstance = useRef<Chart | null>(null)
  const coverageChartInstance = useRef<Chart | null>(null)

  // Filter out common words and single characters
  const filterOutliers = (words: Record<string, number>) => {
    const commonWords = new Set(['the', 'and', 'or', 'a', 'an', 'in', 'on', 'at', 'to', 'for', 'of', 'with'])
    return Object.entries(words)
      .filter(([word]) => !commonWords.has(word.toLowerCase()) && word.length > 1)
      .sort((a, b) => b[1] - a[1])
  }

  // Prepare word cloud data
  const resumeWords = filterOutliers(data.resume_word_frequency)
    .map(([text, value]) => ({ text, value }))
  const jdWords = filterOutliers(data.jd_word_frequency)
    .map(([text, value]) => ({ text, value }))

  // Calculate overall match percentage
  const overallMatch = Math.round((data.similarity_score + (data.semantic_similarity_score / 100)) / 2 * 100)

  useEffect(() => {
    // Cleanup previous charts
    if (skillsChartInstance.current) skillsChartInstance.current.destroy()
    if (experienceChartInstance.current) experienceChartInstance.current.destroy()
    if (coverageChartInstance.current) coverageChartInstance.current.destroy()

    // Skills Chart
    if (skillsChartRef.current) {
      const ctx = skillsChartRef.current.getContext('2d')
      if (ctx) {
        const skillCategories = Object.keys(data.matched_skills)
        const matchedCounts = skillCategories.map(cat => data.matched_skills[cat]?.length || 0)
        const missingCounts = skillCategories.map(cat => data.missing_skills[cat]?.length || 0)

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
        })
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
                data.responsibility_coverage_score,
                data.requirement_coverage_score,
                100 - ((data.responsibility_coverage_score + data.requirement_coverage_score) / 2)
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
        })
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
            <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">AI Insights</h3>
            <p className="text-gray-700 dark:text-gray-300 leading-relaxed">{data.insights_summary}</p>
          </div>
        </div>
      </div>

      {/* Enhanced AI Insights */}
      {data.ai_insights && (
        <div className="bg-gradient-to-r from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20 p-6 rounded-lg border border-purple-200 dark:border-purple-800">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-purple-600 dark:text-purple-400" />
              AI-Powered Analysis
            </h3>
            <div className="flex items-center gap-2 text-xs text-gray-500 dark:text-gray-400">
              {data.ai_insights.model_used && (
                <span>Model: {data.ai_insights.model_used}</span>
              )}
              {data.ai_insights.tokens_used && (
                <span>•</span>
              )}
              {data.ai_insights.tokens_used && (
                <span>Tokens: {data.ai_insights.tokens_used}</span>
              )}
            </div>
          </div>
          
          <div className="grid md:grid-cols-2 gap-6">
            {/* Match Analysis */}
            <div>
              <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-3">Match Analysis</h4>
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600 dark:text-gray-400">AI Match Score</span>
                  <span className={`font-semibold ${getScoreColor(data.ai_insights.match_score)}`}>
                    {data.ai_insights.match_score}%
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600 dark:text-gray-400">Alignment Strength</span>
                  <span className="font-medium text-gray-900 dark:text-gray-100 capitalize">
                    {data.ai_insights.alignment_strength}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600 dark:text-gray-400">Experience Assessment</span>
                  <span className="font-medium text-gray-900 dark:text-gray-100 capitalize">
                    {data.ai_insights.experience_assessment}
                  </span>
                </div>
              </div>
            </div>
            
            {/* Quick Wins */}
            <div>
              <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-3">Quick Wins</h4>
              <div className="space-y-2">
                {data.ai_insights.quick_wins.map((win, index) => (
                  <div key={index} className="flex items-start gap-2">
                    <CheckCircle className="w-4 h-4 text-green-500 mt-0.5 flex-shrink-0" />
                    <span className="text-sm text-gray-700 dark:text-gray-300">{win}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
          
          {/* Skills Analysis */}
          <div className="mt-6 grid md:grid-cols-2 gap-6">
            <div>
              <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-3">Top Matched Skills</h4>
              <div className="flex flex-wrap gap-2">
                {data.ai_insights.top_matched_skills.map((skill, index) => (
                  <span 
                    key={index}
                    className="px-3 py-1 text-xs font-medium bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-200 rounded-full"
                  >
                    {skill}
                  </span>
                ))}
              </div>
            </div>
            
            <div>
              <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-3">Critical Missing Skills</h4>
              <div className="flex flex-wrap gap-2">
                {data.ai_insights.critical_missing_skills.map((skill, index) => (
                  <span 
                    key={index}
                    className="px-3 py-1 text-xs font-medium bg-red-100 dark:bg-red-900/30 text-red-800 dark:text-red-200 rounded-full"
                  >
                    {skill}
                  </span>
                ))}
              </div>
            </div>
          </div>
          
          {/* ATS & Role Fit */}
          <div className="mt-6 grid md:grid-cols-2 gap-6">
            <div className="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
              <h4 className="font-medium text-blue-900 dark:text-blue-100 mb-2">ATS Optimization</h4>
              <p className="text-sm text-blue-800 dark:text-blue-200">
                {data.ai_insights.ats_optimization_tip}
              </p>
            </div>
            
            <div className="p-4 bg-green-50 dark:bg-green-900/20 rounded-lg">
              <h4 className="font-medium text-green-900 dark:text-green-100 mb-2">Role Fit Assessment</h4>
              <p className="text-sm text-green-800 dark:text-green-200">
                {data.ai_insights.role_fit_reason}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Key Metrics */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-sm">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">Overall Match</h3>
            <Target className="w-5 h-5 text-blue-500" />
          </div>
          <div className="mt-2">
            <span className={`text-2xl font-bold ${getScoreColor(overallMatch)}`}>
              {overallMatch}%
            </span>
            <div className="mt-2 w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-full">
              <div 
                className={`h-full ${getScoreBgColor(overallMatch)} rounded-full transition-all duration-500`}
                style={{ width: `${overallMatch}%` }}
              />
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-sm">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">Experience</h3>
            <Briefcase className="w-5 h-5 text-purple-500" />
          </div>
          <div className="mt-2">
            <span className="text-lg font-semibold text-gray-900 dark:text-gray-100">
              {data.years_experience_resume}
            </span>
            <span className="text-sm text-gray-500 dark:text-gray-400"> / {data.years_experience_required} yrs</span>
            {data.experience_gap !== 0 && (
              <div className="mt-1">
                {data.experience_gap > 0 ? (
                  <span className="text-xs text-red-600 dark:text-red-400">-{data.experience_gap} years</span>
                ) : (
                  <span className="text-xs text-green-600 dark:text-green-400">+{Math.abs(data.experience_gap)} years</span>
                )}
              </div>
            )}
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-sm">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">Action Verbs</h3>
            <Zap className="w-5 h-5 text-orange-500" />
          </div>
          <div className="mt-2">
            <span className={`text-2xl font-bold ${getScoreColor(data.action_verb_analysis.strong_verb_score * 10)}`}>
              {Math.round(data.action_verb_analysis.strong_verb_score)}/10
            </span>
            <div className="text-xs text-gray-500 dark:text-gray-400 mt-1">
              {data.action_verb_analysis.verb_count} verbs found
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-sm">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">Education</h3>
            <Award className="w-5 h-5 text-green-500" />
          </div>
          <div className="mt-2">
            {data.education_match ? (
              <CheckCircle className="w-8 h-8 text-green-500" />
            ) : (
              <XCircle className="w-8 h-8 text-red-500" />
            )}
            <div className="text-xs text-gray-500 dark:text-gray-400 mt-1">
              {data.education_match ? 'Requirements met' : 'Check requirements'}
            </div>
          </div>
        </div>
      </div>

      {/* Charts Section */}
      <div className="grid md:grid-cols-2 gap-6">
        <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-sm">
          <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-4">Skills Breakdown</h3>
          <div className="h-64">
            <canvas ref={skillsChartRef} />
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-sm">
          <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-4">Coverage Analysis</h3>
          <div className="h-64">
            <canvas ref={coverageChartRef} />
          </div>
        </div>
      </div>

      {/* Word Clouds */}
      <div className="grid md:grid-cols-2 gap-6">
        <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-sm">
          <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-4">Resume Word Cloud</h3>
          <div className="h-64">
            <WordCloud words={resumeWords} type="resume" />
          </div>
        </div>
        <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-sm">
          <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-4">Job Description Word Cloud</h3>
          <div className="h-64">
            <WordCloud words={jdWords} type="jd" />
          </div>
        </div>
      </div>

      {/* Skills Analysis */}
      <div className="grid md:grid-cols-3 gap-6">
        <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-sm">
          <div className="flex items-center gap-2 mb-3">
            <CheckCircle className="w-4 h-4 text-green-500" />
            <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">Matched Skills</h3>
          </div>
          <div className="space-y-2">
            {Object.entries(data.matched_skills).map(([category, skills]) => (
              <div key={category}>
                <h4 className="text-xs font-medium text-gray-400 uppercase">{category.replace('_', ' ')}</h4>
                <div className="flex flex-wrap gap-1 mt-1">
                  {skills.map((skill) => (
                    <span
                      key={skill}
                      className="px-2 py-0.5 text-xs bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-100 rounded-full"
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-sm">
          <div className="flex items-center gap-2 mb-3">
            <XCircle className="w-4 h-4 text-red-500" />
            <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">Missing Skills</h3>
          </div>
          <div className="space-y-2">
            {Object.entries(data.missing_skills).map(([category, skills]) => (
              <div key={category}>
                <h4 className="text-xs font-medium text-gray-400 uppercase">{category.replace('_', ' ')}</h4>
                <div className="flex flex-wrap gap-1 mt-1">
                  {skills.map((skill) => (
                    <span
                      key={skill}
                      className="px-2 py-0.5 text-xs bg-red-100 dark:bg-red-900/30 text-red-800 dark:text-red-100 rounded-full"
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-sm">
          <div className="flex items-center gap-2 mb-3">
            <TrendingUp className="w-4 h-4 text-blue-500" />
            <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">Extra Skills</h3>
          </div>
          <div className="space-y-2">
            {Object.entries(data.extra_skills).map(([category, skills]) => (
              <div key={category}>
                <h4 className="text-xs font-medium text-gray-400 uppercase">{category.replace('_', ' ')}</h4>
                <div className="flex flex-wrap gap-1 mt-1">
                  {skills.map((skill) => (
                    <span
                      key={skill}
                      className="px-2 py-0.5 text-xs bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-100 rounded-full"
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Enhanced Experience Analytics */}
      {data.experience_analysis && (
        <div className="space-y-6">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100">Experience Timeline & Analysis</h2>
          
          {/* Experience by Recency */}
          <div className="grid md:grid-cols-3 gap-4">
            <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-sm">
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">Recent Experience</h3>
                <TrendingUp className="w-4 h-4 text-green-500" />
              </div>
              <div className="text-2xl font-bold text-green-600 dark:text-green-400">
                {data.experience_analysis.experience_by_recency.recent_years}y
              </div>
              <div className="text-xs text-gray-500">Last 2 years</div>
            </div>
            
            <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-sm">
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">Mid-term Experience</h3>
                <Briefcase className="w-4 h-4 text-blue-500" />
              </div>
              <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                {data.experience_analysis.experience_by_recency.mid_term_years}y
              </div>
              <div className="text-xs text-gray-500">2-5 years ago</div>
            </div>
            
            <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-sm">
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">Earlier Experience</h3>
                <BookOpen className="w-4 h-4 text-gray-500" />
              </div>
              <div className="text-2xl font-bold text-gray-600 dark:text-gray-400">
                {data.experience_analysis.experience_by_recency.older_years}y
              </div>
              <div className="text-xs text-gray-500">5+ years ago</div>
            </div>
          </div>

          {/* Career Stability */}
          <div className="grid md:grid-cols-3 gap-4">
            <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-sm">
              <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">Average Job Duration</h3>
              <div className="text-xl font-semibold text-gray-900 dark:text-gray-100">
                {Math.round(data.experience_analysis.career_stability.average_job_duration)} months
              </div>
            </div>
            
            <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-sm">
              <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">Job Changes</h3>
              <div className="text-xl font-semibold text-gray-900 dark:text-gray-100">
                {data.experience_analysis.career_stability.number_of_job_changes}
              </div>
            </div>
            
            <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-sm">
              <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">Longest Tenure</h3>
              <div className="text-xl font-semibold text-gray-900 dark:text-gray-100">
                {data.experience_analysis.career_stability.longest_tenure} years
              </div>
            </div>
          </div>

          {/* Skills Experience Mapping */}
          {data.experience_analysis.skill_experience_mapping && Object.keys(data.experience_analysis.skill_experience_mapping).length > 0 && (
            <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-sm">
              <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-3">Skills by Experience</h3>
              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
                {Object.entries(data.experience_analysis.skill_experience_mapping)
                  .slice(0, 8)
                  .map(([skill, years]) => (
                    <div key={skill} className="flex items-center justify-between p-2 bg-gray-50 dark:bg-gray-700 rounded">
                      <span className="text-sm font-medium text-gray-700 dark:text-gray-300 capitalize">{skill}</span>
                      <span className="text-xs text-gray-500 dark:text-gray-400">{years}y</span>
                    </div>
                  ))}
              </div>
            </div>
          )}

          {/* Employment Gaps */}
          {data.experience_analysis.total_experience.employment_gaps && 
           data.experience_analysis.total_experience.employment_gaps.length > 0 && (
            <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-sm">
              <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-3 flex items-center gap-2">
                <XCircle className="w-4 h-4 text-orange-500" />
                Employment Gaps
              </h3>
              <div className="space-y-2">
                {data.experience_analysis.total_experience.employment_gaps.map((gap: any, index: number) => (
                  <div key={index} className="p-2 bg-orange-50 dark:bg-orange-900/20 rounded text-sm">
                    Gap of {gap.duration_months} months ({gap.duration_years} years)
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Additional Insights */}
      <div className="grid md:grid-cols-2 gap-6">
        <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-sm">
          <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-3">Common Phrases</h3>
          <div className="flex flex-wrap gap-2">
            {data.common_phrases.map((phrase, index) => (
              <span
                key={index}
                className="px-3 py-1 text-sm bg-purple-100 dark:bg-purple-900/30 text-purple-800 dark:text-purple-100 rounded-full"
              >
                {phrase}
              </span>
            ))}
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-sm">
          <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-3">Readability</h3>
          <div className="space-y-3">
            <div>
              <div className="flex justify-between text-sm">
                <span>Resume</span>
                <span className="font-medium">{data.resume_readability.readability_level}</span>
              </div>
              <div className="text-xs text-gray-500">Score: {Math.round(data.resume_readability.flesch_reading_ease)}</div>
            </div>
            <div>
              <div className="flex justify-between text-sm">
                <span>Job Description</span>
                <span className="font-medium">{data.jd_readability.readability_level}</span>
              </div>
              <div className="text-xs text-gray-500">Score: {Math.round(data.jd_readability.flesch_reading_ease)}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}