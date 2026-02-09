# Implementation Tasks: Backend Cleanup and Rebuild (Phase 2a)

## Feature Overview
FastAPI backend with SQLModel ORM connected to Neon PostgreSQL database providing REST API for todo management with 6 endpoints (list, create, get, update, delete, toggle completion) for a temporary single-user implementation.

## Implementation Strategy
Build MVP incrementally starting with foundational setup, then implement each user story in priority order (P1, P2, P3). Each user story will be a complete, independently testable increment.

## Phase 1: Setup Tasks
Initialize project structure and dependencies per implementation plan.

- [ ] T001 Create backend directory structure per plan
- [x] T002 Create backend/CLAUDE.md with backend-specific instructions
- [x] T003 Create backend/pyproject.toml with FastAPI, SQLModel, uvicorn, psycopg2-binary dependencies
- [x] T004 Create backend/requirements.txt from pyproject.toml
- [x] T005 Create .env.example file with database connection parameters
- [x] T006 Set up UV virtual environment in backend directory

## Phase 2: Foundational Tasks
Implement foundational components needed by all user stories.

- [x] T007 Create database/session.py with Neon PostgreSQL connection using SQLModel
- [x] T008 Create models/todo.py with TodoTask model per data model specification
- [x] T009 Create schemas/todo.py with request/response schemas per API contract
- [x] T010 Create core/services/todo_service.py with business logic for task operations
- [x] T011 Create main.py with FastAPI app and database initialization

## Phase 3: User Story 1 - Access Todo List (P1)
As a user, I want to view all my todo tasks in a list so that I can see what I need to do.

**Goal**: Implement GET /api/tasks endpoint to return all tasks
**Independent Test**: Making GET request to /api/tasks returns a list of tasks

### Implementation Tasks:
- [x] T012 [US1] Create GET /api/tasks endpoint in api/tasks.py
- [x] T013 [US1] Implement get_all_tasks in todo_service.py
- [x] T014 [US1] Test endpoint returns all tasks when they exist
- [x] T015 [US1] Test endpoint returns empty array when no tasks exist

## Phase 4: User Story 2 - Create New Todo Task (P1)
As a user, I want to create new todo tasks so that I can track what I need to do.

**Goal**: Implement POST /api/tasks endpoint to create new tasks
**Independent Test**: Making POST request to /api/tasks with task details creates and returns the task

### Implementation Tasks:
- [x] T016 [US2] Create POST /api/tasks endpoint in api/tasks.py
- [x] T017 [US2] Implement create_task in todo_service.py with validation
- [x] T018 [US2] Test endpoint creates task with valid data
- [x] T019 [US2] Test endpoint returns error with invalid data (missing title)

## Phase 5: User Story 3 - View Individual Task Details (P2)
As a user, I want to view detailed information about a specific todo task so that I can see its full description and status.

**Goal**: Implement GET /api/tasks/{id} endpoint to return specific task details
**Independent Test**: Making GET request to /api/tasks/{id} returns details of specific task

### Implementation Tasks:
- [x] T020 [US3] Create GET /api/tasks/{id} endpoint in api/tasks.py
- [x] T021 [US3] Implement get_task_by_id in todo_service.py
- [x] T022 [US3] Test endpoint returns specific task details when it exists
- [x] T023 [US3] Test endpoint returns 404 when task doesn't exist

## Phase 6: User Story 4 - Update Existing Task (P2)
As a user, I want to modify the details of an existing todo task so that I can keep my tasks up to date.

**Goal**: Implement PUT /api/tasks/{id} endpoint to update task details
**Independent Test**: Making PUT request to /api/tasks/{id} updates and returns the task

### Implementation Tasks:
- [x] T024 [US4] Create PUT /api/tasks/{id} endpoint in api/tasks.py
- [x] T025 [US4] Implement update_task in todo_service.py with validation
- [x] T026 [US4] Test endpoint updates task when it exists
- [x] T027 [US4] Test endpoint returns 404 when task doesn't exist

## Phase 7: User Story 5 - Delete Completed/Unwanted Tasks (P3)
As a user, I want to remove tasks I no longer need so that my task list stays organized and manageable.

**Goal**: Implement DELETE /api/tasks/{id} endpoint to remove tasks
**Independent Test**: Making DELETE request to /api/tasks/{id} removes the task from the system

### Implementation Tasks:
- [x] T028 [US5] Create DELETE /api/tasks/{id} endpoint in api/tasks.py
- [x] T029 [US5] Implement delete_task in todo_service.py
- [x] T030 [US5] Test endpoint deletes task when it exists
- [x] T031 [US5] Test endpoint returns 404 when task doesn't exist

## Phase 8: User Story 6 - Toggle Task Completion Status (P2)
As a user, I want to mark tasks as completed or incomplete so that I can track my progress.

**Goal**: Implement PATCH /api/tasks/{id}/complete endpoint to toggle completion status
**Independent Test**: Making PATCH request to /api/tasks/{id}/complete toggles the completion status

### Implementation Tasks:
- [x] T032 [US6] Create PATCH /api/tasks/{id}/complete endpoint in api/tasks.py
- [x] T033 [US6] Implement toggle_task_completion in todo_service.py
- [x] T034 [US6] Test endpoint toggles completion from false to true
- [x] T035 [US6] Test endpoint toggles completion from true to false
- [x] T036 [US6] Test endpoint returns 404 when task doesn't exist

## Phase 9: Polish & Cross-Cutting Concerns
Final implementation details and integration.

- [x] T037 Add proper error handling with descriptive JSON messages per specification
- [x] T038 Add request validation and response formatting per API contract
- [x] T039 Add database connection error handling for edge cases
- [x] T040 Test all endpoints work together with proper data flow
- [x] T041 Update main.py to include all API routes
- [x] T042 Run full test suite to verify all functionality works
- [x] T043 Document any remaining edge cases or error conditions
- [x] T044 Verify all success criteria from spec are met

## Dependencies
- User Story 1 (P1) - Access Todo List: No dependencies
- User Story 2 (P1) - Create New Todo Task: No dependencies
- User Story 3 (P2) - View Individual Task Details: Depends on User Story 1 (need to have tasks to view)
- User Story 4 (P2) - Update Existing Task: Depends on User Story 2 (need to create tasks to update)
- User Story 5 (P3) - Delete Tasks: Depends on User Story 2 (need to create tasks to delete)
- User Story 6 (P2) - Toggle Completion: Depends on User Story 2 (need to create tasks to toggle)

## Parallel Execution Opportunities
- [P] T012-T015 (US1) and T016-T019 (US2) can be developed in parallel since they operate on different endpoints
- [P] T020-T023 (US3) and T024-T027 (US4) can be developed in parallel after US1/US2 are complete
- [P] T028-T031 (US5) and T032-T036 (US6) can be developed in parallel after US2 is complete

## MVP Scope
Minimal Viable Product includes User Story 1 (Access Todo List) and User Story 2 (Create New Todo Task) which provide the core functionality for a basic todo system.