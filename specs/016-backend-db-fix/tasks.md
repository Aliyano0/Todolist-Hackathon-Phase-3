# Implementation Tasks: Backend Database Schema Fix

## Feature Overview
Implementation of backend database schema fix to resolve the critical issue where the FastAPI backend is trying to access priority and category columns in the todotask table that don't exist in the current database.

## Implementation Strategy
- **MVP First**: Begin with User Story 1 (Fix Database Schema Mismatch) to establish core functionality
- **Incremental Delivery**: Build upon each user story in priority order (P1, P2, P3)
- **Parallel Execution**: Identified tasks that can be executed in parallel where possible
- **Independent Testing**: Each user story can be tested independently upon completion

## Dependencies
- User Story 1 (Database Schema Fix) must be completed before User Stories 2 and 3
- Foundational components (database migration, models) must be established before API fixes

## Parallel Execution Examples
- **Models & Services**: Data models and service functions can be created in parallel
- **API Endpoints**: Different API endpoints can be updated in parallel after foundational components are ready

---

## Phase 1: Setup Tasks

- [x] T001 Create database migration script for adding priority and category columns in backend/database/migrations.py
- [x] T002 Update CLAUDE.md files to document the new database schema changes
- [x] T003 Verify existing project structure matches the documented structure in plan.md

---

## Phase 2: Foundational Tasks

- [x] T004 [P] Update TodoTask model with priority and category fields in backend/models/todo.py
- [ ] T005 [P] Update TodoTask schema with priority and category fields in backend/schemas/todo.py
- [ ] T006 [P] Update TodoService functions to handle priority and category in backend/core/services/todo_service.py
- [x] T007 [P] Create database migration function to add missing columns in backend/database/migrations.py
- [ ] T008 [P] Update main.py to run migration on startup in backend/main.py
- [ ] T009 Update frontend types to include priority and category fields in frontend/types/todo.ts

---

## Phase 3: User Story 1 - Fix Database Schema Mismatch (Priority: P1)

**Goal**: Create proper database migration to add missing priority and category columns to resolve the "column does not exist" errors.

**Independent Test**: Can be fully tested by making API calls to list, create, update, and retrieve todo items and verifying that no database errors occur, delivering the core functionality of the enhanced todo app.

**Acceptance Scenarios**:
1. Given a user accesses the todo API endpoints, When they request todo data, Then the API should return data without "column does not exist" errors
2. Given a user creates or updates a todo item with priority and category, When the request is processed, Then the operation should complete successfully without database errors

- [x] T010 [US1] Implement SQL migration script to add priority and category columns in backend/database/migrations.py
- [x] T011 [US1] Add migration function to handle existing records with default values in backend/database/migrations.py
- [x] T012 [US1] Test migration script on a copy of existing database
- [x] T013 [US1] Verify migration can be run idempotently without errors
- [ ] T014 [US1] Update database session to run migration automatically on startup in backend/database/session.py
- [x] T015 [US1] Verify migration runs successfully when application starts

---

## Phase 4: User Story 2 - Restore API Functionality (Priority: P2)

**Goal**: Update all API endpoints to properly handle the new priority and category fields.

**Independent Test**: Can be fully tested by exercising all API endpoints (GET, POST, PUT, PATCH) and verifying they return proper responses without errors.

**Acceptance Scenarios**:
1. Given a user makes API calls to todo endpoints, When they perform CRUD operations, Then all operations should complete successfully with proper responses
2. Given a user tries to filter or sort by priority/category, When they make API requests, Then the API should handle these operations properly

- [x] T016 [US2] Update GET /api/tasks endpoint to return priority and category fields in backend/api/tasks.py
- [x] T017 [US2] Update POST /api/tasks endpoint to accept priority and category parameters in backend/api/tasks.py
- [x] T018 [US2] Update PUT /api/tasks/{id} endpoint to handle priority and category updates in backend/api/tasks.py
- [x] T019 [US2] Update PATCH /api/tasks/{id}/toggle-complete endpoint to include priority/category in response in backend/api/tasks.py
- [ ] T020 [US2] Update API request/response schemas to include new fields in backend/schemas/todo.py
- [x] T021 [US2] Test all API endpoints with priority and category data
- [ ] T022 [US2] Verify API endpoints return proper error messages for invalid priority/category values

---

## Phase 5: User Story 3 - Maintain Data Consistency (Priority: P3)

**Goal**: Ensure data integrity during migration and maintain backward compatibility with existing todo items.

**Independent Test**: Can be fully tested by verifying that existing todo items are properly updated with default priority/category values and that no data is lost during the migration.

**Acceptance Scenarios**:
1. Given existing todo items in the database, When the migration is applied, Then all existing items should have valid priority and category values
2. Given the migration process, When it runs, Then no existing data should be lost or corrupted

- [x] T023 [US3] Implement data validation for priority field ('high', 'medium', 'low') in backend/models/todo.py
- [x] T024 [US3] Implement data validation for category field in backend/models/todo.py
- [x] T025 [US3] Add error handling for database migration failures in backend/database/migrations.py
- [x] T026 [US3] Update existing records with default priority ('medium') and category ('personal') values in backend/database/migrations.py
- [x] T027 [US3] Test migration with existing data to ensure no data loss
- [x] T028 [US3] Verify backward compatibility with existing todo items without priority/category
- [x] T029 [US3] Add comprehensive error logging for migration process in backend/database/migrations.py

---

## Phase 6: Integration & Polish

- [x] T030 Update frontend API client to handle priority and category fields in frontend/lib/api.ts
- [ ] T031 Update frontend components to display priority and category information in frontend/components/todo/
- [x] T032 Test end-to-end functionality with database migration and API updates
- [x] T033 Verify all existing functionality remains intact after schema changes
- [x] T034 Run comprehensive tests to ensure no regressions were introduced
- [x] T035 Update documentation to reflect the new schema and API changes
- [x] T036 Perform final testing of database migration with various data scenarios
- [x] T037 Verify performance goals (migration completes in under 30 seconds)
- [ ] T038 Update README and quickstart guides with migration instructions
- [x] T039 Prepare for feature handoff and final review
- [x] T040 Clean up duplicate backend directory structure to eliminate code duplication
- [x] T041 Update API test suite to include priority and category fields in test requests
- [x] T042 Fix API endpoint mismatch to resolve 404 errors between frontend and backend