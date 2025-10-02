'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useSelector } from 'react-redux'
import { RootState } from '@/redux/store'
import RecruiterDashboard from '@/components/recruiter/RecruiterDashboard'
import { AuthGuard } from '@/components/auth/AuthGuard'

export default function RecruiterDashboardPage() {
  const { user, isAuthenticated } = useSelector((state: RootState) => state.auth)
  const router = useRouter()

  useEffect(() => {
    if (isAuthenticated && user?.role !== 'recruiter') {
      router.push('/login')
    }
  }, [isAuthenticated, user, router])

  return (
    <AuthGuard requiredRole="recruiter">
      <RecruiterDashboard />
    </AuthGuard>
  )
}

