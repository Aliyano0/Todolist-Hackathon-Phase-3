# Tasks: Backend-Frontend API Integration Review

**Feature**: Backend-Frontend API Integration Review
**Branch**: `013-backend-frontend-review`
**Generated**: 2026-02-02

## Implementation Strategy

This feature focuses on reviewing and aligning the existing backend (FastAPI) and frontend (Next.js) implementations to ensure proper communication and consistency. The approach will be to first resolve server startup issues, then align API contracts, and finally standardize data models.

## Phase 1: Setup & Environment Verification

- [X] T001 Create directory structure for contracts documentation in specs/013-backend-frontend-review/contracts/
- [X] T002 Verify backend server can start successfully with current configuration in backend/main.py
- [X] T003 Verify frontend server can start successfully with current configuration in frontend/package.json
- [X] T004 Document current API endpoints from backend/api/tasks.py for reference

## Phase 2: Foundational Tasks

- [X] T010 [P] Update backend API routes from `/api/tasks` to `/api/todos` in backend/api/tasks.py to match frontend expectations
- [X] T011 [P] Create API response wrapper to convert direct arrays to `{ data: [...] }` format in backend/api/tasks.py
- [X] T012 [P] Create utility function to convert snake_case fields to camelCase in backend/utils/format_utils.py
- [X] T013 [P] Create ID conversion utility to transform integer IDs to string IDs in backend/utils/id_converter.py

## Phase 3: [US1] API Documentation and Integration (Priority: P1)

**Goal**: Ensure frontend can successfully make API calls to all backend endpoints and receive expected responses without errors.

**Independent Test Criteria**: The frontend can successfully make API calls to all backend endpoints and receive expected responses without errors.

**Acceptance Scenarios**:
1. Given the backend API is running, when a frontend makes a GET request to any endpoint, then the API returns properly formatted data with appropriate HTTP status codes
2. Given the backend API is running, when a frontend makes a POST/PUT/DELETE request with valid data, then the API processes the request and returns appropriate success/error responses

- [X] T020 [US1] Implement GET /api/todos endpoint that returns wrapped response with camelCase fields in backend/api/tasks.py
- [X] T021 [US1] Implement POST /api/todos endpoint that accepts and returns data with proper field transformations in backend/api/tasks.py
- [X] T022 [US1] Implement GET /api/todos/{id} endpoint that returns single todo with proper formatting in backend/api/tasks.py
- [X] T023 [US1] Implement PUT /api/todos/{id} endpoint that updates todo with proper field transformations in backend/api/tasks.py
- [X] T024 [US1] Implement DELETE /api/todos/{id} endpoint that properly deletes todo in backend/api/tasks.py
- [X] T025 [US1] Implement PATCH /api/todos/{id}/toggle endpoint that toggles completion status in backend/api/tasks.py
- [X] T026 [US1] Update frontend API client in frontend/lib/api.ts to call new `/api/todos` endpoints instead of `/todos`
- [X] T027 [US1] Test frontend-backend communication with all CRUD operations in integration test

## Phase 4: [US2] System Consistency Check (Priority: P1)

**Goal**: Ensure both frontend and backend follow consistent patterns for data structures, error handling, and API communication protocols.

**Independent Test Criteria**: Both frontend and backend follow consistent patterns for data structures, error handling, and API communication protocols.

**Acceptance Scenarios**:
1. Given both frontend and backend codebases, when a consistency review is performed, then matching data models and business logic are identified and standardized
2. Given inconsistent implementations are found, when the review is complete, then recommendations for improvements are documented

- [X] T030 [US2] Update backend TodoTask model to include string ID field in backend/models/todo.py
- [X] T031 [US2] Create API response schema that matches frontend TodoItem interface in backend/schemas/todo.py
- [X] T032 [US2] Update frontend TodoItem interface to align with backend response format in frontend/types/todo.ts
- [X] T033 [US2] Implement error handling consistency between frontend and backend in backend/api/tasks.py and frontend/lib/api.ts
- [X] T034 [US2] Document all identified inconsistencies and their resolutions in docs/inconsistency-report.md
- [X] T035 [US2] Update frontend hooks to handle new response format in frontend/hooks/useTodos.ts

## Phase 5: [US3] Server Startup and Error Resolution (Priority: P1)

**Goal**: Ensure both frontend and backend servers can start successfully in the local development environment without errors.

**Independent Test Criteria**: Running the specified startup commands for both frontend and backend results in successful server initialization without runtime errors.

**Acceptance Scenarios**:
1. Given the development environment is properly set up, when frontend server starts with 'npm run dev', then the server starts successfully and serves the application
2. Given the development environment is properly set up, when backend server starts with the specified uvicorn command, then the server starts successfully and serves API endpoints

- [X] T040 [US3] Test backend server startup with updated API endpoints in backend/main.py
- [X] T041 [US3] Test frontend server startup with updated API client in frontend/pages/index.tsx
- [X] T042 [US3] Verify all API endpoints return correct HTTP status codes in backend/api/tasks.py
- [X] T043 [US3] Verify frontend can successfully connect to backend API endpoints in frontend/lib/api.ts
- [X] T044 [US3] Create startup verification script in scripts/verify-integration.sh
- [X] T045 [US3] Document any remaining issues in docs/residual-issues.md

## Phase 6: Polish & Cross-Cutting Concerns

- [X] T050 Update documentation to reflect new API endpoints and data models in docs/api-contracts.md
- [X] T051 Create comprehensive test suite for all integrated endpoints in backend/tests/integration_tests.py
- [X] T052 Update README with new integration instructions in INTEGRATION_README.md
- [X] T053 Verify all user stories work end-to-end in integrated system
- [X] T054 Clean up temporary workarounds and create follow-up issues for future improvements

## Dependencies

- User Story 1 (API Integration) must be completed before User Story 2 (Consistency Check) can begin
- User Story 2 (Consistency Check) must be completed before User Story 3 (Server Startup) can be fully verified
- Foundational tasks (Phase 2) must be completed before any user story phases can begin

## Parallel Execution Opportunities

- Tasks T010-T013 in Phase 2 can be executed in parallel as they involve different utilities
- Tasks T020-T025 in US1 can be developed in parallel as they're different endpoints
- Tasks T030-T032 in US2 can be worked on simultaneously as they involve model alignment