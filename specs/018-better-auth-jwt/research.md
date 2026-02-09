# Research: Multi-User Authentication System

**Feature**: 018-better-auth-jwt
**Date**: 2026-02-08
**Purpose**: Document technical decisions, best practices, and alternatives for Better Auth + JWT authentication implementation

## Overview

This document captures research findings for implementing a secure multi-user authentication system using Better Auth (Next.js) as the authentication authority and FastAPI as the verification layer. All decisions prioritize security, simplicity, and alignment with the constitution's principles.

---

## 1. Authentication Architecture

### Decision: Better Auth as Single Authentication Authority

**Rationale**:
- Better Auth is a modern, TypeScript-first authentication library designed for Next.js
- Handles token issuance, session management, and security best practices automatically
- Reduces backend complexity by making it stateless (verification only)
- Aligns with "Simplicity First" principle - let specialized library handle auth complexity
- Provides built-in security features (CSRF protection, secure cookie handling)

**Alternatives Considered**:
- **Custom JWT implementation on backend**: Rejected because it duplicates logic, increases complexity, and requires maintaining two auth systems
- **NextAuth.js**: Rejected because Better Auth is more modern, has better TypeScript support, and simpler configuration
- **Backend-only auth (FastAPI issues tokens)**: Rejected because it violates the "Better Auth as authority" requirement and adds backend complexity

**Implementation Details**:
- Better Auth configured with credentials provider (email + password)
- JWT plugin enabled for token generation
- Tokens signed with HS256 algorithm using shared secret (BETTER_AUTH_SECRET)
- 7-day token expiry (604800 seconds)
- Token payload includes: sub (user_id as UUID string), email, exp

**References**:
- Better Auth documentation (to be fetched via context7 MCP)
- JWT RFC 7519 standard

---

## 2. JWT Token Verification (Backend)

### Decision: FastAPI Dependency Injection for JWT Verification

**Rationale**:
- FastAPI's dependency injection system provides clean, reusable middleware
- Allows centralized token verification logic
- Easy to test in isolation
- Follows clean architecture principles (separation of concerns)
- Enables fine-grained control over which routes require authentication

**Alternatives Considered**:
- **Global middleware**: Rejected because it applies to all routes (including health checks, docs)
- **Route-level decorators**: Rejected because FastAPI dependencies are more idiomatic and testable
- **Manual verification in each route**: Rejected due to code duplication and maintenance burden

**Implementation Details**:
- Create `dependencies/auth.py` with `get_current_user` dependency
- Dependency extracts JWT from Authorization header (Bearer scheme)
- Verifies signature using python-jose with BETTER_AUTH_SECRET
- Validates expiration timestamp
- Decodes user_id from `sub` claim
- Returns user_id (UUID) for use in route handlers
- Raises HTTPException(401) for invalid/missing tokens
- Raises HTTPException(403) for user_id mismatch with path parameter

**Code Pattern**:
```python
from fastapi import Depends, HTTPException, Header
from jose import jwt, JWTError
import uuid

async def get_current_user(authorization: str = Header(None)) -> uuid.UUID:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")

    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = uuid.UUID(payload.get("sub"))
        return user_id
    except (JWTError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid token")
```

**References**:
- FastAPI dependency injection documentation (via context7 MCP)
- python-jose library documentation

---

## 3. Password Security

### Decision: bcrypt for Password Hashing

**Rationale**:
- Industry standard for password hashing (OWASP recommended)
- Built-in salt generation (prevents rainbow table attacks)
- Adaptive cost factor (can increase difficulty as hardware improves)
- Resistant to brute-force attacks due to intentional slowness
- Well-tested and widely adopted in production systems

**Alternatives Considered**:
- **Argon2**: Rejected because bcrypt is simpler, more widely supported, and sufficient for this use case
- **PBKDF2**: Rejected because bcrypt is more resistant to GPU-based attacks
- **Plain SHA-256**: Rejected because it's too fast and vulnerable to brute-force

**Implementation Details**:
- Use bcrypt library with default cost factor (12 rounds)
- Hash passwords on registration before storing in database
- Verify passwords on login by comparing hashed values
- Never store or log plain-text passwords
- Password requirements: 8+ characters, uppercase, lowercase, number, special character

**Code Pattern**:
```python
import bcrypt

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
```

**References**:
- OWASP Password Storage Cheat Sheet
- bcrypt library documentation

---

## 4. Database Schema Migration

### Decision: Clean Slate Migration (Drop and Recreate)

**Rationale**:
- Development environment allows data loss
- Simplifies migration from integer IDs to UUIDs (no complex data transformation)
- Removes old authentication tables/fields that are no longer needed
- Ensures schema consistency with new design
- Faster to implement than data-preserving migration
- Aligns with "Simplicity First" principle

**Alternatives Considered**:
- **Data-preserving migration**: Rejected because it adds complexity, requires mapping integer IDs to UUIDs, and this is a development environment
- **Dual-write strategy**: Rejected because it's overly complex for a development migration
- **Manual SQL scripts**: Rejected in favor of SQLModel's create_all() for consistency

**Implementation Details**:
- Create migration script: `migrations/uuid_migration.py`
- Drop all existing tables (User, TodoTask, Category, AuthToken, etc.)
- Recreate tables with UUID primary keys using SQLModel
- User table: id (UUID), email (unique), password_hash, email_verified, verification_token, reset_token, reset_token_expires, created_at, updated_at
- TodoTask table: id (UUID), user_id (UUID FK), title, description, completed, priority, category, created_at, updated_at
- Add indexes on user_id for performance
- Document migration in quickstart.md

**Code Pattern**:
```python
from sqlmodel import SQLModel, create_engine
from models import User, TodoTask

# Drop all tables
SQLModel.metadata.drop_all(engine)

# Create all tables with new schema
SQLModel.metadata.create_all(engine)
```

**References**:
- SQLModel documentation (via context7 MCP)
- PostgreSQL UUID best practices

---

## 5. Async Database Operations

### Decision: SQLModel with asyncpg Driver

**Rationale**:
- asyncpg is the fastest PostgreSQL driver for Python
- SQLModel provides clean ORM interface with Pydantic integration
- Async operations prevent blocking on database I/O
- Neon Serverless PostgreSQL requires async driver for optimal performance
- Aligns with FastAPI's async capabilities

**Alternatives Considered**:
- **psycopg2 (sync)**: Rejected because it blocks the event loop and reduces concurrency
- **psycopg3 (async)**: Rejected because asyncpg has better performance and wider adoption
- **Raw SQL with asyncpg**: Rejected because SQLModel provides type safety and reduces boilerplate

**Implementation Details**:
- Install asyncpg==0.30.0 (specific version for compatibility)
- Use `create_async_engine` from SQLModel
- Create `AsyncSession` for database operations
- All route handlers use `async def`
- Database queries use `await session.exec(statement)`
- Connection string format: `postgresql+asyncpg://user:pass@host/db`

**Code Pattern**:
```python
from sqlmodel import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_session():
    async with async_session() as session:
        yield session
```

**References**:
- SQLModel async documentation (via context7 MCP)
- asyncpg documentation
- Neon PostgreSQL async best practices

---

## 6. Token Storage (Frontend)

### Decision: Better Auth Default Mechanism (httpOnly Cookies)

**Rationale**:
- httpOnly cookies are immune to XSS attacks (JavaScript cannot access them)
- Automatically sent with every request (no manual header management)
- Better Auth handles cookie security (Secure flag, SameSite attribute)
- Simplifies frontend code (no manual token storage/retrieval)
- Aligns with "let Better Auth handle it" principle

**Alternatives Considered**:
- **localStorage**: Rejected because it's vulnerable to XSS attacks
- **sessionStorage**: Rejected because tokens don't persist across tabs and are still XSS-vulnerable
- **Memory only**: Rejected because tokens are lost on page refresh

**Implementation Details**:
- Better Auth automatically stores tokens in httpOnly cookies
- Cookies have Secure flag (HTTPS only) in production
- SameSite=Lax prevents CSRF attacks
- 7-day expiration matches JWT token expiry
- Frontend doesn't need to manually manage tokens
- API client automatically includes cookies in requests

**Security Considerations**:
- HTTPS required in production (assumed in constitution)
- CORS configuration must allow credentials
- Backend must validate Origin header

**References**:
- Better Auth cookie configuration (via context7 MCP)
- OWASP Session Management Cheat Sheet

---

## 7. Data Isolation Strategy

### Decision: User ID Filtering at Query Level

**Rationale**:
- Enforces data isolation at the database layer (defense in depth)
- Prevents accidental cross-user data leakage
- Simple to implement (add WHERE user_id = ? to all queries)
- Testable (can verify isolation with integration tests)
- Aligns with "Simplicity First" principle

**Alternatives Considered**:
- **Row-level security (RLS) in PostgreSQL**: Rejected because it adds database complexity and is harder to test
- **Separate databases per user**: Rejected because it's overly complex and doesn't scale
- **Application-level filtering only**: Rejected because it's error-prone (easy to forget)

**Implementation Details**:
- All TodoTask queries include `WHERE user_id = authenticated_user_id`
- FastAPI dependency extracts user_id from JWT
- Route handlers receive user_id as parameter
- Validate path user_id matches JWT user_id (403 if mismatch)
- Database foreign key constraint ensures referential integrity
- Index on user_id for query performance

**Code Pattern**:
```python
@router.get("/api/{user_id}/tasks")
async def get_tasks(
    user_id: uuid.UUID,
    current_user: uuid.UUID = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    if user_id != current_user:
        raise HTTPException(status_code=403, detail="Access denied")

    statement = select(TodoTask).where(TodoTask.user_id == current_user)
    results = await session.exec(statement)
    return results.all()
```

**References**:
- FastAPI security best practices (via context7 MCP)
- OWASP Access Control Cheat Sheet

---

## 8. Frontend Authentication Flow

### Decision: Better Auth with Credentials Provider

**Rationale**:
- Credentials provider supports email/password authentication
- Better Auth handles form validation, error messages, and loading states
- Provides React hooks for easy integration (useSession, useSignIn, useSignUp)
- Automatic redirect to login for protected routes
- Aligns with Next.js 16.1 App Router patterns

**Alternatives Considered**:
- **Custom form handling**: Rejected because Better Auth provides better UX and security
- **Third-party OAuth only**: Rejected because it's out of scope (phase 3 feature)
- **Server-side only auth**: Rejected because it doesn't work with App Router's client components

**Implementation Details**:
- Configure Better Auth in `lib/auth.ts`
- Create AuthProvider wrapping app in `app/layout.tsx`
- Login page: `app/login/page.tsx` with LoginForm component
- Register page: `app/register/page.tsx` with RegisterForm component
- Protected routes check session and redirect if unauthenticated
- Password validation component shows strength indicator
- Error messages displayed inline with form fields

**Code Pattern**:
```typescript
// lib/auth.ts
import { betterAuth } from "better-auth";

export const auth = betterAuth({
  providers: {
    credentials: {
      enabled: true,
    },
  },
  jwt: {
    secret: process.env.BETTER_AUTH_SECRET,
    expiresIn: "7d",
  },
});

// app/login/page.tsx
import { useSignIn } from "better-auth/react";

export default function LoginPage() {
  const { signIn, isPending, error } = useSignIn();

  const handleSubmit = async (e) => {
    await signIn({ email, password });
  };

  return <LoginForm onSubmit={handleSubmit} />;
}
```

**References**:
- Better Auth documentation (via context7 MCP)
- Next.js 16.1 App Router authentication patterns (via nextjs MCP)

---

## 9. API Client Configuration

### Decision: Fetch with Automatic Cookie Inclusion

**Rationale**:
- Fetch API automatically includes cookies when credentials: 'include' is set
- No need for manual Authorization header management
- Works seamlessly with Better Auth's cookie-based tokens
- Simple to configure and maintain

**Alternatives Considered**:
- **Axios with interceptors**: Rejected because fetch is built-in and sufficient
- **Manual header management**: Rejected because cookies are automatic
- **GraphQL client**: Rejected because REST is simpler for this use case

**Implementation Details**:
- Create API client utility in `lib/api.ts`
- Configure fetch with credentials: 'include'
- Base URL points to FastAPI backend
- Error handling for 401 (redirect to login) and 403 (show error)
- Type-safe request/response with TypeScript

**Code Pattern**:
```typescript
// lib/api.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function apiRequest<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    credentials: 'include', // Include cookies
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
  });

  if (response.status === 401) {
    // Redirect to login
    window.location.href = '/login';
  }

  if (!response.ok) {
    throw new Error(`API error: ${response.statusText}`);
  }

  return response.json();
}
```

**References**:
- Fetch API documentation
- Next.js API routes best practices (via nextjs MCP)

---

## 10. Testing Strategy

### Decision: Multi-Layer Testing Approach

**Rationale**:
- Unit tests for isolated logic (password hashing, JWT verification)
- Integration tests for API endpoints with database
- E2E tests for complete authentication flows
- Aligns with TDD workflow in constitution

**Test Coverage**:

**Backend Unit Tests**:
- Password hashing and verification
- JWT token generation and validation
- User model validation
- Task model validation

**Backend Integration Tests**:
- User registration endpoint
- User login endpoint
- JWT verification dependency
- Data isolation (user A cannot access user B's tasks)
- Token expiration handling
- Invalid token handling

**Frontend Unit Tests**:
- LoginForm component
- RegisterForm component
- Password validation logic
- API client error handling

**E2E Tests (Playwright)**:
- Complete registration flow
- Complete login flow
- Protected route access
- Logout flow
- Cross-user access prevention
- Token expiration and re-login

**Implementation Details**:
- Backend: pytest with pytest-asyncio for async tests
- Frontend: Jest + React Testing Library
- E2E: Playwright via MCP browser automation
- Test database: Separate test instance or in-memory SQLite
- Fixtures for test users and tasks
- Mock JWT tokens for unit tests

**References**:
- pytest documentation
- FastAPI testing documentation (via context7 MCP)
- Next.js testing documentation (via nextjs MCP)

---

## Summary of Key Decisions

| Area | Decision | Primary Rationale |
|------|----------|-------------------|
| Auth Authority | Better Auth (Next.js) | Specialized library, handles complexity, security best practices |
| Backend Role | JWT Verification Only | Stateless, simple, aligns with Better Auth authority model |
| Password Hashing | bcrypt | Industry standard, OWASP recommended, resistant to attacks |
| Database Migration | Clean Slate (Drop/Recreate) | Development environment, simplifies UUID migration |
| Database Driver | asyncpg with SQLModel | Best performance, async support, type safety |
| Token Storage | httpOnly Cookies (Better Auth default) | XSS protection, automatic inclusion, secure |
| Data Isolation | Query-level user_id filtering | Simple, testable, defense in depth |
| Frontend Auth | Better Auth Credentials Provider | Built-in validation, hooks, App Router compatible |
| API Client | Fetch with credentials: 'include' | Built-in, automatic cookies, simple |
| Testing | Multi-layer (Unit/Integration/E2E) | Comprehensive coverage, TDD workflow |

---

## Next Steps

1. **Phase 1: Design & Contracts**
   - Create data-model.md with User and Task entity definitions
   - Generate OpenAPI contracts for auth and task endpoints
   - Create quickstart.md with setup instructions
   - Update backend/CLAUDE.md and frontend/CLAUDE.md with auth context

2. **Phase 2: Tasks**
   - Generate tasks.md with implementation breakdown
   - Prioritize tasks by dependency order
   - Include test cases for each task

3. **Implementation**
   - Follow TDD workflow (Red-Green-Refactor)
   - Start with backend JWT verification
   - Then frontend Better Auth integration
   - Finally, data isolation and E2E tests
