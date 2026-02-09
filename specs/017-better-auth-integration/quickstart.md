# Quickstart Guide: JWT-Based Authentication Integration

**Status**: Implemented

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
uv pip install -r requirements.txt  # Installs all dependencies including:
# - python-jose[cryptography] (JWT support)
# - passlib[bcrypt] (password hashing)
# - asyncpg (Neon PostgreSQL driver)
# - email-validator (email validation)

# Set up environment variables
cp .env.example .env
# Edit .env with your database connection string, JWT secrets, and optional SMTP settings
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

### 3. Database Setup
```bash
# In backend directory
python database/migrations.py  # Runs migrations including authentication_token table
```

## Running the Application

### 1. Start Backend Server
```bash
cd backend
source .venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
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
- Authentication endpoints: `backend/api/auth.py` (register, login, verify, reset, logout)
- Authentication dependencies: `backend/dependencies/auth.py` (JWT middleware)
- User model: `backend/models/user.py`
- Auth token model: `backend/models/auth_token.py` (for token storage and revocation)
- JWT utilities: `backend/core/security/jwt.py`
- Token service: `backend/core/services/token_service.py`
- Email service: `backend/core/services/email_service.py`
- Edge case handling: `backend/core/security/edge_cases.py`

### Frontend Configuration
- Main page: `frontend/app/page.tsx`
- Auth pages: `frontend/app/login/page.tsx`, `frontend/app/register/page.tsx`
- Auth components: `frontend/components/auth/` (LoginForm, RegisterForm, ProtectedRoute)
- Auth provider: `frontend/providers/AuthProvider.tsx` (custom React Context)
- API client: `frontend/lib/api.ts` (JWT token management)
- Environment: `frontend/.env.local`

## Authentication Flow
1. User registers with email/password (validated: 8+ chars, uppercase, lowercase, number, special char)
2. Email verification sent (24-hour token expiry, logged to console in dev mode)
3. User verifies email with token
4. User logs in and receives JWT tokens (access: 24h, refresh: 7d)
5. Tokens stored in localStorage and database (for revocation support)
6. Tokens attached to all API requests in Authorization header
7. User can access only their own tasks (user_id in path validated against JWT)
8. Token refresh with sliding expiration for seamless UX
9. Logout revokes tokens from database

## Testing
```bash
# Run backend tests (27 comprehensive authentication test cases)
cd backend
pytest tests/test_authentication.py -v
```

## Email Configuration (Optional)
For production email sending, configure SMTP settings in `.env`:
```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=noreply@todoapp.com
APP_URL=https://your-domain.com
```

In development mode (no SMTP configured), emails are logged to console.