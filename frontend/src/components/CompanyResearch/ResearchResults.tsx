import React from 'react';
import { CompanyResearchResponse } from '@/services/companyResearchApi';
import PortfolioResearch from './PortfolioResearch';

interface ResearchResultsProps {
  results: CompanyResearchResponse;
}

const ResearchResults: React.FC<ResearchResultsProps> = ({ results }) => {
  // Helper function to safely get portfolio data
  const getPortfolioData = () => {
    let portfolioData = results.portfolio_data;
    
    if (!portfolioData && results.task_results) {
      const portfolioTask = results.task_results.find(
        (task: any) => task.source === 'portfolio_research' && task.status === 'completed'
      );
      
      // Development mode logging
      if (process.env.NODE_ENV === 'development') {
        console.log('🔍 Portfolio Research Task Found:', portfolioTask);
        if (portfolioTask) {
          console.log('📊 Portfolio Task Data:', portfolioTask.data);
        }
      }
      
      if (portfolioTask && portfolioTask.data) {
        // Check if data has portfolio_data structure (backend returns summaries at top level)
        if (portfolioTask.data.portfolio_data) {
          // Backend returns: { portfolio_data: {...}, llm_summary: {...}, nlp_summary: {...} }
          portfolioData = {
            ...portfolioTask.data.portfolio_data,
            llm_summary: portfolioTask.data.llm_summary || null,
            nlp_summary: portfolioTask.data.nlp_summary || null
          };
        } else if (portfolioTask.data.domain || portfolioTask.data.pages || portfolioTask.data.llm_summary || portfolioTask.data.nlp_summary) {
          // If no portfolio_data, check if the data itself contains portfolio information
          // This handles cases where the backend returns the data directly
          portfolioData = portfolioTask.data;
        } else if (portfolioTask.data.summary || portfolioTask.data.key_phrases || portfolioTask.data.entities) {
          // Handle case where the data contains summary information directly
          // This might happen if the backend structure is different
          
          // Check if this looks like NLP summary data
          const isNLPSummary = portfolioTask.data.method === 'nlp' || 
                              (portfolioTask.data.key_phrases && portfolioTask.data.entities);
          
          // Check if this looks like LLM summary data  
          const isLLMSummary = portfolioTask.data.method === 'llm' || 
                              (portfolioTask.data.summary && !portfolioTask.data.key_phrases);
          
          portfolioData = {
            domain: portfolioTask.data.domain || 'unknown',
            pages: portfolioTask.data.pages || [],
            raw_text: portfolioTask.data.raw_text || '',
            portfolio_urls: portfolioTask.data.portfolio_urls || [],
            technologies: portfolioTask.data.technologies || [],
            industries: portfolioTask.data.industries || [],
            projects: portfolioTask.data.projects || [],
            scraped_at: portfolioTask.data.scraped_at || new Date().toISOString(),
            total_pages_scraped: portfolioTask.data.total_pages_scraped || 0,
            total_content_length: portfolioTask.data.total_content_length || 0,
            llm_summary: isLLMSummary ? portfolioTask.data : null,
            nlp_summary: isNLPSummary ? portfolioTask.data : null
          };
        }
        
        if (process.env.NODE_ENV === 'development') {
          console.log('✅ Portfolio Data Extracted:', portfolioData);
          if (portfolioData) {
            console.log('🔍 Portfolio Data Structure:', {
              hasDomain: !!portfolioData.domain,
              hasPages: !!portfolioData.pages,
              hasLLMSummary: !!portfolioData.llm_summary,
              hasNLPSummary: !!portfolioData.nlp_summary,
              llmSummaryType: typeof portfolioData.llm_summary,
              nlpSummaryType: typeof portfolioData.nlp_summary
            });
            
            // Additional debugging for summary data
            if (portfolioData.llm_summary) {
              console.log('🤖 LLM Summary Data:', portfolioData.llm_summary);
            }
            if (portfolioData.nlp_summary) {
              console.log('📊 NLP Summary Data:', portfolioData.nlp_summary);
            }
          }
        }
      }
    }
    
    return portfolioData;
  };

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

  const getAuthenticityColor = (score: number) => {
    if (score >= 80) return 'text-green-600 bg-green-100';
    if (score >= 60) return 'text-yellow-600 bg-yellow-100';
    return 'text-red-600 bg-red-100';
  };

  const getAuthenticityLabel = (score: number) => {
    if (score >= 80) return 'High Authenticity';
    if (score >= 60) return 'Moderate Authenticity';
    return 'Low Authenticity';
  };

  // Early return if results is not properly structured
  if (!results) {
    return (
      <div className="bg-card border border-border rounded-lg p-6">
        <div className="text-center text-muted-foreground">
          <p>No research data available</p>
          <p className="text-sm mt-2">Please try running the research again.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Development Mode Indicator */}
      {process.env.NODE_ENV === 'development' && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
          <div className="flex items-center gap-2">
            <span className="text-blue-600">🔧</span>
            <span className="text-sm font-medium text-blue-800">Development Mode Active</span>
            <span className="text-xs text-blue-600">Enhanced debugging and data display enabled</span>
          </div>
        </div>
      )}

      {/* Company Overview */}
      <div className="bg-card border border-border rounded-lg p-6">
        <div className="flex items-start justify-between mb-4">
          <div>
            <h3 className="text-xl font-semibold text-card-foreground mb-2">
              {results.company_name || 'Unknown Company'}
            </h3>
            {results.company_domain && (
              <p className="text-muted-foreground">
                Domain: {results.company_domain}
              </p>
            )}
          </div>
          <div className="text-right">
            <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getAuthenticityColor(results.authenticity_score || 0)}`}>
              {getAuthenticityLabel(results.authenticity_score || 0)}
            </div>
            <div className="text-2xl font-bold text-card-foreground mt-1">
              {(results.authenticity_score || 0)}/100
            </div>
          </div>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
          <div>
            <span className="text-muted-foreground">Research Depth:</span>
            <p className="font-medium capitalize">{results.research_depth || 'Unknown'}</p>
          </div>
          <div>
            <span className="text-muted-foreground">Processing Time:</span>
            <p className="font-medium">{(results.total_processing_time || 0)}s</p>
          </div>
          <div>
            <span className="text-muted-foreground">Total Cost:</span>
            <p className="font-medium">${(results.total_cost || 0).toFixed(4)}</p>
          </div>
        </div>
      </div>

      {/* WHOIS Data */}
      {results.whois_data && (
        <div className="bg-card border border-border rounded-lg p-6">
          <h4 className="text-lg font-semibold text-card-foreground mb-4 flex items-center">
            🌐 Domain Information (WHOIS)
          </h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <span className="text-muted-foreground text-sm">Domain:</span>
              <p className="font-medium">{results.whois_data.domain || 'N/A'}</p>
            </div>
            {results.whois_data.registrar && (
              <div>
                <span className="text-muted-foreground text-sm">Registrar:</span>
                <p className="font-medium">{results.whois_data.registrar}</p>
              </div>
            )}
            {results.whois_data.creation_date && (
              <div>
                <span className="text-muted-foreground text-sm">Created:</span>
                <p className="font-medium">{formatDate(results.whois_data.creation_date)}</p>
              </div>
            )}
            {results.whois_data.expiration_date && (
              <div>
                <span className="text-muted-foreground text-sm">Expires:</span>
                <p className="font-medium">{formatDate(results.whois_data.expiration_date)}</p>
              </div>
            )}
            {results.whois_data.registrant_organization && (
              <div>
                <span className="text-muted-foreground text-sm">Organization:</span>
                <p className="font-medium">{results.whois_data.registrant_organization}</p>
              </div>
            )}
            {results.whois_data.registrant_country && (
              <div>
                <span className="text-muted-foreground text-sm">Country:</span>
                <p className="font-medium">{results.whois_data.registrant_country}</p>
              </div>
            )}
          </div>
          {results.whois_data.status && results.whois_data.status.length > 0 && (
            <div className="mt-4">
              <span className="text-muted-foreground text-sm">Status:</span>
              <div className="flex flex-wrap gap-2 mt-1">
                {results.whois_data.status.map((status, index) => (
                  <span key={index} className="px-2 py-1 bg-muted text-muted-foreground text-xs rounded">
                    {status}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Location Verification */}
      {results.location_verification_data && (
        <div className="bg-card border border-border rounded-lg p-6">
          <h4 className="text-lg font-semibold text-card-foreground mb-4 flex items-center">
            📍 Location Verification
          </h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {results.location_verification_data.google_places_data && (
              <div>
                <h5 className="font-medium text-card-foreground mb-2">Google Places Data</h5>
                <div className="space-y-2 text-sm">
                  {results.location_verification_data.google_places_data.formatted_address && (
                    <p><span className="text-muted-foreground">Address:</span> {results.location_verification_data.google_places_data.formatted_address}</p>
                  )}
                  {results.location_verification_data.google_places_data.city && (
                    <p><span className="text-muted-foreground">City:</span> {results.location_verification_data.google_places_data.city}</p>
                  )}
                  {results.location_verification_data.google_places_data.country && (
                    <p><span className="text-muted-foreground">Country:</span> {results.location_verification_data.google_places_data.country}</p>
                  )}
                </div>
              </div>
            )}
            
            {results.location_verification_data.nominatim_osm_data && (
              <div>
                <h5 className="font-medium text-card-foreground mb-2">OpenStreetMap Data</h5>
                <div className="space-y-2 text-sm">
                  {results.location_verification_data.nominatim_osm_data.formatted_address && (
                    <p><span className="text-muted-foreground">Address:</span> {results.location_verification_data.nominatim_osm_data.formatted_address}</p>
                  )}
                  {results.location_verification_data.nominatim_osm_data.city && (
                    <p><span className="text-muted-foreground">City:</span> {results.location_verification_data.nominatim_osm_data.city}</p>
                  )}
                  {results.location_verification_data.nominatim_osm_data.country && (
                    <p><span className="text-muted-foreground">Country:</span> {results.location_verification_data.nominatim_osm_data.country}</p>
                  )}
                </div>
              </div>
            )}
          </div>
          
          {results.location_verification_data.comparison && (
            <div className="mt-4 p-4 bg-muted/50 rounded-lg">
              <h5 className="font-medium text-card-foreground mb-2">Location Comparison</h5>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                <div>
                  <span className="text-muted-foreground">Similarity Score:</span>
                  <p className="font-medium">{(results.location_verification_data.comparison.address_similarity_score || 0)}%</p>
                </div>
                <div>
                  <span className="text-muted-foreground">Overall Confidence:</span>
                  <p className="font-medium">{(results.location_verification_data.comparison.overall_location_confidence || 0)}%</p>
                </div>
                <div>
                  <span className="text-muted-foreground">City Match:</span>
                  <p className="font-medium">{results.location_verification_data.comparison.city_match ? '✅' : '❌'}</p>
                </div>
                <div>
                  <span className="text-muted-foreground">Country Match:</span>
                  <p className="font-medium">{results.location_verification_data.comparison.country_match ? '✅' : '❌'}</p>
                </div>
              </div>
            </div>
          )}
          
          {results.location_verification_data.risk_factors && results.location_verification_data.risk_factors.length > 0 && (
            <div className="mt-4">
              <span className="text-muted-foreground text-sm">Risk Factors:</span>
              <div className="flex flex-wrap gap-2 mt-1">
                {results.location_verification_data.risk_factors.map((factor, index) => (
                  <span key={index} className="px-2 py-1 bg-red-100 text-red-700 text-xs rounded">
                    {factor}
                  </span>
                ))}
              </div>
            </div>
          )}
          
          {results.location_verification_data.trust_indicators && results.location_verification_data.trust_indicators.length > 0 && (
            <div className="mt-4">
              <span className="text-muted-foreground text-sm">Trust Indicators:</span>
              <div className="flex flex-wrap gap-2 mt-1">
                {results.location_verification_data.trust_indicators.map((indicator, index) => (
                  <span key={index} className="px-2 py-1 bg-green-100 text-green-700 text-xs rounded">
                    {indicator}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Knowledge Graph Data */}
      {results.knowledge_graph_data && (
        <div className="bg-card border border-border rounded-lg p-6">
          <h4 className="text-lg font-semibold text-card-foreground mb-4 flex items-center">
            🧠 Knowledge Graph Data
          </h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {results.knowledge_graph_data.description && (
              <div className="md:col-span-2">
                <span className="text-muted-foreground text-sm">Description:</span>
                <p className="font-medium">{results.knowledge_graph_data.description}</p>
              </div>
            )}
            {results.knowledge_graph_data.industry && (
              <div>
                <span className="text-muted-foreground text-sm">Industry:</span>
                <p className="font-medium">{results.knowledge_graph_data.industry}</p>
              </div>
            )}
            {results.knowledge_graph_data.founded_date && (
              <div>
                <span className="text-muted-foreground text-sm">Founded:</span>
                <p className="font-medium">{results.knowledge_graph_data.founded_date}</p>
              </div>
            )}
            {results.knowledge_graph_data.headquarters && (
              <div>
                <span className="text-muted-foreground text-sm">Headquarters:</span>
                <p className="font-medium">{results.knowledge_graph_data.headquarters}</p>
              </div>
            )}
            {results.knowledge_graph_data.ceo && (
              <div>
                <span className="text-muted-foreground text-sm">CEO:</span>
                <p className="font-medium">{results.knowledge_graph_data.ceo}</p>
              </div>
            )}
            {results.knowledge_graph_data.employees && (
              <div>
                <span className="text-muted-foreground text-sm">Employees:</span>
                <p className="font-medium">{results.knowledge_graph_data.employees}</p>
              </div>
            )}
            {results.knowledge_graph_data.website && (
              <div>
                <span className="text-muted-foreground text-sm">Website:</span>
                <p className="font-medium">
                  <a href={results.knowledge_graph_data.website} target="_blank" rel="noopener noreferrer" className="text-primary hover:underline">
                    {results.knowledge_graph_data.website}
                  </a>
                </p>
              </div>
            )}
          </div>
          
          {results.knowledge_graph_data.subsidiaries && results.knowledge_graph_data.subsidiaries.length > 0 && (
            <div className="mt-4">
              <span className="text-muted-foreground text-sm">Subsidiaries:</span>
              <div className="flex flex-wrap gap-2 mt-1">
                {results.knowledge_graph_data.subsidiaries.map((subsidiary, index) => (
                  <span key={index} className="px-2 py-1 bg-muted text-muted-foreground text-xs rounded">
                    {subsidiary}
                  </span>
                ))}
              </div>
            </div>
          )}
          
          {results.knowledge_graph_data.competitors && results.knowledge_graph_data.competitors.length > 0 && (
            <div className="mt-4">
              <span className="text-muted-foreground text-sm">Competitors:</span>
              <div className="flex flex-wrap gap-2 mt-1">
                {results.knowledge_graph_data.competitors.map((competitor, index) => (
                  <span key={index} className="px-2 py-1 bg-muted text-muted-foreground text-xs rounded">
                    {competitor}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Portfolio Research Summary */}
      {(() => {
        const portfolioData = getPortfolioData();
        
        if (portfolioData) {
          return (
            <div className="space-y-4">
              {/* Portfolio Research Component */}
              <PortfolioResearch portfolioData={portfolioData} />
              
              {/* Quick Portfolio Insights */}
              <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                <h4 className="text-lg font-semibold text-green-800 mb-3 flex items-center gap-2">
                  🎯 Quick Portfolio Insights
                </h4>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                  <div>
                    <span className="text-green-700 font-medium">Pages Analyzed:</span>
                    <p className="text-green-800">{portfolioData.total_pages_scraped || 0}</p>
                  </div>
                  <div>
                    <span className="text-green-700 font-medium">Technologies Found:</span>
                    <p className="text-green-800">{portfolioData.technologies?.length || 0}</p>
                  </div>
                  <div>
                    <span className="text-green-700 font-medium">Content Length:</span>
                    <p className="text-green-800">
                      {portfolioData.total_content_length ? portfolioData.total_content_length.toLocaleString() : '0'} chars
                    </p>
                  </div>
                </div>
                
                {/* LLM Summary Preview */}
                {portfolioData.llm_summary && !portfolioData.llm_summary.error && portfolioData.llm_summary.summary && (
                  <div className="mt-4">
                    <h5 className="font-medium text-green-800 mb-2">🤖 AI Summary Preview</h5>
                    <div className="p-3 bg-green-100 rounded text-sm text-green-800">
                      <p className="line-clamp-3">
                        {portfolioData.llm_summary.summary.substring(0, 300)}
                        {portfolioData.llm_summary.summary.length > 300 && '...'}
                      </p>
                      <div className="mt-2 text-xs text-green-600">
                        Generated using {portfolioData.llm_summary.provider || portfolioData.llm_summary.model_used || 'AI model'}
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          );
        }
        
        return null;
      })()}

      {/* Web Search Results */}
      {results.web_search_results && results.web_search_results.length > 0 && (
        <div className="bg-card border border-border rounded-lg p-6">
          <h4 className="text-lg font-semibold text-card-foreground mb-4 flex items-center">
            🔍 Web Search Results ({results.web_search_results.length} results)
          </h4>
          <div className="space-y-4">
            {results.web_search_results.map((result, index) => (
              <div key={index} className="border-l-4 border-primary pl-4">
                <h5 className="font-medium text-card-foreground mb-1">
                  <a href={result.url} target="_blank" rel="noopener noreferrer" className="text-primary hover:underline">
                    {result.title || 'Untitled'}
                  </a>
                </h5>
                <p className="text-sm text-muted-foreground mb-2">{result.snippet || 'No description available'}</p>
                <div className="flex items-center gap-4 text-xs text-muted-foreground">
                  <span>{result.source || 'Unknown source'}</span>
                  {result.published_date && <span>{formatDate(result.published_date)}</span>}
                  {result.relevance_score && <span>Relevance: {result.relevance_score}%</span>}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* AI Analysis Summary */}
      {results.executive_summary && (
        <div className="bg-card border border-border rounded-lg p-6">
          <h4 className="text-lg font-semibold text-card-foreground mb-4 flex items-center">
            🤖 AI Analysis Summary
          </h4>
          <div className="space-y-4">
            <div>
              <h5 className="font-medium text-card-foreground mb-2">Executive Summary</h5>
              <p className="text-muted-foreground">{results.executive_summary}</p>
            </div>
            
            {results.key_insights && results.key_insights.length > 0 && (
              <div>
                <h5 className="font-medium text-card-foreground mb-2">Key Insights</h5>
                <ul className="list-disc list-inside space-y-1 text-muted-foreground">
                  {results.key_insights.map((insight, index) => (
                    <li key={index}>{insight}</li>
                  ))}
                </ul>
              </div>
            )}
            
            {results.risk_assessment && (
              <div>
                <h5 className="font-medium text-card-foreground mb-2">Risk Assessment</h5>
                <p className="text-muted-foreground">{results.risk_assessment}</p>
              </div>
            )}
            
            {results.recommendations && results.recommendations.length > 0 && (
              <div>
                <h5 className="font-medium text-card-foreground mb-2">Recommendations</h5>
                <ul className="list-disc list-inside space-y-1 text-muted-foreground">
                  {results.recommendations.map((recommendation, index) => (
                    <li key={index}>{recommendation}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Research Metadata */}
      <div className="bg-muted/50 border border-border rounded-lg p-4">
        <div className="text-sm text-muted-foreground">
          <p>Research completed on {formatDate(results.timestamp)}</p>
          <p>Request ID: {results.request_id || 'Unknown'}</p>
          <p>Status: {results.research_status || 'Unknown'}</p>
          {results.sources_used && results.sources_used.length > 0 && (
            <p>Sources used: {results.sources_used.join(', ')}</p>
          )}
          {results.failed_sources && results.failed_sources.length > 0 && (
            <p>Failed sources: {results.failed_sources.join(', ')}</p>
          )}
        </div>
      </div>

      {/* Development Mode: Task Results Debug */}
      {process.env.NODE_ENV === 'development' && results.task_results && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <h4 className="text-lg font-semibold text-yellow-800 mb-3">🔧 Development Mode: Task Results Debug</h4>
          <div className="space-y-3">
            {results.task_results.map((task: any, index: number) => (
              <div key={index} className="border border-yellow-200 rounded p-3 bg-white">
                <div className="flex items-center justify-between mb-2">
                  <span className="font-medium text-yellow-800">{task.source}</span>
                  <span className={`px-2 py-1 text-xs rounded ${
                    task.status === 'completed' ? 'bg-green-100 text-green-800' :
                    task.status === 'failed' ? 'bg-red-100 text-red-800' :
                    'bg-yellow-100 text-yellow-800'
                  }`}>
                    {task.status}
                  </span>
                </div>
                <div className="text-xs text-yellow-700">
                  <p>Processing Time: {task.processing_time?.toFixed(3)}s</p>
                  <p>Cost Estimate: ${task.cost_estimate || 0}</p>
                  {task.error_message && (
                    <p className="text-red-600">Error: {task.error_message}</p>
                  )}
                </div>
                {task.source === 'portfolio_research' && task.data && (
                  <details className="mt-2">
                    <summary className="cursor-pointer text-sm text-yellow-700 hover:text-yellow-800">
                      Portfolio Data Preview
                    </summary>
                    <div className="mt-2 p-2 bg-yellow-100 rounded text-xs">
                      <pre className="whitespace-pre-wrap overflow-auto max-h-32">
                        {JSON.stringify(task.data, null, 2)}
                      </pre>
                    </div>
                  </details>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default ResearchResults;
