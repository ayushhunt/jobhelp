import axios, { AxiosInstance, AxiosResponse } from 'axios';

// API configuration
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
const API_VERSION = '/api/v1';

// Create axios instance with default configuration
const apiClient: AxiosInstance = axios.create({
  baseURL: `${API_BASE_URL}${API_VERSION}`,
  timeout: 30000, // 30 seconds
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging and error handling
apiClient.interceptors.request.use(
  (config) => {
    console.log(`🚀 API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('❌ Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for logging and error handling
apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    console.log(`✅ API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('❌ Response Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// API response types
export interface AnalysisRequest {
  resume_file?: File;
  job_description_file?: File;
  resume_text?: string;
  job_description_text?: string;
  use_ai?: boolean;
  user_id?: string;
  is_premium?: boolean;
  analysis_type?: 'basic' | 'advanced' | 'ai_enhanced';
}

export interface AnalysisResponse {
  basic_analytics: {
    similarity_score: number;
    resume_word_frequency: Record<string, number>;
    jd_word_frequency: Record<string, number>;
    common_keywords: string[];
    missing_keywords: string[];
  };
  advanced_analytics?: {
    semantic_similarity_score: number;
    matched_skills: string[];
    missing_skills: string[];
    extra_skills: string[];
    resume_readability: number;
    jd_readability: number;
    insights_summary: string;
  };
  experience_analysis?: {
    experience_analysis: any;
    career_stability: number;
  };
  ai_insights?: {
    ai_insights: any;
    ai_enabled: boolean;
  };
  analysis_type: string;
  processing_time: number;
  timestamp: string;
}

export interface AIUsageResponse {
  user_id: string;
  daily_usage: number;
  daily_limit: number;
  remaining: number;
  can_use_ai: boolean;
}

export interface ModelInfo {
  id: string;
  name: string;
  provider: string;
  cost_per_1k_tokens: string;
  max_tokens: number;
  context_window: number;
  speed_tier: string;
  quality_tier: string;
}

export interface AvailableModelsResponse {
  available_models: ModelInfo[];
  total_available: number;
  recommended: Record<string, string>;
  free_tier_preference: string[];
  premium_tier_preference: string[];
}

// API service class
export class APIService {
  // Document analysis
  static async analyzeDocuments(data: AnalysisRequest): Promise<AnalysisResponse> {
    const formData = new FormData();
    
    // Add files if provided
    if (data.resume_file) {
      formData.append('resume_file', data.resume_file);
    }
    if (data.job_description_file) {
      formData.append('job_description_file', data.job_description_file);
    }
    
    // Add text if provided
    if (data.resume_text) {
      formData.append('resume_text', data.resume_text);
    }
    if (data.job_description_text) {
      formData.append('job_description_text', data.job_description_text);
    }
    
    // Add query parameters
    const params = new URLSearchParams();
    if (data.use_ai) {
      params.append('use_ai', 'true');
      params.append('analysis_type', 'ai_enhanced');
    } else {
      params.append('analysis_type', 'advanced'); // Always request advanced analysis
    }
    if (data.user_id) {
      params.append('user_id', data.user_id);
    }
    if (data.is_premium !== undefined) {
      params.append('is_premium', data.is_premium.toString());
    }
    
    const response = await apiClient.post(`/analysis/analyze?${params.toString()}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    return response.data;
  }
  
  // AI usage statistics
  static async getAIUsage(userId: string = 'default'): Promise<AIUsageResponse> {
    const response = await apiClient.get(`/analysis/ai-usage?user_id=${userId}`);
    return response.data;
  }
  
  // Available AI models
  static async getAvailableModels(): Promise<AvailableModelsResponse> {
    const response = await apiClient.get('/analysis/ai-models');
    return response.data;
  }
  
  // Cost comparison
  static async getCostComparison(): Promise<any> {
    const response = await apiClient.get('/analysis/ai-costs');
    return response.data;
  }
  
  // Health check
  static async healthCheck(): Promise<any> {
    const response = await axios.get(`${API_BASE_URL}/health`);
    return response.data;
  }
}

// Export the apiClient for direct use if needed
export { apiClient };

// Export default instance
export default APIService;
