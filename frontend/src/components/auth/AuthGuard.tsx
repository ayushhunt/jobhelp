'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useSelector, useDispatch } from 'react-redux'
import { RootState } from '@/redux/store'
import { getCurrentUser } from '@/redux/slices/authSlice'
import { getDashboardPath } from '@/services/auth'
import Loader from '@/components/Loader'

type UserRole = 'applicant' | 'recruiter' | 'admin'

interface AuthGuardProps {
  children: React.ReactNode
  requiredRole?: UserRole
  redirectTo?: string
}

export const AuthGuard = ({ 
  children, 
  requiredRole, 
  redirectTo = '/login' 
}: AuthGuardProps) => {
  const { user, isAuthenticated, isLoading } = useSelector((state: RootState) => state.auth)
  const dispatch = useDispatch()
  const router = useRouter()

  useEffect(() => {
    // Try to get current user if we don't have one
    if (!user && !isLoading) {
      dispatch(getCurrentUser() as any)
    }
  }, [user, isLoading, dispatch])

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push(redirectTo)
    }
  }, [isAuthenticated, isLoading, router, redirectTo])

  useEffect(() => {
    if (requiredRole && user && user.role !== requiredRole) {
      // Redirect to appropriate dashboard based on role
      const dashboardPath = getDashboardPath(user.role)
      router.push(dashboardPath)
    }
  }, [user, requiredRole, router])

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loader />
      </div>
    )
  }

  if (!isAuthenticated || !user) {
    return null // Will redirect in useEffect
  }

  if (requiredRole && user.role !== requiredRole) {
    return null // Will redirect in useEffect
  }

  return <>{children}</>
}
