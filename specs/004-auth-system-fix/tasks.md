# Tasks: Authentication System Fix

## Feature: Unified authentication system using Better Auth with JWT token integration for FastAPI backend

**Goal**: Implement a unified authentication system that resolves the 400 Bad Request error on the POST /auth/register endpoint by properly integrating Better Auth with the FastAPI backend.

## Phase 1: Setup Tasks

- [ ] T001 Create project structure in backend and frontend directories per plan
- [ ] T002 Set up Python virtual environment with UV and install FastAPI dependencies
- [ ] T003 Set up Node.js environment and install Next.js and Better Auth dependencies
- [ ] T004 Configure environment variables for both backend and frontend
- [ ] T005 Initialize database connection with Neon Serverless PostgreSQL

## Phase 2: Foundational Tasks

- [x] T006 [P] Create User model in backend/models/user.py with fields from data model
- [x] T007 [P] Create Authentication Token model in backend/models/auth_token.py with fields from data model
- [x] T008 [P] Create Session model in backend/models/session.py with fields from data model
- [x] T009 Create database initialization script in backend/database/init_db.py
- [x] T010 Set up JWT utilities in backend/core/security/jwt.py with Better Auth compatibility
- [x] T011 Create user service in backend/core/services/user_service.py for authentication operations
- [x] T012 Configure CORS middleware in backend/main.py to allow frontend origin

## Phase 3: [US1] New User Registration (Priority: P1)

**Goal**: Implement user registration functionality that allows new users to sign up for an account on the todo web app.

**Independent Test**: A new user should be able to fill out the registration form with valid credentials and successfully create an account, receiving appropriate feedback upon success or failure.

**Acceptance Scenarios**:
1. Given a new user visits the registration page, When they submit valid credentials (email, password), Then they should receive a success message and be redirected to the main todo dashboard
2. Given a user submits invalid registration data (missing fields, invalid email format), Then they should receive clear error messages indicating what needs to be corrected

- [x] T013 [P] [US1] Implement POST /auth/register endpoint in backend/api/auth.py
- [x] T014 [P] [US1] Create registration request schema in backend/schemas/auth.py
- [x] T015 [P] [US1] Create user response schema in backend/schemas/auth.py
- [x] T016 [P] [US1] Add registration validation logic in backend/core/services/user_service.py
- [x] T017 [P] [US1] Create registration form component in frontend/src/components/RegistrationForm.tsx
- [x] T018 [P] [US1] Create registration page in frontend/src/app/register/page.tsx
- [x] T019 [US1] Integrate registration form with Better Auth in frontend/src/lib/auth.ts
- [ ] T020 [US1] Test registration flow with valid credentials
- [ ] T021 [US1] Test registration flow with invalid credentials and verify error handling

## Phase 4: [US2] User Login and Session Management (Priority: P1)

**Goal**: Implement secure login functionality that allows registered users to access their account and maintain their session.

**Independent Test**: A registered user should be able to log in with their credentials, receive appropriate authentication tokens, and maintain access to protected resources until logout or session expiration.

**Acceptance Scenarios**:
1. Given a registered user enters valid login credentials, When they submit the login form, Then they should be authenticated and granted access to protected todo functionality
2. Given a user attempts to access protected resources without valid authentication, Then they should be redirected to the login page

- [x] T022 [P] [US2] Implement POST /auth/login endpoint in backend/api/auth.py
- [x] T023 [P] [US2] Create login request schema in backend/schemas/auth.py
- [x] T024 [P] [US2] Add login validation and authentication logic in backend/core/services/user_service.py
- [x] T025 [P] [US2] Create login form component in frontend/src/components/LoginForm.tsx
- [x] T026 [P] [US2] Create login page in frontend/src/app/login/page.tsx
- [x] T027 [US2] Integrate login form with Better Auth in frontend/src/lib/auth.ts
- [x] T028 [US2] Implement protected route component in frontend/src/components/ProtectedRoute.tsx
- [ ] T029 [US2] Test login flow with valid credentials
- [ ] T030 [US2] Test login flow with invalid credentials and verify error handling
- [ ] T031 [US2] Test protected route access without authentication

## Phase 5: [US3] Cross-Service Authentication Consistency (Priority: P2)

**Goal**: Ensure authentication works consistently between the frontend Next.js application and the FastAPI backend services without conflicts or errors.

**Independent Test**: Authentication requests from the frontend should be properly processed by the backend without protocol mismatches or error responses.

**Acceptance Scenarios**:
1. Given the authentication system is properly configured, When a user performs any authentication action (register, login, logout), Then the frontend and backend should communicate seamlessly without protocol errors

- [x] T032 [P] [US3] Implement POST /auth/logout endpoint in backend/api/auth.py
- [x] T033 [P] [US3] Implement POST /auth/refresh endpoint in backend/api/auth.py
- [x] T034 [P] [US3] Create logout handler in frontend/src/lib/auth.ts
- [x] T035 [P] [US3] Create token refresh handler in frontend/src/lib/auth.ts
- [x] T036 [P] [US3] Configure Better Auth client in frontend/src/lib/better-auth-client.ts
- [x] T037 [P] [US3] Configure Better Auth server in backend/better-auth-server.ts
- [x] T038 [US3] Update JWT verification middleware to work with Better Auth tokens
- [x] T039 [US3] Implement standardized error response format mapping
- [x] T040 [US3] Test complete authentication flow (register → login → protected access → logout)
- [x] T041 [US3] Verify JWT token compatibility between Better Auth and FastAPI
- [x] T042 [US3] Test token refresh functionality

## Phase 6: Polish & Cross-Cutting Concerns

- [x] T043 Implement password validation according to security requirements
- [x] T044 Add email validation and uniqueness checks
- [x] T045 Implement proper error handling and logging
- [x] T046 Add input sanitization and validation for all authentication endpoints
- [x] T047 Create authentication middleware for protecting API routes
- [x] T048 Update frontend to properly handle Better Auth tokens
- [x] T049 Test end-to-end authentication flow
- [x] T050 Update documentation with new authentication process
- [x] T051 Verify 400 Bad Request error is resolved on POST /auth/register
- [x] T052 Conduct security review of authentication implementation

## Dependencies

- User Story 2 (Login) depends on foundational models and services being complete
- User Story 3 (Consistency) depends on both User Story 1 and 2 being functional
- All authentication endpoints depend on the database models being properly configured

## Parallel Execution Opportunities

- Models can be created in parallel (T006-T008)
- Frontend components can be developed in parallel with backend endpoints (e.g., T013 with T017)
- Authentication endpoints can be implemented in parallel (T022, T032, T033)

## Implementation Strategy

1. **MVP Scope**: Complete User Story 1 (registration) with minimal viable implementation
2. **Incremental Delivery**: Add login functionality (User Story 2), then consistency features (User Story 3)
3. **Security First**: Ensure all authentication flows are secure before adding convenience features
4. **Test Early**: Validate JWT token compatibility and error handling throughout development