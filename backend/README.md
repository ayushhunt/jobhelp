# JobHelp AI API - Backend

A production-ready, modular FastAPI backend for AI-powered resume and job description analysis.

## 🏗️ Architecture

The backend follows a clean, modular architecture with clear separation of concerns:

```
app/
├── api/                    # API layer
│   └── v1/               # API version 1
│       ├── endpoints/    # Route handlers
│       └── api.py        # Main API router
├── core/                  # Core functionality
│   ├── logging/          # Logging configuration
│   └── exceptions/       # Custom exception classes
├── services/              # Business logic services
│   ├── analytics/        # Analytics orchestration
│   ├── llm/              # LLM service management
│   └── parsing/          # Document parsing services
├── utils/                 # Utility functions
│   ├── text_processing/  # Text analysis utilities
│   └── file_handling/    # File processing utilities
├── models/                # Data models
│   └── schemas/          # Pydantic schemas
├── config/                # Configuration management
└── main.py               # Application entry point
```

## 🚀 Features

- **Modular Design**: Clean separation of concerns with dedicated services
- **Production Logging**: Structured logging with file rotation and configurable levels
- **Error Handling**: Custom exception classes with proper HTTP status codes
- **File Processing**: Support for PDF, DOCX, and TXT files
- **Text Analysis**: Advanced NLP-based text processing and similarity analysis
- **AI Integration**: Modular LLM service with usage tracking and rate limiting
- **Experience Parsing**: Intelligent work experience extraction and analysis
- **API Documentation**: Auto-generated OpenAPI documentation
- **Health Checks**: Built-in health monitoring endpoints
- **CORS Support**: Configurable cross-origin resource sharing
- **Environment Configuration**: Centralized settings management

## 📋 Requirements

- Python 3.8+
- FastAPI
- Uvicorn
- NLTK
- PyPDF2
- python-docx
- dateparser
- pydantic-settings

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd jobhelp/backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Download NLTK data**
   ```bash
   python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('averaged_perceptron_tagger')"
   ```

## 🚀 Running the Application

### Development Mode
```bash
python run.py
```

### Production Mode
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Using Docker
```bash
docker build -t jobhelp-api .
docker run -p 8000:8000 jobhelp-api
```

## 📚 API Endpoints

### Analysis Endpoints
- `POST /api/v1/analysis/analyze` - Analyze resume and job description
- `GET /api/v1/analysis/ai-usage` - Get AI usage statistics
- `GET /api/v1/analysis/ai-models` - Get available AI models
- `GET /api/v1/analysis/ai-costs` - Get cost comparison

### System Endpoints
- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /docs` - API documentation (development only)

## ⚙️ Configuration

Configuration is managed through environment variables and the `app/config/settings.py` file:

```python
# API Configuration
API_V1_STR = "/api/v1"
PROJECT_NAME = "JobHelp AI API"
VERSION = "3.0.0"

# Server Configuration
HOST = "0.0.0.0"
PORT = 8000
DEBUG = False

# CORS Configuration
BACKEND_CORS_ORIGINS = ["http://localhost:3000"]

# LLM Configuration
OPENAI_API_KEY = None
ANTHROPIC_API_KEY = None
GROQ_API_KEY = None

# Rate Limiting
RATE_LIMIT_PER_MINUTE = 60

# File Upload
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_FILE_TYPES = [".pdf", ".docx", ".txt"]

# Logging
LOG_LEVEL = "INFO"
LOG_FILE = "logs/app.log"

# AI Usage Limits
FREE_TIER_DAILY_LIMIT = 10
PREMIUM_TIER_DAILY_LIMIT = 100
```

## 🔧 Development

### Project Structure
- **Services**: Business logic and external integrations
- **Utils**: Reusable utility functions
- **Models**: Data structures and validation schemas
- **API**: HTTP endpoint definitions and routing
- **Core**: Application configuration and shared functionality

### Adding New Features
1. Create new service in `app/services/`
2. Add Pydantic schemas in `app/models/schemas/`
3. Create API endpoints in `app/api/v1/endpoints/`
4. Update the main API router in `app/api/v1/api.py`

### Testing
```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_analytics.py
```

## 📊 Logging

The application uses structured logging with configurable levels:

- **Console**: INFO level and above
- **File**: DEBUG level and above (with rotation)
- **Format**: Timestamp, logger name, level, message
- **Rotation**: 10MB files with 5 backups

## 🚨 Error Handling

Custom exception classes provide consistent error handling:

- `JobHelpException`: Base exception class
- `FileProcessingError`: File processing failures
- `TextExtractionError`: Text extraction failures
- `LLMServiceError`: LLM service failures
- `AnalyticsError`: Analytics processing failures
- `ValidationError`: Input validation failures
- `RateLimitExceeded`: Rate limit violations
- `InsufficientCredits`: AI usage limit exceeded

## 🔒 Security

- **CORS**: Configurable cross-origin policies
- **File Validation**: File type and size restrictions
- **Rate Limiting**: Configurable request limits
- **Input Validation**: Pydantic schema validation
- **Error Sanitization**: Production-safe error messages

## 📈 Monitoring

- **Health Checks**: `/health` endpoint for monitoring
- **Structured Logging**: JSON-formatted logs for analysis
- **Performance Metrics**: Request timing and processing metrics
- **Error Tracking**: Comprehensive error logging and categorization

## 🚀 Deployment

### Environment Variables
```bash
# Required
DEBUG=false
LOG_LEVEL=INFO

# Optional
HOST=0.0.0.0
PORT=8000
LOG_FILE=logs/app.log
```

### Production Considerations
- Set `DEBUG=false`
- Configure proper CORS origins
- Set up log file paths
- Configure trusted hosts
- Set appropriate log levels
- Enable health check monitoring

## 🤝 Contributing

1. Follow the existing code structure
2. Add proper logging and error handling
3. Include type hints and docstrings
4. Update tests for new functionality
5. Follow PEP 8 style guidelines

## 📄 License

[Add your license information here]

## 🆘 Support

For issues and questions:
- Check the logs for detailed error information
- Review the API documentation at `/docs`
- Check the health endpoint at `/health`
- Review configuration in `app/config/settings.py`
