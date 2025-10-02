'use client'

import Header from './Header'
import Footer from './Footer'

interface MainLayoutProps {
  children: React.ReactNode
  showFooter?: boolean
}

const MainLayout = ({ children, showFooter = true }: MainLayoutProps) => {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <Header />
      <main className="flex-1">
        {children}
      </main>
      {showFooter && <Footer />}
    </div>
  )
}

export default MainLayout


