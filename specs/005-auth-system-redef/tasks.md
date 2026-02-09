# Implementation Tasks: Better Auth Integration with FastAPI Backend

**Feature**: 005-auth-system-redef | **Date**: 2026-01-27 | **Spec**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md)

## Implementation Strategy

This implementation follows a phased approach with independent user story delivery. Each user story builds upon the foundational components and delivers complete, testable functionality.

- **MVP Scope**: User Story 1 (New User Registration) with basic authentication
- **Incremental Delivery**: Each user story adds complete functionality
- **Parallel Opportunities**: Backend and frontend components can be developed in parallel
- **Testability**: Each story includes independent test criteria

## Phase 1: Setup

Initial project setup and dependency installation for both backend and frontend.

- [X] T001 Create backend/better-auth-server.ts with proper configuration
- [X] T002 Update backend requirements.txt with Better Auth dependencies
- [X] T003 Update frontend package.json with Better Auth dependencies
- [X] T004 Create shared environment variable configuration for JWT secret

## Phase 2: Foundational Components

Core infrastructure components required by all user stories.

- [X] T005 [P] Create backend/models/user.py with User SQLModel based on data model
- [X] T006 [P] Create backend/models/token.py with AuthenticationToken SQLModel based on data model
- [X] T007 [P] Create backend/schemas/auth.py with authentication request/response schemas
- [X] T008 [P] Update backend/schemas/user.py with user schemas
- [X] T009 [P] Create backend/core/services/user_service.py with user business logic
- [X] T010 [P] Update backend/core/security/jwt.py with shared JWT utilities using shared secret
- [X] T011 [P] Create frontend/lib/better-auth-client.ts with Better Auth client configuration
- [X] T012 [P] Create frontend/types/auth.ts with authentication-related TypeScript types
- [X] T013 [P] Update backend/api/better_auth.py with authentication route handlers
- [X] T014 [P] Update frontend/lib/api.ts with Better Auth compatible API client

## Phase 3: User Story 1 - New User Registration (P1)

As a new user, I want to register for an account using the Better Auth system so that I can create and manage my personal todos with secure authentication.

**Goal**: Enable new user registration through Better Auth with proper validation and user creation in backend database.

**Independent Test**: A new user should be able to fill out the registration form with valid credentials through the Better Auth client, successfully create an account, and receive appropriate feedback upon success or failure.

**Acceptance Scenarios**:
1. Given a new user visits the registration page, when they submit valid credentials (email, password) via Better Auth client, then they should receive a success message and be redirected to the main todo dashboard
2. Given a user submits invalid registration data (missing fields, invalid email format), when they submit via Better Auth client, then they should receive clear error messages indicating what needs to be corrected

- [X] T015 [US1] Create frontend/src/app/register/page.tsx with registration page using Better Auth
- [X] T016 [P] [US1] Create frontend/src/components/RegistrationForm.tsx with Better Auth integration
- [X] T017 [P] [US1] Update backend/api/better_auth.py with sign-up endpoint implementation
- [X] T018 [P] [US1] Implement user creation in backend/core/services/user_service.py with Better Auth ID mapping
- [X] T019 [P] [US1] Create frontend/src/lib/auth.ts with registration utility functions
- [X] T020 [P] [US1] Test registration flow with valid credentials
- [X] T021 [P] [US1] Test registration flow with invalid credentials and error handling

## Phase 4: User Story 2 - User Login and Session Management (P1)

As a registered user, I want to be able to securely log into my account using Better Auth and maintain my session so that I can access my todos consistently across visits.

**Goal**: Enable secure login and session management using Better Auth with proper token handling.

**Independent Test**: A registered user should be able to log in with their credentials through Better Auth, receive appropriate authentication tokens, and maintain access to protected resources until logout or session expiration.

**Acceptance Scenarios**:
1. Given a registered user enters valid login credentials via Better Auth client, when they submit the login form, then they should be authenticated and granted access to protected todo functionality
2. Given a user attempts to access protected resources without valid authentication, when they navigate to protected routes, then they should be redirected to the login page

- [X] T022 [US2] Create frontend/src/app/login/page.tsx with login page using Better Auth
- [X] T023 [P] [US2] Create frontend/src/components/LoginForm.tsx with Better Auth integration
- [X] T024 [P] [US2] Update backend/api/better_auth.py with sign-in endpoint implementation
- [X] T025 [P] [US2] Update backend/core/services/user_service.py with authentication logic
- [X] T026 [P] [US2] Create frontend/src/providers/AuthProvider.tsx with authentication context
- [X] T027 [P] [US2] Update frontend/src/lib/auth.ts with login and session management utilities
- [X] T028 [P] [US2] Test login flow with valid credentials
- [X] T029 [P] [US2] Test authentication failure handling

## Phase 5: User Story 3 - Secure API Access with JWT Tokens (P1)

As a user of the todo web app, I expect that my authentication tokens work seamlessly with the FastAPI backend to access protected API routes without conflicts or errors.

**Goal**: Enable API requests to be properly authenticated using Better Auth JWT tokens validated by FastAPI backend.

**Independent Test**: API requests with Better Auth JWT tokens should be properly validated by the FastAPI backend without authentication errors.

**Acceptance Scenarios**:
1. Given a user is authenticated with Better Auth, when they make API requests to the FastAPI backend, then the requests should be properly authenticated using the JWT token
2. Given a user has an expired or invalid JWT token, when they make API requests to the FastAPI backend, then they should receive appropriate error responses and be prompted to re-authenticate

- [X] T030 [US3] Update backend/dependencies/auth.py with JWT token validation dependency using shared secret
- [X] T031 [P] [US3] Update backend/api/todos.py to use JWT authentication for all endpoints
- [X] T032 [P] [US3] Create frontend/src/lib/api.ts with authenticated API request utilities using Bearer tokens
- [X] T033 [P] [US3] Update frontend/src/components/TodoList.tsx to use authenticated API calls
- [X] T034 [P] [US3] Update frontend/src/components/TodoForm.tsx to use authenticated API calls
- [X] T035 [P] [US3] Create centralized error handler in frontend for authentication failures
- [X] T036 [P] [US3] Test API access with valid JWT tokens
- [X] T037 [P] [US3] Test API access with invalid/expired JWT tokens and error handling

## Phase 6: User Story 4 - Better Auth and FastAPI Integration (P2)

As a developer, I want the authentication system to be cleanly separated between Better Auth (frontend) and FastAPI (backend) so that both systems work harmoniously without conflicts.

**Goal**: Complete integration of Better Auth frontend authentication with FastAPI backend validation using shared JWT secret.

**Independent Test**: Better Auth handles user sessions on the frontend while FastAPI validates JWT tokens on the backend without duplication or conflicts.

**Acceptance Scenarios**:
1. Given the Better Auth system is properly configured, when a user performs authentication actions, then the frontend should use Better Auth client while the backend validates JWT tokens appropriately
2. Given API requests include Better Auth JWT tokens, when they reach the FastAPI backend, then they should be validated using the same secret/key as Better Auth

- [X] T038 [US4] Update backend/main.py to include Better Auth compatible routes and JWT validation
- [X] T039 [P] [US4] Create backend/api/better_auth.py with sign-out and refresh endpoints
- [X] T040 [P] [US4] Implement token refresh mechanism in frontend with silent background refresh
- [X] T041 [P] [US4] Update backend/core/security/jwt.py with token refresh functionality
- [X] T042 [P] [US4] Create frontend/src/components/ProtectedRoute.tsx with authentication guard
- [X] T043 [P] [US4] Test complete authentication flow from registration to protected API access
- [X] T044 [P] [US4] Test token refresh functionality during active sessions
- [X] T045 [P] [US4] Test logout functionality clearing both Better Auth session and local storage
- [X] T046 [P] [US4] Implement silent background token refresh mechanism in frontend

## Phase 7: Polish & Cross-Cutting Concerns

Final touches, error handling, and optimization tasks.

- [X] T046 Add comprehensive error handling for JWT validation failures in backend
- [X] T047 Add proper user data isolation based on JWT token user ID in backend
- [X] T048 Add input validation and sanitization for all authentication endpoints
- [X] T049 Add proper logging for authentication events in backend
- [X] T050 Add accessibility improvements to authentication forms in frontend
- [X] T051 Add loading states and UX improvements to authentication flows
- [X] T052 Update documentation for the new authentication system
- [X] T053 Perform end-to-end testing of all authentication flows
- [X] T054 Optimize JWT validation performance to meet <100ms requirement

## Dependencies

- **User Story 2** depends on completion of **User Story 1** (user registration must work before login)
- **User Story 3** depends on completion of **User Story 2** (authentication must work before API access)
- **User Story 4** depends on completion of **User Story 3** (basic integration before full integration)

## Parallel Execution Examples

1. **Backend & Frontend Parallel Development**:
   - While backend team works on T005-T010 (foundational models and services)
   - Frontend team can work on T011-T012 (Better Auth client and types)

2. **Within User Story Parallel Development**:
   - T015 (registration page) and T016 (registration form) can be developed in parallel
   - T017 (sign-up endpoint) and T018 (user service) can be developed in parallel

3. **Across User Stories**:
   - Once foundational components are complete, all user stories can progress in parallel with proper coordination