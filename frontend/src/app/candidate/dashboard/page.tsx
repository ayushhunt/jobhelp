'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useSelector } from 'react-redux'
import { RootState } from '@/redux/store'
import { AuthGuard } from '@/components/auth/AuthGuard'
import CandidateDashboard from '@/components/candidate/CandidateDashboard'

export default function CandidateDashboardPage() {
  const { user, isAuthenticated } = useSelector((state: RootState) => state.auth)
  const router = useRouter()

  useEffect(() => {
    if (isAuthenticated && user?.role !== 'applicant') {
      router.push('/login')
    }
  }, [isAuthenticated, user, router])

  return (
    <AuthGuard requiredRole="applicant">
      <CandidateDashboard />
    </AuthGuard>
  )
}

