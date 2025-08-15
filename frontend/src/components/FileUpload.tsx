'use client'

import { useState, useEffect } from 'react'
import { Upload, FileText, ChevronDown, ChevronUp, Sparkles, Zap } from 'lucide-react'
import Loader from './Loader'

interface FileUploadProps {
  onAnalysisComplete: (data: any) => void;
}

interface StoredData {
  resumeText: string;
  jobDescriptionText: string;
  timestamp: number;
}

export default function FileUpload({ onAnalysisComplete }: FileUploadProps) {
  const [resume, setResume] = useState<File | null>(null)
  const [jobDescription, setJobDescription] = useState<File | null>(null)
  const [resumeText, setResumeText] = useState('')
  const [jobDescriptionText, setJobDescriptionText] = useState('')
  const [loading, setLoading] = useState(false)
  const [isExpanded, setIsExpanded] = useState(true)
  const [savedInputs, setSavedInputs] = useState<StoredData[]>([])
  const [useAI, setUseAI] = useState(false)
  const [aiUsage, setAiUsage] = useState({ daily_usage: 0, daily_limit: 3, remaining: 3, can_use_ai: true })
  const [isPremium, setIsPremium] = useState(false)

  // Load saved inputs from localStorage
  useEffect(() => {
    const saved = localStorage.getItem('jobhelp_saved_inputs')
    if (saved) {
      setSavedInputs(JSON.parse(saved))
    }
    
    // Check AI usage limits
    checkAIUsage()
  }, [])

  const checkAIUsage = async () => {
    try {
      const response = await fetch('http://localhost:8000/ai-usage?user_id=default')
      if (response.ok) {
        const usage = await response.json()
        setAiUsage(usage)
      }
    } catch (error) {
      console.error('Failed to check AI usage:', error)
    }
  }

  const saveCurrentInput = () => {
    const newInput: StoredData = {
      resumeText,
      jobDescriptionText,
      timestamp: Date.now()
    }
    const updatedInputs = [newInput, ...savedInputs].slice(0, 5) // Keep last 5 entries
    setSavedInputs(updatedInputs)
    localStorage.setItem('jobhelp_saved_inputs', JSON.stringify(updatedInputs))
  }

  const loadSavedInput = (input: StoredData) => {
    setResumeText(input.resumeText)
    setJobDescriptionText(input.jobDescriptionText)
    setResume(null)
    setJobDescription(null)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if ((!resume && !resumeText) || (!jobDescription && !jobDescriptionText)) {
      alert('Please provide both resume and job description (either as files or text)')
      return
    }

    saveCurrentInput()
    setLoading(true)
    const formData = new FormData()
    
    if (resume) {
      formData.append('resume_file', resume)
    }
    if (jobDescription) {
      formData.append('job_description_file', jobDescription)
    }
    if (resumeText) {
      formData.append('resume_text', resumeText)
    }
    if (jobDescriptionText) {
      formData.append('job_description_text', jobDescriptionText)
    }

    try {
      // Build URL with query parameters for AI options
      const searchParams = new URLSearchParams()
      if (useAI) {
        searchParams.append('use_ai', 'true')
        searchParams.append('user_id', 'default')
        searchParams.append('is_premium', isPremium.toString())
      }
      
      const url = `http://localhost:8000/analyze${searchParams.toString() ? '?' + searchParams.toString() : ''}`
      
      const response = await fetch(url, {
        method: 'POST',
        body: formData,
        credentials: 'include',
        headers: {
          'Accept': 'application/json',
        },
      })

      if (!response.ok) {
        throw new Error('Analysis failed')
      }

      const data = await response.json()
      onAnalysisComplete(data)
      setIsExpanded(false)
      
      // Refresh AI usage after successful AI analysis
      if (useAI) {
        checkAIUsage()
      }
    } catch (error) {
      console.error('Error:', error)
      alert('Failed to analyze documents. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-white dark:bg-black rounded-xl shadow-lg border border-gray-200 dark:border-gray-800 overflow-hidden">
      <div 
        className="flex items-center justify-between p-4 sm:p-6 cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-900/50 transition-colors"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-black dark:bg-white rounded-lg flex items-center justify-center">
            <Upload className="w-5 h-5 text-white dark:text-black" />
          </div>
          <div>
            <h2 className="text-lg sm:text-xl font-bold text-black dark:text-white">
              Document Upload
            </h2>
            <p className="text-sm text-gray-600 dark:text-gray-400">Upload files or paste text for analysis</p>
          </div>
        </div>
        {isExpanded ? (
          <ChevronUp className="w-6 h-6 text-gray-500 dark:text-gray-400" />
        ) : (
          <ChevronDown className="w-6 h-6 text-gray-500 dark:text-gray-400" />
        )}
      </div>

      {isExpanded && (
        <div className="p-4 sm:p-6 border-t border-gray-200 dark:border-gray-800">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 lg:gap-8">
            {/* Resume Section */}
            <div className="space-y-4">
              <div className="flex items-center space-x-2">
                <div className="w-6 h-6 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center">
                  <FileText className="w-4 h-4 text-blue-600 dark:text-blue-400" />
                </div>
                <h3 className="text-base font-semibold text-black dark:text-white">Resume</h3>
              </div>
              
              {/* File Upload */}
              <div>
                <label className="flex flex-col w-full h-28 border-2 border-gray-300 dark:border-gray-600 border-dashed rounded-xl cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-900/50 transition-all duration-200 hover:border-gray-400 dark:hover:border-gray-500">
                  <div className="flex flex-col items-center justify-center pt-6 pb-6">
                    <Upload className="w-8 h-8 mb-2 text-gray-500 dark:text-gray-400" />
                    <p className="text-sm font-medium text-gray-700 dark:text-gray-300">
                      {resume ? resume.name : 'Upload Resume (PDF/DOCX)'}
                    </p>
                    <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                      Click to browse or drag & drop
                    </p>
                  </div>
                  <input
                    type="file"
                    className="hidden"
                    accept=".pdf,.docx"
                    onChange={(e) => setResume(e.target.files?.[0] || null)}
                  />
                </label>
              </div>

              {/* Text Input */}
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Or paste text directly
                </label>
                <textarea
                  value={resumeText}
                  onChange={(e) => setResumeText(e.target.value)}
                  className="w-full h-32 px-4 py-3 text-sm text-black dark:text-white border rounded-xl focus:outline-none focus:ring-2 focus:ring-black dark:focus:ring-white focus:border-transparent bg-white dark:bg-black border-gray-300 dark:border-gray-600 placeholder-gray-500 dark:placeholder-gray-400 resize-none"
                  placeholder="Paste your resume content here..."
                />
              </div>
            </div>

            {/* Job Description Section */}
            <div className="space-y-4">
              <div className="flex items-center space-x-2">
                <div className="w-6 h-6 bg-green-100 dark:bg-green-900/30 rounded-lg flex items-center justify-center">
                  <FileText className="w-4 h-4 text-green-600 dark:text-green-400" />
                </div>
                <h3 className="text-base font-semibold text-black dark:text-white">Job Description</h3>
              </div>
              
              {/* File Upload */}
              <div>
                <label className="flex flex-col w-full h-28 border-2 border-gray-300 dark:border-gray-600 border-dashed rounded-xl cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-900/50 transition-all duration-200 hover:border-gray-400 dark:hover:border-gray-500">
                  <div className="flex flex-col items-center justify-center pt-6 pb-6">
                    <FileText className="w-8 h-8 mb-2 text-gray-500 dark:text-gray-400" />
                    <p className="text-sm font-medium text-gray-700 dark:text-gray-300">
                      {jobDescription ? jobDescription.name : 'Upload Job Description (PDF/DOCX)'}
                    </p>
                    <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                      Click to browse or drag & drop
                    </p>
                  </div>
                  <input
                    type="file"
                    className="hidden"
                    accept=".pdf,.docx"
                    onChange={(e) => setJobDescription(e.target.files?.[0] || null)}
                  />
                </label>
              </div>

              {/* Text Input */}
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Or paste text directly
                </label>
                <textarea
                  value={jobDescriptionText}
                  onChange={(e) => setJobDescriptionText(e.target.value)}
                  className="w-full h-32 px-4 py-3 text-sm text-black dark:text-white border rounded-xl focus:outline-none focus:ring-2 focus:ring-black dark:focus:ring-white focus:border-transparent bg-white dark:bg-black border-gray-300 dark:border-gray-600 placeholder-gray-500 dark:placeholder-gray-400 resize-none"
                  placeholder="Paste the job description here..."
                />
              </div>
            </div>
          </div>

          {/* Saved Inputs */}
          {savedInputs.length > 0 && (
            <div className="mt-4">
              <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Recent Comparisons</h3>
              <div className="space-y-2">
                {savedInputs.map((input, index) => (
                  <button
                    key={input.timestamp}
                    onClick={() => loadSavedInput(input)}
                    className="w-full text-left px-3 py-2 text-sm text-gray-700 dark:text-gray-300 bg-gray-50 dark:bg-gray-700/50 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
                  >
                    Comparison {index + 1} - {new Date(input.timestamp).toLocaleString()}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* AI Options */}
          <div className="mt-8 p-6 bg-gradient-to-r from-purple-50 via-blue-50 to-indigo-50 dark:from-purple-900/10 dark:via-blue-900/10 dark:to-indigo-900/10 rounded-2xl border border-purple-200 dark:border-purple-800">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-4">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-gradient-to-r from-purple-500 to-blue-500 rounded-xl flex items-center justify-center">
                  <Sparkles className="w-5 h-5 text-white" />
                </div>
                <div>
                  <h3 className="text-base font-semibold text-black dark:text-white">AI-Powered Insights</h3>
                  <span className="px-3 py-1 text-xs bg-purple-100 dark:bg-purple-900/30 text-purple-800 dark:text-purple-200 rounded-full font-medium">
                    {isPremium ? 'Premium' : 'Free Tier'}
                  </span>
                </div>
              </div>
              <label className="flex items-center space-x-3 cursor-pointer">
                <div className="relative">
                  <input
                    type="checkbox"
                    checked={useAI}
                    onChange={(e) => setUseAI(e.target.checked)}
                    disabled={!aiUsage.can_use_ai && !isPremium}
                    className="w-5 h-5 text-purple-600 bg-white dark:bg-black border-2 border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-purple-500 dark:focus:ring-purple-400 focus:border-transparent disabled:opacity-50 disabled:cursor-not-allowed"
                  />
                </div>
                <span className="text-sm font-medium text-black dark:text-white">
                  Enable AI Analysis
                </span>
              </label>
            </div>
            
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 mb-4">
              <div className="flex items-center space-x-2 text-sm">
                <span className="text-2xl">✨</span>
                <span className="text-gray-700 dark:text-gray-300">Personalized suggestions</span>
              </div>
              <div className="flex items-center space-x-2 text-sm">
                <span className="text-2xl">🎯</span>
                <span className="text-gray-700 dark:text-gray-300">ATS optimization</span>
              </div>
              <div className="flex items-center space-x-2 text-sm">
                <span className="text-2xl">🚀</span>
                <span className="text-gray-700 dark:text-gray-300">Role-fit analysis</span>
              </div>
            </div>
            
            {!isPremium && (
              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 p-3 bg-yellow-50 dark:bg-yellow-900/20 rounded-xl border border-yellow-200 dark:border-yellow-800">
                <div className="flex items-center space-x-2">
                  <Zap className="w-4 h-4 text-yellow-600 dark:text-yellow-400" />
                  <span className="text-sm text-gray-700 dark:text-gray-300">
                    Daily limit: <span className="font-semibold">{aiUsage.daily_usage}/{aiUsage.daily_limit}</span> used
                  </span>
                </div>
                {!aiUsage.can_use_ai && (
                  <span className="text-sm text-red-600 dark:text-red-400 font-medium px-3 py-1 bg-red-50 dark:bg-red-900/20 rounded-lg">
                    Daily limit reached
                  </span>
                )}
              </div>
            )}
          </div>

          {/* Submit Button */}
          <button
            onClick={handleSubmit}
            disabled={loading || (!resume && !resumeText) || (!jobDescription && !jobDescriptionText)}
            className="mt-8 w-full py-4 px-6 border border-transparent rounded-xl shadow-lg text-base font-semibold text-white bg-gradient-to-r from-black to-gray-800 dark:from-white dark:to-gray-200 hover:from-gray-800 hover:to-black dark:hover:from-gray-200 dark:hover:to-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-black dark:focus:ring-white disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 transform hover:scale-[1.02] active:scale-[0.98]"
          >
            {loading ? (
              <div className="flex items-center justify-center space-x-2">
                <Loader />
                <span>Analyzing...</span>
              </div>
            ) : (
              <div className="flex items-center justify-center space-x-2">
                {useAI ? (
                  <>
                    <Sparkles className="w-5 h-5" />
                    <span>Analyze with AI ✨</span>
                  </>
                ) : (
                  <>
                    <FileText className="w-5 h-5" />
                    <span>Analyze Documents</span>
                  </>
                )}
              </div>
            )}
          </button>
        </div>
      )}
    </div>
  )
}