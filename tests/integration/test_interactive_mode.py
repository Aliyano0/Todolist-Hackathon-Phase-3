"""Integration tests for interactive mode."""

import pytest
from io import StringIO
from unittest.mock import patch

from adapters.cli.__main__ import main, run_interactive
from adapters.repository.memory_repository import MemoryRepository


class TestInteractiveMode:
    """Integration tests for interactive menu mode."""

    def test_interactive_menu_displays_options(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test that interactive mode displays all menu options."""
        with patch("builtins.input", side_effect=["7"]):  # Exit immediately
            run_interactive()
        captured = capsys.readouterr()

        assert "1. Add Task" in captured.out
        assert "2. List Tasks" in captured.out
        assert "3. Get Task Details" in captured.out
        assert "4. Update Task" in captured.out
        assert "5. Mark Complete/Incomplete" in captured.out
        assert "6. Delete Task" in captured.out
        assert "7. Exit" in captured.out

    def test_interactive_add_task(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test adding a task via interactive mode."""
        inputs = ["1", "Test task", "Test description", "7"]
        with patch("builtins.input", side_effect=inputs):
            run_interactive()
        captured = capsys.readouterr()

        assert 'Added task 1: "Test task"' in captured.out

    def test_interactive_list_tasks(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test listing tasks via interactive mode."""
        # First add a task, then list it
        inputs = ["1", "Buy groceries", "", "2", "7"]
        with patch("builtins.input", side_effect=inputs):
            run_interactive()
        captured = capsys.readouterr()

        assert "Buy groceries" in captured.out
        assert "[ ]" in captured.out

    def test_interactive_exit(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test that exiting interactive mode shows goodbye message."""
        with patch("builtins.input", side_effect=["7"]):
            run_interactive()
        captured = capsys.readouterr()

        assert "Goodbye!" in captured.out

    def test_interactive_invalid_choice(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test that invalid menu choice shows error."""
        inputs = ["99", "7"]  # Invalid choice then exit
        with patch("builtins.input", side_effect=inputs):
            run_interactive()
        captured = capsys.readouterr()

        assert "Invalid choice" in captured.err

    def test_cli_interactive_command(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test CLI interactive command invokes interactive mode."""
        with patch("sys.argv", ["todolist", "interactive"]):
            with patch("builtins.input", side_effect=["7"]):
                main()
        captured = capsys.readouterr()

        assert "Interactive Mode" in captured.out
        assert "1. Add Task" in captured.out
