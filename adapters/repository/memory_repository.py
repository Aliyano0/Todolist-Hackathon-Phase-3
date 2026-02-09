"""In-memory implementation of the repository port."""

from datetime import datetime, timezone
from typing import Any

from src.core.entities.todo import Todo
from src.core.exceptions.todo_errors import TaskNotFoundError
from src.core.ports.repository import Repository


class MemoryRepository(Repository):
    """In-memory implementation of the Repository port."""

    def __init__(self) -> None:
        self._todos: list[Todo] = []
        self._next_id: int = 1

    def add(self, title: str, description: str | None) -> Todo:
        """Add a new todo item."""
        todo = Todo(
            id=self._next_id,
            title=title,
            description=description,
            completed=False,
            created_at=datetime.now(timezone.utc),
        )
        self._todos.append(todo)
        self._next_id += 1
        return todo

    def list_all(self) -> list[Todo]:
        """List all todo items."""
        return list(self._todos)

    def get(self, id: int) -> Todo:
        """Get a todo item by ID."""
        for todo in self._todos:
            if todo.id == id:
                return todo
        raise TaskNotFoundError(id)

    def update(
        self, id: int, title: str | None, description: str | None
    ) -> Todo:
        """Update a todo item."""
        todo = self.get(id)
        if title is not None:
            todo.update_title(title)
        if description is not None:
            todo.update_description(description)
        return todo

    def delete(self, id: int) -> None:
        """Delete a todo item by ID."""
        todo = self.get(id)
        self._todos.remove(todo)

    def mark_complete(self, id: int, complete: bool) -> Todo:
        """Mark a todo item as complete or incomplete."""
        todo = self.get(id)
        if complete:
            todo.complete()
        else:
            todo.mark_incomplete()
        return todo
