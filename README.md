# JobHelp - AI-Powered Resume and Job Description Analytics

A modern, modular SaaS application for analyzing and comparing job descriptions and resumes using advanced NLP techniques and AI insights.

## ✨ Features

- **Document Processing**: Upload and parse PDF, DOCX, and TXT files
- **Advanced Analytics**: Word frequency analysis, keyword extraction, and similarity scoring
- **AI-Powered Insights**: Get intelligent recommendations and skill gap analysis
- **Interactive Dashboard**: Beautiful, responsive analytics dashboard with charts and visualizations
- **Modular Architecture**: Clean, maintainable codebase with separation of concerns
- **Real-time Processing**: Fast document analysis with progress tracking
- **User Management**: AI usage tracking and premium features support

## 🚀 Tech Stack

### Frontend
- **Framework**: Next.js 15 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Charts**: Chart.js with D3.js integration
- **State Management**: React Hooks with custom hooks
- **HTTP Client**: Axios with centralized API service

### Backend
- **Framework**: FastAPI with async support
- **Language**: Python 3.9+
- **Architecture**: Modular service-oriented design
- **NLP Libraries**: NLTK, spaCy, textstat
- **Validation**: Pydantic with comprehensive schemas
- **Logging**: Centralized logging with rotation
- **Error Handling**: Custom exception classes with proper HTTP status codes

### Infrastructure
- **Containerization**: Docker with docker-compose
- **API Documentation**: Auto-generated OpenAPI/Swagger docs
- **CORS**: Configurable cross-origin resource sharing
- **Environment**: Pydantic settings management

## 🏗️ Project Architecture

```
jobhelp/
├── frontend/                    # Next.js frontend application
│   ├── src/
│   │   ├── app/               # Next.js app directory
│   │   ├── components/        # React components
│   │   ├── services/          # API service layer
│   │   ├── hooks/             # Custom React hooks
│   │   └── utils/             # Utility functions
│   ├── public/                # Static assets
│   └── package.json
├── backend/                    # FastAPI backend application
│   ├── app/
│   │   ├── api/               # API endpoints and routing
│   │   │   └── v1/           # API version 1
│   │   ├── core/              # Core functionality
│   │   │   ├── exceptions/    # Custom exception classes
│   │   │   └── logging/       # Logging configuration
│   │   ├── models/            # Data models and schemas
│   │   ├── services/          # Business logic services
│   │   │   ├── analytics/     # Document analysis service
│   │   │   ├── llm/          # AI/LLM integration
│   │   │   └── parsing/      # Experience parsing service
│   │   └── utils/             # Utility functions
│   ├── requirements.txt
│   └── run.py                 # Application entry point
├── docker/                     # Docker configuration
└── docs/                      # Documentation
```

## 🚀 Getting Started

### Prerequisites

- **Node.js**: 18+ (for frontend)
- **Python**: 3.9+ (for backend)
- **Package Managers**: npm and pip

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd jobhelp
   ```

2. **Set up the backend**
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up the frontend**
   ```bash
   cd ../frontend
   npm install
   ```

4. **Start the development servers**
   ```bash
   # Terminal 1 - Backend
   cd backend
   python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

   # Terminal 2 - Frontend
   cd frontend
   npm run dev
   ```

5. **Open your browser**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## 🔧 Configuration

### Backend Environment Variables

Create a `.env` file in the `backend/` directory:

```env
# API Configuration
API_V1_STR=/api/v1
PROJECT_NAME=JobHelp AI API
VERSION=3.0.0

# Server Configuration
SERVER_HOST=0.0.0.0
SERVER_PORT=8000

# CORS Configuration
CORS_ORIGINS=["http://localhost:3000"]

# AI Service Configuration
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
PARALLEL_API_KEY=your_parallel_api_key_here

# File Upload Limits
MAX_FILE_SIZE=10485760  # 10MB
ALLOWED_EXTENSIONS=["pdf", "docx", "txt"]

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log

# AI Usage Limits
FREE_TIER_DAILY_LIMIT=3
PREMIUM_TIER_DAILY_LIMIT=50
```

### Frontend Environment Variables

Create a `.env.local` file in the `frontend/` directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📡 API Endpoints

### Base URL: `/api/v1`

#### Document Analysis
- **POST** `/analysis/analyze` - Analyze resume and job description
- **GET** `/analysis/ai-usage` - Get AI usage statistics
- **GET** `/analysis/ai-models` - Get available AI models
- **GET** `/analysis/ai-costs` - Get cost comparison

#### Health Check
- **GET** `/health` - Service health status

### Example API Request

```bash
curl -X POST "http://localhost:8000/api/v1/analysis/analyze" \
  -H "Content-Type: multipart/form-data" \
  -F "resume_file=@resume.pdf" \
  -F "job_description_file=@job_description.pdf" \
  -F "use_ai=true" \
  -F "user_id=default" \
  -F "is_premium=false"
```

### Example API Response

```json
{
  "basic_analytics": {
    "similarity_score": 0.75,
    "resume_word_frequency": {"python": 5, "javascript": 3},
    "jd_word_frequency": {"python": 4, "react": 3},
    "common_keywords": ["python", "web"],
    "missing_keywords": ["react", "node"]
  },
  "advanced_analytics": {
    "semantic_similarity_score": 0.82,
    "matched_skills": ["python", "git"],
    "missing_skills": ["react", "docker"],
    "extra_skills": ["java", "spring"],
    "resume_readability": 65.2,
    "jd_readability": 58.7,
    "insights_summary": "Strong technical foundation with room for growth in modern web technologies."
  },
  "analysis_type": "advanced",
  "processing_time": 2.45,
  "timestamp": "2024-01-01T12:00:00Z"
}
```

## 🧪 Testing

### Backend Testing
```bash
cd backend
python3 -m pytest tests/
```

### Frontend Testing
```bash
cd frontend
npm run test
```

### API Testing
```bash
# Test the health endpoint
curl http://localhost:8000/health

# Test AI usage endpoint
curl "http://localhost:8000/api/v1/analysis/ai-usage?user_id=test"
```

## 🐳 Docker Deployment

### Development
```bash
docker-compose up -d
```

### Production
```bash
docker-compose -f docker-compose.prod.yml up -d
```

## 📚 Development

### Code Structure

The application follows a clean, modular architecture:

- **Services**: Business logic and external integrations
- **Models**: Data schemas and validation
- **API**: HTTP endpoints and request/response handling
- **Utils**: Helper functions and utilities
- **Hooks**: Reusable React logic
- **Components**: UI components with proper separation of concerns

### Adding New Features

1. **Backend**: Add new services in `app/services/`, schemas in `app/models/`, and endpoints in `app/api/`
2. **Frontend**: Add new components in `src/components/`, hooks in `src/hooks/`, and services in `src/services/`

### Code Quality

- **Backend**: Uses Pydantic for validation, proper error handling, and comprehensive logging
- **Frontend**: TypeScript for type safety, ESLint for code quality, and Tailwind for consistent styling

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow the existing code structure and patterns
- Add proper TypeScript types and validation
- Include error handling and logging
- Write tests for new functionality
- Update documentation as needed

## 📄 License



## 🆘 Support

- **Documentation**: Check the `/docs` endpoint for interactive API documentation
- **Issues**: Report bugs and feature requests via GitHub Issues
- **Discussions**: Join the community discussions for questions and ideas

---

**Built with ❤️ using modern web technologies and best practices**
