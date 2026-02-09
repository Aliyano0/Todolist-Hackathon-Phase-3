"""Tests for the DeleteTodo use case."""

import pytest

from adapters.repository.memory_repository import MemoryRepository
from src.core.exceptions.todo_errors import TaskNotFoundError
from src.core.use_cases.delete_todo import DeleteTodo


class TestDeleteTodoUseCase:
    """Tests for the DeleteTodo use case."""

    def test_delete_task(self) -> None:
        """Test deleting a task."""
        repo = MemoryRepository()
        repo.add("Buy groceries", None)
        repo.add("Call mom", None)
        use_case = DeleteTodo(repo)

        use_case.execute(1)

        todos = repo.list_all()
        assert len(todos) == 1
        assert todos[0].id == 2

    def test_delete_nonexistent_raises_error(self) -> None:
        """Test that deleting a non-existent task raises error."""
        repo = MemoryRepository()
        use_case = DeleteTodo(repo)

        with pytest.raises(TaskNotFoundError):
            use_case.execute(999)

    def test_delete_preserves_order(self) -> None:
        """Test that deleting preserves order of remaining tasks."""
        repo = MemoryRepository()
        repo.add("First", None)
        repo.add("Second", None)
        repo.add("Third", None)
        use_case = DeleteTodo(repo)

        use_case.execute(2)

        todos = repo.list_all()
        assert len(todos) == 2
        assert todos[0].title == "First"
        assert todos[1].title == "Third"
