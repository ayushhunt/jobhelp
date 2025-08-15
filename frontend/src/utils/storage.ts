// Local storage utility functions
export interface StoredInput {
  resumeText: string;
  jobDescriptionText: string;
  timestamp: number;
}

const STORAGE_KEYS = {
  SAVED_INPUTS: 'jobhelp_saved_inputs',
  USER_PREFERENCES: 'jobhelp_user_preferences',
  THEME: 'jobhelp_theme',
} as const;

export class StorageManager {
  // Saved inputs management
  static getSavedInputs(): StoredInput[] {
    try {
      const saved = localStorage.getItem(STORAGE_KEYS.SAVED_INPUTS);
      return saved ? JSON.parse(saved) : [];
    } catch (error) {
      console.error('Failed to parse saved inputs:', error);
      return [];
    }
  }

  static saveInput(input: StoredInput): void {
    try {
      const saved = this.getSavedInputs();
      const updated = [input, ...saved].slice(0, 5); // Keep last 5 entries
      localStorage.setItem(STORAGE_KEYS.SAVED_INPUTS, JSON.stringify(updated));
    } catch (error) {
      console.error('Failed to save input:', error);
    }
  }

  static clearSavedInputs(): void {
    try {
      localStorage.removeItem(STORAGE_KEYS.SAVED_INPUTS);
    } catch (error) {
      console.error('Failed to clear saved inputs:', error);
    }
  }

  // User preferences management
  static getUserPreferences() {
    try {
      const saved = localStorage.getItem(STORAGE_KEYS.USER_PREFERENCES);
      return saved ? JSON.parse(saved) : {};
    } catch (error) {
      console.error('Failed to parse user preferences:', error);
      return {};
    }
  }

  static saveUserPreferences(preferences: Record<string, any>): void {
    try {
      localStorage.setItem(STORAGE_KEYS.USER_PREFERENCES, JSON.stringify(preferences));
    } catch (error) {
      console.error('Failed to save user preferences:', error);
    }
  }

  // Theme management
  static getTheme(): 'light' | 'dark' | 'system' {
    try {
      return (localStorage.getItem(STORAGE_KEYS.THEME) as 'light' | 'dark' | 'system') || 'system';
    } catch (error) {
      console.error('Failed to get theme:', error);
      return 'system';
    }
  }

  static setTheme(theme: 'light' | 'dark' | 'system'): void {
    try {
      localStorage.setItem(STORAGE_KEYS.THEME, theme);
    } catch (error) {
      console.error('Failed to set theme:', error);
    }
  }

  // Generic storage operations
  static setItem(key: string, value: any): void {
    try {
      localStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
      console.error(`Failed to set item ${key}:`, error);
    }
  }

  static getItem<T>(key: string, defaultValue: T): T {
    try {
      const saved = localStorage.getItem(key);
      return saved ? JSON.parse(saved) : defaultValue;
    } catch (error) {
      console.error(`Failed to get item ${key}:`, error);
      return defaultValue;
    }
  }

  static removeItem(key: string): void {
    try {
      localStorage.removeItem(key);
    } catch (error) {
      console.error(`Failed to remove item ${key}:`, error);
    }
  }

  // Clear all app data
  static clearAll(): void {
    try {
      Object.values(STORAGE_KEYS).forEach(key => {
        localStorage.removeItem(key);
      });
    } catch (error) {
      console.error('Failed to clear all storage:', error);
    }
  }
}
