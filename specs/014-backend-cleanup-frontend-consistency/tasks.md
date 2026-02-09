# Tasks: Backend Cleanup and Frontend Consistency

**Feature**: Backend Cleanup and Frontend Consistency
**Branch**: `014-backend-cleanup-frontend-consistency`
**Generated**: 2026-02-02

## Implementation Strategy

This feature focuses on cleaning up unnecessary files from the backend codebase while preserving essential functionality for basic todo CRUD operations. We'll ensure consistent communication between frontend and backend using existing API contracts with the same data model as the frontend. The approach will be to first remove unnecessary authentication-related files, then align API contracts, and finally verify frontend-backend consistency.

## Phase 1: Setup & Environment Verification

- [X] T001 Verify backend directory structure and locate files from 008-backend-cleanup-rebuild feature in backend/
- [X] T002 Verify frontend directory structure and ensure Next.js 16+ compatibility in frontend/
- [X] T003 Document current state of backend API endpoints in backend/api/
- [X] T004 Document current state of frontend API integration in frontend/lib/api.ts

## Phase 2: Foundational Tasks

- [X] T010 [P] Remove authentication-related API endpoints in backend/api/auth.py
- [X] T011 [P] Remove user management API endpoints in backend/api/user.py
- [X] T012 [P] Remove Better Auth integration files in backend/api/better_auth.py and backend/better-auth-server.ts
- [X] T013 [P] Remove authentication models in backend/models/auth_token.py, backend/models/session.py, backend/models/token.py
- [X] T014 [P] Remove user model in backend/models/user.py
- [X] T015 [P] Remove authentication schemas in backend/schemas/auth.py, backend/schemas/user.py
- [X] T016 [P] Remove authentication services in backend/core/services/user_service.py
- [X] T017 [P] Remove authentication dependencies in backend/dependencies/auth.py
- [X] T018 [P] Remove security modules in backend/core/security/ and backend/security/
- [X] T019 [P] Remove authentication-related middleware, errors, and logging files if they exist
- [X] T020 [P] Update main.py to remove auth-related imports and router inclusion in backend/main.py

## Phase 3: [US1] Basic Todo CRUD Operations (Priority: P1)

**Goal**: Ensure the user can perform basic todo operations (create, read, update, delete) through a consistent UI without any authentication system.

**Independent Test Criteria**: The user can add, view, edit, and delete todos through the frontend interface, with all operations persisting correctly in the backend database.

**Acceptance Scenarios**:
1. Given the application is running, when a user adds a new todo with title and description, then the todo appears in the todo list with correct information
2. Given a todo exists in the system, when a user modifies the todo's title or description, then the changes are saved and reflected in the list
3. Given a todo exists in the system, when a user deletes the todo, then it is removed from the list and database
4. Given a todo exists in the system, when a user marks it as complete/incomplete, then the status is updated correctly

- [X] T030 [US1] Verify GET /api/todos endpoint returns all todos with proper response format in backend/api/tasks.py
- [X] T031 [US1] Verify POST /api/todos endpoint creates new todo with proper validation in backend/api/tasks.py
- [X] T032 [US1] Verify GET /api/todos/{id} endpoint returns specific todo with proper format in backend/api/tasks.py
- [X] T033 [US1] Verify PUT /api/todos/{id} endpoint updates todo with proper validation in backend/api/tasks.py
- [X] T034 [US1] Verify DELETE /api/todos/{id} endpoint deletes todo and returns proper response in backend/api/tasks.py
- [X] T035 [US1] Verify PATCH /api/todos/{id}/toggle endpoint toggles completion status in backend/api/tasks.py
- [X] T036 [US1] Test basic CRUD operations work without authentication requirements in backend/
- [X] T037 [US1] Update frontend API client to ensure all CRUD operations work with cleaned backend in frontend/lib/api.ts

## Phase 4: [US2] Backend Code Cleanup and Optimization (Priority: P1)

**Goal**: Review and clean up the backend codebase by removing unnecessary files from the 008-backend-cleanup-rebuild feature while keeping essential files.

**Independent Test Criteria**: The backend runs correctly with only the necessary files from the 008-backend-cleanup-rebuild feature, and all functionality remains intact.

**Acceptance Scenarios**:
1. Given the backend codebase, when unnecessary files from 008-backend-cleanup-rebuild are removed, then the application continues to function correctly
2. Given the cleaned backend codebase, when the application is started, then all necessary endpoints are accessible and working

- [X] T040 [US2] Remove BETTER_AUTH_INTEGRATION.md documentation file in backend/
- [X] T041 [US2] Clean up main.py to ensure only necessary imports and configurations remain in backend/main.py
- [X] T042 [US2] Update requirements.txt to remove unnecessary authentication dependencies in backend/requirements.txt
- [X] T043 [US2] Update pyproject.toml to remove unnecessary authentication dependencies in backend/pyproject.toml
- [X] T044 [US2] Verify all todo-related endpoints still function after cleanup in backend/api/tasks.py
- [X] T045 [US2] Verify database connection and session management still work after cleanup in backend/database/session.py
- [X] T046 [US2] Verify all todo business logic services still work after cleanup in backend/core/services/todo_service.py

## Phase 5: [US3] Frontend-Backend Consistency (Priority: P2)

**Goal**: Ensure the frontend and backend work consistently together without authentication so that the user can have a reliable experience performing todo operations.

**Independent Test Criteria**: The frontend can communicate with the backend without authentication issues, and data flows correctly in both directions.

**Acceptance Scenarios**:
1. Given the frontend and backend are connected, when a user performs a CRUD operation, then the data is correctly transmitted and stored
2. Given the frontend and backend, when data is modified in one place, then it's correctly reflected in the other

- [X] T050 [US3] Update frontend API client to use consistent endpoint paths in frontend/lib/api.ts
- [X] T051 [US3] Ensure response format consistency between backend and frontend in backend/api/tasks.py and frontend/lib/api.ts
- [X] T052 [US3] Verify ID type consistency (string IDs) between backend and frontend in backend/api/tasks.py and frontend/lib/api.ts
- [X] T053 [US3] Ensure field naming consistency (camelCase) between backend and frontend in backend/api/tasks.py and frontend/lib/api.ts
- [X] T054 [US3] Test frontend-backend communication without authentication requirements in integration test
- [X] T055 [US3] Update frontend components to handle consistent data format in frontend/components/todo/
- [X] T056 [US3] Verify UI consistency using existing shadcn UI components in frontend/components/

## Phase 6: Polish & Cross-Cutting Concerns

- [X] T060 Update documentation to reflect cleaned up backend structure in docs/
- [X] T061 Create comprehensive test suite for all endpoints in backend/tests/
- [X] T062 Update README with new setup instructions reflecting the cleaned up structure in README.md
- [X] T063 Verify all user stories work end-to-end in integrated system
- [X] T064 Clean up temporary workarounds and create follow-up issues for future improvements

## Dependencies

- User Story 1 (Basic Todo CRUD Operations) can be developed in parallel with User Story 2 (Backend Code Cleanup) since they focus on different aspects
- User Story 3 (Frontend-Backend Consistency) depends on completion of both US1 and US2 to ensure proper communication
- Foundational tasks (Phase 2) must be completed before any user story phases can begin

## Parallel Execution Opportunities

- Tasks T010-T019 in Phase 2 can be executed in parallel as they involve removing different authentication-related files
- Tasks T030-T036 in US1 can be developed in parallel as they're different CRUD operations
- Tasks T040-T046 in US2 can be worked on simultaneously as they involve various cleanup activities
- Tasks T050-T056 in US3 can be developed in parallel as they involve different consistency aspects