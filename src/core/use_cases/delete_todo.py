"""Use case for deleting a todo."""

from src.core.ports.repository import Repository


class DeleteTodo:
    """Use case for deleting a todo item."""

    def __init__(self, repository: Repository) -> None:
        """Initialize with a repository."""
        self._repository = repository

    def execute(self, id: int) -> None:
        """Delete a todo item by ID.

        Args:
            id: The ID of the todo to delete

        Raises:
            TaskNotFoundError: If no todo with the given ID exists
        """
        self._repository.delete(id)
