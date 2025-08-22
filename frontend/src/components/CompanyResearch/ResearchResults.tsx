import React from 'react';
import { CompanyResearchResponse } from '@/services/companyResearchApi';

interface ResearchResultsProps {
  results: CompanyResearchResponse;
}

const ResearchResults: React.FC<ResearchResultsProps> = ({ results }) => {
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
    </div>
  );
};

export default ResearchResults;
