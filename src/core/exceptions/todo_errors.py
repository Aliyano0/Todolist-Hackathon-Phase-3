"""Domain exceptions for the todo application."""


class TodoError(Exception):
    """Base exception for todo-related errors."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class TitleEmptyError(TodoError):
    """Raised when title is empty or whitespace-only."""

    def __init__(self) -> None:
        super().__init__("Title cannot be empty")


class TitleTooLongError(TodoError):
    """Raised when title exceeds 200 characters."""

    def __init__(self) -> None:
        super().__init__("Title cannot exceed 200 characters")


class TaskNotFoundError(TodoError):
    """Raised when task ID is not found."""

    def __init__(self, task_id: int) -> None:
        super().__init__(f"Task {task_id} not found")


class InvalidIdError(TodoError):
    """Raised when ID format is invalid."""

    def __init__(self) -> None:
        super().__init__("Invalid ID format")
