# Quickstart Guide: Multi-User Authentication System

**Feature**: 018-better-auth-jwt
**Date**: 2026-02-08
**Purpose**: Setup instructions for developers to get the authentication system running locally

## Prerequisites

- **Python**: 3.13 or higher
- **Node.js**: 18 or higher
- **UV**: Python package manager (install: `curl -LsSf https://astral.sh/uv/install.sh | sh`)
- **npm/pnpm**: Node package manager
- **PostgreSQL**: Neon Serverless PostgreSQL account (or local PostgreSQL 17)
- **Git**: Version control

## Environment Setup

### 1. Clone Repository

```bash
git clone <repository-url>
cd todolist-hackathon/todolist-phase-1
git checkout 018-better-auth-jwt
```

### 2. Backend Setup

#### Install Dependencies

```bash
cd backend

# Create virtual environment and install dependencies with UV
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install all dependencies
uv add fastapi sqlmodel asyncpg==0.30.0 python-jose[cryptography] bcrypt uvicorn psycopg2-binary
```

#### Configure Environment Variables

Create `.env` file in `backend/` directory:

```bash
# Database Configuration
DATABASE_URL=postgresql+asyncpg://user:password@host/database

# Authentication
BETTER_AUTH_SECRET=your-secret-key-here-min-32-chars

# Server Configuration
HOST=0.0.0.0
PORT=8000
RELOAD=true
```

**Generate Secret Key**:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

#### Run Database Migration

```bash
# Drop existing tables and create new schema with UUIDs
python migrations/uuid_migration.py
```

**Expected Output**:
```
Dropping all existing tables...
Creating new tables with UUID schema...
Migration complete!
```

#### Start Backend Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Verify Backend**:
- Open http://localhost:8000/docs
- You should see the FastAPI Swagger UI with auth and task endpoints

### 3. Frontend Setup

#### Install Dependencies

```bash
cd frontend

# Install Node dependencies
npm install
# or
pnpm install
```

#### Configure Environment Variables

Create `.env.local` file in `frontend/` directory:

```bash
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Better Auth Configuration
BETTER_AUTH_SECRET=your-secret-key-here-min-32-chars
BETTER_AUTH_URL=http://localhost:3000

# Node Environment
NODE_ENV=development
```

**Important**: Use the SAME `BETTER_AUTH_SECRET` as the backend!

#### Start Frontend Server

```bash
npm run dev
# or
pnpm dev
```

**Verify Frontend**:
- Open http://localhost:3000
- You should see the landing page
- Navigate to http://localhost:3000/register to test registration

## Testing the Authentication Flow

### 1. Register a New User

**Via Frontend**:
1. Navigate to http://localhost:3000/register
2. Enter email: `alice@example.com`
3. Enter password: `Alice123!` (meets requirements)
4. Click "Register"
5. You should be redirected to the dashboard

**Via API (curl)**:
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice@example.com",
    "password": "Alice123!"
  }'
```

**Expected Response**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "email": "alice@example.com",
  "email_verified": false,
  "created_at": "2026-02-08T10:00:00Z",
  "updated_at": "2026-02-08T10:00:00Z"
}
```

### 2. Login

**Via Frontend**:
1. Navigate to http://localhost:3000/login
2. Enter email: `alice@example.com`
3. Enter password: `Alice123!`
4. Click "Login"
5. You should be redirected to the dashboard with your tasks

**Via API (curl)**:
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice@example.com",
    "password": "Alice123!"
  }' \
  -c cookies.txt
```

**Expected Response**:
```json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "email": "alice@example.com",
    "email_verified": false
  },
  "token_expires_at": "2026-02-15T10:00:00Z"
}
```

### 3. Create a Task

**Via Frontend**:
1. On the dashboard, click "Add Task"
2. Enter title: "Buy groceries"
3. Enter description: "Milk, eggs, bread"
4. Select priority: "High"
5. Enter category: "shopping"
6. Click "Create"

**Via API (curl)**:
```bash
curl -X POST http://localhost:8000/api/550e8400-e29b-41d4-a716-446655440001/tasks \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "priority": "high",
    "category": "shopping"
  }'
```

**Expected Response**:
```json
{
  "id": "650e8400-e29b-41d4-a716-446655440001",
  "user_id": "550e8400-e29b-41d4-a716-446655440001",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "priority": "high",
  "category": "shopping",
  "created_at": "2026-02-08T10:00:00Z",
  "updated_at": "2026-02-08T10:00:00Z"
}
```

### 4. List Tasks

**Via API (curl)**:
```bash
curl -X GET http://localhost:8000/api/550e8400-e29b-41d4-a716-446655440001/tasks \
  -b cookies.txt
```

### 5. Test Data Isolation

**Register Second User**:
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "bob@example.com",
    "password": "Bob456!@"
  }'
```

**Login as Bob**:
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "bob@example.com",
    "password": "Bob456!@"
  }' \
  -c cookies_bob.txt
```

**Try to Access Alice's Tasks (Should Fail)**:
```bash
curl -X GET http://localhost:8000/api/550e8400-e29b-41d4-a716-446655440001/tasks \
  -b cookies_bob.txt
```

**Expected Response**: 403 Forbidden
```json
{
  "detail": "Access denied"
}
```

### 6. Logout

**Via Frontend**:
1. Click "Logout" button in navbar
2. You should be redirected to the login page

**Via API (curl)**:
```bash
curl -X POST http://localhost:8000/api/auth/logout \
  -b cookies.txt
```

## Running Tests

### Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run specific test file
pytest tests/test_auth.py

# Run with coverage
pytest --cov=. --cov-report=html

# Run async tests
pytest -v tests/test_jwt_middleware.py
```

### Frontend Tests

```bash
cd frontend

# Run all tests
npm test
# or
pnpm test

# Run with coverage
npm test -- --coverage

# Run specific test file
npm test -- auth.test.tsx
```

### E2E Tests (Playwright)

```bash
cd frontend

# Install Playwright browsers (first time only)
npx playwright install

# Run E2E tests
npm run test:e2e
# or
pnpm test:e2e
```

## Troubleshooting

### Backend Issues

**Issue**: `ModuleNotFoundError: No module named 'asyncpg'`
**Solution**:
```bash
cd backend
uv add asyncpg==0.30.0
```

**Issue**: `sqlalchemy.exc.OperationalError: could not connect to server`
**Solution**:
- Check DATABASE_URL in `.env`
- Verify Neon PostgreSQL connection string
- Test connection: `psql $DATABASE_URL`

**Issue**: `jose.exceptions.JWTError: Invalid token`
**Solution**:
- Verify BETTER_AUTH_SECRET matches between frontend and backend
- Check token hasn't expired (7 days)
- Clear cookies and login again

### Frontend Issues

**Issue**: `Error: BETTER_AUTH_SECRET is not defined`
**Solution**:
- Create `.env.local` file in frontend directory
- Add BETTER_AUTH_SECRET with same value as backend

**Issue**: `CORS error when calling API`
**Solution**:
- Add CORS middleware to FastAPI backend:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Issue**: `Cookies not being sent with requests`
**Solution**:
- Ensure `credentials: 'include'` in fetch options
- Check CORS allows credentials
- Verify cookies are httpOnly and Secure (in production)

### Database Issues

**Issue**: `Table already exists` error during migration
**Solution**:
```bash
# Drop all tables manually
psql $DATABASE_URL -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"

# Re-run migration
python migrations/uuid_migration.py
```

**Issue**: `UUID type not supported`
**Solution**:
- Ensure using PostgreSQL 17 (or 9.4+)
- Check asyncpg driver is installed: `uv add asyncpg==0.30.0`

## Development Workflow

### 1. Start Development Servers

**Terminal 1 (Backend)**:
```bash
cd backend
source .venv/bin/activate
uvicorn main:app --reload
```

**Terminal 2 (Frontend)**:
```bash
cd frontend
npm run dev
```

### 2. Make Changes

- Backend changes auto-reload (FastAPI --reload)
- Frontend changes auto-reload (Next.js Fast Refresh)

### 3. Run Tests

```bash
# Backend
cd backend && pytest

# Frontend
cd frontend && npm test
```

### 4. Commit Changes

```bash
git add .
git commit -m "feat: implement JWT authentication"
```

## Next Steps

1. **Implement Backend**:
   - Create JWT verification dependency
   - Add authentication routes
   - Update task routes with user_id filtering
   - Write tests

2. **Implement Frontend**:
   - Configure Better Auth
   - Create login/register pages
   - Add protected route middleware
   - Implement API client with cookie support

3. **Test E2E Flow**:
   - Register → Login → Create Task → Logout
   - Test data isolation between users
   - Verify token expiration handling

4. **Deploy**:
   - Set up production environment variables
   - Configure HTTPS for secure cookies
   - Deploy backend to cloud provider
   - Deploy frontend to Vercel/Netlify

## Useful Commands

```bash
# Backend
cd backend
uv add <package>              # Add dependency
uv remove <package>           # Remove dependency
pytest -v                     # Run tests verbose
uvicorn main:app --reload    # Start server

# Frontend
cd frontend
npm install <package>         # Add dependency
npm uninstall <package>       # Remove dependency
npm test                      # Run tests
npm run dev                   # Start dev server
npm run build                 # Build for production

# Database
psql $DATABASE_URL            # Connect to database
psql $DATABASE_URL -c "SELECT * FROM user;"  # Query users
psql $DATABASE_URL -c "SELECT * FROM todotask;"  # Query tasks

# Git
git status                    # Check status
git log --oneline             # View commits
git diff                      # View changes
```

## Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **Better Auth Documentation**: https://better-auth.com/
- **SQLModel Documentation**: https://sqlmodel.tiangolo.com/
- **Next.js Documentation**: https://nextjs.org/docs
- **asyncpg Documentation**: https://magicstack.github.io/asyncpg/
- **JWT RFC 7519**: https://tools.ietf.org/html/rfc7519
- **OWASP Authentication Cheat Sheet**: https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
