"""Tests for the MemoryRepository implementation."""

import pytest

from adapters.repository.memory_repository import MemoryRepository
from src.core.exceptions.todo_errors import TaskNotFoundError


class TestMemoryRepositoryAdd:
    """Tests for the add operation."""

    def test_add_first_task(self) -> None:
        """Test adding the first task."""
        repo = MemoryRepository()
        todo = repo.add("Buy groceries", None)
        assert todo.id == 1
        assert todo.title == "Buy groceries"
        assert todo.description is None
        assert todo.completed is False

    def test_add_multiple_tasks(self) -> None:
        """Test adding multiple tasks."""
        repo = MemoryRepository()
        todo1 = repo.add("Buy groceries", None)
        todo2 = repo.add("Call mom", "Discuss weekend")
        assert todo1.id == 1
        assert todo2.id == 2

    def test_add_with_description(self) -> None:
        """Test adding a task with description."""
        repo = MemoryRepository()
        todo = repo.add("Buy groceries", "Milk, eggs, bread")
        assert todo.description == "Milk, eggs, bread"


class TestMemoryRepositoryListAll:
    """Tests for the list_all operation."""

    def test_list_empty(self) -> None:
        """Test listing when empty."""
        repo = MemoryRepository()
        assert repo.list_all() == []

    def test_list_all_returns_in_order(self) -> None:
        """Test that list_all returns tasks in creation order."""
        repo = MemoryRepository()
        repo.add("First", None)
        repo.add("Second", None)
        repo.add("Third", None)
        todos = repo.list_all()
        assert len(todos) == 3
        assert todos[0].title == "First"
        assert todos[1].title == "Second"
        assert todos[2].title == "Third"


class TestMemoryRepositoryGet:
    """Tests for the get operation."""

    def test_get_existing_task(self) -> None:
        """Test getting an existing task."""
        repo = MemoryRepository()
        repo.add("Buy groceries", None)
        todo = repo.get(1)
        assert todo.title == "Buy groceries"

    def test_get_nonexistent_task(self) -> None:
        """Test getting a non-existent task raises error."""
        repo = MemoryRepository()
        with pytest.raises(TaskNotFoundError):
            repo.get(999)


class TestMemoryRepositoryUpdate:
    """Tests for the update operation."""

    def test_update_title(self) -> None:
        """Test updating the title."""
        repo = MemoryRepository()
        repo.add("Buy groceries", None)
        todo = repo.update(1, "Buy milk", None)
        assert todo.title == "Buy milk"

    def test_update_description(self) -> None:
        """Test updating the description."""
        repo = MemoryRepository()
        repo.add("Buy groceries", None)
        todo = repo.update(1, None, "New description")
        assert todo.description == "New description"

    def test_update_both(self) -> None:
        """Test updating both title and description."""
        repo = MemoryRepository()
        repo.add("Buy groceries", None)
        todo = repo.update(1, "Buy milk", "New description")
        assert todo.title == "Buy milk"
        assert todo.description == "New description"


class TestMemoryRepositoryDelete:
    """Tests for the delete operation."""

    def test_delete_task(self) -> None:
        """Test deleting a task."""
        repo = MemoryRepository()
        repo.add("Buy groceries", None)
        repo.add("Call mom", None)
        assert len(repo.list_all()) == 2
        repo.delete(1)
        assert len(repo.list_all()) == 1
        assert repo.list_all()[0].id == 2

    def test_delete_nonexistent_task(self) -> None:
        """Test deleting a non-existent task raises error."""
        repo = MemoryRepository()
        with pytest.raises(TaskNotFoundError):
            repo.delete(999)


class TestMemoryRepositoryMarkComplete:
    """Tests for the mark_complete operation."""

    def test_mark_complete(self) -> None:
        """Test marking a task as complete."""
        repo = MemoryRepository()
        repo.add("Buy groceries", None)
        todo = repo.mark_complete(1, True)
        assert todo.completed is True

    def test_mark_incomplete(self) -> None:
        """Test marking a complete task as incomplete."""
        repo = MemoryRepository()
        repo.add("Buy groceries", None)
        repo.mark_complete(1, True)
        todo = repo.mark_complete(1, False)
        assert todo.completed is False

    def test_mark_complete_nonexistent(self) -> None:
        """Test marking a non-existent task raises error."""
        repo = MemoryRepository()
        with pytest.raises(TaskNotFoundError):
            repo.mark_complete(999, True)
