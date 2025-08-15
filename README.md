# JobHelp - Resume and Job Description Analytics

A powerful SaaS application for analyzing and comparing job descriptions and resumes using advanced NLP techniques.

## Features

- Document upload and parsing (PDF/DOCX)
- Word frequency analysis
- Keyword extraction and matching
- Skills comparison
- Interactive analytics dashboard
- Similarity scoring

## Tech Stack

- Frontend: Next.js 14, TypeScript, Tailwind CSS
- Backend: Python FastAPI
- Database: PostgreSQL
- NLP: spaCy, scikit-learn, NLTK
- Infrastructure: Docker, AWS/Vercel

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.9+
- PostgreSQL
- Docker (optional)

### Installation

1. Clone the repository

2. Set up the backend:
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

3. Create a `.env` file in the backend directory:
   ```
   DATABASE_URL=postgresql://jobhelp:jobhelp@localhost:5432/jobhelp
   CORS_ORIGINS=http://localhost:3000
   ```

4. Set up PostgreSQL:
   Option 1 - Using Docker:
   ```bash
   docker-compose up -d
   ```
   
   Option 2 - Manual Installation:
   - Install PostgreSQL
   - Create a database named 'jobhelp'
   - Create a user 'jobhelp' with password 'jobhelp'
   - Grant all privileges on the database to the user

5. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```

6. Start the development servers:
   ```bash
   # Backend
   cd backend
   uvicorn main:app --reload

   # Frontend (in a new terminal)
   cd frontend
   npm run dev
   ```

7. Open http://localhost:3000 in your browser

## Project Structure

```
jobhelp/
├── frontend/           # Next.js frontend application
│   ├── src/
│   │   ├── app/       # Next.js app directory
│   │   └── components/# React components
├── backend/           # FastAPI backend application
│   ├── main.py       # Main application file
│   └── requirements.txt
├── docker/           # Docker configuration
└── docs/            # Documentation
```

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://jobhelp:jobhelp@localhost:5432/jobhelp
CORS_ORIGINS=http://localhost:3000
```

## API Endpoints

### POST /analyze
Analyzes a resume and job description.

Request:
- Content-Type: multipart/form-data
- Fields:
  - resume: File (PDF/DOCX)
  - job_description: File (PDF/DOCX)

Response:
```json
{
  "similarity_score": 0.85,
  "resume_word_frequency": {
    "python": 5,
    "javascript": 3
  },
  "jd_word_frequency": {
    "python": 4,
    "react": 3
  },
  "common_keywords": ["python", "web"],
  "missing_keywords": ["react", "node"]
}
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details