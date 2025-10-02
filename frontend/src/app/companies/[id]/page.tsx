import { notFound } from 'next/navigation'
import CompanyProfile from '@/components/companies/CompanyProfile'

interface CompanyPageProps {
  params: {
    id: string
  }
}

export async function generateMetadata({ params }: CompanyPageProps) {
  // In a real app, you'd fetch company data here
  return {
    title: `Company Profile - JobHelp`,
    description: `Learn more about this company and explore their job opportunities`
  }
}

export default function CompanyPage({ params }: CompanyPageProps) {
  const { id } = params

  if (!id) {
    notFound()
  }

  return <CompanyProfile companyId={id} />
}
