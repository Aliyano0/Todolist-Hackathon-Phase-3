# Data Model: Todo Console App

**Date**: 2026-01-02
**Feature**: Todo Console App (001-todo-console-app)

## Entities

### Todo

Represents a single task item.

```python
@dataclass
class Todo:
    id: int                      # Unique identifier (1-based, auto-increment)
    title: str                   # Task title (1-200 chars, non-empty)
    description: str | None      # Optional description (None or any length)
    completed: bool              # Completion status (default False)
    created_at: datetime         # Creation timestamp (UTC)
```

#### Field Specifications

| Field | Type | Constraints | Validation |
|-------|------|-------------|------------|
| id | int | > 0, sequential | Auto-assigned by repository |
| title | str | 1-200 chars, not whitespace-only | Trimmed, validated before save |
| description | str \| None | Optional, any length | None or non-empty string |
| completed | bool | N/A | Default False |
| created_at | datetime | N/A | UTC timestamp at creation |

#### State Transitions

```
┌─────────────┐     mark_complete()     ┌─────────────┐
│  incomplete │ ─────────────────────→ │   complete  │
└─────────────┘                        └─────────────┘
       ↑                                   |
       |                            mark_incomplete()
       └───────────────────────────────────┘
```

### TodoList

Container for managing Todo entities. Not an entity itself, but the aggregate root.

```python
class TodoList:
    def add(self, title: str, description: str | None = None) -> Todo: ...
    def list_all(self) -> list[Todo]: ...
    def get(self, id: int) -> Todo: ...
    def update(self, id: int, title: str | None, description: str | None) -> Todo: ...
    def delete(self, id: int) -> None: ...
    def mark_complete(self, id: int, complete: bool) -> Todo: ...
```

## Value Objects

### Title

```python
@dataclass(frozen=True)
class Title:
    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise TitleEmptyError("Title cannot be empty")
        if len(self.value) > 200:
            raise TitleTooLongError("Title cannot exceed 200 characters")
```

## Domain Exceptions

### Exception Hierarchy

```
TodoError (base)
├── TitleEmptyError
├── TitleTooLongError
├── TaskNotFoundError
└── InvalidIdError
```

### Error Messages

| Exception | Message Format |
|-----------|----------------|
| TitleEmptyError | "Title cannot be empty" |
| TitleTooLongError | "Title cannot exceed 200 characters" |
| TaskNotFoundError | "Task not found" |
| InvalidIdError | "Invalid ID format" |

## Repository Interface (Port)

```python
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Protocol

class Repository(Protocol):
    """Port for todo repository operations."""

    def add(self, title: str, description: str | None) -> Todo: ...
    def list_all(self) -> list[Todo]: ...
    def get(self, id: int) -> Todo: ...
    def update(self, id: int, title: str | None, description: str | None) -> Todo: ...
    def delete(self, id: int) -> None: ...
    def mark_complete(self, id: int, complete: bool) -> Todo: ...
```

## Data Storage Schema

### In-Memory Implementation

```python
class MemoryRepository:
    def __init__(self) -> None:
        self._todos: list[Todo] = []
        self._next_id: int = 1
```

| Storage | Type | Description |
|---------|------|-------------|
| _todos | list[Todo] | Ordered list maintaining creation order |
| _next_id | int | Auto-incrementing ID counter |

### Data Invariants

1. IDs are unique and never reused
2. List order reflects creation order (newest at end)
3. All Todo objects in list have valid state

## Validation Rules

### Title Validation

```python
def validate_title(title: str) -> str:
    stripped = title.strip()
    if not stripped:
        raise TitleEmptyError("Title cannot be empty")
    if len(stripped) > 200:
        raise TitleTooLongError("Title cannot exceed 200 characters")
    return stripped
```

### ID Validation

```python
def parse_id(raw: str) -> int:
    try:
        id = int(raw)
        if id < 1:
            raise InvalidIdError("Invalid ID format")
        return id
    except ValueError:
        raise InvalidIdError("Invalid ID format")
```
