"""Use case for marking a todo complete/incomplete."""

from src.core.entities.todo import Todo
from src.core.ports.repository import Repository


class MarkComplete:
    """Use case for marking a todo as complete or incomplete."""

    def __init__(self, repository: Repository) -> None:
        """Initialize with a repository."""
        self._repository = repository

    def execute(self, id: int, complete: bool) -> Todo:
        """Mark a todo item as complete or incomplete.

        Args:
            id: The ID of the todo to update
            complete: True to mark as complete, False to mark as incomplete

        Returns:
            The updated Todo item

        Raises:
            TaskNotFoundError: If no todo with the given ID exists
        """
        return self._repository.mark_complete(id, complete)
