'use client'

export default function Loader() {
  return (
    <div className="flex space-x-2 justify-center items-center h-full">
      <div className="animate-bounce w-2.5 h-2.5 bg-gray-600 dark:bg-gray-300 rounded-full" style={{ animationDelay: '0s' }}></div>
      <div className="animate-bounce w-2.5 h-2.5 bg-gray-600 dark:bg-gray-300 rounded-full" style={{ animationDelay: '0.2s' }}></div>
      <div className="animate-bounce w-2.5 h-2.5 bg-gray-600 dark:bg-gray-300 rounded-full" style={{ animationDelay: '0.4s' }}></div>
    </div>
  )
}
