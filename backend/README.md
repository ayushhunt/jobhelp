# JobHelp AI API - Backend

A modern, modular FastAPI application for AI-powered resume and job description analysis.

## 🏗️ Project Structure

```
backend/
├── app/                           # Main application package
│   ├── api/                      # API layer
│   │   └── v1/                  # API version 1
│   │       ├── api.py           # Main API router
│   │       └── endpoints/       # API endpoints
│   │           ├── analysis.py  # Document analysis endpoints
│   │           └── llm.py       # LLM provider management
│   ├── core/                     # Core functionality
│   │   ├── config/              # Configuration management
│   │   ├── exceptions/          # Custom exceptions and handlers
│   │   └── logging/             # Logging configuration
│   ├── models/                   # Data models and schemas
│   │   └── schemas/             # Pydantic schemas
│   ├── services/                 # Business logic services
│   │   ├── analytics/           # Document analysis orchestration
│   │   ├── llm/                 # LLM integration
│   │   │   ├── providers/       # LLM provider implementations
│   │   │   ├── llm_service.py  # Business logic layer
│   │   │   ├── llm_orchestrator.py # Provider management
│   │   │   └── provider_factory.py # Provider factory
│   │   └── parsing/             # Experience parsing
│   └── utils/                    # Utility functions
│       ├── file_handling/       # Document processing
│       └── text_processing/     # Text analysis utilities
├── logs/                         # Application logs
├── main.py                       # Main entry point
├── start.py                      # Simple production startup
├── requirements.txt              # Python dependencies
├── env.example                   # Environment variables template
└── README.md                     # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip package manager

### Installation
```bash
# Clone and navigate to backend directory
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Setup
```bash
# Copy environment template
cp env.example .env

# Edit .env with your API keys
nano .env
```

### Production Startup
```bash
# Simple production start (recommended)
python3 start.py

# Or use main entry point
python3 main.py

# Or use uvicorn directly
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 🔧 Configuration

### Environment Variables (.env)
```env
# API Configuration
API_V1_STR=/api/v1
PROJECT_NAME=JobHelp AI API
VERSION=3.0.0

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=false

# CORS Configuration
BACKEND_CORS_ORIGINS=["http://localhost:3000", "http://127.0.0.1:3000"]

# LLM Configuration
GROQ_API_KEY=your_groq_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log

# AI Usage Limits
FREE_TIER_DAILY_LIMIT=10
PREMIUM_TIER_DAILY_LIMIT=100
```

## 📡 API Endpoints

### Base URL: `/api/v1`

#### Document Analysis
- **POST** `/analysis/analyze` - Analyze resume and job description
- **GET** `/analysis/ai-usage` - Get AI usage statistics

#### LLM Management
- **GET** `/llm/status` - Get LLM service status
- **GET** `/llm/providers` - List available LLM providers
- **POST** `/llm/switch-provider` - Switch LLM provider
- **GET** `/llm/current-provider` - Get current provider info
- **POST** `/llm/test-provider` - Test specific provider

#### Health Check
- **GET** `/health` - Service health status

## 🤖 LLM Providers

### Supported Providers
1. **Groq** (Recommended) - Ultra-fast inference
2. **Gemini** - Google's AI models
3. **OpenAI** - GPT models
4. **Mock** - Testing/development only

### Provider Selection
```python
from app.services.llm.llm_service import LLMService

# Initialize service
llm_service = LLMService()

# Switch providers
llm_service.switch_provider('groq')      # Switch to Groq
llm_service.switch_provider('gemini')    # Switch to Gemini
llm_service.switch_provider('openai')    # Switch to OpenAI

# Auto-selection (happens automatically when needed)
# Prefers: Groq → Gemini → OpenAI → Mock
```

## 🏗️ Architecture

### Design Principles
- **Single Responsibility**: Each module has one clear purpose
- **Dependency Inversion**: High-level modules don't depend on low-level details
- **Interface Segregation**: Clean, focused interfaces
- **Separation of Concerns**: Business logic, data access, and presentation are separate

### Service Layer
- **Analytics Service**: Orchestrates document analysis workflow
- **LLM Service**: Business logic for AI insights generation
- **LLM Orchestrator**: Manages provider selection and switching
- **Provider Factory**: Creates and manages LLM provider instances

### Data Flow
```
Client Request → API Endpoint → Service Layer → LLM Orchestrator → Provider → Response
                ↓
            Validation → Business Logic → Data Processing → Response Formatting
```

## 🧪 Development

### Adding New Features
1. **New API Endpoint**: Add to `app/api/v1/endpoints/`
2. **New Service**: Add to `app/services/`
3. **New Provider**: Add to `app/services/llm/providers/`
4. **New Schema**: Add to `app/models/schemas/`
5. **New Utility**: Add to `app/utils/`

### Code Quality
- **Type Safety**: Full TypeScript-like type checking with Pydantic
- **Error Handling**: Centralized exception handling with proper HTTP status codes
- **Logging**: Comprehensive logging with rotation and formatting
- **Testing**: Modular design enables easy unit testing

## 🚀 Production Deployment

### Docker (Recommended)
```bash
# Build and run with Docker
docker build -t jobhelp-api .
docker run -p 8000:8000 jobhelp-api
```

### Systemd Service
```bash
# Create service file
sudo nano /etc/systemd/system/jobhelp-api.service

# Enable and start service
sudo systemctl enable jobhelp-api
sudo systemctl start jobhelp-api
```

### Environment Variables
```bash
# Set production environment variables
export DEBUG=false
export LOG_LEVEL=WARNING
export GROQ_API_KEY=your_production_key
```

## 📊 Monitoring & Logging

### Log Files
- **Application Logs**: `logs/app.log`
- **Access Logs**: Enabled by default with uvicorn
- **Error Logs**: Centralized error handling and logging

### Health Checks
```bash
# Check service health
curl http://localhost:8000/health

# Check LLM service status
curl http://localhost:8000/api/v1/llm/status
```

## 🔒 Security

### CORS Configuration
- Configurable origins via `BACKEND_CORS_ORIGINS`
- Secure by default for production

### Rate Limiting
- Built-in rate limiting per endpoint
- Configurable limits via settings

### API Keys
- Secure storage in environment variables
- Never hardcoded in source code

## 📝 Troubleshooting

### Common Issues
1. **Port Already in Use**: `lsof -ti:8000 | xargs kill -9`
2. **Missing Dependencies**: `pip install -r requirements.txt`
3. **API Key Issues**: Check `.env` file configuration
4. **Provider Errors**: Verify API keys and provider availability

### Debug Mode
```bash
# Enable debug mode
export DEBUG=true
export LOG_LEVEL=DEBUG

# Start with debug logging
python3 start.py
```

## 📚 Additional Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/    https://youtu.be/foGklduxhM0?si=2OWjEVCkNDMfYX07 
- **Pydantic Documentation**: https://pydantic-docs.helpmanual.io/   
- **Uvicorn Documentation**: https://www.uvicorn.org/

---

**Built with ❤️ using modern Python web technologies and best practices**
