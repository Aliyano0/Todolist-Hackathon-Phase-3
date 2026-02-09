# Quickstart: Todo Console App

**Date**: 2026-01-02
**Feature**: Todo Console App (001-todo-console-app)

## Prerequisites

- Python 3.13 or higher
- UV package manager

## Setup

1. **Initialize the project with UV**:
   ```bash
   uv init --python 3.13 --name todolist
   ```

2. **Add pytest for testing**:
   ```bash
   uv add --dev pytest
   ```

3. **Install the package**:
   ```bash
   uv sync
   ```

4. **Verify installation**:
   ```bash
   python -m todolist --help
   ```

## Project Structure

```
todolist/
├── src/
│   └── todolist/
│       ├── __init__.py
│       ├── core/
│       │   ├── __init__.py
│       │   ├── entities/
│       │   ├── use_cases/
│       │   ├── ports/
│       │   └── exceptions/
│       └── adapters/
│           ├── __init__.py
│           ├── cli/
│           └── repository/
├── tests/
├── pyproject.toml
└── README.md
```

## Running the Application

From the project root:

```bash
# Using Python module
python -m todolist

# Or via entry point (after installation)
todolist
```

## Usage Examples

### Add a task

```bash
$ todolist add "Buy groceries"
Added task 1: "Buy groceries"

$ todolist add "Call mom" --description "Discuss weekend plans"
Added task 2: "Call mom"
```

### List all tasks

```bash
$ todolist list
ID  | Status | Title
----|--------|--------------------------
1   | [ ]    | Buy groceries
2   | [ ]    | Call mom
```

### Mark task complete

```bash
$ todolist mark 1 --complete
Marked task 1 as complete

$ todolist list
ID  | Status | Title
----|--------|--------------------------
1   | [X]    | Buy groceries
2   | [ ]    | Call mom
```

### Get task details

```bash
$ todolist get 1
Task #1
Title: Buy groceries
Description:
Status: [X] Complete
Created: 2026-01-02 10:30:45
```

### Update a task

```bash
$ todolist update 1 --title "Buy groceries and household items"
Updated task 1
```

### Delete a task

```bash
$ todolist delete 1
Deleted task 1
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/unit/use_cases/test_add_todo.py
```

## Development Workflow

1. **Pick a task** from `specs/001-todo-console-app/tasks.md`
2. **Write a failing test** in the appropriate test file
3. **Implement the feature** to make the test pass
4. **Refactor** while tests stay green
5. **Commit** your changes

## Common Issues

### "Python 3.13 not found"

Ensure Python 3.13 is installed:
```bash
uv python install 3.13
```

### "Command not found: todolist"

Ensure the package is installed:
```bash
uv sync
```

## Next Steps

- See `specs/001-todo-console-app/tasks.md` for implementation tasks
- See `contracts/cli-commands.md` for CLI specification
- See `data-model.md` for entity definitions
