# Quickstart Guide: Authentication System Fix

## Overview
This guide provides the necessary steps to set up and run the unified authentication system using Better Auth with JWT token integration for the FastAPI backend.

## Prerequisites
- Python 3.13+ installed
- Node.js 18+ and npm/yarn installed
- UV package manager installed
- PostgreSQL database (Neon Serverless recommended)
- Git for version control

## Backend Setup (FastAPI)

### 1. Clone and Navigate to Backend Directory
```bash
cd backend
```

### 2. Install Dependencies with UV
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install fastapi sqlmodel python-jose[cryptography] uvicorn bcrypt psycopg2-binary python-multipart python-dotenv
```

### 3. Environment Configuration
Create a `.env` file in the backend directory:
```env
DATABASE_URL=postgresql://username:password@localhost/dbname
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 4. Initialize Database
```bash
python -c "from database.init_db import create_db_and_tables; create_db_and_tables()"
```

### 5. Run Backend Server
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Frontend Setup (Next.js)

### 1. Navigate to Frontend Directory
```bash
cd frontend
```

### 2. Install Dependencies
```bash
npm install
# or
yarn install
# or
pnpm install
```

### 3. Environment Configuration
Create a `.env.local` file in the frontend directory:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000
AUTH_SECRET=your-auth-secret
```

### 4. Run Frontend Development Server
```bash
npm run dev
# or
yarn dev
# or
pnpm dev
```

## Better Auth Configuration

### 1. Frontend Setup
The frontend should be configured to use Better Auth for authentication. The authentication flow should:

- Integrate with the existing AuthProvider to use Better Auth tokens
- Handle JWT token storage and retrieval
- Implement proper token refresh mechanisms
- Ensure proper error handling for authentication failures

### 2. Backend Integration
The backend should be updated to:

- Accept JWT tokens from Better Auth
- Validate tokens using the appropriate verification mechanism
- Map Better Auth user IDs to the existing user model
- Maintain compatibility with existing API endpoints

## API Endpoints

### Authentication Endpoints
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `POST /auth/logout` - User logout
- `POST /auth/refresh` - Token refresh

### Protected Todo Endpoints
- `GET /api/{user_id}/tasks` - Get user's tasks
- `POST /api/{user_id}/tasks` - Create new task
- `GET /api/{user_id}/tasks/{id}` - Get specific task
- `PUT /api/{user_id}/tasks/{id}` - Update task
- `DELETE /api/{user_id}/tasks/{id}` - Delete task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle completion

## Running Tests

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Troubleshooting

### Common Issues:
1. **400 Bad Request on Registration**: Ensure request format matches expected schema
2. **JWT Token Mismatch**: Verify token signing algorithms match between frontend and backend
3. **CORS Issues**: Ensure backend allows requests from frontend origin
4. **Database Connection**: Verify DATABASE_URL is correctly configured

### Environment Variables:
- Ensure all required environment variables are set in both backend and frontend
- Use consistent API URLs between frontend and backend configurations
- Verify secret keys match between authentication systems

## Next Steps
1. Complete Better Auth integration in frontend
2. Update backend JWT verification to work with Better Auth tokens
3. Test authentication flow end-to-end
4. Verify error handling and response consistency