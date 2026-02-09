"""Tests for the MarkComplete use case."""

import pytest

from adapters.repository.memory_repository import MemoryRepository
from src.core.use_cases.mark_complete import MarkComplete


class TestMarkCompleteUseCase:
    """Tests for the MarkComplete use case."""

    def test_mark_incomplete_as_complete(self) -> None:
        """Test marking an incomplete task as complete."""
        repo = MemoryRepository()
        repo.add("Buy groceries", None)
        use_case = MarkComplete(repo)

        todo = use_case.execute(1, True)

        assert todo.completed is True

    def test_mark_complete_as_incomplete(self) -> None:
        """Test marking a complete task as incomplete."""
        repo = MemoryRepository()
        todo = repo.add("Buy groceries", None)
        repo.mark_complete(todo.id, True)
        use_case = MarkComplete(repo)

        todo = use_case.execute(1, False)

        assert todo.completed is False

    def test_mark_nonexistent_raises_error(self) -> None:
        """Test that marking a non-existent task raises error."""
        from src.core.exceptions.todo_errors import TaskNotFoundError

        repo = MemoryRepository()
        use_case = MarkComplete(repo)

        with pytest.raises(TaskNotFoundError):
            use_case.execute(999, True)
