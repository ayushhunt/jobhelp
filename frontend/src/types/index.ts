// Re-export all types from individual modules
export * from './user';
export * from './job';
export * from './candidate';
export * from './recruiter';
export * from './tools';

// Common API response types
export interface ApiResponse<T> {
  success: boolean;
  data: T;
  message?: string;
  errors?: string[];
}

export interface PaginatedResponse<T> {
  data: T[];
  pagination: {
    page: number;
    pageSize: number;
    total: number;
    totalPages: number;
  };
}

export interface ApiError {
  message: string;
  code?: string;
  field?: string;
}

// Navigation types
export interface NavItem {
  label: string;
  href: string;
  icon?: string;
  children?: NavItem[];
  requiresAuth?: boolean;
  allowedRoles?: string[];
}

// Theme types
export type Theme = 'light' | 'dark' | 'system';

// Loading states
export interface LoadingState {
  isLoading: boolean;
  error: string | null;
}

// Form states
export interface FormState<T> extends LoadingState {
  data: T;
  isDirty: boolean;
  validationErrors: Record<string, string>;
}

// Search and filter types
export interface SearchParams {
  query?: string;
  page?: number;
  pageSize?: number;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
  filters?: Record<string, any>;
}

// Notification types
export interface Notification {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  title: string;
  message: string;
  timestamp: Date;
  read: boolean;
  actionUrl?: string;
}

// File upload types
export interface FileUploadProgress {
  file: File;
  progress: number;
  status: 'pending' | 'uploading' | 'completed' | 'error';
  error?: string;
  url?: string;
}

