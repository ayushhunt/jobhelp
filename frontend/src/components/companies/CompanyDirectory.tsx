'use client'

import MainLayout from '@/components/layout/MainLayout'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'
import Button from '@/components/ui/Button'
import { 
  BuildingOfficeIcon,
  MapPinIcon,
  UserGroupIcon,
  BriefcaseIcon
} from '@heroicons/react/24/outline'

const CompanyDirectory = () => {
  const companies = [
    {
      id: '1',
      name: 'TechCorp Inc.',
      logo: '🏢',
      industry: 'Technology',
      size: '1000-5000 employees',
      location: 'San Francisco, CA',
      openJobs: 25,
      description: 'Leading technology company building the future of digital innovation.',
    },
    {
      id: '2',
      name: 'StartupXYZ',
      logo: '🚀',
      industry: 'SaaS',
      size: '50-200 employees',
      location: 'New York, NY',
      openJobs: 12,
      description: 'Fast-growing startup revolutionizing business productivity.',
    },
    {
      id: '3',
      name: 'DesignStudio',
      logo: '🎨',
      industry: 'Design & Creative',
      size: '10-50 employees',
      location: 'Remote',
      openJobs: 8,
      description: 'Creative agency specializing in digital design and user experience.',
    },
  ]

  return (
    <MainLayout>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Company Directory
          </h1>
          <p className="mt-2 text-gray-600 dark:text-gray-400">
            Discover amazing companies and explore their opportunities
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {companies.map((company) => (
            <Card key={company.id} className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="flex items-center space-x-4">
                  <div className="text-4xl">{company.logo}</div>
                  <div>
                    <CardTitle className="text-lg">{company.name}</CardTitle>
                    <p className="text-sm text-gray-500">{company.industry}</p>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600 dark:text-gray-300 mb-4">
                  {company.description}
                </p>
                
                <div className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
                  <div className="flex items-center">
                    <UserGroupIcon className="h-4 w-4 mr-2" />
                    {company.size}
                  </div>
                  <div className="flex items-center">
                    <MapPinIcon className="h-4 w-4 mr-2" />
                    {company.location}
                  </div>
                  <div className="flex items-center">
                    <BriefcaseIcon className="h-4 w-4 mr-2" />
                    {company.openJobs} open positions
                  </div>
                </div>

                <div className="flex space-x-2 mt-6">
                  <Button variant="outline" size="sm" className="flex-1">
                    View Profile
                  </Button>
                  <Button size="sm" className="flex-1">
                    View Jobs
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        <div className="text-center mt-8">
          <Button variant="outline" size="lg">
            Load More Companies
          </Button>
        </div>
      </div>
    </MainLayout>
  )
}

export default CompanyDirectory


