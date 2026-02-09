"""Use case for adding a new todo."""

from src.core.entities.todo import Todo
from src.core.exceptions.todo_errors import TitleEmptyError, TitleTooLongError
from src.core.ports.repository import Repository


class AddTodo:
    """Use case for adding a new todo item."""

    def __init__(self, repository: Repository) -> None:
        """Initialize with a repository."""
        self._repository = repository

    def execute(self, title: str, description: str | None) -> Todo:
        """Add a new todo item.

        Args:
            title: The title of the todo (1-200 chars, non-empty)
            description: Optional description of the todo

        Returns:
            The created Todo item with assigned ID

        Raises:
            TitleEmptyError: If title is empty or whitespace-only
            TitleTooLongError: If title exceeds 200 characters
        """
        # Validate title
        stripped_title = title.strip()
        if not stripped_title:
            raise TitleEmptyError()
        if len(stripped_title) > 200:
            raise TitleTooLongError()

        return self._repository.add(stripped_title, description)
