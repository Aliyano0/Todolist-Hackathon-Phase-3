"""Use case for updating a todo."""

from src.core.entities.todo import Todo
from src.core.exceptions.todo_errors import TitleEmptyError, TitleTooLongError
from src.core.ports.repository import Repository


class UpdateTodo:
    """Use case for updating a todo item."""

    def __init__(self, repository: Repository) -> None:
        """Initialize with a repository."""
        self._repository = repository

    def execute(
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
            TitleEmptyError: If title is provided but empty or whitespace-only
            TitleTooLongError: If title exceeds 200 characters
            TaskNotFoundError: If no todo with the given ID exists
        """
        # Validate title if provided
        if title is not None:
            stripped_title = title.strip()
            if not stripped_title:
                raise TitleEmptyError()
            if len(stripped_title) > 200:
                raise TitleTooLongError()
            title = stripped_title

        return self._repository.update(id, title, description)
