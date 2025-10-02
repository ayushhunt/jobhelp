'use client'

import Link from 'next/link'
import MainLayout from './layout/MainLayout'
import Button from './ui/Button'
import { Card, CardContent } from './ui/Card'
import {
  BriefcaseIcon,
  UserGroupIcon,
  ChartBarIcon,
  SparklesIcon,
  CheckCircleIcon,
  StarIcon
} from '@heroicons/react/24/outline'

const LandingPage = () => {
  const features = [
    {
      name: 'AI-Powered Matching',
      description: 'Smart algorithms connect the right candidates with the right opportunities.',
      icon: SparklesIcon,
    },
    {
      name: 'Comprehensive Analytics',
      description: 'Detailed insights and analytics for both recruiters and candidates.',
      icon: ChartBarIcon,
    },
    {
      name: 'Seamless Communication',
      description: 'Built-in messaging and interview scheduling tools.',
      icon: UserGroupIcon,
    },
    {
      name: 'Free Career Tools',
      description: 'Resume builder, salary estimator, and interview prep tools.',
      icon: BriefcaseIcon,
    },
  ]

  const testimonials = [
    {
      name: 'Sarah Chen',
      role: 'Software Engineer',
      company: 'TechCorp',
      content: 'JobHelp helped me land my dream job in just 2 weeks. The AI matching was incredibly accurate!',
      rating: 5,
    },
    {
      name: 'Michael Rodriguez',
      role: 'HR Director',
      company: 'InnovateCo',
      content: 'We reduced our hiring time by 60% using JobHelp. The candidate quality is outstanding.',
      rating: 5,
    },
    {
      name: 'Emily Johnson',
      role: 'Product Manager',
      company: 'StartupXYZ',
      content: 'The career tools are amazing. The resume builder helped me get 3x more interviews.',
      rating: 5,
    },
  ]

  const pricingPlans = [
    {
      name: 'Starter',
      price: '$49',
      period: '/month',
      description: 'Perfect for small teams',
      features: [
        '5 job postings',
        '100 candidate contacts',
        'Basic analytics',
        'Email support',
      ],
    },
    {
      name: 'Professional',
      price: '$149',
      period: '/month',
      description: 'Most popular for growing companies',
      features: [
        '25 job postings',
        '500 candidate contacts',
        'Advanced analytics',
        'Priority support',
        'Team collaboration',
        'Custom branding',
      ],
      popular: true,
    },
    {
      name: 'Enterprise',
      price: '$399',
      period: '/month',
      description: 'For large organizations',
      features: [
        'Unlimited job postings',
        'Unlimited candidate contacts',
        'Custom integrations',
        '24/7 dedicated support',
        'Advanced security',
        'Custom reporting',
      ],
    },
  ]

  return (
    <MainLayout>
      {/* Hero Section */}
      <section className="relative bg-white dark:bg-gray-900 overflow-hidden">
        <div className="max-w-7xl mx-auto">
          <div className="relative z-10 pb-8 bg-white dark:bg-gray-900 sm:pb-16 md:pb-20 lg:max-w-2xl lg:w-full lg:pb-28 xl:pb-32">
            <main className="mt-10 mx-auto max-w-7xl px-4 sm:mt-12 sm:px-6 md:mt-16 lg:mt-20 lg:px-8 xl:mt-28">
              <div className="sm:text-center lg:text-left">
                <h1 className="text-4xl tracking-tight font-extrabold text-gray-900 dark:text-white sm:text-5xl md:text-6xl">
                  <span className="block">Hire Smarter.</span>
                  <span className="block text-blue-600 dark:text-blue-400">Get Hired Faster.</span>
                </h1>
                <p className="mt-3 text-base text-gray-500 dark:text-gray-300 sm:mt-5 sm:text-lg sm:max-w-xl sm:mx-auto md:mt-5 md:text-xl lg:mx-0">
                  Revolutionary AI-powered platform that connects top talent with amazing opportunities. 
                  Experience the future of recruitment.
                </p>
                <div className="mt-5 sm:mt-8 sm:flex sm:justify-center lg:justify-start space-y-4 sm:space-y-0 sm:space-x-4">
                  <Link href="/auth/register?role=recruiter">
                    <Button size="lg" className="w-full sm:w-auto">
                      Post a Job
                    </Button>
                  </Link>
                  <Link href="/auth/register?role=candidate">
                    <Button variant="outline" size="lg" className="w-full sm:w-auto">
                      Find Jobs
                    </Button>
                  </Link>
                </div>
              </div>
            </main>
          </div>
        </div>
        <div className="lg:absolute lg:inset-y-0 lg:right-0 lg:w-1/2">
          <div className="h-56 w-full bg-gradient-to-r from-blue-400 to-purple-500 sm:h-72 md:h-96 lg:w-full lg:h-full flex items-center justify-center">
            <div className="text-white text-center">
              <ChartBarIcon className="h-32 w-32 mx-auto mb-4 opacity-80" />
              <p className="text-xl font-medium">AI-Powered Matching</p>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-12 bg-gray-50 dark:bg-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="lg:text-center">
            <h2 className="text-base text-blue-600 dark:text-blue-400 font-semibold tracking-wide uppercase">Features</h2>
            <p className="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 dark:text-white sm:text-4xl">
              Everything you need to succeed
            </p>
          </div>

          <div className="mt-10">
            <div className="space-y-10 md:space-y-0 md:grid md:grid-cols-2 md:gap-x-8 md:gap-y-10">
              {features.map((feature) => (
                <div key={feature.name} className="relative">
                  <div className="absolute flex items-center justify-center h-12 w-12 rounded-md bg-blue-500 text-white">
                    <feature.icon className="h-6 w-6" />
                  </div>
                  <p className="ml-16 text-lg leading-6 font-medium text-gray-900 dark:text-white">
                    {feature.name}
                  </p>
                  <p className="mt-2 ml-16 text-base text-gray-500 dark:text-gray-300">
                    {feature.description}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="py-12 bg-white dark:bg-gray-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h2 className="text-3xl font-extrabold text-gray-900 dark:text-white">
              Trusted by thousands
            </h2>
            <p className="mt-4 text-lg text-gray-500 dark:text-gray-300">
              See what our users are saying about JobHelp
            </p>
          </div>

          <div className="mt-12 grid grid-cols-1 gap-8 md:grid-cols-3">
            {testimonials.map((testimonial) => (
              <Card key={testimonial.name} className="text-center">
                <CardContent className="pt-6">
                  <div className="flex justify-center mb-4">
                    {[...Array(testimonial.rating)].map((_, i) => (
                      <StarIcon key={i} className="h-5 w-5 text-yellow-400 fill-current" />
                    ))}
                  </div>
                  <p className="text-gray-600 dark:text-gray-300 mb-4">
                    "{testimonial.content}"
                  </p>
                  <div>
                    <p className="font-semibold text-gray-900 dark:text-white">
                      {testimonial.name}
                    </p>
                    <p className="text-sm text-gray-500 dark:text-gray-400">
                      {testimonial.role} at {testimonial.company}
                    </p>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section className="py-12 bg-gray-50 dark:bg-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h2 className="text-3xl font-extrabold text-gray-900 dark:text-white">
              Simple, transparent pricing
            </h2>
            <p className="mt-4 text-lg text-gray-500 dark:text-gray-300">
              Choose the plan that's right for your business
            </p>
          </div>

          <div className="mt-12 grid grid-cols-1 gap-8 md:grid-cols-3">
            {pricingPlans.map((plan) => (
              <Card key={plan.name} className={`text-center relative ${plan.popular ? 'ring-2 ring-blue-500' : ''}`}>
                {plan.popular && (
                  <div className="absolute top-0 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
                    <span className="inline-flex px-4 py-1 rounded-full text-sm font-semibold bg-blue-500 text-white">
                      Most Popular
                    </span>
                  </div>
                )}
                <CardContent className="pt-6">
                  <h3 className="text-xl font-semibold text-gray-900 dark:text-white">
                    {plan.name}
                  </h3>
                  <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">
                    {plan.description}
                  </p>
                  <div className="mt-4">
                    <span className="text-4xl font-extrabold text-gray-900 dark:text-white">
                      {plan.price}
                    </span>
                    <span className="text-base font-medium text-gray-500 dark:text-gray-400">
                      {plan.period}
                    </span>
                  </div>
                  <ul className="mt-6 space-y-3">
                    {plan.features.map((feature) => (
                      <li key={feature} className="flex items-center justify-center">
                        <CheckCircleIcon className="h-5 w-5 text-green-500 mr-2" />
                        <span className="text-sm text-gray-700 dark:text-gray-300">
                          {feature}
                        </span>
                      </li>
                    ))}
                  </ul>
                  <div className="mt-8">
                    <Button className="w-full" variant={plan.popular ? 'primary' : 'outline'}>
                      Get Started
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-blue-600 dark:bg-blue-700">
        <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:py-16 lg:px-8 lg:flex lg:items-center lg:justify-between">
          <h2 className="text-3xl font-extrabold tracking-tight text-white sm:text-4xl">
            <span className="block">Ready to get started?</span>
            <span className="block text-blue-200">Join thousands of users today.</span>
          </h2>
          <div className="mt-8 flex lg:mt-0 lg:flex-shrink-0">
            <div className="inline-flex rounded-md shadow">
              <Link href="/auth/register">
                <Button size="lg" className="bg-white text-blue-600 hover:bg-gray-50">
                  Get started for free
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>
    </MainLayout>
  )
}

export default LandingPage


