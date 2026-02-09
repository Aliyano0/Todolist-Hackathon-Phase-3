"""Tests for the GetTodo use case."""

import pytest

from adapters.repository.memory_repository import MemoryRepository
from src.core.exceptions.todo_errors import TaskNotFoundError
from src.core.use_cases.get_todo import GetTodo


class TestGetTodoUseCase:
    """Tests for the GetTodo use case."""

    def test_get_existing_task(self) -> None:
        """Test getting an existing task."""
        repo = MemoryRepository()
        repo.add("Buy groceries", "Milk, eggs, bread")
        use_case = GetTodo(repo)

        todo = use_case.execute(1)

        assert todo.id == 1
        assert todo.title == "Buy groceries"
        assert todo.description == "Milk, eggs, bread"
        assert todo.completed is False

    def test_get_nonexistent_task_raises_error(self) -> None:
        """Test that getting a non-existent task raises error."""
        repo = MemoryRepository()
        use_case = GetTodo(repo)

        with pytest.raises(TaskNotFoundError):
            use_case.execute(999)

    def test_get_returns_all_fields(self) -> None:
        """Test that get returns all task fields."""
        repo = MemoryRepository()
        repo.add("Task", "Description")
        use_case = GetTodo(repo)

        todo = use_case.execute(1)

        assert hasattr(todo, "id")
        assert hasattr(todo, "title")
        assert hasattr(todo, "description")
        assert hasattr(todo, "completed")
        assert hasattr(todo, "created_at")
