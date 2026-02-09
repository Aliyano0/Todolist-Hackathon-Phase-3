"""Tests for the ListTodos use case."""

import pytest

from adapters.repository.memory_repository import MemoryRepository
from src.core.use_cases.list_todos import ListTodos
from src.core.ports.repository import Repository


class TestListTodosUseCase:
    """Tests for the ListTodos use case."""

    def test_list_empty(self) -> None:
        """Test listing when there are no tasks."""
        repo: Repository = MemoryRepository()
        use_case = ListTodos(repo)
        todos = use_case.execute()
        assert todos == []

    def test_list_all_returns_in_order(self) -> None:
        """Test that list returns tasks in creation order."""
        repo = MemoryRepository()
        repo.add("First", None)
        repo.add("Second", None)
        repo.add("Third", None)

        use_case = ListTodos(repo)
        todos = use_case.execute()

        assert len(todos) == 3
        assert todos[0].title == "First"
        assert todos[1].title == "Second"
        assert todos[2].title == "Third"

    def test_list_with_completed_tasks(self) -> None:
        """Test listing tasks with mixed completion status."""
        repo = MemoryRepository()
        todo1 = repo.add("Task 1", None)
        todo2 = repo.add("Task 2", None)
        repo.mark_complete(todo1.id, True)

        use_case = ListTodos(repo)
        todos = use_case.execute()

        assert len(todos) == 2
        assert todos[0].completed is True
        assert todos[1].completed is False
