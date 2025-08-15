'use client'

import { useTheme } from './ThemeProvider'
import { Sun, Moon, Monitor } from 'lucide-react'

export default function ThemeToggle() {
  const { theme, setTheme } = useTheme()

  return (
    <div className="p-2">
      <div className="flex items-center space-x-1 p-1 bg-gray-100 dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800">
        <button
          onClick={() => setTheme('light')}
          className={`p-2.5 rounded-lg transition-all duration-200 ${
            theme === 'light' 
              ? 'bg-black text-white shadow-lg scale-105' 
              : 'text-gray-600 dark:text-gray-400 hover:text-black dark:hover:text-white hover:bg-gray-200 dark:hover:bg-gray-800'
          }`}
          title="Light theme"
        >
          <Sun className="w-4 h-4" />
        </button>
        <button
          onClick={() => setTheme('dark')}
          className={`p-2.5 rounded-lg transition-all duration-200 ${
            theme === 'dark' 
              ? 'bg-white text-black shadow-lg scale-105' 
              : 'text-gray-600 dark:text-gray-400 hover:text-black dark:hover:text-white hover:bg-gray-200 dark:hover:bg-gray-800'
          }`}
          title="Dark theme"
        >
          <Moon className="w-4 h-4" />
        </button>
        <button
          onClick={() => setTheme('system')}
          className={`p-2.5 rounded-lg transition-all duration-200 ${
            theme === 'system' 
              ? 'bg-gray-800 text-white shadow-lg scale-105' 
              : 'text-gray-600 dark:text-gray-400 hover:text-black dark:hover:text-white hover:bg-gray-200 dark:hover:bg-gray-800'
          }`}
          title="System theme"
        >
          <Monitor className="w-4 h-4" />
        </button>
      </div>
      <p className="text-xs text-gray-500 dark:text-gray-400 text-center mt-2">Theme</p>
    </div>
  )
}