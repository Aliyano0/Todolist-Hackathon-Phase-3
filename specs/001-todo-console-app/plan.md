# Implementation Plan: Todo Console App

**Branch**: `001-todo-console-app` | **Date**: 2026-01-02 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-todo-console-app/spec.md`

## Summary

Build an in-memory Python console todo application following clean architecture principles. The application provides five core CLI commands: add, list, get, update, delete, and mark-complete. All domain logic resides in `src/core/` with zero external dependencies. The app uses UV for project management and pytest for testing. Implementation follows TDD with 100% unit test coverage for core domain code.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: None (standard library only)
**Storage**: In-memory dict/list (session-only)
**Testing**: pytest
**Target Platform**: Cross-platform CLI (Linux, macOS, Windows)
**Project Type**: Single console application
**Performance Goals**: Command execution under 1 second; test suite under 5 seconds
**Constraints**: 200-character title limit; 10 max cyclomatic complexity; 50-line max function length
**Scale/Scope**: Single-user; up to 1000 tasks per session (memory limit only)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Product Architect Mindset | PASS | Architecture decisions documented |
| II. Clean Architecture Mandatory | PASS | Domain/ports/adapters structure defined |
| III. Simplicity First | PASS | Minimal implementation per feature |
| IV. Five Core Features Only | PASS | Scope constrained to 5 features |
| V. Zero Persistence Mandate | PASS | In-memory only, no file/DB I/O |
| VI. Standard Library Only | PASS | No third-party CLI frameworks |
| VII. TDD (Non-Negotiable) | PASS | Red-Green-Refactor enforced |

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-console-app/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   └── cli-commands.md
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code

```text
src/
└── core/
    ├── entities/
    │   └── todo.py           # Todo entity, value objects
    ├── ports/
    │   ├── repository.py     # Repository port (interface)
    │   └── cli.py            # CLI port (interface)
    ├── use_cases/
    │   ├── add_todo.py
    │   ├── list_todos.py
    │   ├── get_todo.py
    │   ├── update_todo.py
    │   ├── delete_todo.py
    │   └── mark_complete.py
    └── exceptions/
        └── todo_errors.py    # Domain exceptions

adapters/
├── cli/
│   └── argparse_adapter.py   # argparse implementation
└── repository/
    └── memory_repository.py  # In-memory implementation

tests/
├── unit/
│   ├── entities/
│   │   └── test_todo.py
│   ├── use_cases/
│   │   ├── test_add_todo.py
│   │   ├── test_list_todos.py
│   │   ├── test_get_todo.py
│   │   ├── test_update_todo.py
│   │   ├── test_delete_todo.py
│   │   └── test_mark_complete.py
│   └── ports/
│       └── test_repository.py
└── integration/
    └── test_cli_flow.py

pyproject.toml     # UV project configuration
README.md
```

**Structure Decision**: Single project with clean architecture separation. `src/core/` contains domain logic with zero dependencies. `adapters/` contains I/O implementations. Tests mirror the source structure for clear mapping.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | No violations | N/A |

## Phase 0: Research Summary

All technical decisions resolved from constitution and spec. No additional research needed.

- **CLI Framework**: Use argparse (standard library) per Constitution VI
- **Testing**: Use pytest (standard Python testing)
- **Project Management**: Use UV per constitution amendment
- **Data Storage**: In-memory list per Constitution V

## Phase 1: Design Artifacts

### Key Design Decisions

1. **Todo Entity**: Simple dataclass with id, title, description, completed, created_at
2. **Repository Port**: Abstract base class defining CRUD operations
3. **Use Cases**: One class per operation, depending only on repository port
4. **CLI Adapter**: argparse subparsers for each command, depends on use cases
5. **Error Handling**: Domain exceptions raised by use cases, caught by CLI adapter

### Data Flow

```
CLI (argparse) → Use Case → Repository Port → Memory Repository → Todo Entity
                   ↓
              Domain Exception → CLI Adapter → stderr
```
