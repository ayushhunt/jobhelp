'use client'

import { useState } from 'react'
import { FileText, BarChart2, Settings, Menu, X } from 'lucide-react'
import Link from 'next/link'
import ThemeToggle from './ThemeToggle'

interface LayoutProps {
  children: React.ReactNode
}

export default function Layout({ children }: LayoutProps) {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true)

  const menuItems = [
    { name: 'Resume Analytics', icon: <FileText className="w-4 h-4" />, path: '/' },
    { name: 'Coming Soon', icon: <BarChart2 className="w-4 h-4" />, path: '/coming-soon' },
    { name: 'Settings', icon: <Settings className="w-4 h-4" />, path: '/settings' },
  ]

  return (
    <div className="flex h-screen bg-background text-foreground">
      {/* Mobile overlay */}
      {isSidebarOpen && (
        <div 
          className="fixed inset-0 bg-black/50 z-10 lg:hidden"
          onClick={() => setIsSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <div 
        className={`fixed lg:static lg:translate-x-0 z-20 ${
          isSidebarOpen ? 'translate-x-0' : '-translate-x-full'
        } transition-all duration-300 ease-in-out flex flex-col w-64 sm:w-72 lg:w-64 h-screen px-4 py-6 bg-card border-r border-border shadow-lg lg:shadow-none`}
      >
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
              <FileText className="w-5 h-5 text-primary-foreground" />
            </div>
            <span className="text-xl font-bold text-foreground">JobHelp</span>
          </div>
          <button 
            onClick={() => setIsSidebarOpen(false)}
            className="lg:hidden p-2 rounded-lg hover:bg-secondary transition-colors"
          >
            <X className="w-5 h-5 text-muted-foreground" />
          </button>
        </div>

        <div className="flex flex-col justify-between flex-1">
          <nav className="space-y-2">
            {menuItems.map((item) => (
              <Link
                key={item.name}
                href={item.path}
                className="flex items-center px-3 py-3 text-sm font-medium text-muted-foreground transition-all duration-200 rounded-xl hover:bg-secondary hover:text-foreground group"
              >
                <div className="p-2 rounded-lg bg-secondary group-hover:bg-accent transition-colors">
                  {item.icon}
                </div>
                <span className="ml-3">{item.name}</span>
              </Link>
            ))}
          </nav>

          <div className="border-t border-border pt-4">
            <ThemeToggle />
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 h-screen overflow-y-auto bg-muted">
        <header className="sticky top-0 z-10 flex items-center h-16 px-4 sm:px-6 lg:px-8 bg-card/80 backdrop-blur-md border-b border-border">
          <button 
            onClick={() => setIsSidebarOpen(true)}
            className="lg:hidden p-2 rounded-lg hover:bg-secondary transition-colors"
          >
            <Menu className="w-6 h-6 text-muted-foreground" />
          </button>
          <div className="ml-4 sm:ml-6">
            <h1 className="text-lg font-semibold text-foreground">Resume Analysis</h1>
            <p className="text-sm text-muted-foreground">AI-powered job matching insights</p>
          </div>
        </header>
        <main className="p-4 sm:p-6 lg:p-8 max-w-7xl mx-auto">{children}</main>
      </div>
    </div>
  )
}