'use client'

import { useState, useEffect } from 'react'
import { Upload, FileText, ChevronDown, ChevronUp, Sparkles, Zap, History, Trash2 } from 'lucide-react'
import Loader from './Loader'
import { useAnalysis } from '../hooks/useAnalysis'
import { useAIUsage } from '../hooks/useAIUsage'
import { StorageManager, StoredInput } from '../utils/storage'
import { AnalysisRequest } from '../services/api'

interface FileUploadProps {
  onAnalysisComplete: (data: any) => void;
}

export default function FileUpload({ onAnalysisComplete }: FileUploadProps) {
  // File and text state
  const [resume, setResume] = useState<File | null>(null)
  const [jobDescription, setJobDescription] = useState<File | null>(null)
  const [resumeText, setResumeText] = useState('')
  const [jobDescriptionText, setJobDescriptionText] = useState('')
  
  // UI state
  const [isExpanded, setIsExpanded] = useState(true)
  const [savedInputs, setSavedInputs] = useState<StoredInput[]>([])
  const [useAI, setUseAI] = useState(false)
  const [isPremium, setIsPremium] = useState(false)

  // Custom hooks
  const { loading, error, analysisData, analyzeDocuments } = useAnalysis()
  const { aiUsage } = useAIUsage()

  // Notify parent when analysis is complete
  useEffect(() => {
    if (analysisData) {
      onAnalysisComplete(analysisData)
      setIsExpanded(false)
    }
  }, [analysisData, onAnalysisComplete])

  // Load saved inputs and preferences on mount
  useEffect(() => {
    const saved = StorageManager.getSavedInputs()
    setSavedInputs(saved)
    
    const preferences = StorageManager.getUserPreferences()
    setIsPremium(preferences.isPremium || false)
  }, [])

  // Save current input to storage
  const saveCurrentInput = () => {
    const newInput: StoredInput = {
      resumeText,
      jobDescriptionText,
      timestamp: Date.now()
    }
    StorageManager.saveInput(newInput)
    setSavedInputs(StorageManager.getSavedInputs())
  }

  // Load saved input
  const loadSavedInput = (input: StoredInput) => {
    setResumeText(input.resumeText)
    setJobDescriptionText(input.jobDescriptionText)
    setResume(null)
    setJobDescription(null)
  }

  // Clear saved input
  const clearSavedInput = (timestamp: number) => {
    const updated = savedInputs.filter(input => input.timestamp !== timestamp)
    StorageManager.setItem('jobhelp_saved_inputs', updated)
    setSavedInputs(updated)
  }

  // Handle form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if ((!resume && !resumeText) || (!jobDescription && !jobDescriptionText)) {
      alert('Please provide both resume and job description (either as files or text)')
      return
    }

    saveCurrentInput()
    
    const analysisRequest: AnalysisRequest = {
      resume_file: resume || undefined,
      job_description_file: jobDescription || undefined,
      resume_text: resumeText || undefined,
      job_description_text: jobDescriptionText || undefined,
      use_ai: useAI,
      user_id: 'default',
      is_premium: isPremium
    }

    try {
      await analyzeDocuments(analysisRequest)
    } catch (error) {
      console.error('Analysis failed:', error)
    }
  }

  // Handle file changes
  const handleFileChange = (file: File | null, type: 'resume' | 'jobDescription') => {
    if (type === 'resume') {
      setResume(file)
      setResumeText('') // Clear text when file is selected
    } else {
      setJobDescription(file)
      setJobDescriptionText('') // Clear text when file is selected
    }
  }

  // Handle text changes
  const handleTextChange = (text: string, type: 'resume' | 'jobDescription') => {
    if (type === 'resume') {
      setResumeText(text)
      setResume(null) // Clear file when text is entered
    } else {
      setJobDescriptionText(text)
      setJobDescription(null) // Clear file when text is entered
    }
  }

  // Save user preferences
  const handlePremiumChange = (premium: boolean) => {
    setIsPremium(premium)
    StorageManager.saveUserPreferences({ isPremium: premium })
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 mb-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
          Document Analysis
        </h2>
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
        >
          {isExpanded ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
        </button>
      </div>

      {isExpanded && (
        <>
          {/* AI Usage Status */}
          {aiUsage && (
            <div className="mb-4 p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
              <div className="flex items-center justify-between text-sm">
                <span className="text-blue-700 dark:text-blue-300">
                  AI Usage: {aiUsage.daily_usage}/{aiUsage.daily_limit}
                </span>
                <span className={`px-2 py-1 rounded-full text-xs ${
                  aiUsage.can_use_ai 
                    ? 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-300'
                    : 'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-300'
                }`}>
                  {aiUsage.can_use_ai ? 'Available' : 'Limit Reached'}
                </span>
              </div>
            </div>
          )}

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Resume Input */}
            <div className="space-y-2">
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                Resume
              </label>
              <div className="flex space-x-2">
                <input
                  type="file"
                  accept=".pdf,.docx,.txt"
                  onChange={(e) => handleFileChange(e.target.files?.[0] || null, 'resume')}
                  className="flex-1 text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 dark:file:bg-blue-900/20 dark:file:text-blue-300"
                />
                <span className="text-gray-400">or</span>
                <input
                  type="text"
                  placeholder="Paste resume text here..."
                  value={resumeText}
                  onChange={(e) => handleTextChange(e.target.value, 'resume')}
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                />
              </div>
            </div>

            {/* Job Description Input */}
            <div className="space-y-2">
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                Job Description
              </label>
              <div className="flex space-x-2">
                <input
                  type="file"
                  accept=".pdf,.docx,.txt"
                  onChange={(e) => handleFileChange(e.target.files?.[0] || null, 'jobDescription')}
                  className="flex-1 text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 dark:file:bg-blue-900/20 dark:file:text-blue-300"
                />
                <span className="text-gray-400">or</span>
                <input
                  type="text"
                  placeholder="Paste job description text here..."
                  value={jobDescriptionText}
                  onChange={(e) => handleTextChange(e.target.value, 'jobDescription')}
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                />
              </div>
            </div>

            {/* AI Options */}
            <div className="flex items-center space-x-4">
              <label className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  checked={useAI}
                  onChange={(e) => setUseAI(e.target.checked)}
                  disabled={!aiUsage?.can_use_ai}
                  className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                  <Sparkles className="inline w-4 h-4 mr-1" />
                  Enable AI Insights
                </span>
              </label>
              
              <label className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  checked={isPremium}
                  onChange={(e) => handlePremiumChange(e.target.checked)}
                  className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                  <Zap className="inline w-4 h-4 mr-1" />
                  Premium User
                </span>
              </label>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white font-medium py-2 px-4 rounded-md transition duration-200 flex items-center justify-center space-x-2"
            >
              {loading ? (
                <>
                  <Loader />
                  <span>Analyzing...</span>
                </>
              ) : (
                <>
                  <Upload className="w-4 h-4" />
                  <span>Analyze Documents</span>
                </>
              )}
            </button>
          </form>

          {/* Error Display */}
          {error && (
            <div className="mt-4 p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
              <p className="text-red-700 dark:text-red-300 text-sm">{error}</p>
            </div>
          )}

          {/* Saved Inputs */}
          {savedInputs.length > 0 && (
            <div className="mt-6">
              <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-3 flex items-center">
                <History className="w-5 h-5 mr-2" />
                Saved Inputs
              </h3>
              <div className="space-y-2">
                {savedInputs.map((input, index) => (
                  <div key={input.timestamp} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                    <div className="flex-1 min-w-0">
                      <p className="text-sm text-gray-900 dark:text-white truncate">
                        Resume: {input.resumeText.substring(0, 50)}...
                      </p>
                      <p className="text-sm text-gray-500 dark:text-gray-400 truncate">
                        JD: {input.jobDescriptionText.substring(0, 50)}...
                      </p>
                      <p className="text-xs text-gray-400 dark:text-gray-500">
                        {new Date(input.timestamp).toLocaleString()}
                      </p>
                    </div>
                    <div className="flex space-x-2 ml-3">
                      <button
                        onClick={() => loadSavedInput(input)}
                        className="p-1 text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300"
                        title="Load this input"
                      >
                        <FileText className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => clearSavedInput(input.timestamp)}
                        className="p-1 text-red-600 hover:text-red-800 dark:text-red-400 dark:hover:text-red-300"
                        title="Delete this input"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </>
      )}
    </div>
  )
}