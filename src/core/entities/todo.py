"""Todo entity representing a single task item."""

from dataclasses import dataclass, field
from datetime import datetime, timezone

from src.core.exceptions.todo_errors import TitleEmptyError, TitleTooLongError


@dataclass
class Todo:
    """Represents a single task item."""

    id: int
    title: str
    description: str | None
    completed: bool
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self) -> None:
        """Validate the todo after initialization."""
        self._validate_title(self.title)

    @staticmethod
    def _validate_title(title: str) -> None:
        """Validate that the title is not empty and within length limits."""
        stripped = title.strip()
        if not stripped:
            raise TitleEmptyError()
        if len(stripped) > 200:
            raise TitleTooLongError()

    def complete(self) -> None:
        """Mark this task as complete."""
        self.completed = True

    def mark_incomplete(self) -> None:
        """Mark this task as incomplete."""
        self.completed = False

    def update_title(self, new_title: str) -> None:
        """Update the title of this task."""
        self._validate_title(new_title)
        self.title = new_title

    def update_description(self, new_description: str | None) -> None:
        """Update the description of this task."""
        self.description = new_description
