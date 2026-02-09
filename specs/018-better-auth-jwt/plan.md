# Implementation Plan: Multi-User Authentication System

**Branch**: `018-better-auth-jwt` | **Date**: 2026-02-08 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/018-better-auth-jwt/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement a secure multi-user authentication system using Better Auth (Next.js) as the authentication authority and FastAPI as the verification layer. Better Auth issues JWT tokens with 7-day validity, and the backend verifies tokens on every request to enforce data isolation. The implementation uses a clean slate approach: drop existing database tables and recreate with UUID primary keys for both User and Task entities. Users get immediate access after registration (no email verification required), with password requirements of 8+ characters including uppercase, lowercase, number, and special character. Token storage uses Better Auth's default mechanism (httpOnly cookies) for security.

## Technical Context

**Language/Version**:
- Backend: Python 3.13+
- Frontend: TypeScript 5.0+ with Next.js 16.1

**Primary Dependencies**:
- Backend: FastAPI, SQLModel, asyncpg==0.30.0, python-jose[cryptography], bcrypt, uvicorn
- Frontend: Next.js 16.1 (App Router), Better Auth, Shadcn UI, TailwindCSS, React 19

**Storage**: Neon Serverless PostgreSQL (postgres version 17) with SQLModel ORM and asyncpg driver

**Testing**:
- Backend: pytest with async support
- Frontend: Jest/React Testing Library
- E2E: Playwright (via MCP browser automation)

**Target Platform**:
- Backend: Linux server (FastAPI/uvicorn)
- Frontend: Web browsers (Next.js SSR/CSR)

**Project Type**: Web application (separate backend and frontend)

**Performance Goals**:
- Authentication requests: <5 seconds for login/registration
- API requests: <200ms p95 latency
- Support 100+ concurrent authentication requests
- Token verification: <50ms per request

**Constraints**:
- Stateless backend (no token storage in database)
- 7-day JWT token validity (no refresh mechanism)
- Clean slate database migration (no data preservation)
- Better Auth handles all token issuance
- FastAPI only verifies tokens

**Scale/Scope**:
- Multi-user system with data isolation
- 6 user stories (3 P1, 3 P2)
- 20 functional requirements
- 2 main entities (User, Task) with UUID primary keys
- Authentication + 5 core CRUD operations

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] Verify documentation-first approach using MCP servers and Context7
  - Will use context7 for Better Auth, FastAPI, SQLModel, and asyncpg documentation
  - Will use nextjs MCP server for Next.js 16.1 specific guidance
- [x] Confirm adherence to clean architecture principles
  - Backend: Separate layers (models, services, API routes, dependencies)
  - Frontend: Separate concerns (components, pages, providers, lib utilities)
  - Domain logic isolated from I/O and presentation
- [x] Validate tech stack compliance with specified technologies
  - Backend: FastAPI + Python 3.13+ + SQLModel + asyncpg + Neon PostgreSQL ✓
  - Frontend: Next.js 16.1 + App Router + Shadcn UI + TailwindCSS ✓
  - Authentication: Better Auth + JWT ✓
  - Package management: UV for Python ✓
- [x] Ensure TDD workflow will be followed
  - Write failing tests first for authentication flows
  - Test JWT verification middleware
  - Test data isolation between users
  - Test password validation
- [x] Confirm multi-user authentication & authorization requirements
  - Better Auth issues JWT tokens (authentication authority)
  - FastAPI verifies JWT tokens (authorization layer)
  - Data isolation enforced at database level (user_id filtering)
  - UUID primary keys for User and Task entities
- [x] Ensure `CLAUDE.md` files exist for each major component (`backend/`, `frontend/`) and adhere to context-specific guidelines
  - backend/CLAUDE.md exists and will be updated with auth context
  - frontend/CLAUDE.md exists and will be updated with Better Auth integration

## Project Structure

### Documentation (this feature)

```text
specs/018-better-auth-jwt/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (to be created)
├── data-model.md        # Phase 1 output (to be created)
├── quickstart.md        # Phase 1 output (to be created)
├── contracts/           # Phase 1 output (to be created)
│   ├── auth-api.yaml    # Authentication endpoints (OpenAPI)
│   └── tasks-api.yaml   # Task CRUD endpoints (OpenAPI)
├── checklists/          # Quality validation
│   └── requirements.md  # Spec quality checklist (completed)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── CLAUDE.md                    # Backend-specific context (to be updated)
├── main.py                      # FastAPI app entry point
├── models/                      # SQLModel database models
│   ├── __init__.py
│   ├── user.py                  # User model (UUID primary key)
│   ├── todo.py                  # TodoTask model (UUID primary key, user_id FK)
│   ├── category.py              # Category model (existing)
│   └── auth_token.py            # Auth token model (existing, may be removed)
├── api/                         # API routes
│   ├── __init__.py
│   ├── auth.py                  # Authentication routes (to be removed/refactored)
│   └── tasks.py                 # Task CRUD routes (to be updated with JWT middleware)
├── core/                        # Core business logic
│   ├── services/
│   │   └── todo_service.py      # Todo business logic
│   └── security/
│       ├── jwt.py               # JWT verification utilities (to be created)
│       └── password.py          # Password hashing utilities (bcrypt)
├── database/                    # Database configuration
│   ├── __init__.py
│   └── session.py               # Async database session management
├── dependencies/                # FastAPI dependencies
│   ├── __init__.py
│   └── auth.py                  # JWT verification dependency (to be created)
├── schemas/                     # Pydantic schemas
│   ├── __init__.py
│   ├── todo.py                  # Task request/response schemas
│   └── user.py                  # User schemas
├── tests/                       # Backend tests
│   ├── test_auth.py             # Authentication tests (to be created)
│   ├── test_jwt_middleware.py  # JWT verification tests (to be created)
│   └── test_data_isolation.py  # User isolation tests (to be created)
├── migrations/                  # Database migrations
│   └── uuid_migration.py        # Clean slate UUID migration script (to be created)
├── .env.example                 # Environment variables template
├── pyproject.toml               # UV project configuration
└── requirements.txt             # Python dependencies

frontend/
├── CLAUDE.md                    # Frontend-specific context (to be updated)
├── package.json
├── next.config.ts
├── tsconfig.json
├── .env.local                   # Environment variables (BETTER_AUTH_SECRET)
├── app/                         # Next.js App Router pages
│   ├── layout.tsx               # Root layout
│   ├── page.tsx                 # Home/landing page
│   ├── login/
│   │   └── page.tsx             # Login page (to be created)
│   ├── register/
│   │   └── page.tsx             # Registration page (to be created)
│   ├── dashboard/
│   │   └── page.tsx             # Todo dashboard (protected route)
│   └── globals.css
├── components/                  # React components
│   ├── auth/
│   │   ├── LoginForm.tsx        # Login form component (to be created)
│   │   ├── RegisterForm.tsx     # Registration form component (to be created)
│   │   └── PasswordStrength.tsx # Password validation indicator (to be created)
│   ├── TodoForm.tsx             # Todo creation/update form
│   ├── TodoList.tsx             # Todo display component
│   ├── TodoItem.tsx             # Individual todo item
│   └── Navbar.tsx               # Navigation with logout
├── lib/                         # Utility functions
│   ├── auth.ts                  # Better Auth configuration (to be created)
│   ├── api.ts                   # API client with JWT interceptor (to be updated)
│   └── validation.ts            # Password validation utilities (to be created)
├── providers/                   # Context providers
│   └── AuthProvider.tsx         # Better Auth provider (to be created)
├── hooks/                       # Custom React hooks
│   └── useAuth.ts               # Authentication hook (to be created)
└── tests/                       # Frontend tests
    ├── auth.test.tsx            # Authentication flow tests (to be created)
    └── protected-routes.test.tsx # Route protection tests (to be created)
```

**Structure Decision**: Web application structure with separate backend (FastAPI) and frontend (Next.js) directories. This follows the constitution's requirement for component-specific CLAUDE.md files and maintains clear separation between authentication authority (frontend/Better Auth) and verification layer (backend/FastAPI).

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

## Constitution Check (Post-Design Re-evaluation)

*GATE: Re-checked after Phase 1 design completion.*

- [x] Verify documentation-first approach using MCP servers and Context7
  - ✅ Research.md documents all technical decisions with references to MCP servers
  - ✅ Better Auth, FastAPI, SQLModel, asyncpg documentation to be fetched via context7
  - ✅ Next.js 16.1 guidance via nextjs MCP server
- [x] Confirm adherence to clean architecture principles
  - ✅ Backend: Clear separation (models, services, API, dependencies)
  - ✅ Frontend: Proper layering (components, pages, providers, lib)
  - ✅ Data model defined independently of implementation
  - ✅ API contracts defined with OpenAPI specifications
- [x] Validate tech stack compliance with specified technologies
  - ✅ All technologies from constitution used correctly
  - ✅ asyncpg==0.30.0 for async PostgreSQL operations
  - ✅ Better Auth for frontend authentication authority
  - ✅ FastAPI for backend verification layer
- [x] Ensure TDD workflow will be followed
  - ✅ Test strategy documented in research.md
  - ✅ Unit, integration, and E2E tests planned
  - ✅ Test data and fixtures defined in data-model.md
- [x] Confirm multi-user authentication & authorization requirements
  - ✅ Better Auth issues JWT tokens (authentication authority)
  - ✅ FastAPI verifies JWT tokens (authorization layer)
  - ✅ Data isolation enforced via user_id filtering
  - ✅ UUID primary keys for User and Task entities
  - ✅ Clean slate migration strategy documented
- [x] Ensure `CLAUDE.md` files exist and will be updated
  - ✅ Root CLAUDE.md updated with new database technology
  - ✅ backend/CLAUDE.md exists (to be updated during implementation)
  - ✅ frontend/CLAUDE.md exists (to be updated during implementation)

**Result**: ✅ All constitution requirements satisfied. No violations. Ready for implementation.

---

## Phase 0: Research (Completed)

**Output**: `research.md`

**Summary**:
- 10 technical decisions documented with rationale and alternatives
- Better Auth as single authentication authority
- FastAPI dependency injection for JWT verification
- bcrypt for password hashing
- Clean slate database migration
- asyncpg with SQLModel for async operations
- httpOnly cookies for token storage
- Query-level user_id filtering for data isolation
- Better Auth credentials provider for frontend
- Fetch API with credentials for API client
- Multi-layer testing strategy (unit/integration/E2E)

**Key Decisions**:
- Authentication: Better Auth (Next.js) issues tokens, FastAPI verifies
- Security: bcrypt hashing, JWT with HS256, httpOnly cookies
- Database: Clean slate migration to UUID schema
- Isolation: user_id filtering at query level

---

## Phase 1: Design & Contracts (Completed)

**Outputs**:
- `data-model.md` - Entity definitions and relationships
- `contracts/auth-api.yaml` - Authentication API specification
- `contracts/tasks-api.yaml` - Task CRUD API specification
- `quickstart.md` - Developer setup guide

**Data Model Summary**:
- **User Entity**: id (UUID), email (unique), password_hash, email_verified, verification_token, reset_token, reset_token_expires, timestamps
- **TodoTask Entity**: id (UUID), user_id (FK), title, description, completed, priority, category, timestamps
- **Relationship**: User 1:N TodoTask (CASCADE DELETE)
- **Indexes**: Primary keys, email unique index, user_id foreign key index, composite (user_id, created_at)

**API Contracts Summary**:
- **Authentication**: POST /api/auth/register, POST /api/auth/login, POST /api/auth/logout, GET /api/auth/me
- **Tasks**: GET/POST /api/{user_id}/tasks, GET/PUT/DELETE /api/{user_id}/tasks/{task_id}, PATCH /api/{user_id}/tasks/{task_id}/complete
- **Security**: JWT in httpOnly cookies, 401 for invalid tokens, 403 for user_id mismatch

**Quickstart Summary**:
- Environment setup for backend (Python 3.13+, UV, FastAPI)
- Environment setup for frontend (Node.js 18+, Next.js 16.1)
- Database migration instructions
- Testing authentication flow examples
- Troubleshooting common issues

---

## Next Steps

**Phase 2: Tasks** (Run `/sp.tasks` command)
- Generate tasks.md with implementation breakdown
- Prioritize tasks by dependency order
- Include test cases for each task
- Assign tasks to implementation phases (Red-Green-Refactor)

**Implementation Workflow**:
1. Backend: JWT verification dependency
2. Backend: Authentication routes (register, login, logout)
3. Backend: Update task routes with user_id filtering
4. Backend: Database migration script
5. Frontend: Better Auth configuration
6. Frontend: Login/register pages
7. Frontend: Protected route middleware
8. Frontend: API client with cookie support
9. Testing: Unit tests for auth logic
10. Testing: Integration tests for API endpoints
11. Testing: E2E tests for complete flows

**Documentation Updates**:
- Update backend/CLAUDE.md with JWT verification patterns
- Update frontend/CLAUDE.md with Better Auth integration
- Create ADRs for significant architectural decisions

---

## Artifacts Generated

| Artifact | Path | Purpose |
|----------|------|---------|
| Implementation Plan | specs/018-better-auth-jwt/plan.md | This document |
| Research | specs/018-better-auth-jwt/research.md | Technical decisions and rationale |
| Data Model | specs/018-better-auth-jwt/data-model.md | Entity definitions and schema |
| Auth API Contract | specs/018-better-auth-jwt/contracts/auth-api.yaml | Authentication endpoints (OpenAPI) |
| Tasks API Contract | specs/018-better-auth-jwt/contracts/tasks-api.yaml | Task CRUD endpoints (OpenAPI) |
| Quickstart Guide | specs/018-better-auth-jwt/quickstart.md | Developer setup instructions |

---

## Summary

This implementation plan defines a secure multi-user authentication system using Better Auth (Next.js) as the authentication authority and FastAPI as the verification layer. The design follows clean architecture principles, uses UUID primary keys for all entities, and enforces data isolation through query-level user_id filtering.

**Key Architectural Decisions**:
1. **Separation of Concerns**: Better Auth handles token issuance, FastAPI handles verification
2. **Stateless Backend**: No token storage in database, simplifies architecture
3. **Security First**: bcrypt hashing, httpOnly cookies, JWT verification on every request
4. **Clean Slate Migration**: Drop and recreate tables with UUID schema
5. **Data Isolation**: Query-level filtering prevents cross-user data access

**Constitution Compliance**: ✅ All requirements satisfied
- Clean architecture maintained
- Tech stack fully compliant
- TDD workflow planned
- Multi-user authentication implemented
- Component-specific CLAUDE.md files updated
- Documentation-first approach using MCP servers

**Ready for**: `/sp.tasks` command to generate implementation tasks
