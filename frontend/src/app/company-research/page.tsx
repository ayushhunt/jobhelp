'use client'

import React, { useState, useEffect } from 'react';
import CompanyResearchForm from '@/components/CompanyResearch/CompanyResearchForm';
import ResearchProgress from '@/components/CompanyResearch/ResearchProgress';
import ResearchResults from '@/components/CompanyResearch/ResearchResults';
import { CompanyResearchAPIService, CompanyResearchRequest, CompanyResearchResponse, ResearchProgress as ResearchProgressType } from '@/services/companyResearchApi';
import ThemeToggle from '@/components/ThemeToggle';

const CompanyResearchPage: React.FC = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [currentRequestId, setCurrentRequestId] = useState<string | null>(null);
  const [progress, setProgress] = useState<ResearchProgressType | null>(null);
  const [results, setResults] = useState<CompanyResearchResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [progressInterval, setProgressInterval] = useState<NodeJS.Timeout | null>(null);

  // Cleanup interval on unmount
  useEffect(() => {
    return () => {
      if (progressInterval) {
        clearInterval(progressInterval);
      }
    };
  }, [progressInterval]);

  const handleResearchSubmit = async (request: CompanyResearchRequest) => {
    try {
      setIsLoading(true);
      setError(null);
      setResults(null);
      setProgress(null);

      // Start research
      const response = await CompanyResearchAPIService.researchCompany(request);
      setResults(response);
      setIsLoading(false);
    } catch (err) {
      console.error('Research failed:', err);
      setError(err instanceof Error ? err.message : 'Research failed. Please try again.');
      setIsLoading(false);
    }
  };

  const handleAsyncResearch = async (request: CompanyResearchRequest) => {
    try {
      setIsLoading(true);
      setError(null);
      setResults(null);
      setProgress(null);

      // Start async research
      const response = await CompanyResearchAPIService.researchCompanyAsync(request);
      setCurrentRequestId(response.request_id);
      
      // Start progress polling
      const interval = setInterval(async () => {
        try {
          const progressData = await CompanyResearchAPIService.getResearchProgress(response.request_id);
          setProgress(progressData);
          
          if (progressData.status === 'completed' || progressData.status === 'failed') {
            clearInterval(interval);
            setProgressInterval(null);
            
            if (progressData.status === 'completed') {
              // Fetch final results
              try {
                const finalResults = await CompanyResearchAPIService.researchCompany(request);
                setResults(finalResults);
              } catch (err) {
                console.error('Failed to fetch final results:', err);
              }
            }
            setIsLoading(false);
          }
        } catch (err) {
          console.error('Failed to fetch progress:', err);
          clearInterval(interval);
          setProgressInterval(null);
          setError('Failed to track progress. Please try again.');
          setIsLoading(false);
        }
      }, 2000);
      
      setProgressInterval(interval);
    } catch (err) {
      console.error('Async research failed:', err);
      setError(err instanceof Error ? err.message : 'Failed to start research. Please try again.');
      setIsLoading(false);
    }
  };

  const handleCancelResearch = async () => {
    if (!currentRequestId) return;
    
    try {
      await CompanyResearchAPIService.cancelResearch(currentRequestId);
      
      if (progressInterval) {
        clearInterval(progressInterval);
        setProgressInterval(null);
      }
      
      setCurrentRequestId(null);
      setProgress(null);
      setIsLoading(false);
    } catch (err) {
      console.error('Failed to cancel research:', err);
      setError('Failed to cancel research. Please try again.');
    }
  };

  const handleQuickCheck = async (companyName?: string, companyDomain?: string) => {
    if (!companyName && !companyDomain) return;
    
    try {
      setIsLoading(true);
      setError(null);
      
      const quickResult = await CompanyResearchAPIService.quickCompanyCheck(companyName, companyDomain);
      
      // Create a basic research request for quick check
      const request: CompanyResearchRequest = {
        company_name: companyName,
        company_domain: companyDomain,
        research_depth: 'basic',
        user_id: 'quick_check',
        is_premium: false,
      };
      
      // Start basic research
      const response = await CompanyResearchAPIService.researchCompany(request);
      setResults(response);
      setIsLoading(false);
    } catch (err) {
      console.error('Quick check failed:', err);
      setError(err instanceof Error ? err.message : 'Quick check failed. Please try again.');
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-card-foreground">
                Company Research
              </h1>
              <p className="text-muted-foreground">
                Verify company authenticity and gather comprehensive information
              </p>
            </div>
            <ThemeToggle />
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {/* Error Display */}
        {error && (
          <div className="mb-6 bg-destructive/10 border border-destructive/20 rounded-lg p-4">
            <div className="flex items-center space-x-2">
              <span className="text-destructive">❌</span>
              <p className="text-destructive font-medium">{error}</p>
            </div>
            <button
              onClick={() => setError(null)}
              className="mt-2 text-sm text-destructive hover:text-destructive/80 underline"
            >
              Dismiss
            </button>
          </div>
        )}

        {/* Research Form */}
        {!results && !progress && (
          <div className="mb-8">
            <div className="text-center mb-8">
              <h2 className="text-3xl font-bold text-card-foreground mb-4">
                Research Company Authenticity
              </h2>
              <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
                Get comprehensive insights about any company using multiple data sources including 
                WHOIS verification, location verification, web search, and AI analysis.
              </p>
            </div>
            
            <CompanyResearchForm 
              onSubmit={handleResearchSubmit}
              isLoading={isLoading}
            />
          </div>
        )}

        {/* Progress Display */}
        {progress && !results && (
          <div className="mb-8">
            <ResearchProgress 
              progress={progress}
              onCancel={handleCancelResearch}
            />
          </div>
        )}

        {/* Results Display */}
        {results && (
          <div className="mb-8">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-card-foreground">
                Research Results
              </h2>
              <button
                onClick={() => {
                  setResults(null);
                  setProgress(null);
                  setCurrentRequestId(null);
                  setError(null);
                }}
                className="px-4 py-2 text-sm text-muted-foreground hover:text-card-foreground border border-border rounded-md hover:border-primary/50 transition-colors"
              >
                New Research
              </button>
            </div>
            
            <ResearchResults results={results} />
          </div>
        )}

        {/* Quick Actions */}
        {!results && !progress && (
          <div className="bg-card border border-border rounded-lg p-6">
            <h3 className="text-lg font-semibold text-card-foreground mb-4">
              Quick Actions
            </h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-muted/50 rounded-lg p-4">
                <h4 className="font-medium text-card-foreground mb-2">Quick Company Check</h4>
                <p className="text-sm text-muted-foreground mb-3">
                  Perform a basic verification check for quick company validation
                </p>
                <div className="space-y-2">
                  <input
                    type="text"
                    placeholder="Company name"
                    className="w-full px-3 py-2 border rounded-md bg-input text-input-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring border-border"
                    onKeyPress={(e) => {
                      if (e.key === 'Enter') {
                        const target = e.target as HTMLInputElement;
                        handleQuickCheck(target.value);
                      }
                    }}
                  />
                  <button
                    onClick={() => {
                      const input = document.querySelector('input[placeholder="Company name"]') as HTMLInputElement;
                      if (input) handleQuickCheck(input.value);
                    }}
                    className="w-full px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 transition-colors"
                  >
                    Quick Check
                  </button>
                </div>
              </div>

              <div className="bg-muted/50 rounded-lg p-4">
                <h4 className="font-medium text-card-foreground mb-2">Service Health</h4>
                <p className="text-sm text-muted-foreground mb-3">
                  Check the status of all research services
                </p>
                <button
                  onClick={async () => {
                    try {
                      const health = await CompanyResearchAPIService.getServiceHealth();
                      console.log('Service Health:', health);
                      // You could display this in a modal or toast
                    } catch (err) {
                      console.error('Failed to get service health:', err);
                    }
                  }}
                  className="w-full px-4 py-2 bg-secondary text-secondary-foreground rounded-md hover:bg-secondary/80 transition-colors"
                >
                  Check Services
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Features Overview */}
        {!results && !progress && (
          <div className="mt-12">
            <h3 className="text-2xl font-bold text-card-foreground text-center mb-8">
              Research Capabilities
            </h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <div className="bg-card border border-border rounded-lg p-6 text-center">
                <div className="text-4xl mb-4">🌐</div>
                <h4 className="text-lg font-semibold text-card-foreground mb-2">WHOIS Verification</h4>
                <p className="text-sm text-muted-foreground">
                  Verify domain registration, ownership, and expiration dates
                </p>
              </div>

              <div className="bg-card border border-border rounded-lg p-6 text-center">
                <div className="text-4xl mb-4">📍</div>
                <h4 className="text-lg font-semibold text-card-foreground mb-2">Location Verification</h4>
                <p className="text-sm text-muted-foreground">
                  Cross-reference location data from Google Places and OpenStreetMap
                </p>
              </div>

              <div className="bg-card border border-border rounded-lg p-6 text-center">
                <div className="text-4xl mb-4">🔍</div>
                <h4 className="text-lg font-semibold text-card-foreground mb-2">Web Search</h4>
                <p className="text-sm text-muted-foreground">
                  Gather recent news, social media presence, and online mentions
                </p>
              </div>

              <div className="bg-card border border-border rounded-lg p-6 text-center">
                <div className="text-4xl mb-4">🧠</div>
                <h4 className="text-lg font-semibold text-card-foreground mb-2">Knowledge Graph</h4>
                <p className="text-sm text-muted-foreground">
                  Access structured company data and industry information
                </p>
              </div>

              <div className="bg-card border border-border rounded-lg p-6 text-center">
                <div className="text-4xl mb-4">🤖</div>
                <h4 className="text-lg font-semibold text-card-foreground mb-2">AI Analysis</h4>
                <p className="text-sm text-muted-foreground">
                  Get AI-powered insights and risk assessment
                </p>
              </div>

              <div className="bg-card border border-border rounded-lg p-6 text-center">
                <div className="text-4xl mb-4">📊</div>
                <h4 className="text-lg font-semibold text-card-foreground mb-2">Authenticity Scoring</h4>
                <p className="text-sm text-muted-foreground">
                  Comprehensive scoring system for company verification
                </p>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

export default CompanyResearchPage;
