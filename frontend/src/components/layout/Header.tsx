'use client'

import { useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useSelector, useDispatch } from 'react-redux'
import { RootState } from '@/redux/store'
import { logoutUser } from '@/redux/slices/authSlice'
// Removed theme toggle - using auto-detection
import Button from '@/components/ui/Button'
import {
  UserIcon,
  BriefcaseIcon,
  BuildingOfficeIcon,
  WrenchScrewdriverIcon,
  Bars3Icon,
  XMarkIcon
} from '@heroicons/react/24/outline'

const Header = () => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)
  const { user, isAuthenticated } = useSelector((state: RootState) => state.auth)
  const dispatch = useDispatch()
  const router = useRouter()

  const handleLogout = () => {
    dispatch(logoutUser() as any)
    router.push('/')
  }

  const navigation = [
    { name: 'Jobs', href: '/jobs', icon: BriefcaseIcon },
    { name: 'Companies', href: '/companies', icon: BuildingOfficeIcon },
    { name: 'Tools', href: '/tools', icon: WrenchScrewdriverIcon },
  ]

  const userNavigation = user?.role === 'applicant' ? [
    { name: 'Dashboard', href: '/candidate/dashboard' },
    { name: 'Profile', href: '/candidate/profile' },
    { name: 'Applications', href: '/candidate/applications' },
    { name: 'Jobs', href: '/candidate/jobs' },
    { name: 'Interviews', href: '/candidate/interviews' },
    { name: 'Settings', href: '/candidate/settings' },
  ] : user?.role === 'recruiter' ? [
    { name: 'Dashboard', href: '/recruiter/dashboard' },
    { name: 'Jobs', href: '/recruiter/jobs' },
    { name: 'Candidates', href: '/recruiter/candidates' },
    { name: 'Interviews', href: '/recruiter/interviews' },
    { name: 'Settings', href: '/recruiter/settings' },
  ] : []

  return (
    <header className="bg-white dark:bg-gray-900 shadow-sm border-b border-gray-200 dark:border-gray-700">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex">
            <Link href="/" className="flex items-center">
              <span className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                JobHelp
              </span>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            {navigation.map((item) => (
              <Link
                key={item.name}
                href={item.href}
                className="flex items-center text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white px-3 py-2 text-sm font-medium"
              >
                <item.icon className="h-4 w-4 mr-1" />
                {item.name}
              </Link>
            ))}
          </nav>

          {/* Desktop Auth */}
          <div className="hidden md:flex items-center space-x-4">
            {isAuthenticated ? (
              <div className="flex items-center space-x-4">
                <div className="relative group">
                  <button className="flex items-center text-sm rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                    <UserIcon className="h-8 w-8 rounded-full bg-gray-200 dark:bg-gray-700 p-1" />
                    <span className="ml-2 text-gray-700 dark:text-gray-300">
                      {user?.firstName} {user?.lastName}
                    </span>
                  </button>
                  
                  {/* Dropdown */}
                  <div className="absolute right-0 mt-2 w-48 bg-white dark:bg-gray-800 rounded-md shadow-lg py-1 z-10 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200">
                    {userNavigation.map((item) => (
                      <Link
                        key={item.name}
                        href={item.href}
                        className="block px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
                      >
                        {item.name}
                      </Link>
                    ))}
                    <button
                      onClick={handleLogout}
                      className="block w-full text-left px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
                    >
                      Sign out
                    </button>
                  </div>
                </div>
              </div>
            ) : (
              <div className="flex items-center space-x-4">
                <Link href="/login">
                  <Button variant="ghost">Sign in</Button>
                </Link>
                <Link href="/register">
                  <Button>Get started</Button>
                </Link>
              </div>
            )}
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden flex items-center">
            <button
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              className="ml-2 inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500"
            >
              {isMobileMenuOpen ? (
                <XMarkIcon className="block h-6 w-6" />
              ) : (
                <Bars3Icon className="block h-6 w-6" />
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile menu */}
      {isMobileMenuOpen && (
        <div className="md:hidden">
          <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3 border-t border-gray-200 dark:border-gray-700">
            {navigation.map((item) => (
              <Link
                key={item.name}
                href={item.href}
                className="flex items-center text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white block px-3 py-2 text-base font-medium"
                onClick={() => setIsMobileMenuOpen(false)}
              >
                <item.icon className="h-5 w-5 mr-2" />
                {item.name}
              </Link>
            ))}

            {isAuthenticated ? (
              <div className="pt-4 pb-3 border-t border-gray-200 dark:border-gray-700">
                <div className="px-3 py-2">
                  <div className="text-base font-medium text-gray-800 dark:text-white">
                    {user?.firstName} {user?.lastName}
                  </div>
                  <div className="text-sm font-medium text-gray-500 dark:text-gray-400">
                    {user?.email}
                  </div>
                </div>
                <div className="mt-3 space-y-1">
                  {userNavigation.map((item) => (
                    <Link
                      key={item.name}
                      href={item.href}
                      className="block px-3 py-2 text-base font-medium text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white"
                      onClick={() => setIsMobileMenuOpen(false)}
                    >
                      {item.name}
                    </Link>
                  ))}
                  <button
                    onClick={handleLogout}
                    className="block w-full text-left px-3 py-2 text-base font-medium text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white"
                  >
                    Sign out
                  </button>
                </div>
              </div>
            ) : (
              <div className="pt-4 pb-3 border-t border-gray-200 dark:border-gray-700 space-y-2">
                <Link href="/login" className="block px-3 py-2">
                  <Button variant="ghost" className="w-full">Sign in</Button>
                </Link>
                <Link href="/register" className="block px-3 py-2">
                  <Button className="w-full">Get started</Button>
                </Link>
              </div>
            )}
          </div>
        </div>
      )}
    </header>
  )
}

export default Header
