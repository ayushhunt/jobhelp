# JobHelp AI - Backend Documentation

## 📋 Table of Contents

1. [Overview](#overview)
2. [Project Structure](#project-structure)
3. [API Endpoints](#api-endpoints)
4. [Authentication System](#authentication-system)
5. [Database Management](#database-management)
6. [Configuration](#configuration)
7. [Development Setup](#development-setup)
8. [Deployment](#deployment)
9. [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

JobHelp AI Backend is a FastAPI-based REST API that provides:
- **AI-powered resume analysis** using multiple LLM providers
- **Company research tools** with web scraping and knowledge graphs
- **User authentication** with JWT tokens and role-based access
- **Email integration** with Resend API for notifications
- **Caching layer** with Redis for performance optimization

### Tech Stack
- **Framework**: FastAPI 0.104.1
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Cache**: Redis (Upstash compatible)
- **Authentication**: JWT with HTTP-only cookies
- **Email**: Resend API
- **AI/LLM**: OpenAI, Gemini, Groq, Anthropic
- **Deployment**: Docker + Docker Compose

---

## 🏗️ Project Structure

```
backend/
├── app/                          # Main application package
│   ├── api/                      # API routes and endpoints
│   │   └── v1/                   # API version 1
│   │       ├── api.py           # Main API router
│   │       └── endpoints/        # Individual endpoint modules
│   │           ├── auth.py      # Authentication endpoints
│   │           ├── analysis.py  # Resume analysis endpoints
│   │           ├── llm.py       # LLM provider endpoints
│   │           ├── company_research.py  # Company research endpoints
│   │           └── oauth.py     # OAuth authentication
│   ├── core/                     # Core functionality
│   │   ├── database.py          # Database configuration
│   │   ├── redis_cache.py       # Redis caching
│   │   ├── simple_auth_middleware.py  # Authentication middleware
│   │   ├── exceptions/          # Custom exceptions
│   │   └── logging/             # Logging configuration
│   ├── models/                   # Data models
│   │   ├── entities/            # Database entities (SQLAlchemy)
│   │   │   └── user.py         # User model
│   │   └── schemas/             # Pydantic schemas
│   │       ├── auth.py         # Authentication schemas
│   │       ├── analysis.py     # Analysis schemas
│   │       └── company_research.py  # Company research schemas
│   ├── services/                 # Business logic services
│   │   ├── auth/                # Authentication services
│   │   │   ├── auth_service.py  # User management
│   │   │   ├── jwt_service.py   # JWT token handling
│   │   │   └── oauth_service.py # OAuth integration
│   │   ├── email_service.py     # Email service (Resend)
│   │   ├── llm/                 # LLM provider services
│   │   ├── company_research/    # Company research services
│   │   ├── analytics/           # Analytics services
│   │   └── parsing/             # Document parsing services
│   ├── utils/                    # Utility functions
│   │   ├── file_handling/       # File processing utilities
│   │   └── text_processing/     # Text analysis utilities
│   ├── config/                   # Configuration
│   │   └── settings.py          # Application settings
│   └── main.py                   # FastAPI application factory
├── create_tables.py              # Database table creation script
├── manage_database.py            # Database management CLI
├── test_db_connection.py         # Database connection test
├── main.py                       # Application entry point
├── requirements.txt              # Python dependencies
├── env.example                   # Environment variables template
└── README_AUTH_SYSTEM.md         # Authentication system docs
```

---

## 🔌 API Endpoints

### Base URL
- **Development**: `http://localhost:8000`
- **API Prefix**: `/api/v1`

### Health Check
```
GET /health
```
Returns system health status including database and Redis connectivity.

### Authentication Endpoints
```
POST   /api/v1/auth/register          # User registration
POST   /api/v1/auth/login             # User login
POST   /api/v1/auth/logout            # User logout
GET    /api/v1/auth/me                # Get current user info
POST   /api/v1/auth/refresh           # Refresh access token
POST   /api/v1/auth/forgot-password   # Request password reset
POST   /api/v1/auth/reset-password    # Reset password with token
POST   /api/v1/auth/verify-email      # Verify email with token
POST   /api/v1/auth/resend-verification  # Resend verification email
```

### OAuth Endpoints
```
GET    /api/v1/auth/google            # Google OAuth login
GET    /api/v1/auth/google/callback   # Google OAuth callback
GET    /api/v1/auth/github            # GitHub OAuth login
GET    /api/v1/auth/github/callback   # GitHub OAuth callback
```

### Analysis Endpoints
```
POST   /api/v1/analysis/documents     # Analyze resume/job description
GET    /api/v1/analysis/history       # Get analysis history
```

### LLM Provider Endpoints
```
POST   /api/v1/llm/chat              # Chat with LLM
GET    /api/v1/llm/providers         # List available providers
POST   /api/v1/llm/analyze           # LLM-powered analysis
```

### Company Research Endpoints
```
POST   /api/v1/company-research/analyze     # Research company
GET    /api/v1/company-research/history     # Get research history
POST   /api/v1/company-research/portfolio   # Portfolio research
```

---

## 🔐 Authentication System

### Overview
- **JWT-based authentication** with access and refresh tokens
- **HTTP-only cookies** for secure token storage
- **Automatic token refresh** for seamless user experience
- **Role-based access control** (Admin, Applicant, Recruiter)
- **Email verification** required for account activation

### User Roles
- **Admin**: Full system access, user management
- **Applicant**: Job seekers, resume analysis access
- **Recruiter**: Hiring managers, company research access

### Token Management
- **Access Token**: 30 minutes expiry, stored in HTTP-only cookie
- **Refresh Token**: 7 days expiry, used for automatic token renewal
- **Verification Token**: Email verification (24 hours expiry)
- **Reset Token**: Password reset (1 hour expiry)

### Middleware Usage
```python
from app.core.simple_auth_middleware import (
    require_auth,           # Any authenticated user
    require_admin,          # Admin only
    require_applicant,      # Applicant only
    require_recruiter,      # Recruiter only
    require_verified_user,  # Email verified users only
    optional_auth          # Optional authentication
)

# Example endpoint with role-based protection
@router.get("/admin-dashboard")
async def admin_dashboard(user: User = Depends(require_admin)):
    return {"message": "Admin access granted"}
```

### Registration Flow
1. User submits registration form (email, password, full_name, role)
2. System creates user account with hashed password
3. Verification email sent via Resend API
4. User clicks verification link to activate account
5. Welcome email sent upon successful verification

---

## 🗄️ Database Management

### Database Schema

#### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255),
    hashed_password VARCHAR(255),
    auth_provider authprovider DEFAULT 'local',
    provider_id VARCHAR(255),
    role userrole DEFAULT 'applicant',
    is_active BOOLEAN DEFAULT true,
    is_verified BOOLEAN DEFAULT false,
    password_reset_token VARCHAR(255),
    password_reset_expires TIMESTAMP,
    verification_token VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP,
    last_login TIMESTAMP
);
```

#### Enum Types
```sql
CREATE TYPE userrole AS ENUM ('admin', 'applicant', 'recruiter');
CREATE TYPE authprovider AS ENUM ('local', 'google', 'github');
```

### Database Management Commands

#### Create Tables
```bash
# Create all database tables
python3 create_tables.py

# Or use the management script
python3 manage_database.py create
```

#### Reset Database
```bash
# ⚠️  WARNING: This will delete ALL data!
python3 manage_database.py reset
```

#### Check Database Status
```bash
python3 manage_database.py check
```

#### Run Migrations
```bash
python3 manage_database.py migrate
```

#### Test Database Connection
```bash
python3 test_db_connection.py
```

### Manual Database Operations

#### Connect to Database
```bash
# Using psql (replace with your credentials)
psql -h localhost -U postgres -d jobhelp
```

#### Check Tables
```sql
\dt                          -- List all tables
\d users                     -- Describe users table
\dT                          -- List custom types (enums)
```

#### Check Enum Values
```sql
SELECT enumlabel 
FROM pg_enum e 
JOIN pg_type t ON e.enumtypid = t.oid 
WHERE t.typname = 'userrole';
```

#### Reset User Data
```sql
-- Delete all users (careful!)
DELETE FROM users;

-- Reset auto-increment
ALTER SEQUENCE users_id_seq RESTART WITH 1;
```

#### Fix Enum Issues
```sql
-- Drop and recreate enum types
DROP TABLE IF EXISTS users CASCADE;
DROP TYPE IF EXISTS userrole CASCADE;
DROP TYPE IF EXISTS authprovider CASCADE;

CREATE TYPE userrole AS ENUM ('admin', 'applicant', 'recruiter');
CREATE TYPE authprovider AS ENUM ('local', 'google', 'github');

-- Then run create_tables.py to recreate tables
```

---

## ⚙️ Configuration

### Environment Variables

#### Required Variables
```bash
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/jobhelp

# JWT Security
JWT_SECRET_KEY=your-super-secret-jwt-key-minimum-32-characters
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Email Service
RESEND_API_KEY=your_resend_api_key_here
EMAIL_FROM=noreply@yourdomain.com

# Redis Cache
REDIS_URL=rediss://username:password@host:port/database
```

#### Optional Variables
```bash
# LLM Providers
OPENAI_API_KEY=your_openai_key
GEMINI_API_KEY=your_gemini_key
GROQ_API_KEY=your_groq_key
ANTHROPIC_API_KEY=your_anthropic_key

# OAuth
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret

# Frontend
FRONTEND_URL=http://localhost:3000
```

### Settings Management
All configuration is managed through `app/config/settings.py` using Pydantic Settings:

```python
from app.config.settings import settings

# Access configuration
database_url = settings.get_database_url
api_key = settings.OPENAI_API_KEY
debug_mode = settings.DEBUG
```

---

## 🚀 Development Setup

### Prerequisites
- Python 3.9+
- PostgreSQL 12+
- Redis (or Upstash Redis)
- Git

### Quick Start
```bash
# 1. Clone repository
git clone <repository-url>
cd jobhelp/backend

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup environment variables
cp env.example .env
# Edit .env with your configuration

# 5. Setup database
python3 manage_database.py create

# 6. Test connection
python3 test_db_connection.py

# 7. Run development server
python3 main.py
# Or: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Development Tools
```bash
# Run with auto-reload
uvicorn app.main:app --reload

# Run tests
python3 test_db_connection.py

# Check API documentation
# Visit: http://localhost:8000/docs (Swagger UI)
# Visit: http://localhost:8000/redoc (ReDoc)
```

---

## 🐳 Deployment

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Manual Deployment
```bash
# 1. Setup production environment
export DEBUG=false
export JWT_SECRET_KEY="your-production-secret"

# 2. Install production dependencies
pip install -r requirements.txt

# 3. Setup database
python3 manage_database.py create

# 4. Run with production server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Production Checklist
- [ ] Set strong JWT_SECRET_KEY
- [ ] Configure production database
- [ ] Setup Redis cache
- [ ] Configure email service (Resend)
- [ ] Setup HTTPS/SSL
- [ ] Configure CORS origins
- [ ] Setup monitoring and logging
- [ ] Configure backup strategy

---

## 🔧 Troubleshooting

### Common Issues

#### Database Connection Issues
```bash
# Check database status
python3 manage_database.py check

# Test basic connection
python3 test_db_connection.py

# Common solutions:
# 1. Check DATABASE_URL in .env
# 2. Ensure PostgreSQL is running
# 3. Verify database exists and user has permissions
```

#### Enum Type Errors
```
Error: invalid input value for enum userrole: "APPLICANT"
```
**Solution:**
```bash
# Run enum migration
python3 manage_database.py migrate

# Or reset database (⚠️  deletes data)
python3 manage_database.py reset
```

#### Authentication Issues
```bash
# Check JWT configuration
grep JWT .env

# Verify token expiration settings
# Access tokens: 30 minutes (default)
# Refresh tokens: 7 days (default)
```

#### Email Service Issues
```
Error: You can only send testing emails to your own email address
```
**Solution:**
- Verify domain with Resend at https://resend.com/domains
- Update EMAIL_FROM to use verified domain
- Or use your verified email for testing

#### Redis Connection Issues
```bash
# Check Redis URL format
# Format: rediss://username:password@host:port/database

# Test Redis connection
python3 -c "from app.core.redis_cache import redis_cache; print(redis_cache.test_connection())"
```

### Debug Mode
Enable debug mode for detailed error messages:
```bash
export DEBUG=true
python3 main.py
```

### Log Analysis
Check application logs:
```bash
# View logs
tail -f logs/app.log

# Or check console output in debug mode
```

---

## 📞 Support

### Getting Help
1. **Check this documentation** for common solutions
2. **Review error logs** for specific error messages
3. **Test database connection** using provided scripts
4. **Verify environment configuration** in `.env` file

### Useful Commands Reference
```bash
# Database Management
python3 manage_database.py check    # Check database status
python3 manage_database.py create   # Create tables
python3 manage_database.py reset    # Reset database
python3 manage_database.py migrate  # Run migrations

# Development
python3 main.py                     # Start development server
python3 test_db_connection.py       # Test database connection

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## 📝 API Documentation

### Interactive Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Health Check
```bash
curl http://localhost:8000/health
```

### Authentication Examples
```bash
# Register new user
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123",
    "full_name": "John Doe",
    "role": "applicant"
  }'

# Login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'

# Get current user (requires authentication)
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Cookie: access_token=your_access_token_here"
```

---

*Last updated: December 2024*
*Version: 1.0.0*
