# Quickstart Guide: Backend Cleanup and Frontend Consistency

## Prerequisites
- Python 3.13+ with uv package manager
- Node.js 18+ with npm
- Neon Serverless PostgreSQL database (or local PostgreSQL)

## Backend Setup

### 1. Navigate to Backend Directory
```bash
cd backend
```

### 2. Install Python Dependencies
```bash
uv venv  # Creates virtual environment
source .venv/bin/activate
uv pip install -r requirements.txt
```

### 3. Set Up Environment Variables
```bash
cp .env.example .env
# Edit .env with your database connection string
```

### 4. Clean Up Unnecessary Files
Remove files that are not needed for basic todo CRUD operations without authentication:
```bash
# Remove authentication-related files
rm api/auth.py
rm api/better_auth.py
rm api/user.py
rm better-auth-server.ts
rm BETTER_AUTH_INTEGRATION.md
rm models/auth_token.py
rm models/session.py
rm models/token.py
rm models/user.py
rm schemas/auth.py
rm schemas/user.py
rm core/security/jwt.py
rm core/security/session.py
rm security/jwt.py
rm dependencies/auth.py
rm core/services/user_service.py
rm core/middleware.py  # if it contains auth middleware
rm core/errors.py      # if it contains auth-related errors
rm core/logging.py     # if it contains auth-related logging
```

### 5. Initialize Database
```bash
python -c "from database.session import create_db_and_tables; create_db_and_tables()"
```

## Frontend Setup

### 1. Navigate to Frontend Directory
```bash
cd frontend
```

### 2. Install Node.js Dependencies
```bash
npm install
```

### 3. Set Up Environment Variables
```bash
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
- API routes: `backend/api/tasks.py` (now only contains todo-related endpoints)
- Database models: `backend/models/todo.py`
- Database session: `backend/database/session.py`

### Frontend Configuration
- Main page: `frontend/app/page.tsx`
- Todo components: `frontend/components/todo/`
- API client: `frontend/lib/api.ts`
- Environment: `frontend/.env.local`

## API Endpoints (After Cleanup)
- GET `/api/todos` - Retrieve all todos
- POST `/api/todos` - Create a new todo
- GET `/api/todos/{id}` - Get specific todo
- PUT `/api/todos/{id}` - Update todo
- DELETE `/api/todos/{id}` - Delete todo
- PATCH `/api/todos/{id}/toggle` - Toggle completion status

## Troubleshooting
- If backend fails to start, ensure the virtual environment is activated
- If frontend can't connect to backend, check that the API URL in `.env.local` matches the backend server address
- If database connection fails, verify your PostgreSQL connection string in `.env`
- If authentication errors occur, ensure all auth-related files have been properly removed