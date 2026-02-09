"""Tests for the UpdateTodo use case."""

import pytest

from adapters.repository.memory_repository import MemoryRepository
from src.core.exceptions.todo_errors import TitleEmptyError
from src.core.use_cases.update_todo import UpdateTodo


class TestUpdateTodoUseCase:
    """Tests for the UpdateTodo use case."""

    def test_update_title_only(self) -> None:
        """Test updating only the title."""
        repo = MemoryRepository()
        repo.add("Buy groceries", None)
        use_case = UpdateTodo(repo)

        todo = use_case.execute(1, "Buy milk", None)

        assert todo.title == "Buy milk"
        assert todo.description is None

    def test_update_description_only(self) -> None:
        """Test updating only the description."""
        repo = MemoryRepository()
        repo.add("Buy groceries", None)
        use_case = UpdateTodo(repo)

        todo = use_case.execute(1, None, "Milk, eggs, bread")

        assert todo.title == "Buy groceries"
        assert todo.description == "Milk, eggs, bread"

    def test_update_both(self) -> None:
        """Test updating both title and description."""
        repo = MemoryRepository()
        repo.add("Buy groceries", None)
        use_case = UpdateTodo(repo)

        todo = use_case.execute(1, "Buy milk", "Full description")

        assert todo.title == "Buy milk"
        assert todo.description == "Full description"

    def test_update_empty_title_raises_error(self) -> None:
        """Test that updating with empty title raises error."""
        repo = MemoryRepository()
        repo.add("Buy groceries", None)
        use_case = UpdateTodo(repo)

        with pytest.raises(TitleEmptyError):
            use_case.execute(1, "", None)

    def test_update_whitespace_title_raises_error(self) -> None:
        """Test that updating with whitespace title raises error."""
        repo = MemoryRepository()
        repo.add("Buy groceries", None)
        use_case = UpdateTodo(repo)

        with pytest.raises(TitleEmptyError):
            use_case.execute(1, "   ", None)

    def test_update_nonexistent_raises_error(self) -> None:
        """Test that updating a non-existent task raises error."""
        from src.core.exceptions.todo_errors import TaskNotFoundError

        repo = MemoryRepository()
        use_case = UpdateTodo(repo)

        with pytest.raises(TaskNotFoundError):
            use_case.execute(999, "New title", None)
