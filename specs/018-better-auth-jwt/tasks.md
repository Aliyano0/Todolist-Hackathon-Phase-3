# Tasks: Multi-User Authentication System

**Input**: Design documents from `/specs/018-better-auth-jwt/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Included per constitution's TDD workflow requirement

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/` directory
- **Frontend**: `frontend/` directory
- Paths shown below follow the web application structure from plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Verify Python 3.13+ and Node.js 18+ are installed
- [ ] T002 Install UV package manager for Python backend
- [ ] T003 [P] Install backend dependencies: fastapi, sqlmodel, asyncpg==0.30.0, python-jose[cryptography], bcrypt, uvicorn in backend/
- [ ] T004 [P] Install frontend dependencies: better-auth, shadcn-ui, tailwindcss in frontend/
- [ ] T005 [P] Create backend/.env file with DATABASE_URL and BETTER_AUTH_SECRET
- [ ] T006 [P] Create frontend/.env.local file with NEXT_PUBLIC_API_URL and BETTER_AUTH_SECRET
- [ ] T007 [P] Configure CORS middleware in backend/main.py to allow frontend origin with credentials
- [ ] T008 [P] Set up access to context7 MCP server for Better Auth, FastAPI, SQLModel documentation
- [ ] T009 [P] Set up access to nextjs MCP server for Next.js 16.1 documentation
- [ ] T010 [P] Update backend/CLAUDE.md with JWT verification patterns and async SQLModel usage
- [ ] T011 [P] Update frontend/CLAUDE.md with Better Auth integration and protected routes patterns

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T012 Create database migration script in backend/migrations/uuid_migration.py to drop all tables and recreate with UUID schema
- [ ] T013 Run database migration to create clean slate UUID schema
- [ ] T014 [P] Create User model in backend/models/user.py with UUID primary key, email, password_hash, email_verified, verification_token, reset_token fields
- [ ] T015 [P] Create TodoTask model in backend/models/todo.py with UUID primary key, user_id foreign key, title, description, completed, priority, category fields
- [ ] T016 [P] Create password hashing utilities in backend/core/security/password.py using bcrypt
- [ ] T017 [P] Create JWT verification utilities in backend/core/security/jwt.py using python-jose
- [ ] T018 Create JWT verification dependency in backend/dependencies/auth.py (get_current_user function)
- [ ] T019 Create async database session dependency in backend/database/session.py using create_async_engine and AsyncSession
- [ ] T020 [P] Configure Better Auth in frontend/lib/auth.ts with credentials provider and JWT plugin
- [ ] T021 [P] Create AuthProvider component in frontend/providers/AuthProvider.tsx
- [ ] T022 [P] Create API client utility in frontend/lib/api.ts with credentials: 'include' for cookie support
- [ ] T023 [P] Create password validation utility in frontend/lib/validation.ts for 8+ chars, uppercase, lowercase, number, special char
- [ ] T024 Wrap app with AuthProvider in frontend/app/layout.tsx

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Registration and Account Creation (Priority: P1) 🎯 MVP

**Goal**: Allow new users to create accounts with email and password, get immediate access

**Independent Test**: Submit registration form with valid email/password, verify account creation, confirm user receives access token and is logged in

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T025 [P] [US1] Write unit test for password hashing in backend/tests/test_password.py
- [ ] T026 [P] [US1] Write unit test for User model validation in backend/tests/test_user_model.py
- [ ] T027 [P] [US1] Write integration test for registration endpoint in backend/tests/test_auth.py (test_register_success, test_register_duplicate_email, test_register_invalid_email, test_register_weak_password)
- [ ] T028 [P] [US1] Write frontend component test for RegisterForm in frontend/tests/RegisterForm.test.tsx

### Implementation for User Story 1

- [ ] T029 [P] [US1] Create User registration schema in backend/schemas/user.py (UserRegistration, UserResponse)
- [ ] T030 [US1] Implement user registration endpoint POST /api/auth/register in backend/api/auth.py (validate email uniqueness, hash password, create user, issue JWT via Better Auth)
- [ ] T031 [P] [US1] Create RegisterForm component in frontend/components/auth/RegisterForm.tsx with email and password fields
- [ ] T032 [P] [US1] Create PasswordStrength indicator component in frontend/components/auth/PasswordStrength.tsx
- [ ] T033 [US1] Create registration page in frontend/app/register/page.tsx using RegisterForm
- [ ] T034 [US1] Implement registration form submission with API call to /api/auth/register
- [ ] T035 [US1] Add client-side validation for email format and password requirements
- [ ] T036 [US1] Add error handling for duplicate email and display user-friendly messages
- [ ] T037 [US1] Verify all tests pass for User Story 1

**Checkpoint**: At this point, User Story 1 should be fully functional - users can register and get logged in

---

## Phase 4: User Story 2 - User Login and Session Management (Priority: P1)

**Goal**: Allow existing users to log in with email/password and maintain 7-day session

**Independent Test**: Enter valid credentials on login page, verify authentication, confirm access to user-specific data, verify session persists across browser sessions

### Tests for User Story 2

- [ ] T038 [P] [US2] Write unit test for password verification in backend/tests/test_password.py
- [ ] T039 [P] [US2] Write integration test for login endpoint in backend/tests/test_auth.py (test_login_success, test_login_invalid_credentials, test_login_nonexistent_user)
- [ ] T040 [P] [US2] Write frontend component test for LoginForm in frontend/tests/LoginForm.test.tsx
- [ ] T041 [P] [US2] Write E2E test for login flow in frontend/tests/e2e/login.spec.ts using Playwright

### Implementation for User Story 2

- [ ] T042 [P] [US2] Create User login schema in backend/schemas/user.py (UserLogin, LoginResponse)
- [ ] T043 [US2] Implement user login endpoint POST /api/auth/login in backend/api/auth.py (find user by email, verify password, issue JWT via Better Auth)
- [ ] T044 [P] [US2] Create LoginForm component in frontend/components/auth/LoginForm.tsx with email and password fields
- [ ] T045 [US2] Create login page in frontend/app/login/page.tsx using LoginForm
- [ ] T046 [US2] Implement login form submission with API call to /api/auth/login
- [ ] T047 [US2] Add error handling for invalid credentials without revealing which field was incorrect
- [ ] T048 [US2] Implement redirect to dashboard after successful login
- [ ] T049 [US2] Verify JWT token is stored in httpOnly cookie by Better Auth
- [ ] T050 [US2] Verify all tests pass for User Story 2

**Checkpoint**: At this point, User Stories 1 AND 2 should both work - users can register and login

---

## Phase 5: User Story 3 - Secure Access to Personal Data (Priority: P1)

**Goal**: Enforce data isolation so users can only access their own tasks, never another user's data

**Independent Test**: Login as User A, create tasks, attempt to access User B's tasks using User A's credentials, verify access is denied

### Tests for User Story 3

- [ ] T051 [P] [US3] Write unit test for JWT verification dependency in backend/tests/test_jwt_middleware.py
- [ ] T052 [P] [US3] Write integration test for data isolation in backend/tests/test_data_isolation.py (test_user_can_access_own_tasks, test_user_cannot_access_other_user_tasks, test_invalid_token_returns_401, test_user_id_mismatch_returns_403)
- [ ] T053 [P] [US3] Write frontend test for protected routes in frontend/tests/protected-routes.test.tsx
- [ ] T054 [P] [US3] Write E2E test for data isolation in frontend/tests/e2e/data-isolation.spec.ts

### Implementation for User Story 3

- [ ] T055 [US3] Update task routes in backend/api/tasks.py to use get_current_user dependency for JWT verification
- [ ] T056 [US3] Add user_id path parameter validation in all task endpoints (verify path user_id matches JWT user_id, return 403 if mismatch)
- [ ] T057 [US3] Update all task queries to filter by authenticated user_id (WHERE user_id = current_user)
- [ ] T058 [US3] Add 401 Unauthorized response for missing/invalid JWT tokens
- [ ] T059 [US3] Add 403 Forbidden response for user_id mismatch
- [ ] T060 [P] [US3] Create protected route middleware in frontend/app/middleware.ts to check authentication
- [ ] T061 [P] [US3] Create useAuth hook in frontend/hooks/useAuth.ts for accessing Better Auth session
- [ ] T062 [US3] Update API client in frontend/lib/api.ts to handle 401 errors (redirect to login)
- [ ] T063 [US3] Update API client to handle 403 errors (show access denied message)
- [ ] T064 [US3] Protect dashboard route in frontend/app/dashboard/page.tsx (redirect to login if not authenticated)
- [ ] T065 [US3] Update task API calls to include user_id from authenticated session
- [ ] T066 [US3] Verify all tests pass for User Story 3

**Checkpoint**: All P1 user stories complete - users can register, login, and access only their own data securely

---

## Phase 6: User Story 4 - Automatic Session Expiration (Priority: P2)

**Goal**: Tokens expire after 7 days, users are redirected to login when accessing with expired token

**Independent Test**: Simulate token expiration (or wait 7 days), attempt to access protected page, verify redirect to login

### Tests for User Story 4

- [ ] T067 [P] [US4] Write unit test for token expiry validation in backend/tests/test_jwt_middleware.py (test_expired_token_returns_401)
- [ ] T068 [P] [US4] Write integration test for expired token handling in backend/tests/test_auth.py (test_expired_token_access_denied)
- [ ] T069 [P] [US4] Write E2E test for token expiration in frontend/tests/e2e/token-expiration.spec.ts

### Implementation for User Story 4

- [ ] T070 [US4] Verify JWT verification dependency checks token expiration (exp claim)
- [ ] T071 [US4] Ensure expired tokens return 401 Unauthorized
- [ ] T072 [US4] Update frontend API client to detect 401 from expired token and redirect to login
- [ ] T073 [US4] Add user-friendly message on login page explaining session expired
- [ ] T074 [US4] Verify all tests pass for User Story 4

**Checkpoint**: Token expiration works correctly - users must re-login after 7 days

---

## Phase 7: User Story 5 - User Logout (Priority: P2)

**Goal**: Users can log out, clearing their session and redirecting to login page

**Independent Test**: Login, click logout, verify session cleared, attempt to access protected page, verify redirect to login

### Tests for User Story 5

- [ ] T075 [P] [US5] Write integration test for logout endpoint in backend/tests/test_auth.py (test_logout_clears_cookie)
- [ ] T076 [P] [US5] Write frontend test for logout button in frontend/tests/Navbar.test.tsx
- [ ] T077 [P] [US5] Write E2E test for logout flow in frontend/tests/e2e/logout.spec.ts

### Implementation for User Story 5

- [ ] T078 [US5] Implement logout endpoint POST /api/auth/logout in backend/api/auth.py (clear auth cookie)
- [ ] T079 [P] [US5] Add logout button to Navbar component in frontend/components/Navbar.tsx
- [ ] T080 [US5] Implement logout handler using Better Auth signOut function
- [ ] T081 [US5] Redirect to login page after logout
- [ ] T082 [US5] Verify logout clears httpOnly cookie
- [ ] T083 [US5] Verify all tests pass for User Story 5

**Checkpoint**: Logout functionality complete - users can explicitly end their session

---

## Phase 8: User Story 6 - Unauthorized Access Prevention (Priority: P2)

**Goal**: Unauthenticated users and malicious actors cannot access protected resources

**Independent Test**: Attempt to access protected endpoints without token, with invalid token, or with another user's token, verify all attempts are denied

### Tests for User Story 6

- [ ] T084 [P] [US6] Write integration test for unauthorized access in backend/tests/test_auth.py (test_no_token_returns_401, test_invalid_token_returns_401, test_malformed_token_returns_401)
- [ ] T085 [P] [US6] Write E2E test for unauthorized access in frontend/tests/e2e/unauthorized.spec.ts

### Implementation for User Story 6

- [ ] T086 [US6] Verify all protected routes require valid JWT token
- [ ] T087 [US6] Verify missing token returns 401 Unauthorized
- [ ] T088 [US6] Verify invalid/malformed token returns 401 Unauthorized
- [ ] T089 [US6] Verify tampered token signature returns 401 Unauthorized
- [ ] T090 [US6] Add comprehensive error messages for different unauthorized scenarios
- [ ] T091 [US6] Verify frontend displays appropriate error messages for 401/403 responses
- [ ] T092 [US6] Verify all tests pass for User Story 6

**Checkpoint**: All user stories complete - comprehensive authentication system with security

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T093 [P] Add comprehensive logging for authentication events in backend/core/logging.py
- [ ] T094 [P] Add rate limiting consideration documentation in docs/security.md
- [ ] T095 [P] Verify quickstart.md instructions work end-to-end
- [ ] T096 [P] Update backend/CLAUDE.md with final authentication patterns and lessons learned
- [ ] T097 [P] Update frontend/CLAUDE.md with Better Auth integration best practices
- [ ] T098 Code cleanup and remove any old authentication code from previous implementations
- [ ] T099 Verify all environment variables are documented in .env.example files
- [ ] T100 Run full test suite (backend: pytest, frontend: npm test, E2E: playwright)
- [ ] T101 Performance testing: Verify 100+ concurrent authentication requests work correctly
- [ ] T102 Security review: Verify password hashing, JWT verification, data isolation all working correctly
- [ ] T103 Create ADR for Better Auth as authentication authority decision in history/adr/
- [ ] T104 Create ADR for clean slate UUID migration decision in history/adr/

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-8)**: All depend on Foundational phase completion
  - User Story 1 (P1): Registration - Can start after Foundational
  - User Story 2 (P1): Login - Can start after Foundational (independent of US1 but integrates with it)
  - User Story 3 (P1): Data Isolation - Depends on US1 and US2 (needs users to exist)
  - User Story 4 (P2): Token Expiration - Depends on US2 (needs login to exist)
  - User Story 5 (P2): Logout - Depends on US2 (needs login to exist)
  - User Story 6 (P2): Unauthorized Access - Can start after Foundational (tests security)
- **Polish (Phase 9)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational - Integrates with US1 but independently testable
- **User Story 3 (P1)**: Depends on US1 and US2 - Needs users to be able to register and login first
- **User Story 4 (P2)**: Depends on US2 - Needs login functionality to test expiration
- **User Story 5 (P2)**: Depends on US2 - Needs login functionality to test logout
- **User Story 6 (P2)**: Can start after Foundational - Tests security independently

### Within Each User Story

- Tests MUST be written and FAIL before implementation (TDD workflow)
- Models before services
- Services before endpoints
- Backend implementation before frontend integration
- Core implementation before error handling
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T003-T011)
- All Foundational tasks marked [P] can run in parallel within Phase 2 (T014-T024)
- Once Foundational phase completes:
  - US1 and US2 can start in parallel (different endpoints)
  - US6 can start in parallel (tests security independently)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1 (Registration)

```bash
# Launch all tests for User Story 1 together:
Task: "Write unit test for password hashing in backend/tests/test_password.py"
Task: "Write unit test for User model validation in backend/tests/test_user_model.py"
Task: "Write integration test for registration endpoint in backend/tests/test_auth.py"
Task: "Write frontend component test for RegisterForm in frontend/tests/RegisterForm.test.tsx"

# Launch frontend components together:
Task: "Create RegisterForm component in frontend/components/auth/RegisterForm.tsx"
Task: "Create PasswordStrength indicator component in frontend/components/auth/PasswordStrength.tsx"
```

---

## Parallel Example: User Story 3 (Data Isolation)

```bash
# Launch all tests for User Story 3 together:
Task: "Write unit test for JWT verification dependency in backend/tests/test_jwt_middleware.py"
Task: "Write integration test for data isolation in backend/tests/test_data_isolation.py"
Task: "Write frontend test for protected routes in frontend/tests/protected-routes.test.tsx"
Task: "Write E2E test for data isolation in frontend/tests/e2e/data-isolation.spec.ts"

# Launch frontend components together:
Task: "Create protected route middleware in frontend/app/middleware.ts"
Task: "Create useAuth hook in frontend/hooks/useAuth.ts"
```

---

## Implementation Strategy

### MVP First (User Stories 1-3 Only)

1. Complete Phase 1: Setup (T001-T011)
2. Complete Phase 2: Foundational (T012-T024) - CRITICAL
3. Complete Phase 3: User Story 1 - Registration (T025-T037)
4. Complete Phase 4: User Story 2 - Login (T038-T050)
5. Complete Phase 5: User Story 3 - Data Isolation (T051-T066)
6. **STOP and VALIDATE**: Test all P1 stories independently
7. Deploy/demo MVP with core authentication

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (Users can register!)
3. Add User Story 2 → Test independently → Deploy/Demo (Users can login!)
4. Add User Story 3 → Test independently → Deploy/Demo (Data is secure!)
5. Add User Story 4 → Test independently → Deploy/Demo (Sessions expire)
6. Add User Story 5 → Test independently → Deploy/Demo (Users can logout)
7. Add User Story 6 → Test independently → Deploy/Demo (Security hardened)
8. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T024)
2. Once Foundational is done:
   - Developer A: User Story 1 (Registration) - T025-T037
   - Developer B: User Story 2 (Login) - T038-T050
   - Developer C: User Story 6 (Security) - T084-T092
3. After US1 and US2 complete:
   - Developer A: User Story 3 (Data Isolation) - T051-T066
   - Developer B: User Story 4 (Expiration) - T067-T074
   - Developer C: User Story 5 (Logout) - T075-T083
4. Stories complete and integrate independently

---

## Task Summary

**Total Tasks**: 104

**Tasks by Phase**:
- Phase 1 (Setup): 11 tasks
- Phase 2 (Foundational): 13 tasks (BLOCKING)
- Phase 3 (US1 - Registration): 13 tasks
- Phase 4 (US2 - Login): 13 tasks
- Phase 5 (US3 - Data Isolation): 16 tasks
- Phase 6 (US4 - Expiration): 8 tasks
- Phase 7 (US5 - Logout): 9 tasks
- Phase 8 (US6 - Unauthorized): 9 tasks
- Phase 9 (Polish): 12 tasks

**Tasks by User Story**:
- US1 (Registration): 13 tasks (4 tests + 9 implementation)
- US2 (Login): 13 tasks (4 tests + 9 implementation)
- US3 (Data Isolation): 16 tasks (4 tests + 12 implementation)
- US4 (Expiration): 8 tasks (3 tests + 5 implementation)
- US5 (Logout): 9 tasks (3 tests + 6 implementation)
- US6 (Unauthorized): 9 tasks (2 tests + 7 implementation)

**Parallel Opportunities**: 45 tasks marked [P] can run in parallel within their phase

**Independent Test Criteria**:
- US1: Submit registration form, verify account created, confirm access token received
- US2: Enter credentials, verify authentication, confirm session persists
- US3: Login as User A, create tasks, attempt User B access, verify denial
- US4: Simulate expiration, attempt access, verify redirect to login
- US5: Login, click logout, verify session cleared, verify redirect
- US6: Attempt access without/with invalid token, verify all denied

**MVP Scope**: User Stories 1-3 (Registration + Login + Data Isolation) = 42 tasks

---

## Notes

- [P] tasks = different files, no dependencies within phase
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- TDD workflow: Write tests first, ensure they fail, then implement
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Constitution compliance: Clean architecture, TDD, multi-user auth, CLAUDE.md updates
- All tasks follow strict checklist format: `- [ ] [TaskID] [P?] [Story?] Description with file path`
