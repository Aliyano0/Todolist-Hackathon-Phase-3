# Quickstart: Better Auth Integration with FastAPI Backend

## Prerequisites

- Python 3.13+
- Node.js 18+
- UV package manager
- PostgreSQL (or Neon Serverless PostgreSQL)

## Setup

### 1. Clone and Install Dependencies

```bash
# Install Python dependencies
cd backend
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt

# Install frontend dependencies
cd ../frontend
npm install
```

### 2. Configure Environment Variables

Create `.env` files in both backend and frontend:

**Backend (.env)**:
```env
DATABASE_URL=postgresql://username:password@localhost/dbname
JWT_SECRET=your-shared-jwt-secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALLOWED_ORIGINS=http://localhost:3000
```

**Frontend (.env.local)**:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_JWT_SECRET=your-shared-jwt-secret
```

### 3. Initialize Better Auth

Install Better Auth in the frontend:

```bash
cd frontend
npm install better-auth
```

Configure Better Auth with the same JWT secret as the backend.

### 4. Run the Applications

**Backend**:
```bash
cd backend
uv run python -m main
```

**Frontend**:
```bash
cd frontend
npm run dev
```

## Key Integration Points

1. **JWT Secret**: Both Better Auth and FastAPI backend use the same JWT secret
2. **User ID Mapping**: Better Auth user IDs are used as primary keys in the backend database
3. **Token Flow**: Better Auth generates JWT tokens, which are validated by FastAPI backend
4. **Authorization Headers**: All API requests include Bearer tokens in the Authorization header

## Testing the Integration

1. Register a new user via the frontend registration form
2. Log in with the new account
3. Access protected API endpoints (should include valid JWT in headers)
4. Verify that user data is properly isolated