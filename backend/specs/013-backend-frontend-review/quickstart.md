# Quickstart Guide: Backend-Frontend Todo Application

## Prerequisites
- Python 3.13+ with uv package manager
- Node.js 18+ with npm
- Neon Serverless PostgreSQL database (or local PostgreSQL)

## Setup Instructions

### 1. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
uv venv  # Creates virtual environment
source .venv/bin/activate
uv pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database connection string

# Initialize database
python -c "from database.session import create_db_and_tables; create_db_and_tables()"
```

### 2. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Set up environment variables
cp .env.local.example .env.local
# Edit .env.local with your backend API URL (default: http://localhost:8000)
```

## Running the Application

### 1. Start Backend Server
```bash
cd backend
source .venv/bin/activate
uv run -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Start Frontend Server
```bash
cd frontend
npm run dev
```

### 3. Access the Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Backend API Docs: http://localhost:8000/docs

## Key Configuration Points

### Backend Configuration
- Main application: `backend/main.py`
- API routes: `backend/api/tasks.py` (currently) or `backend/api/todos.py`
- Database models: `backend/models/todo.py`
- Database session: `backend/database/session.py`

### Frontend Configuration
- Main page: `frontend/app/page.tsx`
- Todo components: `frontend/components/todo/`
- API client: `frontend/lib/api.ts`
- Environment: `frontend/.env.local`

## Known Issues to Address
1. API endpoint mismatch: Backend uses `/api/tasks`, frontend calls `/todos`
2. Data model inconsistency: Different field naming conventions
3. Response format mismatch: Backend returns direct arrays, frontend expects wrapped responses
4. ID type mismatch: Backend uses integers, frontend expects strings

## Development Commands
```bash
# Run backend tests
cd backend && source .venv/bin/activate && python -m pytest

# Run frontend linting
cd frontend && npm run lint

# Run frontend type checking
cd frontend && npm run type-check
```

## Troubleshooting
- If backend fails to start, ensure the virtual environment is activated
- If frontend can't connect to backend, check that the API URL in `.env.local` matches the backend server address
- If database connection fails, verify your PostgreSQL connection string in `.env`