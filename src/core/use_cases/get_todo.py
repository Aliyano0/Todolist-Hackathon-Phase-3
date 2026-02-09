"""Use case for getting a single todo."""

from src.core.entities.todo import Todo
from src.core.exceptions.todo_errors import TaskNotFoundError
from src.core.ports.repository import Repository


class GetTodo:
    """Use case for getting a single todo item by ID."""

    def __init__(self, repository: Repository) -> None:
        """Initialize with a repository."""
        self._repository = repository

    def execute(self, id: int) -> Todo:
        """Get a todo item by ID.

        Args:
            id: The ID of the todo to retrieve

        Returns:
            The Todo item

        Raises:
            TaskNotFoundError: If no todo with the given ID exists
        """
        try:
            return self._repository.get(id)
        except TaskNotFoundError:
            raise
