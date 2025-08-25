# Portfolio Research Service

## Overview

The Portfolio Research Service is a comprehensive component that automatically researches company portfolios by scraping their websites and creating detailed summaries using both LLM and NLP approaches. This service provides insights into what companies do, their sectors, projects, products, and technologies.

## Features

### 🔍 **Web Scraping**
- **Intelligent URL Discovery**: Automatically finds portfolio-related pages using keyword analysis
- **Content Extraction**: Uses both Trafilatura (primary) and BeautifulSoup (fallback) for robust content extraction
- **Rate Limiting**: Configurable delays between requests to be respectful to target websites
- **Content Validation**: Filters out low-quality or irrelevant content

### 🤖 **LLM-Based Summarization**
- **Structured Analysis**: Generates comprehensive summaries covering business model, sectors, projects, and technologies
- **Cost Optimization**: Configurable token limits and temperature settings
- **Fallback Handling**: Gracefully handles LLM API failures

### 📊 **NLP-Based Summarization**
- **Keyword Extraction**: Uses KeyBERT for identifying key phrases and concepts
- **Text Summarization**: Implements TextRank and LSA algorithms via Sumy library
- **Entity Recognition**: Extracts named entities using spaCy
- **Technology Detection**: Pattern-based identification of technologies and tools

### ⚙️ **Configuration & Optimization**
- **Multiple Presets**: Fast, thorough, and cost-optimized configurations
- **Customizable Settings**: Adjustable timeouts, page limits, and content thresholds
- **Performance Tuning**: Configurable NLP parameters for different use cases

## Architecture

```
PortfolioResearchService
├── Web Scraping Layer
│   ├── URL Discovery
│   ├── Content Extraction
│   └── Data Cleaning
├── Analysis Layer
│   ├── LLM Orchestrator
│   ├── NLP Pipeline
│   └── Pattern Matching
└── Configuration Layer
    ├── Preset Configs
    ├── Custom Settings
    └── Performance Tuning
```

## Usage

### Basic Usage

```python
from app.services.company_research.research_sources.portfolio_research_service import PortfolioResearchService

# Initialize with default configuration
service = PortfolioResearchService()

# Perform research
result = await service.research("Company Name", "company.com")
```

### Advanced Configuration

```python
from app.services.company_research.research_sources.portfolio_config import CONFIG_PRESETS

# Use preset configurations
fast_service = PortfolioResearchService(config=CONFIG_PRESETS["fast"])
thorough_service = PortfolioResearchService(config=CONFIG_PRESETS["thorough"])

# Custom configuration
custom_config = PortfolioResearchConfig(
    max_pages=20,
    max_content_length=100000,
    summary_sentences=10
)
custom_service = PortfolioResearchService(config=custom_config)
```

## Configuration Options

### Web Scraping
- `session_timeout`: HTTP session timeout (seconds)
- `max_pages`: Maximum number of pages to scrape
- `max_content_length`: Maximum content length per page (characters)
- `request_delay`: Delay between requests (seconds)

### NLP Processing
- `summary_sentences`: Number of sentences in summary
- `keyphrase_ngram_range`: Range for keyphrase extraction (min, max)
- `max_keywords`: Maximum number of keywords to extract
- `min_keyword_score`: Minimum score threshold for keywords

### LLM Settings
- `max_tokens`: Maximum tokens for LLM response
- `temperature`: Creativity level for LLM (0.0-1.0)

## Output Structure

```python
{
    "portfolio_data": {
        "domain": "company.com",
        "pages": [...],  # List of scraped pages
        "raw_text": "...",  # Combined text content
        "technologies": [...],  # Detected technologies
        "industries": [...],  # Identified industries
        "projects": [...]  # Found projects
    },
    "llm_summary": {
        "summary": "...",  # LLM-generated summary
        "method": "llm",
        "model_used": "gpt-4",
        "generated_at": "2024-01-01T00:00:00Z"
    },
    "nlp_summary": {
        "summary": "...",  # NLP-generated summary
        "method": "nlp",
        "key_phrases": [...],  # Extracted key phrases
        "entities": {...},  # Named entities by type
        "techniques_used": ["keybert", "sumy", "spacy"]
    }
}
```

## Dependencies

### Core Dependencies
- `aiohttp`: Async HTTP client for web scraping
- `beautifulsoup4`: HTML parsing and navigation
- `trafilatura`: Advanced content extraction
- `lxml`: XML/HTML processing backend

### NLP Dependencies
- `keybert`: Keyword extraction using BERT embeddings
- `spacy`: Named entity recognition and text processing
- `sumy`: Text summarization algorithms
- `sentence-transformers`: BERT-based sentence embeddings

### LLM Dependencies
- Integrated with existing LLM orchestrator
- Supports multiple providers (OpenAI, Gemini, Groq)
- Configurable fallback mechanisms

## Performance Considerations

### Speed vs. Quality Trade-offs
- **Fast Preset**: 5 pages, 25K chars, 3 sentences summary
- **Standard**: 10 pages, 50K chars, 5 sentences summary  
- **Thorough**: 15 pages, 75K chars, 7 sentences summary

### Cost Optimization
- **NLP-First**: Use NLP summaries when LLM costs are high
- **Configurable Limits**: Adjust token limits and page counts
- **Smart Fallbacks**: Graceful degradation when services fail

### Memory Management
- **Content Limits**: Configurable maximum content lengths
- **Streaming Processing**: Process pages incrementally
- **Garbage Collection**: Automatic cleanup of large text objects

## Error Handling

### Robust Fallbacks
- **Content Extraction**: Trafilatura → BeautifulSoup → Basic text
- **Summarization**: TextRank → LSA → Simple sentence extraction
- **LLM Failures**: Automatic fallback to NLP-only processing

### Graceful Degradation
- **Partial Results**: Return available data even if some sources fail
- **Error Reporting**: Detailed error messages for debugging
- **Health Monitoring**: Service health checks and retry logic

## Security & Ethics

### Web Scraping Best Practices
- **Rate Limiting**: Respectful delays between requests
- **User-Agent Headers**: Proper identification of requests
- **Robots.txt Compliance**: Respect website crawling policies
- **Content Validation**: Filter out sensitive or inappropriate content

### Data Privacy
- **Content Filtering**: Remove PII and sensitive information
- **Storage Limits**: Configurable content retention policies
- **Access Controls**: Integration with existing authentication systems

## Integration Points

### Company Research Pipeline
- **Orchestrator Integration**: Seamless integration with main research pipeline
- **Data Aggregation**: Portfolio data included in comprehensive company reports
- **Cost Tracking**: Integrated cost estimation and tracking

### API Endpoints
- **Standalone Service**: Can be used independently for portfolio analysis
- **Batch Processing**: Support for multiple company analysis
- **Async Processing**: Non-blocking operation for better performance

## Future Enhancements

### Planned Features
- **Multi-language Support**: International portfolio analysis
- **Image Analysis**: Logo and visual content processing
- **Social Media Integration**: Portfolio presence on social platforms
- **Competitive Analysis**: Cross-company portfolio comparison

### Performance Improvements
- **Caching Layer**: Redis-based content caching
- **Parallel Processing**: Concurrent page scraping
- **Machine Learning**: Improved content relevance scoring
- **CDN Integration**: Faster content delivery

## Troubleshooting

### Common Issues
1. **SpaCy Model Missing**: Run `python -m spacy download en_core_web_sm`
2. **Content Extraction Failures**: Check website structure and accessibility
3. **LLM API Errors**: Verify API keys and rate limits
4. **Memory Issues**: Reduce `max_content_length` and `max_pages`

### Debug Mode
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Service will now provide detailed logging
service = PortfolioResearchService()
```

## Contributing

### Development Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Download spaCy model: `python -m spacy download en_core_web_sm`
3. Run tests: `python test_portfolio.py`

### Code Standards
- Follow existing code style and patterns
- Add comprehensive error handling
- Include docstrings for all methods
- Write unit tests for new features

### Testing
- Test with various website structures
- Verify fallback mechanisms work correctly
- Performance testing with different configurations
- Integration testing with main pipeline

