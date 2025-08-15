import { useState, useCallback } from 'react';
import { APIService, AnalysisRequest, AnalysisResponse } from '../services/api';

interface UseAnalysisReturn {
  // State
  loading: boolean;
  error: string | null;
  analysisData: AnalysisResponse | null;
  
  // Actions
  analyzeDocuments: (data: AnalysisRequest) => Promise<void>;
  resetAnalysis: () => void;
  clearError: () => void;
}

export const useAnalysis = (): UseAnalysisReturn => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [analysisData, setAnalysisData] = useState<AnalysisResponse | null>(null);

  const analyzeDocuments = useCallback(async (data: AnalysisRequest) => {
    try {
      setLoading(true);
      setError(null);
      
      const result = await APIService.analyzeDocuments(data);
      setAnalysisData(result);
    } catch (err: any) {
      const errorMessage = err.response?.data?.message || err.message || 'Analysis failed';
      setError(errorMessage);
      console.error('Analysis error:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  const resetAnalysis = useCallback(() => {
    setAnalysisData(null);
    setError(null);
  }, []);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  return {
    loading,
    error,
    analysisData,
    analyzeDocuments,
    resetAnalysis,
    clearError,
  };
};
