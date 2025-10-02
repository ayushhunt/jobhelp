import axios, { AxiosInstance, AxiosResponse } from 'axios';

// API configuration
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
const API_VERSION = '/api/v1';

// Create axios instance for company research
const companyResearchClient: AxiosInstance = axios.create({
  baseURL: `${API_BASE_URL}${API_VERSION}/company-research`,
  timeout: 60000, // 60 seconds for research operations
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
companyResearchClient.interceptors.request.use(
  (config) => {
    console.log(`🔍 Company Research Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('❌ Company Research Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor
companyResearchClient.interceptors.response.use(
  (response: AxiosResponse) => {
    console.log(`✅ Company Research Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('❌ Company Research Response Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// Types for Company Research
export interface CompanyResearchRequest {
  company_name?: string;
  company_domain?: string;
  research_depth: 'basic' | 'standard' | 'comprehensive';
  include_employee_reviews?: boolean;
  include_financial_data?: boolean;
  user_id: string;
  is_premium: boolean;
}

export interface LocationData {
  source: string;
  address?: string;
  city?: string;
  state?: string;
  country?: string;
  postal_code?: string;
  latitude?: number;
  longitude?: number;
  formatted_address?: string;
  place_id?: string;
  confidence_score?: number;
  last_updated: string;
}

export interface LocationComparison {
  address_similarity_score: number;
  coordinate_distance_km?: number;
  city_match: boolean;
  state_match: boolean;
  country_match: boolean;
  postal_code_match: boolean;
  overall_location_confidence: number;
}

export interface LocationVerificationData {
  company_name: string;
  search_query: string;
  google_places_data?: LocationData;
  nominatim_osm_data?: LocationData;
  comparison?: LocationComparison;
  authenticity_score: number;
  verification_status: 'verified' | 'suspicious' | 'unknown';
  risk_factors: string[];
  trust_indicators: string[];
  last_verified: string;
}

export interface WHOISData {
  domain: string;
  registrar?: string;
  creation_date?: string;
  expiration_date?: string;
  updated_date?: string;
  status: string[];
  name_servers: string[];
  registrant_organization?: string;
  registrant_country?: string;
  admin_contact?: Record<string, string>;
  tech_contact?: Record<string, string>;
  dnssec?: string;
  last_checked: string;
}

export interface WebSearchResult {
  title: string;
  url: string;
  snippet: string;
  source: string;
  published_date?: string;
  relevance_score?: number;
  content_type: string;
}

export interface KnowledgeGraphData {
  entity_id?: string;
  name: string;
  description?: string;
  entity_type?: string;
  industry?: string;
  founded_date?: string;
  headquarters?: string;
  ceo?: string;
  employees?: string;
  revenue?: string;
  website?: string;
  social_media?: Record<string, string>;
  subsidiaries?: string[];
  competitors?: string[];
}

export interface CompanyAuthenticity {
  domain_age_days?: number;
  domain_reputation_score?: number;
  social_presence_score?: number;
  news_mentions_count?: number;
  employee_reviews_count?: number;
  authenticity_score?: number;
  risk_factors: string[];
  trust_indicators: string[];
  overall_assessment: string;
}

export interface CompanyGrowth {
  employee_growth_trend?: string;
  funding_rounds?: Record<string, any>[];
  acquisition_history?: Record<string, any>[];
}

export interface PortfolioPageData {
  url: string;
  title: string;
  text: string;
  scraped_at: string;
}

export interface PortfolioSummary {
  summary: string;
  method: string;
  model_used?: string;
  key_phrases?: string[];
  entities?: Record<string, string[]>;
  techniques_used?: string[];
  error?: string;
  generated_at: string;
}

export interface PortfolioData {
  domain: string;
  pages: PortfolioPageData[];
  raw_text: string;
  portfolio_urls: string[];
  technologies: string[];
  industries: string[];
  projects: string[];
  scraped_at: string;
  total_pages_scraped: number;
  total_content_length: number;
  llm_summary: PortfolioSummary;
  nlp_summary: PortfolioSummary;
}

export interface CompanyResearchResponse {
  request_id: string;
  company_name: string;
  company_domain?: string;
  research_depth: string;
  
  // Individual research data fields (matching backend schema)
  whois_data?: WHOISData;
  web_search_results?: WebSearchResult[];
  knowledge_graph_data?: KnowledgeGraphData;
  location_verification_data?: LocationVerificationData;
  ai_analysis_data?: any;
  
  // Synthesized insights
  company_authenticity?: CompanyAuthenticity;
  company_growth?: CompanyGrowth;
  employee_insights?: any;
  portfolio_data?: PortfolioData;
  
  // AI-generated summary
  executive_summary?: string;
  key_insights?: string[];
  risk_assessment?: string;
  recommendations?: string[];
  
  // Research metadata
  authenticity_score: number;
  research_status: string;
  total_cost: number;
  total_processing_time: number;
  timestamp: string;
  
  // Task-level results
  sources_used?: string[];
  failed_sources?: string[];
  task_results?: any[];
}

export interface ResearchProgress {
  request_id: string;
  company_name: string;
  overall_progress: number;
  status: 'pending' | 'in_progress' | 'completed' | 'failed' | 'partial';
  completed_tasks: string[];
  current_task?: string;
  estimated_completion?: string;
  last_updated: string;
}

export interface ResearchCostEstimate {
  research_depth: string;
  estimated_total_cost: number;
  cost_breakdown: Record<string, number>;
  cost_optimization_tips: string[];
  alternative_research_options: Record<string, any>[];
}

export interface ServiceHealth {
  overall_status: string;
  services: Record<string, {
    is_healthy: boolean;
    last_checked: string;
    error_message?: string;
  }>;
  active_sessions: number;
}

export interface ResearchSourceInfo {
  available_sources: Record<string, {
    name: string;
    description: string;
    cost_per_request: number;
    is_healthy: boolean;
    capabilities: string[];
  }>;
  total_sources: number;
  research_depths: string[];
}

export interface QuickCheckResult {
  company_name: string;
  company_domain?: string;
  domain_verified: boolean;
  web_presence: boolean;
  basic_authenticity: string;
  research_status: string;
  processing_time: number;
}

// Company Research API Service
export class CompanyResearchAPIService {
  // Perform comprehensive company research
  static async researchCompany(request: CompanyResearchRequest): Promise<CompanyResearchResponse> {
    const response = await companyResearchClient.post('/research', request);
    return response.data;
  }

  // Initiate asynchronous research
  static async researchCompanyAsync(request: CompanyResearchRequest): Promise<{ request_id: string; status: string; message: string }> {
    const response = await companyResearchClient.post('/research/async', request);
    return response.data;
  }

  // Get research progress
  static async getResearchProgress(requestId: string): Promise<ResearchProgress> {
    const response = await companyResearchClient.get(`/research/progress/${requestId}`);
    return response.data;
  }

  // Cancel research
  static async cancelResearch(requestId: string): Promise<{ message: string; request_id: string }> {
    const response = await companyResearchClient.delete(`/research/cancel/${requestId}`);
    return response.data;
  }

  // Get cost estimate
  static async getCostEstimate(researchDepth: string = 'standard'): Promise<ResearchCostEstimate> {
    const response = await companyResearchClient.get(`/research/cost-estimate?research_depth=${researchDepth}`);
    return response.data;
  }

  // Get service health
  static async getServiceHealth(): Promise<ServiceHealth> {
    const response = await companyResearchClient.get('/research/health');
    return response.data;
  }

  // Test all services
  static async testAllServices(): Promise<{
    overall_status: string;
    test_results: Record<string, boolean>;
    timestamp: string;
  }> {
    const response = await companyResearchClient.post('/research/test-services');
    return response.data;
  }

  // Get research sources info
  static async getResearchSources(): Promise<ResearchSourceInfo> {
    const response = await companyResearchClient.get('/research/sources');
    return response.data;
  }

  // Quick company check
  static async quickCompanyCheck(
    companyName?: string,
    companyDomain?: string
  ): Promise<QuickCheckResult> {
    const params = new URLSearchParams();
    if (companyName) params.append('company_name', companyName);
    if (companyDomain) params.append('company_domain', companyDomain);
    
    const response = await companyResearchClient.get(`/research/quick-check?${params.toString()}`);
    return response.data;
  }

  // Stream research progress (Server-Sent Events)
  static createProgressStream(requestId: string): EventSource {
    return new EventSource(`${API_BASE_URL}${API_VERSION}/company-research/research/stream/${requestId}`);
  }
}

// Export the client for direct use if needed
export { companyResearchClient };

// Export default instance
export default CompanyResearchAPIService;

