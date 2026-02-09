---

description: "Task list template for feature implementation"
---

# Tasks: Todo Console App

**Input**: Design documents from `/specs/001-todo-console-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), data-model.md, contracts/

**Tests**: TDD approach - all tasks include test-first workflow per constitution

**Organization**: Tasks are grouped by user story to enable independent implementation and testing

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- Project root: `/mnt/c/Study/claude-code/todolist-hackathon/todolist-phase-1/`
- Domain code: `src/core/`
- Adapters: `adapters/`
- Tests: `tests/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Initialize UV project with Python 3.13 in pyproject.toml
- [x] T002 [P] Create directory structure per plan.md:
  - `src/core/entities/`
  - `src/core/ports/`
  - `src/core/use_cases/`
  - `src/core/exceptions/`
  - `adapters/cli/`
  - `adapters/repository/`
  - `tests/unit/entities/`
  - `tests/unit/use_cases/`
  - `tests/unit/ports/`
  - `tests/integration/`
- [x] T003 [P] Configure pytest in pyproject.toml (testpaths, python_files)
- [x] T004 [P] Create `__init__.py` files for all packages

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 Create domain exceptions in `src/core/exceptions/todo_errors.py`:
  - `TodoError` base class
  - `TitleEmptyError`
  - `TitleTooLongError`
  - `TaskNotFoundError`
  - `InvalidIdError`
- [x] T006 [P] Create Todo entity in `src/core/entities/todo.py`:
  - `id: int` field
  - `title: str` field
  - `description: str | None` field
  - `completed: bool` field
  - `created_at: datetime` field
  - `__post_init__` validation
- [x] T007 [P] Create Repository port in `src/core/ports/repository.py`:
  - Abstract methods: `add()`, `list_all()`, `get()`, `update()`, `delete()`, `mark_complete()`
- [x] T008 [P] Create MemoryRepository in `adapters/repository/memory_repository.py`:
  - `_todos: list[Todo]` storage
  - `_next_id: int` counter
  - Implement all Repository port methods
  - Auto-increment ID on add
- [x] T009 Write unit tests for Todo entity in `tests/unit/entities/test_todo.py`
- [x] T010 [P] Write unit tests for MemoryRepository in `tests/unit/ports/test_repository.py`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add Tasks (Priority: P1)

**Goal**: Users can add new tasks with title and optional description

**Independent Test**: Run `todo add "Buy groceries"` → verify task appears in list with correct data

**Acceptance Criteria**:
- Task created with sequential ID
- Title validated (1-200 chars, non-empty)
- Optional description stored correctly
- Success message: "Added task 1: \"Buy groceries\""
- Error: "Error: Title cannot be empty" for invalid titles

### Tests for User Story 1

- [x] T011 [P] [US1] Write failing test in `tests/unit/use_cases/test_add_todo.py`:
  - Test adding task with title only
  - Test adding task with title and description
  - Test error on empty title
  - Test error on whitespace-only title
  - Test error on title > 200 chars

### Implementation for User Story 1

- [x] T012 [US1] Create AddTodo use case in `src/core/use_cases/add_todo.py`:
  - Depends on Repository port
  - Validates title (1-200 chars, non-empty)
  - Calls `repository.add()`
  - Returns Todo
- [x] T013 [P] [US1] Create CLI add subparser in `adapters/cli/argparse_adapter.py`:
  - `add` subcommand with `--title`/`-t` and `--description`/`-d` flags
  - Parse and validate inputs
  - Call AddTodo use case
  - Print success message
- [x] T014 [US1] Create CLI entry point in `adapters/cli/__main__.py`:
  - argparse.ArgumentParser with subparsers
  - Main help command
  - Forward to subcommands

**Checkpoint**: User Story 1 complete - can add tasks via CLI

---

## Phase 4: User Story 2 - View Tasks (Priority: P1)

**Goal**: Users can list all tasks with status indicators and view individual task details

**Independent Test**: Add tasks with different statuses → run `todo list` → verify [X]/[ ] indicators correct

**Acceptance Criteria**:
- List shows all tasks in creation order
- Complete tasks show `[X]`, incomplete show `[ ]`
- Empty list shows friendly message
- `todo get <id>` shows full task details (title, description, status, created_at)
- Error for non-existent ID: "Error: Task not found"

### Tests for User Story 2

- [x] T015 [P] [US2] Write failing test in `tests/unit/use_cases/test_list_todos.py`:
  - Test listing all tasks
  - Test empty list message
  - Test status indicators ([X]/[ ])
- [x] T016 [P] [US2] Write failing test in `tests/unit/use_cases/test_get_todo.py`:
  - Test getting task by ID
  - Test task not found error
  - Test getting all task fields

### Implementation for User Story 2

- [x] T017 [US2] Create ListTodos use case in `src/core/use_cases/list_todos.py`:
  - Depends on Repository port
  - Returns `list[Todo]` from repository
- [x] T018 [US2] Create GetTodo use case in `src/core/use_cases/get_todo.py`:
  - Depends on Repository port
  - Raises `TaskNotFoundError` if not found
  - Returns Todo
- [x] T019 [P] [US2] Add CLI list subparser in `adapters/cli/argparse_adapter.py`:
  - `list` subcommand with optional `--simple` flag
  - Format output with status indicators
  - Handle empty list case
- [x] T020 [P] [US2] Add CLI get subparser in `adapters/cli/argparse_adapter.py`:
  - `get` subcommand with `--id` flag
  - Format full task details
  - Handle "Task not found" error

**Checkpoint**: User Story 2 complete - can list and get tasks via CLI

---

## Phase 5: User Story 3 - Mark Tasks Complete (Priority: P1)

**Goal**: Users can toggle task completion status

**Independent Test**: Create task → mark complete → verify [X] → mark incomplete → verify [ ]

**Acceptance Criteria**:
- `todo mark <id> --complete` sets status to complete
- `todo mark <id> --incomplete` sets status to incomplete
- Status updates reflected in `todo list` output
- Error for invalid ID format: "Error: Invalid ID format"

### Tests for User Story 3

- [x] T021 [P] [US3] Write failing test in `tests/unit/use_cases/test_mark_complete.py`:
  - Test marking incomplete as complete
  - Test marking complete as incomplete
  - Test error on invalid ID

### Implementation for User Story 3

- [x] T022 [US3] Create MarkComplete use case in `src/core/use_cases/mark_complete.py`:
  - Depends on Repository port
  - Takes `id: int` and `complete: bool`
  - Calls repository method
  - Returns updated Todo
- [x] T023 [P] [US3] Add CLI mark subparser in `adapters/cli/argparse_adapter.py`:
  - `mark` subcommand with `--id`, `--complete`/`-c`, `--incomplete`/`-C`
  - Parse ID with validation
  - Print success message

**Checkpoint**: User Story 3 complete - can toggle task completion via CLI

---

## Phase 6: User Story 4 - Update Tasks (Priority: P2)

**Goal**: Users can modify task title and/or description

**Independent Test**: Create task → update title/description → verify changes persist

**Acceptance Criteria**:
- `todo update <id> --title "New title"` updates title only
- `todo update <id> --desc "New desc"` updates description only
- Both fields can be updated together
- Error on empty title: "Error: Title cannot be empty"
- Error on invalid ID: "Error: Invalid ID format"

### Tests for User Story 4

- [x] T024 [P] [US4] Write failing test in `tests/unit/use_cases/test_update_todo.py`:
  - Test updating title only
  - Test updating description only
  - Test updating both
  - Test error on empty title
  - Test error on invalid ID

### Implementation for User Story 4

- [x] T025 [US4] Create UpdateTodo use case in `src/core/use_cases/update_todo.py`:
  - Depends on Repository port
  - Validates title if provided
  - Updates only provided fields
  - Returns updated Todo
- [x] T026 [P] [US4] Add CLI update subparser in `adapters/cli/argparse_adapter.py`:
  - `update` subcommand with `--id`, `--title`/`-t`, `--description`/`-d`
  - Validate inputs
  - Handle errors

**Checkpoint**: User Story 4 complete - can update tasks via CLI

---

## Phase 7: User Story 5 - Delete Tasks (Priority: P2)

**Goal**: Users can remove tasks by ID

**Independent Test**: Create task → delete it → verify it no longer appears in list

**Acceptance Criteria**:
- `todo delete <id>` removes task from list
- Error on invalid ID: "Error: Invalid ID format"
- Deleted task ID is not reused

### Tests for User Story 5

- [x] T027 [P] [US5] Write failing test in `tests/unit/use_cases/test_delete_todo.py`:
  - Test deleting task by ID
  - Test error on invalid ID
  - Test deleted task not in list

### Implementation for User Story 5

- [x] T028 [US5] Create DeleteTodo use case in `src/core/use_cases/delete_todo.py`:
  - Depends on Repository port
  - Removes task from repository
- [x] T029 [P] [US5] Add CLI delete subparser in `adapters/cli/argparse_adapter.py`:
  - `delete` subcommand with `--id` flag
  - Validate ID
  - Print success message

**Checkpoint**: User Story 5 complete - can delete tasks via CLI

---

## Phase 8: User Story 6 - Interactive Mode (Priority: P1)

**Goal**: Users can enter an interactive menu-driven session to manage tasks without typing full commands for each operation.

**Independent Test**: Run `todolist interactive` → select menu options → verify operations work within session.

**Acceptance Criteria**:
- Interactive mode invoked via `todolist interactive` or `todolist --interactive`
- Menu displays options 1-6 with descriptions
- Option 7 exits the session
- All 5 core operations available through menu prompts
- Invalid input shows error and redisplays menu
- Session persists tasks between menu selections

### Tests for User Story 6

- [ ] T030 [P] [US6] Write failing test in `tests/integration/test_interactive_mode.py`:
  - Test starting interactive mode
  - Test menu displays all options
  - Test add task via interactive menu
  - Test list tasks via interactive menu
  - Test exit option terminates session

### Implementation for User Story 6

- [ ] T031 [US6] Create interactive mode function in `adapters/cli/__main__.py`:
  - `run_interactive()` function with menu loop
  - Display menu with numbered options 1-7
  - Handle user input and route to appropriate operations
  - Continue loop until user selects exit
- [ ] T032 [P] [US6] Add CLI interactive subparser in `adapters/cli/__main__.py`:
  - `interactive` subcommand
  - `--interactive` / `-i` flag as alternative entry point
  - Call `run_interactive()` function

**Checkpoint**: User Story 6 complete - can use interactive menu mode

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T033 [P] Add help command in `adapters/cli/__main__.py`:
  - `help` subcommand
  - Show all commands and usage
- [x] T034 [P] Add `--help` and `--version` global options:
  - Show help for any command with `--help`
  - Add version info to parser
- [x] T035 Write integration test in `tests/integration/test_cli_flow.py`:
  - Full user journey: add → list → mark → list → delete
- [x] T036 Update `pyproject.toml` with console scripts entry point:
  - `todolist = "adapters.cli.__main__:main"`
- [x] T037 Create README.md with setup and usage instructions
- [ ] T038 Run full test suite with `pytest --cov` to verify coverage

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User stories can proceed in parallel after Foundational
  - Or sequentially in priority order (US1 → US2 → US3 → US4 → US5)
- **User Story 6 (Phase 8)**: Can start after Foundational - No dependencies on other stories
- **Polish (Phase 9)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (Add)**: Can start after Foundational - No dependencies on other stories
- **User Story 2 (View)**: Can start after Foundational - No dependencies on other stories
- **User Story 3 (Mark Complete)**: Can start after Foundational - No dependencies on other stories
- **User Story 4 (Update)**: Can start after Foundational - No dependencies on other stories
- **User Story 5 (Delete)**: Can start after Foundational - No dependencies on other stories
- **User Story 6 (Interactive)**: Can start after Foundational - No dependencies on other stories

### Within Each User Story

1. Tests (TDD) MUST be written and FAIL before implementation
2. Use case implementation
3. CLI adapter implementation
4. Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel
- Once Foundational is done, all user stories can start in parallel
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1 (Add Tasks)
4. **STOP and VALIDATE**: Test adding tasks independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Add)
   - Developer B: User Story 2 (View)
   - Developer C: User Story 3 (Mark Complete)
   - Developer D: User Story 4 + 5 (Update + Delete)
3. Stories complete and integrate independently

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Write failing test in tests/unit/use_cases/test_add_todo.py"
Task: "Create AddTodo use case in src/core/use_cases/add_todo.py"
Task: "Create CLI add subparser in adapters/cli/argparse_adapter.py"
```

---

## Task Summary

| Phase | Tasks | Description |
|-------|-------|-------------|
| Phase 1: Setup | T001-T004 | Project initialization |
| Phase 2: Foundational | T005-T010 | Core domain, exceptions, repository |
| Phase 3: US1 (Add) | T011-T014 | Add tasks feature |
| Phase 4: US2 (View) | T015-T020 | List and get tasks |
| Phase 5: US3 (Mark) | T021-T023 | Toggle completion |
| Phase 6: US4 (Update) | T024-T026 | Update task details |
| Phase 7: US5 (Delete) | T027-T029 | Delete tasks |
| Phase 8: US6 (Interactive) | T030-T032 | Interactive menu mode |
| Phase 9: Polish | T033-T037 | Cross-cutting, integration, README |

**Total Tasks**: 37

**Tasks per User Story**:
- US1 (Add): 4 tasks (T011-T014)
- US2 (View): 6 tasks (T015-T020)
- US3 (Mark): 3 tasks (T021-T023)
- US4 (Update): 3 tasks (T024-T026)
- US5 (Delete): 3 tasks (T027-T029)
- US6 (Interactive): 3 tasks (T030-T032)

**MVP Scope**: Phase 1 + Phase 2 + Phase 3 = User Story 1 (Add Tasks)

**Parallel Opportunities**: 12 tasks marked with [P] can run in parallel
