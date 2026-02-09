# Implementation Plan: JWT-Based Authentication Integration

**Branch**: `017-better-auth-integration` | **Date**: 2026-02-04 | **Updated**: 2026-02-07 | **Status**: Implemented | **Spec**: [../specs/017-better-auth-integration/spec.md](../specs/017-better-auth-integration/spec.md)
**Input**: Feature specification from `/specs/017-better-auth-integration/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of comprehensive JWT-based authentication system for the todo application, including email/password authentication, secure API access with user isolation, token management, and proper session handling. The approach includes: 1) implementing custom JWT authentication on the FastAPI backend with token storage and revocation, 2) adding email verification and password reset functionality, 3) modifying API endpoints to filter data by authenticated user_id with path validation, 4) implementing frontend authentication with React Context and real-time validation, and 5) comprehensive security features including edge case handling and authentication event logging.

**Implementation Decision**: Instead of using the Better Auth library, a custom JWT-based authentication system was implemented in FastAPI. This provides better integration with the existing FastAPI backend, full control over authentication flows, and comprehensive security features including token revocation, email verification, and detailed logging.

## Technical Context

**Language/Version**: Python 3.13+ for backend, TypeScript 5.0+ for frontend
**Primary Dependencies**: FastAPI, SQLModel, Neon Serverless PostgreSQL (with asyncpg), Next.js 16.1+, python-jose[cryptography], passlib[bcrypt]
**Storage**: Neon Serverless PostgreSQL database with SQLModel ORM, includes authentication_token table for token management
**Testing**: pytest for backend (27 comprehensive test cases), Jest for frontend
**Target Platform**: Web application (Next.js 16.1+)
**Project Type**: Full-stack web application with comprehensive authentication and user isolation
**Performance Goals**: JWT token validation occurs in under 100 milliseconds per request, user registration/login completes within 5 seconds
**Constraints**: JWT tokens must be securely stored and transmitted, user data privacy maintained per regulations, authentication should not significantly impact performance, passwords must meet security requirements (8+ chars, uppercase, lowercase, number, special character)
**Scale/Scope**: Multi-user todo application with proper data isolation between users, token revocation support, email verification, and password reset functionality

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] Verify documentation-first approach using MCP servers and Context7
- [x] Confirm adherence to clean architecture principles
- [x] Validate tech stack compliance with specified technologies
- [x] Ensure TDD workflow will be followed
- [x] Confirm multi-user authentication & authorization requirements
- [x] Ensure `CLAUDE.md` files exist for each major component (`backend/`, `frontend/`) and adhere to context-specific guidelines

## Project Structure

### Documentation (this feature)

```text
specs/017-better-auth-integration/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── main.py
├── models/
│   ├── user.py                    # User model with authentication fields
│   ├── todo.py                    # TodoTask model with user_id
│   └── auth_token.py              # AuthenticationToken model for token storage
├── api/
│   ├── auth.py                    # Authentication endpoints (register, login, verify, reset, logout)
│   └── tasks.py                   # Task CRUD endpoints with user isolation
├── core/
│   ├── security/
│   │   ├── jwt.py                 # JWT token creation and validation
│   │   └── edge_cases.py          # Edge case handling and validation utilities
│   └── services/
│       ├── user_service.py        # User management and authentication logic
│       ├── todo_service.py        # Todo business logic with user filtering
│       ├── token_service.py       # Token storage and revocation management
│       └── email_service.py       # Email sending for verification and password reset
├── database/
│   ├── session.py                 # Database session with asyncpg
│   └── migrations.py              # Database migrations including auth_token table
├── dependencies/
│   └── auth.py                    # Authentication dependencies and middleware
├── schemas/
│   ├── user.py                    # User request/response schemas
│   └── todo.py                    # Todo request/response schemas
└── tests/
    ├── test_authentication.py     # 27 comprehensive authentication test cases
    └── test_todo_crud.py          # Todo CRUD tests

frontend/
├── app/
│   ├── page.tsx                   # Home page with authentication redirect
│   ├── login/
│   │   └── page.tsx               # Login page
│   ├── register/
│   │   └── page.tsx               # Registration page
│   ├── todos/
│   │   └── page.tsx               # Todo list page (protected)
│   └── profile/
│       └── page.tsx               # User profile page (protected)
├── components/
│   ├── auth/
│   │   ├── LoginForm.tsx          # Login form with validation
│   │   ├── RegisterForm.tsx       # Registration form with password strength
│   │   └── ProtectedRoute.tsx     # Route protection wrapper
│   ├── todo/
│   │   ├── TodoItem.tsx
│   │   ├── TodoForm.tsx
│   │   └── TodoList.tsx
│   ├── navigation/
│   │   └── Navbar.tsx             # Navigation with auth state
│   └── ui/                        # Shadcn UI components
├── providers/
│   └── AuthProvider.tsx           # Custom authentication context provider
├── hooks/
│   └── useTodos.ts
├── lib/
│   └── api.ts                     # API client with JWT token management
└── types/
    └── todo.ts

tests/
├── frontend/
│   ├── __tests__/
│   └── setup.ts
└── backend/
    ├── conftest.py
    ├── test_authentication.py     # Comprehensive auth test suite
    └── test_todo_crud.py
```

**Structure Decision**: Full-stack web application with comprehensive JWT-based authentication. Backend uses FastAPI with SQLModel ORM for database interactions, custom JWT middleware for authentication, token storage in database for revocation support, and email service for verification/password reset. Frontend uses Next.js with custom React Context for authentication state management, real-time validation, and JWT token handling in API requests.

## Phase 0: Research

### Technology Decisions

#### TD-001: Custom JWT Authentication Implementation
**Decision**: Implement custom JWT-based authentication in FastAPI instead of using Better Auth library
**Context**: Feature requires secure user authentication and JWT token management for API access with full control over authentication flows
**Options Considered**:
1. Better Auth library - designed for full-stack integration but primarily for Next.js/Node.js backends
2. Custom JWT authentication - full control, better FastAPI integration
3. Third-party auth provider (Auth0, Firebase) - external dependency, less control
**Option Chosen**: Custom JWT authentication with python-jose[cryptography] and passlib[bcrypt]
**Rationale**:
- Better Auth is designed for Node.js backends, not optimal for FastAPI
- Custom implementation provides full control over authentication flows
- Better integration with existing FastAPI architecture
- Enables comprehensive security features (token revocation, detailed logging, edge case handling)
- No external service dependencies
**Consequences**:
- More implementation work but better suited to FastAPI
- Full control over security features and authentication flows
- Easier to extend and customize for future requirements
- Comprehensive token management with database storage

#### TD-002: JWT Token Management with Database Storage
**Decision**: Implement refresh tokens with sliding expiration and database storage for revocation support
**Context**: Feature requires 24-hour access token expiration with refresh capabilities and ability to revoke tokens
**Options Considered**:
1. Short-lived tokens only - simple but poor UX
2. Refresh tokens with sliding expiration - balances security and UX
3. Long-lived tokens - security risk
4. Stateless JWT only - no revocation capability
5. JWT with database storage - enables revocation
**Option Chosen**: Refresh tokens (7-day expiry) with sliding expiration and database storage for both access and refresh tokens
**Rationale**:
- Sliding expiration provides seamless user experience
- Database storage enables token revocation for logout and security
- Access tokens (24h) balance security with performance
- Refresh tokens (7d) reduce login frequency
**Consequences**:
- More complex token management but better user experience and security
- Database queries for token validation (mitigated with proper indexing)
- Enables logout and logout-all-sessions functionality
- Supports security monitoring and audit trails

#### TD-003: Backend Authentication Middleware
**Decision**: Use python-jose[cryptography] for JWT verification in FastAPI
**Context**: Feature requires JWT token validation on backend API endpoints
**Option Considered**: python-jose vs. PyJWT vs. FastAPI's built-in security
**Option Chosen**: python-jose[cryptography] - well-maintained, supports required algorithms
**Consequences**: Secure token validation, additional dependency, proper error handling

### Security & Privacy

#### SP-001: User Data Isolation with Path Validation
**Decision**: Implement user_id filtering in all API endpoints with validation that path user_id matches JWT token
**Context**: Each user must only see/modify their own tasks, prevent unauthorized access via path manipulation
**Options Considered**:
1. No filtering - insecure
2. Client-side filtering - insecure
3. Server-side filtering by user_id - secure but could be bypassed
4. Server-side filtering with path validation - most secure
**Option Chosen**: Server-side filtering by user_id with validation that path user_id matches JWT token user_id
**Rationale**: Prevents users from accessing other users' data even if they modify the API path
**Consequences**: Secure data isolation, prevents unauthorized access, returns 403 Forbidden for mismatched user_id

#### SP-002: Password Security with Comprehensive Validation
**Decision**: Enforce password requirements: 8+ characters, 1 uppercase, 1 lowercase, 1 number, 1 special character
**Context**: Feature requires secure password handling with industry-standard requirements
**Options Considered**: Various complexity requirements from weak to very strong
**Option Chosen**: 8+ chars, uppercase, lowercase, number, special character - OWASP recommended
**Rationale**: Balances security with usability, prevents common weak passwords
**Consequences**: More secure passwords, better user security, validation on both frontend and backend

#### SP-003: Token Storage and Revocation
**Decision**: Store authentication tokens in database with revocation support
**Context**: Need ability to logout users and revoke compromised tokens
**Options Considered**:
1. Stateless JWT only - no revocation capability
2. JWT with blacklist - scales poorly
3. JWT with database storage - enables revocation
**Option Chosen**: Store hashed tokens in database with revocation flag
**Rationale**: Enables logout, logout-all-sessions, and security incident response
**Consequences**: Database queries for validation, but enables critical security features

#### SP-004: Email Verification Requirement
**Decision**: Require email verification before allowing login
**Context**: Prevent fake accounts and ensure valid email addresses
**Options Considered**: No verification vs. optional verification vs. required verification
**Option Chosen**: Required email verification with 24-hour token expiry
**Rationale**: Ensures valid email addresses, prevents spam accounts
**Consequences**: Additional step in registration flow, email service dependency

#### SP-005: Comprehensive Edge Case Handling
**Decision**: Implement validation utilities for all authentication edge cases
**Context**: Need robust error handling and security validation
**Implementation**: Created edge_cases.py with validation for email format, password strength, token format, user_id format, token age, etc.
**Rationale**: Prevents security vulnerabilities from malformed inputs
**Consequences**: More robust system, better error messages, comprehensive security

#### SP-006: Authentication Event Logging
**Decision**: Log all authentication events for security monitoring
**Context**: Need audit trail for security incidents and monitoring
**Implementation**: Comprehensive logging in all auth endpoints with masked email addresses
**Rationale**: Enables security monitoring, incident response, and compliance
**Consequences**: Increased log volume, but critical for security

## Phase 1: Design

### Data Model

#### DM-001: User Entity with Authentication Fields
**Decision**: Create User entity with comprehensive authentication fields
**Context**: Feature requires user accounts with email/password authentication, verification, and password reset
**Fields Implemented**:
- id (UUID, primary key)
- email (String, unique, indexed)
- password_hash (String, bcrypt hashed)
- email_verified (Boolean, default false)
- verification_token (String, nullable, for email verification)
- reset_token (String, nullable, for password reset)
- reset_token_expires (DateTime, nullable)
- created_at (DateTime)
- updated_at (DateTime)
**Option Chosen**: Extended user model with all authentication fields
**Rationale**: Supports complete authentication flow including verification and password reset
**Consequences**: Foundation for comprehensive authentication system, data storage requirements

#### DM-002: Task Entity Enhancement with User Ownership
**Decision**: Add user_id foreign key to existing TodoTask model for ownership tracking
**Context**: Feature requires user isolation of tasks
**Options Considered**:
1. Separate task tables per user - poor scalability
2. user_id field in existing TodoTask table - efficient
3. No isolation - insecure
**Option Chosen**: user_id field (UUID, foreign key to User.id, indexed) in existing TodoTask table
**Rationale**: Efficient data storage, proper ownership tracking, enables user isolation queries
**Consequences**: Requires database migration, all task queries must filter by user_id

#### DM-003: Authentication Token Entity
**Decision**: Create AuthenticationToken entity for token storage and revocation
**Context**: Need to track issued tokens for revocation support (logout, security incidents)
**Fields Implemented**:
- id (UUID, primary key)
- user_id (UUID, foreign key to User.id, indexed)
- token_type (String, enum: access|refresh)
- token_value (String, hashed SHA256)
- expires_at (DateTime)
- created_at (DateTime)
- revoked (Boolean, default false)
**Rationale**: Enables token revocation, logout functionality, and security monitoring
**Consequences**: Database queries for token validation, but enables critical security features

### API Contracts

#### AC-001: Comprehensive Authentication Endpoints
**Decision**: Implement complete set of authentication endpoints
**Context**: Feature requires full authentication lifecycle management
**Endpoints Implemented**:
- POST /api/auth/register - User registration with email verification
- POST /api/auth/login - User login returning JWT tokens
- POST /api/auth/verify-email - Email verification with token
- POST /api/auth/forgot-password - Request password reset
- POST /api/auth/reset-password - Reset password with token
- POST /api/auth/refresh - Refresh access token (sliding expiration)
- GET /api/auth/me - Get current user profile
- POST /api/auth/logout - Logout (revoke current token)
- POST /api/auth/logout-all - Logout from all sessions
**Rationale**: Complete authentication flow with all necessary operations
**Consequences**: Comprehensive API surface, proper authentication lifecycle management

#### AC-002: Protected Task Endpoints with User Isolation
**Decision**: Modify task endpoints to require JWT token and include user_id in path with validation
**Context**: Feature requires authenticated access to tasks with strict user isolation
**Pattern Implemented**: /api/{user_id}/tasks with JWT token in Authorization header
**Validation**: Path user_id must match JWT token user_id, returns 403 if mismatch
**Endpoints**:
- GET /api/{user_id}/tasks - List user's tasks
- POST /api/{user_id}/tasks - Create task for user
- PUT /api/{user_id}/tasks/{id} - Update user's task
- DELETE /api/{user_id}/tasks/{id} - Delete user's task
- PATCH /api/{user_id}/tasks/{id}/toggle - Toggle task completion
**Rationale**: Explicit user context in URL, prevents path manipulation attacks
**Consequences**: Changed API contract, secure access control, proper user isolation

### Architecture Decisions

#### AD-001: Authentication Layer Separation
**Decision**: Implement authentication as a separate layer using dependencies and middleware
**Context**: Feature requires consistent auth across multiple endpoints
**Option Considered**: Inline auth checks vs. dependency injection vs. middleware approach
**Option Chosen**: FastAPI dependencies for current user extraction
**Consequences**: Clean separation of concerns, reusable auth logic, testability

#### AD-002: Frontend API Integration
**Decision**: Update frontend API client to include JWT tokens in request headers
**Context**: Feature requires authenticated API calls from frontend
**Option Considered**: Manual header management vs. centralized client vs. interceptors
**Option Chosen**: Update existing ApiClient to automatically attach tokens
**Consequences**: Seamless auth integration, reduced client-side complexity, consistent behavior

## Phase 2: Implementation Strategy

The implementation will follow an incremental approach:
1. Set up authentication infrastructure (dependencies, models, schemas)
2. Implement backend authentication endpoints and middleware
3. Update task endpoints to enforce user isolation
4. Integrate Better Auth in frontend with JWT handling
5. Update frontend API client to use authentication
6. Test full authentication flow and user isolation

## Phase 3: Validation & Testing

Comprehensive testing approach including:
- Unit tests for authentication logic
- Integration tests for protected endpoints
- End-to-end tests for complete auth flow
- Security tests for user isolation
- Performance tests for token validation speed

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [N/A] | [No violations identified] | [All constitution requirements met] |
