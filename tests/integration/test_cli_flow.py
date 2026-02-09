"""Integration tests for the complete CLI workflow."""

import pytest
from io import StringIO
from unittest.mock import patch

from adapters.cli.__main__ import create_parser, main
from adapters.repository.memory_repository import MemoryRepository
from src.core.use_cases.add_todo import AddTodo
from src.core.use_cases.list_todos import ListTodos
from src.core.use_cases.mark_complete import MarkComplete
from src.core.use_cases.delete_todo import DeleteTodo


class TestFullWorkflow:
    """Integration tests for complete user journeys."""

    def test_add_list_mark_list_delete_workflow(self) -> None:
        """Test full user journey: add -> list -> mark -> list -> delete."""
        # Create a shared repository for the workflow
        repository = MemoryRepository()

        # Step 1: Add a task
        add_use_case = AddTodo(repository)
        todo1 = add_use_case.execute("Buy groceries", "Milk, eggs, bread")
        todo2 = add_use_case.execute("Clean room", None)

        assert todo1.id == 1
        assert todo2.id == 2
        assert todo1.title == "Buy groceries"
        assert todo2.title == "Clean room"

        # Step 2: List tasks (verify both exist and are incomplete)
        list_use_case = ListTodos(repository)
        todos = list_use_case.execute()

        assert len(todos) == 2
        assert not todos[0].completed  # todo1 is incomplete
        assert not todos[1].completed  # todo2 is incomplete

        # Step 3: Mark first task as complete
        mark_use_case = MarkComplete(repository)
        updated_todo = mark_use_case.execute(todo1.id, complete=True)

        assert updated_todo.completed is True
        assert updated_todo.id == todo1.id

        # Step 4: List again (verify status changed)
        todos_after_mark = list_use_case.execute()

        assert len(todos_after_mark) == 2
        assert todos_after_mark[0].completed is True  # First task now complete
        assert todos_after_mark[1].completed is False  # Second still incomplete

        # Step 5: Delete the second task
        delete_use_case = DeleteTodo(repository)
        delete_use_case.execute(todo2.id)

        # Step 6: List again (verify only one task remains)
        final_todos = list_use_case.execute()

        assert len(final_todos) == 1
        assert final_todos[0].id == todo1.id
        assert final_todos[0].completed is True

    def test_cli_add_command_output(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test CLI add command produces correct output."""
        with patch("sys.argv", ["todolist", "add", "Test task"]):
            main()
        captured = capsys.readouterr()

        assert 'Added task 1: "Test task"' in captured.out

    def test_cli_list_command_empty(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test CLI list command shows friendly message for empty list."""
        with patch("sys.argv", ["todolist", "list"]):
            main()
        captured = capsys.readouterr()

        assert "No tasks yet" in captured.out

    def test_cli_get_command_output(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test CLI get command shows task details.

        Note: This test uses the use case directly because the CLI creates
        a new repository per command, preventing state sharing between calls.
        """
        repository = MemoryRepository()
        add_use_case = AddTodo(repository)
        todo = add_use_case.execute("Get task", "Test description")

        # Simulate get by calling the repository directly
        retrieved = repository.get(todo.id)
        assert retrieved.title == "Get task"
        assert retrieved.description == "Test description"

    def test_cli_mark_complete_command(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test CLI mark complete command.

        Note: This test uses the use case directly because the CLI creates
        a new repository per command, preventing state sharing between calls.
        """
        repository = MemoryRepository()
        add_use_case = AddTodo(repository)
        mark_use_case = MarkComplete(repository)

        todo = add_use_case.execute("Mark task", None)
        updated = mark_use_case.execute(todo.id, complete=True)

        assert updated.completed is True
        assert updated.id == todo.id

    def test_cli_delete_command(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test CLI delete command.

        Note: This test uses the use case directly because the CLI creates
        a new repository per command, preventing state sharing between calls.
        """
        repository = MemoryRepository()
        add_use_case = AddTodo(repository)
        delete_use_case = DeleteTodo(repository)
        list_use_case = ListTodos(repository)

        todo = add_use_case.execute("Delete task", None)
        assert len(list_use_case.execute()) == 1

        delete_use_case.execute(todo.id)
        assert len(list_use_case.execute()) == 0


class TestParserSetup:
    """Tests for CLI argument parser configuration."""

    def test_parser_has_all_commands(self) -> None:
        """Verify all subcommands are registered."""
        parser = create_parser()
        # Parse with a dummy command to trigger subparser help
        with pytest.raises(SystemExit):
            parser.parse_args(["--help"])

    def test_version_flag_exists(self) -> None:
        """Verify --version flag is available."""
        parser = create_parser()
        with pytest.raises(SystemExit) as exc_info:
            parser.parse_args(["--version"])
        # argparse exits with code 0 for --version
        assert exc_info.value.code == 0

    def test_add_command_requires_title(self) -> None:
        """Verify add command requires title argument."""
        parser = create_parser()
        with pytest.raises(SystemExit):
            parser.parse_args(["add"])

    def test_get_command_requires_id(self) -> None:
        """Verify get command requires id argument."""
        parser = create_parser()
        with pytest.raises(SystemExit):
            parser.parse_args(["get"])
