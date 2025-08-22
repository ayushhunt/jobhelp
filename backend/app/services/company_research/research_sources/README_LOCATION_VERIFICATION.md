# Location Verification Service

## Overview

The Location Verification Service is a comprehensive solution for verifying company locations by cross-referencing data from multiple authoritative sources. It provides authenticity scoring based on data consistency and reliability metrics.

## Features

- **Multi-Source Data Fetching**: Retrieves location data from Google Places API and Nominatim OSM API
- **Intelligent Comparison**: Compares data sources using advanced algorithms
- **Authenticity Scoring**: Provides confidence scores based on data consistency
- **Risk Assessment**: Identifies potential discrepancies and trust indicators
- **Cost Optimization**: Uses free OSM data as fallback when Google Places API is unavailable

## Data Sources

### 1. Google Places API
- **Provider**: Google Maps Platform
- **Cost**: $0.017 per Text Search request
- **Data Quality**: High (commercial-grade)
- **Coverage**: Global
- **Rate Limits**: 100,000 requests per day (free tier)

**Required Setup**:
```bash
# Add to your .env file
GOOGLE_PLACES_API_KEY=your_api_key_here
```

### 2. Nominatim OSM API
- **Provider**: OpenStreetMap Foundation
- **Cost**: Free
- **Data Quality**: Variable (community-maintained)
- **Coverage**: Global
- **Rate Limits**: 1 request per second (recommended)

## Architecture

```
CompanyResearchRequest
         ↓
LocationVerificationService
         ↓
    ┌─────────────┬─────────────┐
    ↓             ↓             ↓
Google Places  Nominatim    Comparison
    API         OSM API      Engine
    ↓             ↓             ↓
LocationData  LocationData  LocationComparison
    ↓             ↓             ↓
    └─────────────┼─────────────┘
                  ↓
         LocationVerificationData
                  ↓
         Authenticity Scoring
```

## Data Models

### LocationData
```python
class LocationData(BaseModel):
    source: str                    # "google_places" or "nominatim_osm"
    address: Optional[str]         # Full address
    city: Optional[str]            # City name
    state: Optional[str]           # State/province
    country: Optional[str]         # Country
    postal_code: Optional[str]     # Postal/ZIP code
    latitude: Optional[float]      # GPS latitude
    longitude: Optional[float]     # GPS longitude
    formatted_address: Optional[str] # Formatted address string
    place_id: Optional[str]        # Source-specific identifier
    confidence_score: Optional[float] # Source confidence (0-1)
    last_updated: datetime         # Last update timestamp
```

### LocationComparison
```python
class LocationComparison(BaseModel):
    address_similarity_score: float      # Address similarity (0-1)
    coordinate_distance_km: Optional[float] # Distance between coordinates
    city_match: bool                     # City field match
    state_match: bool                    # State field match
    country_match: bool                  # Country field match
    postal_code_match: bool              # Postal code match
    overall_location_confidence: float   # Overall confidence score (0-1)
```

### LocationVerificationData
```python
class LocationVerificationData(BaseModel):
    company_name: str                    # Company name
    search_query: str                    # Search query used
    google_places_data: Optional[LocationData]
    nominatim_osm_data: Optional[LocationData]
    comparison: Optional[LocationComparison]
    authenticity_score: float            # Overall authenticity (0-1)
    verification_status: str             # "verified", "suspicious", "unknown"
    risk_factors: List[str]              # Identified risk factors
    trust_indicators: List[str]          # Trust indicators
    last_verified: datetime              # Verification timestamp
```

## Scoring Algorithm

### Authenticity Score Calculation

The authenticity score is calculated using a weighted algorithm:

1. **Base Score (40%)**: Address similarity between sources
2. **Coordinate Distance (30%)**: Geographic proximity bonus/penalty
3. **Field Matches (20%)**: Individual field match bonuses
4. **Source Quality (10%)**: Confidence scores from individual sources

### Scoring Breakdown

| Score Range | Status | Description |
|-------------|--------|-------------|
| 0.8 - 1.0  | Verified | High confidence, data sources agree |
| 0.6 - 0.79 | Suspicious | Moderate confidence, some discrepancies |
| 0.0 - 0.59 | Unknown | Low confidence, significant discrepancies |

### Coordinate Distance Scoring

| Distance | Score Impact | Description |
|----------|-------------|-------------|
| < 1 km   | +0.3        | Excellent match |
| 1-5 km   | +0.2        | Good match |
| 5-10 km  | +0.1        | Acceptable match |
| > 10 km  | -0.2        | Poor match |

## Usage Examples

### Basic Usage
```python
from app.services.company_research.research_sources.location_verification_service import LocationVerificationService

# Initialize service
service = LocationVerificationService()

# Perform location verification
result = await service.research("Google", "google.com")

# Access results
print(f"Authenticity Score: {result['authenticity_score']}")
print(f"Verification Status: {result['verification_status']}")
print(f"Risk Factors: {result['risk_factors']}")
```

### Integration with Company Research
```python
from app.services.company_research.company_research_orchestrator import CompanyResearchOrchestrator

# The service is automatically included in standard and comprehensive research
orchestrator = CompanyResearchOrchestrator()

# Standard research includes location verification
request = CompanyResearchRequest(
    company_name="Microsoft",
    research_depth="standard"  # Includes location verification
)

response = await orchestrator.research_company(request)
```

## Configuration

### Environment Variables
```bash
# Required for Google Places API
GOOGLE_PLACES_API_KEY=your_api_key_here

# Optional: Customize service behavior
LOCATION_VERIFICATION_TIMEOUT=30
LOCATION_VERIFICATION_MAX_RETRIES=3
```

### Service Configuration
```python
class LocationVerificationService(BaseResearchSource):
    def __init__(self):
        super().__init__(ResearchSource.LOCATION_VERIFICATION)
        self.google_places_api_key = getattr(settings, 'GOOGLE_PLACES_API_KEY', None)
        self.google_places_base_url = "https://maps.googleapis.com/maps/api/place"
        self.nominatim_base_url = "https://nominatim.openstreetmap.org"
```

## Error Handling

The service implements robust error handling:

1. **API Failures**: Graceful fallback to available sources
2. **Rate Limiting**: Automatic retry with exponential backoff
3. **Data Validation**: Comprehensive input validation and sanitization
4. **Partial Results**: Returns partial data when possible

### Error Response Format
```python
{
    "company_name": "Company Name",
    "error": "Error description",
    "authenticity_score": 0.0,
    "verification_status": "unknown"
}
```

## Performance Considerations

### Optimization Strategies
1. **Parallel Execution**: Fetches data from both sources simultaneously
2. **Caching**: Implements result caching for repeated queries
3. **Timeout Management**: Configurable timeouts prevent hanging requests
4. **Connection Pooling**: Efficient HTTP connection management

### Rate Limiting
- **Google Places API**: 100,000 requests/day (free tier)
- **Nominatim OSM**: 1 request/second (recommended)
- **Service Level**: Automatic rate limiting and queuing

## Monitoring and Logging

### Log Levels
- **INFO**: Successful operations and data quality metrics
- **WARNING**: API failures and data discrepancies
- **ERROR**: Critical failures and service unavailability

### Metrics
- Response times for each data source
- Success/failure rates
- Data quality scores
- Cost tracking for paid APIs

## Testing

### Unit Tests
```bash
# Run location verification tests
python -m pytest tests/test_location_verification.py -v
```

### Integration Tests
```bash
# Test with real APIs (requires API keys)
python -m pytest tests/test_location_verification_integration.py -v
```

### Mock Testing
```bash
# Test without external dependencies
python -m pytest tests/test_location_verification_mock.py -v
```

## Troubleshooting

### Common Issues

1. **Google Places API Key Invalid**
   - Verify API key in .env file
   - Check API key permissions and quotas
   - Ensure Places API is enabled in Google Cloud Console

2. **Nominatim OSM Rate Limiting**
   - Implement request throttling
   - Use multiple Nominatim instances
   - Consider caching results

3. **Data Discrepancies**
   - Review search query optimization
   - Check address component parsing
   - Verify coordinate system consistency

### Debug Mode
```python
import logging
logging.getLogger('app.services.company_research.research_sources.location_verification_service').setLevel(logging.DEBUG)
```

## Future Enhancements

### Planned Features
1. **Additional Data Sources**: Bing Maps, Here Maps, MapBox
2. **Advanced Geocoding**: Reverse geocoding and address validation
3. **Machine Learning**: Improved similarity scoring algorithms
4. **Real-time Updates**: Webhook-based location change notifications
5. **Batch Processing**: Bulk location verification for multiple companies

### API Extensions
1. **Location History**: Track location changes over time
2. **Geographic Clustering**: Identify company office networks
3. **Travel Time Analysis**: Calculate commute times between locations
4. **Demographic Data**: Population and business density information

## Contributing

### Development Setup
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables
4. Run tests: `python -m pytest`

### Code Standards
- Follow PEP 8 style guidelines
- Include comprehensive docstrings
- Write unit tests for new features
- Update documentation for API changes

## License

This service is part of the JobHelp AI platform and follows the same licensing terms.

## Support

For technical support or feature requests:
- Create an issue in the project repository
- Contact the development team
- Check the project documentation

---

*Last updated: August 2024*
*Version: 1.0.0*
