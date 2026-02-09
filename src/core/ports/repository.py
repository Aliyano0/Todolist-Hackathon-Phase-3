"""Repository port for todo storage operations."""

from abc import ABC, abstractmethod
from typing import Protocol

from src.core.entities.todo import Todo


class Repository(Protocol):
    """Port for todo repository operations."""

    @abstractmethod
    def add(self, title: str, description: str | None) -> Todo:
        """Add a new todo item.

        Args:
            title: The title of the todo (1-200 chars, non-empty)
            description: Optional description of the todo

        Returns:
            The created Todo item with assigned ID
        """
        ...

    @abstractmethod
    def list_all(self) -> list[Todo]:
        """List all todo items.

        Returns:
            List of all todo items in creation order
        """
        ...

    @abstractmethod
    def get(self, id: int) -> Todo:
        """Get a todo item by ID.

        Args:
            id: The ID of the todo to retrieve

        Returns:
            The Todo item

        Raises:
            TaskNotFoundError: If no todo with the given ID exists
        """
        ...

    @abstractmethod
    def update(
        self, id: int, title: str | None, description: str | None
    ) -> Todo:
        """Update a todo item.

        Args:
            id: The ID of the todo to update
            title: New title (or None to keep existing)
            description: New description (or None to keep existing)

        Returns:
            The updated Todo item

        Raises:
            TaskNotFoundError: If no todo with the given ID exists
        """
        ...

    @abstractmethod
    def delete(self, id: int) -> None:
        """Delete a todo item by ID.

        Args:
            id: The ID of the todo to delete

        Raises:
            TaskNotFoundError: If no todo with the given ID exists
        """
        ...

    @abstractmethod
    def mark_complete(self, id: int, complete: bool) -> Todo:
        """Mark a todo item as complete or incomplete.

        Args:
            id: The ID of the todo to update
            complete: True to mark as complete, False to mark as incomplete

        Returns:
            The updated Todo item

        Raises:
            TaskNotFoundError: If no todo with the given ID exists
        """
        ...
