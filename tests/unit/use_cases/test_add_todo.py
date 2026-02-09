"""Tests for the AddTodo use case."""

import pytest

from src.core.exceptions.todo_errors import TitleEmptyError, TitleTooLongError


class TestAddTodoUseCase:
    """Tests for the AddTodo use case."""

    def test_add_todo_with_title_only(self, repository) -> None:
        """Test adding a todo with only a title."""
        from src.core.use_cases.add_todo import AddTodo

        use_case = AddTodo(repository)
        todo = use_case.execute("Buy groceries", None)

        assert todo.id == 1
        assert todo.title == "Buy groceries"
        assert todo.description is None
        assert todo.completed is False

    def test_add_todo_with_title_and_description(self, repository) -> None:
        """Test adding a todo with title and description."""
        from src.core.use_cases.add_todo import AddTodo

        use_case = AddTodo(repository)
        todo = use_case.execute("Buy groceries", "Milk, eggs, bread")

        assert todo.title == "Buy groceries"
        assert todo.description == "Milk, eggs, bread"

    def test_add_todo_empty_title_raises_error(self, repository) -> None:
        """Test that adding a todo with empty title raises error."""
        from src.core.use_cases.add_todo import AddTodo

        use_case = AddTodo(repository)
        with pytest.raises(TitleEmptyError):
            use_case.execute("", None)

    def test_add_todo_whitespace_title_raises_error(self, repository) -> None:
        """Test that adding a todo with whitespace-only title raises error."""
        from src.core.use_cases.add_todo import AddTodo

        use_case = AddTodo(repository)
        with pytest.raises(TitleEmptyError):
            use_case.execute("   ", None)

    def test_add_todo_title_too_long_raises_error(self, repository) -> None:
        """Test that adding a todo with title > 200 chars raises error."""
        from src.core.use_cases.add_todo import AddTodo

        use_case = AddTodo(repository)
        long_title = "x" * 201
        with pytest.raises(TitleTooLongError):
            use_case.execute(long_title, None)

    def test_add_multiple_todos(self, repository) -> None:
        """Test adding multiple todos increments IDs."""
        from src.core.use_cases.add_todo import AddTodo

        use_case = AddTodo(repository)
        todo1 = use_case.execute("First", None)
        todo2 = use_case.execute("Second", None)
        todo3 = use_case.execute("Third", None)

        assert todo1.id == 1
        assert todo2.id == 2
        assert todo3.id == 3
