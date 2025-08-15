import { useState, useEffect, useCallback } from 'react';
import { APIService, AIUsageResponse } from '../services/api';

interface UseAIUsageReturn {
  // State
  aiUsage: AIUsageResponse | null;
  loading: boolean;
  error: string | null;
  
  // Actions
  refreshUsage: () => Promise<void>;
  clearError: () => void;
}

export const useAIUsage = (userId: string = 'default'): UseAIUsageReturn => {
  const [aiUsage, setAiUsage] = useState<AIUsageResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchUsage = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      
      const result = await APIService.getAIUsage(userId);
      setAiUsage(result);
    } catch (err: any) {
      const errorMessage = err.response?.data?.message || err.message || 'Failed to fetch AI usage';
      setError(errorMessage);
      console.error('AI usage fetch error:', err);
    } finally {
      setLoading(false);
    }
  }, [userId]);

  const refreshUsage = useCallback(async () => {
    await fetchUsage();
  }, [fetchUsage]);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  // Fetch usage on mount and when userId changes
  useEffect(() => {
    fetchUsage();
  }, [fetchUsage]);

  return {
    aiUsage,
    loading,
    error,
    refreshUsage,
    clearError,
  };
};
