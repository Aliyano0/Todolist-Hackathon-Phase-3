# Quickstart Guide: Auth System Integration

## Overview
This guide provides instructions for setting up and running the authentication system with Better Auth, NextJS frontend, and FastAPI backend.

## Prerequisites
- Python 3.13+ installed
- Node.js 18+ installed
- PostgreSQL database (Neon Serverless recommended)
- UV package manager for Python dependencies

## Environment Setup

### Backend Environment
Create `.env` file in the `backend/` directory:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/auth_db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=43200  # 30 days in minutes
REFRESH_TOKEN_EXPIRE_DAYS=30
```

### Frontend Environment
Create `.env.local` file in the `frontend/` directory:
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_JWT_SECRET=your-jwt-secret
NEXTAUTH_URL=http://localhost:3000
```

## Backend Setup

### 1. Install Python Dependencies
```bash
cd backend
uv venv  # Create virtual environment
source .venv/bin/activate  # Activate virtual environment
uv pip install fastapi sqlmodel python-jose[cryptography] better-auth psycopg2-binary uvicorn
```

### 2. Initialize Database
```bash
# Run database migrations
python -m backend.database.init
```

### 3. Start Backend Server
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Frontend Setup

### 1. Install Node Dependencies
```bash
cd frontend
npm install
```

### 2. Start Frontend Development Server
```bash
cd frontend
npm run dev
```

## Authentication Flow

### User Registration
1. User visits `/register` page
2. User submits email, name, and password
3. Frontend validates input (8+ chars, uppercase, lowercase, number)
4. Request sent to backend `/api/auth/signup`
5. Backend creates user in database with hashed password
6. Backend generates JWT token
7. Frontend stores JWT token in secure manner
8. User redirected to dashboard

### User Login
1. User visits `/login` page
2. User submits email and password
3. Request sent to backend `/api/auth/login`
4. Backend verifies credentials
5. Backend generates JWT token
6. Frontend stores JWT token
7. User redirected to dashboard

### Protected Routes
1. Check for valid JWT token in local storage
2. If valid, allow access to protected route
3. If invalid/expired, redirect to login
4. Backend verifies JWT token on each protected API call

## API Endpoints

### Authentication Endpoints
- `POST /api/auth/signup` - Register new user
- `POST /api/auth/login` - Login existing user
- `POST /api/auth/logout` - Logout user
- `POST /api/auth/refresh` - Refresh JWT token

### Protected Endpoints
- `GET /api/user/profile` - Get user profile (requires valid JWT)
- `PUT /api/user/profile` - Update user profile (requires valid JWT)

## Error Handling

### Common Error Codes
- `400`: Bad Request (invalid input)
- `401`: Unauthorized (invalid credentials)
- `403`: Forbidden (insufficient permissions)
- `404`: Not Found (resource doesn't exist)
- `409`: Conflict (duplicate email)
- `500`: Internal Server Error (unexpected error)

### Error Response Format
```json
{
  "detail": "Error message",
  "error_code": "ERROR_CODE"
}
```

## Development Commands

### Backend Commands
```bash
# Run tests
python -m pytest

# Run with auto-reload
uvicorn main:app --reload

# Format code
black .

# Check types
mypy .
```

### Frontend Commands
```bash
# Run tests
npm test

# Build for production
npm run build

# Run linting
npm run lint

# Format code
npm run format
```

## Troubleshooting

### 503 Service Unavailable Error
- Check if the backend server is running
- Verify database connection
- Check if the authentication service is properly configured
- Look at backend logs for more details

### JWT Token Issues
- Verify SECRET_KEY is properly set in environment
- Check token expiration times
- Ensure proper token storage and retrieval

### Database Connection Issues
- Verify DATABASE_URL is properly set
- Check if PostgreSQL server is running
- Ensure proper database permissions