import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios'

// API configuration
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
const API_VERSION = '/api/v1'

class ApiClient {
  private instance: AxiosInstance

  constructor(baseURL?: string) {
    this.instance = axios.create({
      baseURL: baseURL || `${API_BASE_URL}${API_VERSION}`,
      timeout: 120000, // Increased to 2 minutes for company research
      withCredentials: true, // This will include cookies in requests
      headers: {
        'Content-Type': 'application/json',
      },
    })

    this.setupInterceptors()
  }

  private setupInterceptors() {
    // Request interceptor for logging
    this.instance.interceptors.request.use(
      (config) => {
        console.log(`🚀 API Request: ${config.method?.toUpperCase()} ${config.url}`)
        return config
      },
      (error) => {
        console.error('❌ Request Error:', error)
        return Promise.reject(error)
      }
    )

    // Response interceptor for logging and error handling
    this.instance.interceptors.response.use(
      (response: AxiosResponse) => {
        console.log(`✅ API Response: ${response.status} ${response.config.url}`)
        return response
      },
      (error) => {
        console.error('❌ Response Error:', error.response?.data || error.message)
        
        if (error.response?.status === 401) {
          // Handle unauthorized access - redirect to login
          if (typeof window !== 'undefined') {
            window.location.href = '/login'
          }
        }

        return Promise.reject(this.handleError(error))
      }
    )
  }

  private handleError(error: any) {
    if (error.response) {
      // Server responded with error status
      return {
        message: error.response.data?.message || error.response.data?.detail || 'An error occurred',
        status: error.response.status,
        data: error.response.data
      }
    } else if (error.request) {
      // Request was made but no response received
      return {
        message: 'Network error. Please check your connection.',
        status: 0
      }
    } else {
      // Something else happened
      return {
        message: error.message || 'An unexpected error occurred',
        status: 0
      }
    }
  }

  // HTTP Methods - simplified to return response.data directly
  async get<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.instance.get(url, config)
    return response.data
  }

  async post<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.instance.post(url, data, config)
    return response.data
  }

  async put<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.instance.put(url, data, config)
    return response.data
  }

  async patch<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.instance.patch(url, data, config)
    return response.data
  }

  async delete<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.instance.delete(url, config)
    return response.data
  }

  // File upload
  async uploadFile<T>(
    url: string, 
    file: File, 
    onUploadProgress?: (progressEvent: any) => void
  ): Promise<T> {
    const formData = new FormData()
    formData.append('file', file)

    const response = await this.instance.post(url, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress,
    })

    return response.data
  }

  // Get axios instance for custom requests
  getInstance(): AxiosInstance {
    return this.instance
  }
}

// Create and export default instance
export const apiClient = new ApiClient()
export default apiClient
