# Research: Todo Console App

**Date**: 2026-01-02
**Feature**: Todo Console App (001-todo-console-app)

## Overview

This document captures research findings for the Todo Console App implementation. All decisions are derived from the project constitution and feature specification.

## Technology Decisions

### CLI Framework: argparse (Standard Library)

**Decision**: Use `argparse` from Python standard library

**Rationale**:
- Constitution VI mandates "Standard library only; no external CLI libraries"
- argparse is the built-in solution for CLI argument parsing
- Supports subparsers for command organization (add, list, get, etc.)
- Familiar to Python developers; well-documented

**Alternatives Considered**:
- Click/Typer: Rejected - third-party library prohibited by constitution
- Manual parsing: Rejected - error-prone, less maintainable
- sys.argv: Rejected - no structure for complex CLI needs

### Testing Framework: pytest

**Decision**: Use pytest for unit and integration testing

**Rationale**:
- pytest is the de facto standard for Python testing
- Built into most Python distributions or easily installable
- Supports fixtures, parametrize, and clean test discovery
- Compatible with TDD workflow

**Alternatives Considered**:
- unittest: More verbose; pytest offers cleaner syntax
- doctest: Limited to documentation examples
- hypothesis: Useful for property-based testing but adds complexity

### Project Management: UV

**Decision**: Use UV for package management and virtual environments

**Rationale**:
- Constitution amendment specifies "Use UV to initialize the project and use UV venv"
- UV is a fast Python package manager written in Rust
- Creates isolated environments without pip/virtualenv overhead
- Compatible with pyproject.toml

### Data Storage: In-Memory

**Decision**: Use Python list/dict for in-memory storage

**Rationale**:
- Constitution V mandates "Zero Persistence Mandate"
- In-memory is simplest for session-only data
- No serialization/deserialization complexity
- Phase II will replace with persistent storage

**Implementation**:
```python
# Simple in-memory storage
todos: list[Todo] = []
next_id: int = 1
```

## Clean Architecture Implementation

### Layer Structure

```
src/core/           # Domain layer - zero external dependencies
├── entities/       # Business entities (Todo)
├── use_cases/      # Business logic (AddTodo, ListTodos, etc.)
├── ports/          # Interfaces (Repository, CLI)
└── exceptions/     # Domain exceptions

adapters/           # I/O layer - implements ports
├── cli/            # argparse adapter
└── repository/     # In-memory repository
```

### Dependency Rule

- Inner layers (entities, use_cases) know nothing about outer layers
- Outer layers (adapters) depend on inner layer interfaces
- All dependencies point inward

### Port/Adapter Pattern

**Repository Port** (interface in src/core/ports/):
```python
class Repository(ABC):
    @abstractmethod
    def add(self, title: str, description: str | None) -> Todo: ...
    @abstractmethod
    def list_all(self) -> list[Todo]: ...
    # ... other CRUD operations
```

**Memory Repository** (implementation in adapters/repository/):
```python
class MemoryRepository(Repository):
    def __init__(self) -> None:
        self._todos: list[Todo] = []
        self._next_id: int = 1
```

## Error Handling Strategy

### Domain Exceptions

```python
class TodoError(Exception):
    """Base exception for todo-related errors."""

class TitleEmptyError(TodoError):
    """Raised when title is empty or whitespace."""

class TitleTooLongError(TodoError):
    """Raised when title exceeds 200 characters."""

class TaskNotFoundError(TodoError):
    """Raised when task ID not found."""

class InvalidIdError(TodoError):
    """Raised when ID format is invalid."""
```

### Error Flow

1. Use case validates input and raises domain exception
2. CLI adapter catches exception and prints "Error: <message>"
3. Non-zero exit code for error conditions

## File Structure Decisions

### Project Root Layout

```
pyproject.toml      # UV config, dependencies, entry point
README.md           # Setup and usage instructions
src/core/           # Domain logic (importable)
tests/              # Test suite
```

### Why This Structure?

- Clean separation of domain (src/core/) from adapters
- Tests mirror source structure for discoverability
- pyproject.toml at root for UV recognition
- No src/ prefix for adapters to keep structure flat

## Conclusion

All technical decisions align with the project constitution:
- Standard library only (no third-party dependencies)
- Clean architecture with ports and adapters
- In-memory storage for Phase I
- pytest for testing
- UV for project management
