'use client'

import React, { useState } from 'react';
import { CompanyResearchRequest } from '@/services/companyResearchApi';

interface CompanyResearchFormProps {
  onSubmit: (request: CompanyResearchRequest) => void;
  isLoading?: boolean;
}

const CompanyResearchForm: React.FC<CompanyResearchFormProps> = ({ onSubmit, isLoading = false }) => {
  const [formData, setFormData] = useState<Partial<CompanyResearchRequest>>({
    company_name: '',
    company_domain: '',
    research_depth: 'standard',
    include_employee_reviews: false,
    include_financial_data: false,
    user_id: 'default',
    is_premium: false,
  });

  const [errors, setErrors] = useState<Record<string, string>>({});

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!formData.company_name && !formData.company_domain) {
      newErrors.general = 'Please provide either a company name or domain';
    }

    if (formData.company_name && formData.company_name.length < 2) {
      newErrors.company_name = 'Company name must be at least 2 characters';
    }

    if (formData.company_domain && !isValidDomain(formData.company_domain)) {
      newErrors.company_domain = 'Please enter a valid domain (e.g., example.com)';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const isValidDomain = (domain: string): boolean => {
    const domainRegex = /^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;
    return domainRegex.test(domain);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (validateForm()) {
      onSubmit(formData as CompanyResearchRequest);
    }
  };

  const handleInputChange = (field: keyof CompanyResearchRequest, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    
    // Clear field-specific error when user starts typing
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: '' }));
    }
    
    // Clear general error when user provides input
    if (errors.general && (field === 'company_name' || field === 'company_domain')) {
      setErrors(prev => ({ ...prev, general: '' }));
    }
  };

  const researchDepthOptions = [
    { value: 'basic', label: 'Basic', description: 'Quick web search verification', cost: '$0.005' },
    { value: 'standard', label: 'Standard', description: 'WHOIS, web search, knowledge graph, location verification', cost: '$0.022' },
    { value: 'comprehensive', label: 'Comprehensive', description: 'All sources + AI analysis', cost: 'Varies' },
  ];

  return (
    <div className="w-full max-w-4xl mx-auto">
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Company Information Section */}
        <div className="bg-card border border-border rounded-lg p-6">
          <h3 className="text-lg font-semibold text-card-foreground mb-4">
            Company Information
          </h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label htmlFor="company_name" className="block text-sm font-medium text-card-foreground mb-2">
                Company Name
              </label>
              <input
                type="text"
                id="company_name"
                value={formData.company_name || ''}
                onChange={(e) => handleInputChange('company_name', e.target.value)}
                placeholder="e.g., Microsoft Corporation"
                className={`w-full px-3 py-2 border rounded-md bg-input text-input-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring ${
                  errors.company_name ? 'border-destructive' : 'border-border'
                }`}
              />
              {errors.company_name && (
                <p className="mt-1 text-sm text-destructive">{errors.company_name}</p>
              )}
            </div>

            <div>
              <label htmlFor="company_domain" className="block text-sm font-medium text-card-foreground mb-2">
                Company Domain (Optional)
              </label>
              <input
                type="text"
                id="company_domain"
                value={formData.company_domain || ''}
                onChange={(e) => handleInputChange('company_domain', e.target.value)}
                placeholder="e.g., microsoft.com"
                className={`w-full px-3 py-2 border rounded-md bg-input text-input-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring ${
                  errors.company_domain ? 'border-destructive' : 'border-border'
                }`}
              />
              {errors.company_domain && (
                <p className="mt-1 text-sm text-destructive">{errors.company_domain}</p>
              )}
            </div>
          </div>

          {errors.general && (
            <p className="mt-2 text-sm text-destructive">{errors.general}</p>
          )}
        </div>

        {/* Research Depth Section */}
        <div className="bg-card border border-border rounded-lg p-6">
          <h3 className="text-lg font-semibold text-card-foreground mb-4">
            Research Depth
          </h3>
          
          <div className="space-y-3">
            {researchDepthOptions.map((option) => (
              <label
                key={option.value}
                className={`flex items-start p-4 border rounded-lg cursor-pointer transition-colors ${
                  formData.research_depth === option.value
                    ? 'border-primary bg-primary/5'
                    : 'border-border hover:border-primary/50'
                }`}
              >
                <input
                  type="radio"
                  name="research_depth"
                  value={option.value}
                  checked={formData.research_depth === option.value}
                  onChange={(e) => handleInputChange('research_depth', e.target.value)}
                  className="mt-1 mr-3 text-primary focus:ring-primary"
                />
                <div className="flex-1">
                  <div className="flex items-center justify-between">
                    <span className="font-medium text-card-foreground">{option.label}</span>
                    <span className="text-sm text-muted-foreground bg-muted px-2 py-1 rounded">
                      {option.cost}
                    </span>
                  </div>
                  <p className="text-sm text-muted-foreground mt-1">{option.description}</p>
                </div>
              </label>
            ))}
          </div>
        </div>

        {/* Additional Options Section */}
        <div className="bg-card border border-border rounded-lg p-6">
          <h3 className="text-lg font-semibold text-card-foreground mb-4">
            Additional Options
          </h3>
          
          <div className="space-y-4">
            <label className="flex items-center">
              <input
                type="checkbox"
                checked={formData.include_employee_reviews || false}
                onChange={(e) => handleInputChange('include_employee_reviews', e.target.checked)}
                className="mr-3 text-primary focus:ring-primary rounded border-border"
              />
              <div>
                <span className="font-medium text-card-foreground">Include Employee Reviews Analysis</span>
                <p className="text-sm text-muted-foreground">
                  Analyze employee reviews and company culture insights
                </p>
              </div>
            </label>

            <label className="flex items-center">
              <input
                type="checkbox"
                checked={formData.include_financial_data || false}
                onChange={(e) => handleInputChange('include_financial_data', e.target.checked)}
                className="mr-3 text-primary focus:ring-primary rounded border-border"
              />
              <div>
                <span className="font-medium text-card-foreground">Include Financial Data Analysis</span>
                <p className="text-sm text-muted-foreground">
                  Analyze financial health, funding rounds, and revenue trends
                </p>
              </div>
            </label>

            <label className="flex items-center">
              <input
                type="checkbox"
                checked={formData.is_premium || false}
                onChange={(e) => handleInputChange('is_premium', e.target.checked)}
                className="mr-3 text-primary focus:ring-primary rounded border-border"
              />
              <div>
                <span className="font-medium text-card-foreground">Premium Access</span>
                <p className="text-sm text-muted-foreground">
                  Unlock advanced features and higher rate limits
                </p>
              </div>
            </label>
          </div>
        </div>

        {/* Submit Button */}
        <div className="flex justify-center">
          <button
            type="submit"
            disabled={isLoading}
            className={`px-8 py-3 rounded-lg font-medium text-primary-foreground transition-all duration-200 ${
              isLoading
                ? 'bg-muted text-muted-foreground cursor-not-allowed'
                : 'bg-primary hover:bg-primary/90 active:scale-95 shadow-lg hover:shadow-xl'
            }`}
          >
            {isLoading ? (
              <div className="flex items-center space-x-2">
                <div className="w-4 h-4 border-2 border-primary-foreground border-t-transparent rounded-full animate-spin"></div>
                <span>Researching...</span>
              </div>
            ) : (
              <span>Start Company Research</span>
            )}
          </button>
        </div>
      </form>
    </div>
  );
};

export default CompanyResearchForm;

