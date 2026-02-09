# Full-Stack Todo Application: Backend-Frontend Integration

## Overview
This document provides information about the integrated full-stack todo application with aligned backend (FastAPI) and frontend (Next.js) components.

## Architecture
- **Backend**: FastAPI with Python 3.13+, SQLModel ORM, Neon Serverless PostgreSQL
- **Frontend**: Next.js 16.1 with App Router, Tailwind CSS, Shadcn UI
- **API Contract**: REST API with wrapped responses and camelCase field naming

## API Endpoints
All API endpoints are available under `/api/todos`:

- `GET /api/todos` - Retrieve all todos
- `POST /api/todos` - Create a new todo
- `GET /api/todos/{id}` - Get a specific todo
- `PUT /api/todos/{id}` - Update a todo
- `DELETE /api/todos/{id}` - Delete a todo
- `PATCH /api/todos/{id}/toggle` - Toggle completion status

## Data Format
- **IDs**: Converted from integers (backend) to strings (frontend)
- **Fields**: Translated from snake_case (backend) to camelCase (frontend)
- **Responses**: Wrapped in `{ "data": ... }` format for frontend compatibility
- **Timestamps**: ISO 8601 format (e.g., "2026-02-02T10:00:00")

## Integration Features
- Backend transforms data to match frontend expectations
- Frontend API client configured to use correct endpoints and handle wrapped responses
- Consistent error handling between components
- Proper HTTP status codes returned from all endpoints

## Running the Application

### Prerequisites
- Python 3.13+ with uv package manager
- Node.js 18+ with npm
- Neon Serverless PostgreSQL database (or local PostgreSQL)

### Backend Setup
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

### Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Set up environment variables
cp .env.local.example .env.local
# Edit .env.local with your backend API URL (default: http://localhost:8000)
```

### Running the Application
```bash
# Terminal 1: Start backend server
cd backend
source .venv/bin/activate
uv run -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Start frontend server
cd frontend
npm run dev
```

Access the application at http://localhost:3000

## Testing
Integration tests are available in `backend/tests/integration_tests.py` and can be run with:
```bash
cd backend
source .venv/bin/activate
python -m pytest tests/integration_tests.py -v
```

## Verification Script
Use the verification script to check the integration:
```bash
./scripts/verify-integration.sh
```

## Resolved Inconsistencies
- API endpoint paths aligned between frontend and backend
- Response format standardized to wrapped responses
- Field naming convention unified to camelCase for frontend
- ID type consistency with string IDs for frontend compatibility
- Error handling patterns synchronized between components

## Future Enhancements
- Authentication system implementation
- Enhanced error handling and retry mechanisms
- Performance optimizations and caching strategies