"""Main entry point for the todo CLI application."""

import argparse
import sys

from src.core.exceptions.todo_errors import TodoError
from src.core.use_cases.add_todo import AddTodo
from adapters.repository.memory_repository import MemoryRepository


# Shared repository instance for session persistence
_repository = MemoryRepository()


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser with all subcommands."""
    parser = argparse.ArgumentParser(
        prog="todolist",
        description="A simple in-memory todo console application",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument(
        "title",
        help="Task title (1-200 characters)",
    )
    add_parser.add_argument(
        "-d",
        "--description",
        dest="description",
        help="Optional task description",
    )

    # List command
    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.add_argument(
        "--simple",
        action="store_true",
        help="Show compact output",
    )

    # Get command
    get_parser = subparsers.add_parser("get", help="Show task details")
    get_parser.add_argument("id", type=int, help="Task ID")

    # Update command
    update_parser = subparsers.add_parser("update", help="Update a task")
    update_parser.add_argument("id", type=int, help="Task ID")
    update_parser.add_argument("-t", "--title", dest="title", help="New task title")
    update_parser.add_argument(
        "-d", "--description", dest="description", help="New task description"
    )

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int, help="Task ID")

    # Mark command
    mark_parser = subparsers.add_parser("mark", help="Mark task complete/incomplete")
    mark_parser.add_argument("id", type=int, help="Task ID")
    mark_parser.add_argument(
        "-c",
        "--complete",
        action="store_true",
        help="Mark as complete",
    )
    mark_parser.add_argument(
        "-C",
        "--incomplete",
        action="store_true",
        help="Mark as incomplete",
    )

    # Interactive command
    interactive_parser = subparsers.add_parser(
        "interactive", help="Enter interactive menu mode"
    )

    return parser


def cmd_add(args: argparse.Namespace) -> None:
    """Handle the add command."""
    use_case = AddTodo(_repository)
    try:
        todo = use_case.execute(args.title, args.description)
        print(f'Added task {todo.id}: "{todo.title}"')
    except TodoError as e:
        print(f"Error: {e.message}", file=sys.stderr)
        sys.exit(1)


def cmd_list(args: argparse.Namespace) -> None:
    """Handle the list command."""
    todos = _repository.list_all()

    if not todos:
        print("No tasks yet. Add one with: todolist add \"Task title\"")
        return

    print("ID  | Status | Title")
    print("----|--------", "-" * 30)
    for todo in todos:
        status = "[X]" if todo.completed else "[ ]"
        print(f"{todo.id:<3}| {status}    | {todo.title}")


def cmd_get(args: argparse.Namespace) -> None:
    """Handle the get command."""
    try:
        todo = _repository.get(args.id)
        status = "Complete" if todo.completed else "Incomplete"
        print(f"Task #{todo.id}")
        print(f"Title: {todo.title}")
        print(f"Description: {todo.description or '(none)'}")
        print(f"Status: [{status}]")
        print(f"Created: {todo.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
    except TodoError as e:
        print(f"Error: {e.message}", file=sys.stderr)
        sys.exit(1)


def cmd_update(args: argparse.Namespace) -> None:
    """Handle the update command."""
    try:
        todo = _repository.update(args.id, args.title, args.description)
        print(f"Updated task {todo.id}")
    except TodoError as e:
        print(f"Error: {e.message}", file=sys.stderr)
        sys.exit(1)


def cmd_delete(args: argparse.Namespace) -> None:
    """Handle the delete command."""
    try:
        _repository.delete(args.id)
        print(f"Deleted task {args.id}")
    except TodoError as e:
        print(f"Error: {e.message}", file=sys.stderr)
        sys.exit(1)


def cmd_mark(args: argparse.Namespace) -> None:
    """Handle the mark command."""
    try:
        complete = args.complete or not args.incomplete
        todo = _repository.mark_complete(args.id, complete)
        status = "complete" if todo.completed else "incomplete"
        print(f"Marked task {todo.id} as {status}")
    except TodoError as e:
        print(f"Error: {e.message}", file=sys.stderr)
        sys.exit(1)


def run_interactive() -> None:
    """Run interactive menu mode for task management."""
    print("=" * 50)
    print("         Todo List - Interactive Mode")
    print("=" * 50)
    print()

    while True:
        print("Menu:")
        print("  1. Add Task")
        print("  2. List Tasks")
        print("  3. Get Task Details")
        print("  4. Update Task")
        print("  5. Mark Complete/Incomplete")
        print("  6. Delete Task")
        print("  7. Exit")
        print()

        choice = input("Enter your choice (1-7): ").strip()

        print()

        if choice == "1":
            # Add Task
            title = input("Enter task title: ").strip()
            if not title:
                print("Error: Title cannot be empty", file=sys.stderr)
                print()
                continue
            if len(title) > 200:
                print("Error: Title cannot exceed 200 characters", file=sys.stderr)
                print()
                continue
            desc = input("Enter task description (optional): ").strip() or None
            try:
                use_case = AddTodo(_repository)
                todo = use_case.execute(title, desc)
                print(f'Added task {todo.id}: "{todo.title}"')
            except TodoError as e:
                print(f"Error: {e.message}", file=sys.stderr)

        elif choice == "2":
            # List Tasks
            todos = _repository.list_all()
            if not todos:
                print("No tasks yet. Add one with option 1.")
            else:
                print("ID  | Status | Title")
                print("----|--------", "-" * 30)
                for todo in todos:
                    status = "[X]" if todo.completed else "[ ]"
                    print(f"{todo.id:<3}| {status}    | {todo.title}")

        elif choice == "3":
            # Get Task Details
            try:
                task_id = int(input("Enter task ID: "))
                todo = _repository.get(task_id)
                status = "Complete" if todo.completed else "Incomplete"
                print(f"Task #{todo.id}")
                print(f"Title: {todo.title}")
                print(f"Description: {todo.description or '(none)'}")
                print(f"Status: [{status}]")
                print(f"Created: {todo.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            except ValueError:
                print("Error: Invalid ID format", file=sys.stderr)
            except TodoError as e:
                print(f"Error: {e.message}", file=sys.stderr)

        elif choice == "4":
            # Update Task
            try:
                task_id = int(input("Enter task ID: "))
                new_title = input("Enter new title (leave empty to keep current): ").strip()
                new_desc = input("Enter new description (leave empty to keep current): ").strip() or None

                title = new_title if new_title else None
                desc = new_desc if new_desc is not None else None

                todo = _repository.update(task_id, title, desc)
                print(f"Updated task {todo.id}")
            except ValueError:
                print("Error: Invalid ID format", file=sys.stderr)
            except TodoError as e:
                print(f"Error: {e.message}", file=sys.stderr)

        elif choice == "5":
            # Mark Complete/Incomplete
            try:
                task_id = int(input("Enter task ID: "))
                status_choice = input("Mark as (c)omplete or (i)ncomplete? ").strip().lower()
                complete = status_choice.startswith("c")
                todo = _repository.mark_complete(task_id, complete)
                status = "complete" if todo.completed else "incomplete"
                print(f"Marked task {todo.id} as {status}")
            except ValueError:
                print("Error: Invalid ID format", file=sys.stderr)
            except TodoError as e:
                print(f"Error: {e.message}", file=sys.stderr)

        elif choice == "6":
            # Delete Task
            try:
                task_id = int(input("Enter task ID: "))
                _repository.delete(task_id)
                print(f"Deleted task {task_id}")
            except ValueError:
                print("Error: Invalid ID format", file=sys.stderr)
            except TodoError as e:
                print(f"Error: {e.message}", file=sys.stderr)

        elif choice == "7":
            # Exit
            print("Goodbye!")
            break

        else:
            print("Error: Invalid choice. Please enter a number 1-7.", file=sys.stderr)

        print()


def main() -> None:
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    # Route to appropriate command handler
    commands = {
        "add": cmd_add,
        "list": cmd_list,
        "get": cmd_get,
        "update": cmd_update,
        "delete": cmd_delete,
        "mark": cmd_mark,
        "interactive": run_interactive,
    }

    handler = commands.get(args.command)
    if handler:
        if args.command == "interactive":
            handler()
        else:
            handler(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
