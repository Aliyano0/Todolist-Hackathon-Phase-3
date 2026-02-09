---
description: "Task list for Todo Backend API implementation"
---

# Tasks: Todo Backend API

**Input**: Design documents from `/specs/002-todo-backend-api/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: TDD approach will be followed with pytest for all components.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- **Backend only**: `backend/` at repository root
- Paths shown below follow the backend-only structure from plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create backend project structure per implementation plan
- [X] T002 [P] Initialize Python 3.13+ project with FastAPI, SQLModel, python-jose[cryptography], uvicorn, psycopg2-binary dependencies using UV
- [X] T003 [P] Configure linting and formatting tools (black, ruff, mypy)
- [X] T004 [P] Set up access to context7 and nextjs mcp servers for documentation
- [X] T005 [P] Create/Update `CLAUDE.md` for `backend/` with relevant context and instructions

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

**Foundational tasks**:

- [X] T006 Set up database schema and migrations framework in backend/database/
- [X] T007 [P] Implement JWT authentication framework in backend/dependencies/auth.py and backend/security/jwt.py
- [X] T008 [P] Set up API routing structure in backend/api/todos.py
- [X] T009 Create base models/entities in backend/models/todo.py based on data model
- [X] T010 Configure error handling and standardized JSON error response framework
- [X] T011 Set up environment configuration management with JWT_SECRET_KEY from environment variable
- [X] T012 Implement database connection pooling in backend/database/session.py
- [X] T013 Configure CORS middleware to allow frontend origins in backend/main.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create Todo Task (Priority: P1) 🎯 MVP

**Goal**: Enable users to create new todo tasks with title and optional description via API

**Independent Test**: Can be fully tested by sending a POST request to the API with valid task data and verifying that the task is stored and retrievable for the authenticated user only.

### Tests for User Story 1 (TDD approach) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T013 [P] [US1] Contract test for POST /{user_id}/tasks endpoint in backend/tests/api/test_create_task.py
- [ ] T014 [P] [US1] Unit test for Task creation service in backend/tests/unit/test_todo_service.py
- [ ] T015 [P] [US1] Integration test for user task creation flow in backend/tests/integration/test_task_creation.py

### Implementation for User Story 1

- [X] T016 [P] [US1] Create Task model in backend/models/todo.py with required fields (id, title, description, completed, user_id, timestamps)
- [X] T017 [US1] Create Task request/response schemas in backend/schemas/todo.py for CreateTaskRequest
- [X] T018 [US1] Implement TodoService in backend/core/services/todo_service.py (create_task method)
- [X] T019 [US1] Implement POST /{user_id}/tasks endpoint in backend/api/todos.py with JWT validation
- [X] T020 [US1] Add input validation and error handling for task creation
- [X] T021 [US1] Add logging for task creation operations

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View Todo Tasks (Priority: P1)

**Goal**: Enable users to view all their todo tasks in a list format

**Independent Test**: Can be fully tested by sending a GET request to the API and verifying that only the authenticated user's tasks are returned, not tasks from other users.

### Tests for User Story 2 (TDD approach) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T022 [P] [US2] Contract test for GET /{user_id}/tasks endpoint in backend/tests/api/test_list_tasks.py
- [ ] T023 [P] [US2] Unit test for Task listing service in backend/tests/unit/test_todo_service.py
- [ ] T024 [P] [US2] Integration test for user task listing flow in backend/tests/integration/test_task_listing.py

### Implementation for User Story 2

- [X] T025 [P] [US2] Extend TodoService in backend/core/services/todo_service.py with list_tasks method
- [X] T026 [US2] Extend Task response schema in backend/schemas/todo.py for list responses
- [X] T027 [US2] Implement GET /{user_id}/tasks endpoint in backend/api/todos.py with JWT validation and user isolation
- [X] T028 [US2] Add proper error handling for task listing
- [X] T029 [US2] Implement GET /{user_id}/tasks/{id} endpoint for specific task details

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Update and Manage Tasks (Priority: P2)

**Goal**: Enable users to modify existing tasks by updating details, marking them as complete/incomplete, or deleting them

**Independent Test**: Can be tested separately for each operation (update, delete, toggle completion) by sending appropriate requests to the API and verifying the changes are persisted correctly.

### Tests for User Story 3 (TDD approach) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T030 [P] [US3] Contract test for PUT /{user_id}/tasks/{id} endpoint in backend/tests/api/test_update_task.py
- [ ] T031 [P] [US3] Contract test for DELETE /{user_id}/tasks/{id} endpoint in backend/tests/api/test_delete_task.py
- [ ] T032 [P] [US3] Contract test for PATCH /{user_id}/tasks/{id}/complete endpoint in backend/tests/api/test_toggle_completion.py
- [ ] T033 [P] [US3] Unit tests for update/delete/toggle operations in backend/tests/unit/test_todo_service.py

### Implementation for User Story 3

- [X] T034 [P] [US3] Extend TodoService in backend/core/services/todo_service.py with update_task, delete_task, and toggle_completion methods
- [X] T035 [US3] Create UpdateTaskRequest schema in backend/schemas/todo.py
- [X] T036 [US3] Implement PUT /{user_id}/tasks/{id} endpoint in backend/api/todos.py with proper validation
- [X] T037 [US3] Implement DELETE /{user_id}/tasks/{id} endpoint in backend/api/todos.py with proper validation
- [X] T038 [US3] Implement PATCH /{user_id}/tasks/{id}/complete endpoint in backend/api/todos.py for toggling completion status
- [X] T039 [US3] Add proper error handling and validation for all management operations

**Checkpoint**: All user stories should now be independently functional

---

[Add more user story phases as needed, following the same pattern]

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T040 [P] Documentation updates in backend/README.md
- [X] T041 Code cleanup and refactoring across all components
- [X] T042 Performance optimization across all stories
- [X] T043 [P] Additional unit tests (if requested) in backend/tests/unit/
- [X] T044 Security hardening (input sanitization, rate limiting, etc.)
- [X] T045 Run quickstart.md validation to ensure setup works correctly
- [X] T046 Add database initialization validation to authentication endpoints
- [X] T047 Create integration test for complete auth flow (register → login → API access → logout)
- [X] T048 Document the authentication flow between frontend and backend components

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Contract test for POST /{user_id}/tasks endpoint in backend/tests/api/test_create_task.py"
Task: "Unit test for Task creation service in backend/tests/unit/test_todo_service.py"
Task: "Integration test for user task creation flow in backend/tests/integration/test_task_creation.py"

# Launch all models for User Story 1 together:
Task: "Create Task model in backend/models/todo.py with required fields (id, title, description, completed, user_id, timestamps)"
Task: "Create Task request/response schemas in backend/schemas/todo.py for CreateTaskRequest"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence