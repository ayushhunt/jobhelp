# JobHelp AI - Backend API

🚀 **AI-powered resume analysis and job matching platform built with FastAPI**

## ✨ Features

- 🤖 **Multi-LLM Analysis** - OpenAI, Gemini, Groq, Anthropic integration
- 📄 **Document Processing** - PDF, DOCX, TXT parsing and analysis
- 🔍 **Company Research** - Automated company data gathering
- 🔐 **Secure Authentication** - JWT with role-based access control
- 📧 **Email Integration** - Resend API for notifications
- ⚡ **High Performance** - Redis caching and optimized queries

## 🚀 Quick Start

```bash
# 1. Setup environment
cp env.example .env
# Edit .env with your configuration

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup database
python3 manage_database.py create

# 4. Start server
python3 main.py --dev  # Development mode
# or
python3 main.py        # Production mode
```

## 📚 Documentation

- **[📖 Complete Backend Documentation](BACKEND_DOCUMENTATION.md)** - Full API reference, database management, deployment guide
- **[🔗 Interactive API Docs](http://localhost:8000/docs)** - Swagger UI (when server running)
- **[❤️ Health Check](http://localhost:8000/health)** - Server status

## 🔧 Database Management

```bash
python3 manage_database.py check    # Check database status
python3 manage_database.py create   # Create all tables
python3 manage_database.py reset    # Reset database (⚠️ deletes data)
python3 test_db_connection.py       # Test database connection
```

## 🎯 API Endpoints

| Endpoint | Description |
|----------|-------------|
| `POST /api/v1/auth/register` | User registration |
| `POST /api/v1/auth/login` | User login |
| `GET /api/v1/auth/me` | Current user info |
| `POST /api/v1/analysis/documents` | Analyze resume/job description |
| `POST /api/v1/company-research/analyze` | Company research |
| `POST /api/v1/llm/chat` | Chat with LLM |

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   FastAPI App   │    │   Authentication │    │   Database      │
│                 │◄──►│                  │◄──►│                 │
│ - API Routes    │    │ - JWT Tokens     │    │ - PostgreSQL    │
│ - Middleware    │    │ - Role-based     │    │ - User Data     │
│ - Validation    │    │ - Email Verify   │    │ - Analytics     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                        │                        │
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   LLM Services  │    │   Email Service  │    │   Redis Cache   │
│                 │    │                  │    │                 │
│ - OpenAI        │    │ - Resend API     │    │ - Session Data  │
│ - Gemini        │    │ - Verification   │    │ - Query Cache   │
│ - Groq          │    │ - Notifications  │    │ - Rate Limiting │
│ - Anthropic     │    │ - Welcome Emails │    │ - Performance   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🔒 Authentication

- **JWT Tokens** with HTTP-only cookies
- **Automatic token refresh** for seamless UX
- **Role-based access**: Admin, Applicant, Recruiter
- **Email verification** required for activation

## 🛠️ Development

```bash
# Development server with auto-reload
python3 main.py --dev

# Production server with multiple workers
python3 main.py --workers 4

# Custom port
python3 main.py --port 8080

# Debug mode
python3 main.py --log-level debug
```

## 📞 Support

For detailed documentation, troubleshooting, and deployment instructions, see:
**[📖 BACKEND_DOCUMENTATION.md](BACKEND_DOCUMENTATION.md)**

---

*Built with ❤️ using FastAPI, PostgreSQL, Redis, and modern Python practices*
