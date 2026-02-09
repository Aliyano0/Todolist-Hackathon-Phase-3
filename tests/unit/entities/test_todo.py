"""Tests for the Todo entity."""

import pytest
from datetime import datetime, timezone

from src.core.entities.todo import Todo
from src.core.exceptions.todo_errors import TitleEmptyError, TitleTooLongError


class TestTodoCreation:
    """Tests for Todo entity creation."""

    def test_create_todo_with_minimal_fields(self) -> None:
        """Test creating a todo with only required fields."""
        todo = Todo(id=1, title="Buy groceries", description=None, completed=False)
        assert todo.id == 1
        assert todo.title == "Buy groceries"
        assert todo.description is None
        assert todo.completed is False
        assert isinstance(todo.created_at, datetime)

    def test_create_todo_with_all_fields(self) -> None:
        """Test creating a todo with all fields."""
        created_at = datetime.now(timezone.utc)
        todo = Todo(
            id=1,
            title="Buy groceries",
            description="Milk, eggs, bread",
            completed=False,
            created_at=created_at,
        )
        assert todo.id == 1
        assert todo.title == "Buy groceries"
        assert todo.description == "Milk, eggs, bread"
        assert todo.completed is False
        assert todo.created_at == created_at


class TestTodoValidation:
    """Tests for Todo title validation."""

    def test_empty_title_raises_error(self) -> None:
        """Test that empty title raises TitleEmptyError."""
        with pytest.raises(TitleEmptyError):
            Todo(id=1, title="", description=None, completed=False)

    def test_whitespace_only_title_raises_error(self) -> None:
        """Test that whitespace-only title raises TitleEmptyError."""
        with pytest.raises(TitleEmptyError):
            Todo(id=1, title="   ", description=None, completed=False)

    def test_title_too_long_raises_error(self) -> None:
        """Test that title exceeding 200 chars raises TitleTooLongError."""
        long_title = "x" * 201
        with pytest.raises(TitleTooLongError):
            Todo(id=1, title=long_title, description=None, completed=False)

    def test_title_exactly_200_chars_is_valid(self) -> None:
        """Test that title of exactly 200 chars is valid."""
        title = "x" * 200
        todo = Todo(id=1, title=title, description=None, completed=False)
        assert todo.title == title


class TestTodoCompletion:
    """Tests for task completion status."""

    def test_complete_sets_completed_true(self) -> None:
        """Test that complete() sets completed to True."""
        todo = Todo(id=1, title="Buy groceries", description=None, completed=False)
        assert todo.completed is False
        todo.complete()
        assert todo.completed is True

    def test_mark_incomplete_sets_completed_false(self) -> None:
        """Test that mark_incomplete() sets completed to False."""
        todo = Todo(id=1, title="Buy groceries", description=None, completed=True)
        assert todo.completed is True
        todo.mark_incomplete()
        assert todo.completed is False


class TestTodoUpdate:
    """Tests for task updates."""

    def test_update_title(self) -> None:
        """Test updating the title."""
        todo = Todo(id=1, title="Buy groceries", description=None, completed=False)
        todo.update_title("Buy groceries and household items")
        assert todo.title == "Buy groceries and household items"

    def test_update_title_validates(self) -> None:
        """Test that updating title still validates."""
        todo = Todo(id=1, title="Buy groceries", description=None, completed=False)
        with pytest.raises(TitleEmptyError):
            todo.update_title("")

    def test_update_description(self) -> None:
        """Test updating the description."""
        todo = Todo(id=1, title="Buy groceries", description=None, completed=False)
        todo.update_description("Milk, eggs, bread, cheese")
        assert todo.description == "Milk, eggs, bread, cheese"

    def test_update_description_to_none(self) -> None:
        """Test setting description to None."""
        todo = Todo(id=1, title="Buy groceries", description="Old", completed=False)
        todo.update_description(None)
        assert todo.description is None
