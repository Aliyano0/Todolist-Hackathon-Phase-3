---
id: 0001
title: Multi-User Auth Specification
stage: spec
date: 2026-02-08
surface: agent
model: claude-sonnet-4-5
feature: 018-better-auth-jwt
branch: 018-better-auth-jwt
user: user
command: /sp.specify
labels: ["authentication", "specification", "multi-user", "jwt", "better-auth"]
links:
  spec: specs/018-better-auth-jwt/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/018-better-auth-jwt/spec.md
  - specs/018-better-auth-jwt/checklists/requirements.md
tests:
  - No tests run (specification phase)
---

## Prompt

Phase 2c — Authentication (Better Auth + JWT, Fully Aligned)

Using:
- Phase 2a backend in /backend
- Phase 2b frontend in /frontend
- Each with its own CLAUDE.md for scoped context

--------------------------------------------------
Step 0 — Clean Slate (Required)
--------------------------------------------------
Remove all existing authentication-related code from both frontend and backend:
- Backend: models, routes, middleware, dependencies, helpers
- Frontend: auth state, interceptors, UI, config
Start with no authentication assumptions.

--------------------------------------------------
Auth Model (Single Source of Truth)
--------------------------------------------------
- Better Auth (Next.js) is the ONLY authentication authority.
- Better Auth issues JWT tokens on user login.
- FastAPI NEVER issues tokens.
- FastAPI ONLY verifies JWT tokens.
- Authentication is fully stateless on the backend.

--------------------------------------------------
JWT Configuration
--------------------------------------------------
- Token type: JWT (JSON Web Token)
- Issuer: Better Auth
- Signing algorithm: HS256
- Expiry: ~7 days
- Payload MUST include:
  - sub: user_id (UUID as string)
  - email
  - exp

--------------------------------------------------
Shared Secret
--------------------------------------------------
Both services MUST use the same secret:

Environment variable:
- BETTER_AUTH_SECRET

Used by:
- Frontend (Better Auth) → sign JWT
- Backend (FastAPI) → verify JWT

--------------------------------------------------
Frontend (Next.js 16+, App Router)
--------------------------------------------------
- Configure Better Auth with:
  - Credentials provider (email + password)
  - JWT plugin enabled
- Better Auth manages:
  - Login
  - Logout
  - Session state
  - JWT issuance

--------------------------------------------------
Frontend API Client Behavior
--------------------------------------------------
- Attach JWT token to EVERY API request:
  Authorization: Bearer <JWT>
- Protect routes:
  - Todo app
  - Profile
- Redirect unauthenticated users to login page
- No refresh token flow required

--------------------------------------------------
Backend (FastAPI + Async SQLModel)
--------------------------------------------------
- Database: Neon Serverless PostgreSQL
- Driver: asyncpg==0.30.0
- ORM: SQLModel (async)

--------------------------------------------------
Data Models (UUID Everywhere)
--------------------------------------------------
User Model:
- id: UUID (primary key, default=uuid.uuid4)
- email: str (unique, indexed)

Task Model:
- id: UUID (primary key)
- user_id: UUID (foreign key → User.id, indexed)
- title, completed, etc.

--------------------------------------------------
JWT Verification Middleware (Critical)
--------------------------------------------------
For all /api routes:

1. Extract JWT from:
   Authorization: Bearer <token>

2. Verify:
   - Signature using BETTER_AUTH_SECRET
   - Token expiry

3. Decode payload:
   - Extract user_id from `sub`

4. Authorization rules:
   - If token missing or invalid → 401 Unauthorized
   - If token user_id != {user_id} in URL → 403 Forbidden

5. Attach authenticated user_id to request context

--------------------------------------------------
API Endpoints (UNCHANGED)
--------------------------------------------------
GET    /api/{user_id}/tasks
POST   /api/{user_id}/tasks
GET    /api/{user_id}/tasks/{id}
PUT    /api/{user_id}/tasks/{id}
DELETE /api/{user_id}/tasks/{id}
PATCH  /api/{user_id}/tasks/{id}/complete

--------------------------------------------------
Data Isolation Rules (Mandatory)
--------------------------------------------------
- Every task is owned by exactly one user (user_id FK)
- ALL queries MUST filter by authenticated user_id
- Cross-user access must always fail

--------------------------------------------------
API Behavior After Auth
--------------------------------------------------
- All endpoints require a valid JWT
- Requests without JWT → 401 Unauthorized
- Users can only read/write their own tasks
- Backend remains stateless

--------------------------------------------------
Testing Checklist (Required)
--------------------------------------------------
- Login via Better Auth
- JWT issued by Better Auth
- JWT attached to API requests
- Backend successfully verifies JWT
- Create/list/update/delete tasks (own user)
- Attempt cross-user access → fails
- Access without JWT → 401
- Full end-to-end auth flow validated

## Response snapshot

Created comprehensive specification for multi-user authentication system on branch 018-better-auth-jwt.

**Specification includes:**
- 6 prioritized user stories (P1-P2) covering registration, login, data access, session management, logout, and security
- 18 functional requirements defining system capabilities
- 10 measurable, technology-agnostic success criteria
- 10 edge cases identified
- Clear scope boundaries with dependencies, assumptions, and exclusions

**Validation:**
- Created quality checklist at specs/018-better-auth-jwt/checklists/requirements.md
- All 16 checklist items passed validation
- No [NEEDS CLARIFICATION] markers needed
- Specification is ready for planning phase

**Key design decisions captured:**
- Multi-user system with email/password authentication
- 7-day token validity period
- Stateless authentication on backend
- Data isolation enforced at database level
- Clear separation between authentication (frontend) and authorization (backend)

## Outcome

- ✅ Impact: Created complete, validated specification for multi-user authentication system with 6 user stories, 18 requirements, and 10 success criteria
- 🧪 Tests: No tests run (specification phase only)
- 📁 Files: Created 2 files (spec.md, requirements.md checklist)
- 🔁 Next prompts: /sp.clarify (optional) or /sp.plan (recommended next step)
- 🧠 Reflection: Specification successfully avoided implementation details while remaining concrete and testable. All requirements are technology-agnostic and measurable. No clarifications needed due to clear user input.

## Evaluation notes (flywheel)

- Failure modes observed: None - specification completed successfully on first attempt
- Graders run and results (PASS/FAIL): Quality checklist validation - PASS (16/16 items)
- Prompt variant (if applicable): Standard /sp.specify workflow
- Next experiment (smallest change to try): Proceed to /sp.plan to create architectural design
