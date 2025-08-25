import React, { useState } from 'react';
import { PortfolioData, PortfolioSummary } from '@/services/companyResearchApi';

interface PortfolioResearchProps {
  portfolioData: PortfolioData;
}

const PortfolioResearch: React.FC<PortfolioResearchProps> = ({ portfolioData }) => {
  const [activeTab, setActiveTab] = useState<'overview' | 'pages' | 'technologies' | 'summaries'>('overview');

  const formatDate = (dateString: string) => {
    if (!dateString) return 'N/A';
    try {
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      });
    } catch (error) {
      return 'Invalid Date';
    }
  };

  const formatContentLength = (length: number) => {
    if (length < 1000) return `${length} characters`;
    if (length < 1000000) return `${(length / 1000).toFixed(1)}K characters`;
    return `${(length / 1000000).toFixed(1)}M characters`;
  };

  const renderSummary = (summary: PortfolioSummary | undefined, type: 'LLM' | 'NLP') => {
    // Safety check for undefined summary
    if (!summary) {
      return (
        <div className="p-4 bg-red-50 border border-red-200 rounded">
          <p className="text-red-700 text-sm">No {type} summary available</p>
        </div>
      );
    }
    
    return (
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h5 className="font-medium text-card-foreground">{type} Summary</h5>
          <div className="flex items-center gap-2 text-xs">
            <span className="px-2 py-1 bg-muted text-muted-foreground rounded">
              {summary.method || 'unknown'}
            </span>
            {summary.model_used && (
              <span className="px-2 py-1 bg-primary/10 text-primary rounded">
                {summary.model_used}
              </span>
            )}
          </div>
        </div>
        
        {summary.error ? (
          <div className="p-3 bg-red-50 border border-red-200 rounded text-red-700 text-sm">
            Error: {summary.error}
          </div>
        ) : summary.summary ? (
          <div className="p-4 bg-muted/30 rounded">
            <p className="text-muted-foreground leading-relaxed">{summary.summary}</p>
          </div>
        ) : (
          <div className="p-4 bg-yellow-50 border border-yellow-200 rounded">
            <p className="text-yellow-700 text-sm">No summary content available</p>
          </div>
        )}

        {summary.key_phrases && summary.key_phrases.length > 0 && (
          <div>
            <h6 className="font-medium text-sm text-card-foreground mb-2">Key Phrases</h6>
            <div className="flex flex-wrap gap-2">
              {summary.key_phrases.map((phrase, index) => (
                <span key={index} className="px-2 py-1 bg-primary/10 text-primary text-xs rounded">
                  {phrase}
                </span>
              ))}
            </div>
          </div>
        )}

        {summary.entities && Object.keys(summary.entities).length > 0 && (
          <div>
            <h6 className="font-medium text-sm text-card-foreground mb-2">Named Entities</h6>
            <div className="space-y-2">
              {Object.entries(summary.entities).map(([entityType, entities]) => (
                <div key={entityType}>
                  <span className="text-xs text-muted-foreground capitalize">{entityType}:</span>
                  <div className="flex flex-wrap gap-1 mt-1">
                    {entities.map((entity, index) => (
                      <span key={index} className="px-2 py-1 bg-muted text-muted-foreground text-xs rounded">
                        {entity}
                      </span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {summary.techniques_used && summary.techniques_used.length > 0 && (
          <div>
            <h6 className="font-medium text-sm text-card-foreground mb-2">Techniques Used</h6>
            <div className="flex flex-wrap gap-1">
              {summary.techniques_used.map((technique, index) => (
                <span key={index} className="px-2 py-1 bg-blue-50 text-blue-700 text-xs rounded">
                  {technique}
                </span>
              ))}
            </div>
          </div>
        )}

        <div className="text-xs text-muted-foreground">
          Generated: {summary.generated_at ? formatDate(summary.generated_at) : 'Unknown'}
        </div>
      </div>
    );
  };

  return (
    <div className="bg-card border border-border rounded-lg">
      {/* Header */}
      <div className="p-6 border-b border-border">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-xl font-semibold text-card-foreground flex items-center gap-2">
            🎯 Portfolio Research
          </h3>
          <div className="text-right">
            <div className="text-sm text-muted-foreground">Domain</div>
            <div className="font-medium">{portfolioData.domain}</div>
          </div>
        </div>
        
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
          <div>
            <span className="text-muted-foreground">Pages Scraped:</span>
            <p className="font-medium">{portfolioData.total_pages_scraped || 0}</p>
          </div>
          <div>
            <span className="text-muted-foreground">Content Length:</span>
            <p className="font-medium">{formatContentLength(portfolioData.total_content_length || 0)}</p>
          </div>
          <div>
            <span className="text-muted-foreground">Technologies:</span>
            <p className="font-medium">{portfolioData.technologies?.length || 0}</p>
          </div>
          <div>
            <span className="text-muted-foreground">Scraped:</span>
            <p className="font-medium">{formatDate(portfolioData.scraped_at)}</p>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="border-b border-border">
        <div className="flex space-x-1 px-6">
          {[
            { id: 'overview', label: 'Overview', icon: '📊' },
            { id: 'pages', label: 'Pages', icon: '📄' },
            { id: 'technologies', label: 'Technologies', icon: '⚙️' },
            { id: 'summaries', label: 'Summaries', icon: '📝' }
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`px-4 py-2 text-sm font-medium rounded-t-lg transition-colors ${
                activeTab === tab.id
                  ? 'bg-primary text-primary-foreground'
                  : 'text-muted-foreground hover:text-card-foreground hover:bg-muted'
              }`}
            >
              <span className="mr-2">{tab.icon}</span>
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      {/* Tab Content */}
      <div className="p-6">
        {activeTab === 'overview' && (
          <div className="space-y-6">
            {/* Portfolio URLs */}
            {portfolioData.portfolio_urls && portfolioData.portfolio_urls.length > 0 && (
              <div>
                <h4 className="font-medium text-card-foreground mb-3">Portfolio URLs Discovered</h4>
                <div className="space-y-2">
                  {portfolioData.portfolio_urls.map((url, index) => (
                    <div key={index} className="flex items-center gap-2">
                      <span className="text-green-500">✓</span>
                      <a 
                        href={url} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="text-primary hover:underline text-sm"
                      >
                        {url}
                      </a>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Industries */}
            {portfolioData.industries && portfolioData.industries.length > 0 && (
              <div>
                <h4 className="font-medium text-card-foreground mb-3">Industries Identified</h4>
                <div className="flex flex-wrap gap-2">
                  {portfolioData.industries.map((industry, index) => (
                    <span key={index} className="px-3 py-1 bg-blue-50 text-blue-700 text-sm rounded-full">
                      {industry}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Projects */}
            {portfolioData.projects && portfolioData.projects.length > 0 && (
              <div>
                <h4 className="font-medium text-card-foreground mb-3">Projects Mentioned</h4>
                <div className="space-y-2">
                  {portfolioData.projects.map((project, index) => (
                    <div key={index} className="p-3 bg-muted/30 rounded">
                      <span className="text-sm text-muted-foreground">{project}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {activeTab === 'pages' && (
          <div className="space-y-4">
            <h4 className="font-medium text-card-foreground mb-4">Scraped Pages ({portfolioData.pages?.length || 0})</h4>
            {portfolioData.pages && portfolioData.pages.map((page, index) => (
              <div key={index} className="border border-border rounded-lg p-4">
                <div className="flex items-start justify-between mb-3">
                  <h5 className="font-medium text-card-foreground">
                    <a 
                      href={page.url} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="text-primary hover:underline"
                    >
                      {page.title || 'Untitled'}
                    </a>
                  </h5>
                  <span className="text-xs text-muted-foreground">
                    {formatDate(page.scraped_at)}
                  </span>
                </div>
                <p className="text-sm text-muted-foreground mb-3">
                  {page.url}
                </p>
                <div className="text-sm text-muted-foreground">
                  <span className="font-medium">Content:</span> {formatContentLength(page.text.length)}
                </div>
                <details className="mt-3">
                  <summary className="cursor-pointer text-sm text-primary hover:underline">
                    View content preview
                  </summary>
                  <div className="mt-2 p-3 bg-muted/30 rounded text-sm text-muted-foreground max-h-32 overflow-y-auto">
                    {page.text.substring(0, 500)}
                    {page.text.length > 500 && '...'}
                  </div>
                </details>
              </div>
            ))}
          </div>
        )}

        {activeTab === 'technologies' && (
          <div>
            <h4 className="font-medium text-card-foreground mb-4">Technologies Identified ({portfolioData.technologies?.length || 0})</h4>
            {portfolioData.technologies && portfolioData.technologies.length > 0 ? (
              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
                {portfolioData.technologies.map((tech, index) => (
                  <div key={index} className="p-3 bg-muted/30 rounded text-center">
                    <span className="text-sm font-medium text-card-foreground">{tech}</span>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center text-muted-foreground py-8">
                <p>No technologies identified in the portfolio content</p>
              </div>
            )}
          </div>
        )}

        {activeTab === 'summaries' && (portfolioData.llm_summary || portfolioData.nlp_summary) && (
          <div className="space-y-8">
            <h4 className="font-medium text-card-foreground mb-6">Portfolio Analysis Summaries</h4>
            
            {/* Development Mode: Data Debug */}
            {process.env.NODE_ENV === 'development' && (
              <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
                <h5 className="font-medium text-yellow-800 mb-2">🔧 Development Debug: Summary Data</h5>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                  <div>
                    <span className="text-yellow-700 font-medium">LLM Summary:</span>
                    <pre className="text-xs text-yellow-600 mt-1 bg-yellow-100 p-2 rounded overflow-auto max-h-2">
                      {JSON.stringify(portfolioData.llm_summary, null, 2)}
                    </pre>
                  </div>
                  <div>
                    <span className="text-yellow-700 font-medium">NLP Summary:</span>
                    <pre className="text-xs text-yellow-600 mt-1 bg-yellow-100 p-2 rounded overflow-auto max-h-2">
                      {JSON.stringify(portfolioData.nlp_summary, null, 2)}
                    </pre>
                  </div>
                </div>
              </div>
            )}
            
            {/* LLM Summary */}
            <div className="border border-border rounded-lg p-6">
              {renderSummary(portfolioData.llm_summary, 'LLM')}
            </div>

            {/* NLP Summary */}
            <div className="border border-border rounded-lg p-6">
              {renderSummary(portfolioData.nlp_summary, 'NLP')}
            </div>
          </div>
        )}
        
        {/* No Summaries Available */}
        {activeTab === 'summaries' && !portfolioData.llm_summary && !portfolioData.nlp_summary && (
          <div className="text-center text-muted-foreground py-12">
            <div className="text-4xl mb-4">📝</div>
            <h4 className="text-lg font-medium mb-2">No Summaries Available</h4>
            <p className="text-sm">Portfolio analysis summaries have not been generated yet.</p>
            {process.env.NODE_ENV === 'development' && (
              <div className="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded text-xs text-yellow-700">
                <strong>Debug Info:</strong> Check if portfolio research completed successfully and summary generation worked.
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default PortfolioResearch;
