"""Use case for listing all todos."""

from src.core.entities.todo import Todo
from src.core.ports.repository import Repository


class ListTodos:
    """Use case for listing all todo items."""

    def __init__(self, repository: Repository) -> None:
        """Initialize with a repository."""
        self._repository = repository

    def execute(self) -> list[Todo]:
        """List all todo items.

        Returns:
            List of all todo items in creation order
        """
        return self._repository.list_all()
