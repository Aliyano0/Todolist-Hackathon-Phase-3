# CLI Contracts: Todo Console App

**Date**: 2026-01-02
**Feature**: Todo Console App (001-todo-console-app)

## Command Overview

```
todo --help
todo <command> --help
```

## Commands

### add - Add a new task

```bash
todo add "Buy groceries"               # Title only
todo add "Call mom" --desc "Discuss weekend plans"  # With description
todo add "Task" -d "Description"       # Short flags
```

| Flag | Short | Description | Required |
|------|-------|-------------|----------|
| --title | -t | Task title (1-200 chars) | Yes* |
| --description | -d | Task description | No |

*Title can also be provided as positional argument.

**Output (success)**:
```
Added task 1: "Buy groceries"
```

**Output (error)**:
```
Error: Title cannot be empty
Error: Title cannot exceed 200 characters
```

**Exit codes**: 0 (success), 1 (error)

---

### list - List all tasks

```bash
todo list                    # Show all tasks
todo list --simple           # Compact format
```

| Flag | Description |
|------|-------------|
| --simple | Compact output (ID and title only) |

**Output (with tasks)**:
```
ID  | Status | Title
----|--------|---------------------------
1   | [ ]    | Buy groceries
2   | [X]    | Call mom
```

**Output (empty)**:
```
No tasks yet. Add one with: todo add "Task title"
```

**Exit codes**: 0 (success)

---

### get - Show task details

```bash
todo get 1                   # Show task 1 details
todo get --id 1              # Explicit ID flag
```

| Flag | Description |
|------|-------------|
| --id | Task ID (required) |

**Output (success)**:
```
Task #1
Title: Buy groceries
Description: Milk, eggs, bread
Status: [ ] Incomplete
Created: 2026-01-02 10:30:45
```

**Output (error)**:
```
Error: Task not found
Error: Invalid ID format
```

**Exit codes**: 0 (success), 1 (error)

---

### update - Update a task

```bash
todo update 1 --title "New title"              # Update title only
todo update 1 --desc "New description"         # Update description only
todo update 1 -t "New" -d "New desc"           # Update both
```

| Flag | Short | Description |
|------|-------|-------------|
| --id | -i | Task ID (positional, first argument) |
| --title | -t | New title (1-200 chars) |
| --description | -d | New description |

**Output (success)**:
```
Updated task 1
```

**Output (error)**:
```
Error: Title cannot be empty
Error: Task not found
Error: Invalid ID format
```

**Exit codes**: 0 (success), 1 (error)

---

### delete - Delete a task

```bash
todo delete 1                # Delete task 1
todo delete --id 1           # Explicit ID flag
```

| Flag | Description |
|------|-------------|
| --id | Task ID (required) |

**Output (success)**:
```
Deleted task 1
```

**Output (error)**:
```
Error: Task not found
Error: Invalid ID format
```

**Exit codes**: 0 (success), 1 (error)

---

### mark - Mark task complete/incomplete

```bash
todo mark 1 --complete       # Mark task 1 as complete
todo mark 1 --incomplete     # Mark task 1 as incomplete
todo mark 1 -c               # Short for --complete
todo mark 1 -i               # Short for --incomplete
```

| Flag | Short | Description |
|------|-------|-------------|
| --id | -i | Task ID (positional, first argument) |
| --complete | -c | Mark as complete |
| --incomplete | -C | Mark as incomplete |

**Output (success)**:
```
Marked task 1 as complete
Marked task 1 as incomplete
```

**Output (error)**:
```
Error: Task not found
Error: Invalid ID format
```

**Exit codes**: 0 (success), 1 (error)

---

### help - Show help

```bash
todo help                    # Show all commands
todo help add                # Show add command help
```

**Output**:
```
Usage: todo <command> [options]

Commands:
  add     Add a new task
  list    List all tasks
  get     Show task details
  update  Update a task
  delete  Delete a task
  mark    Mark task complete/incomplete
  help    Show this help message

Use 'todo <command> --help' for command-specific help.
```

**Exit codes**: 0 (success)

## Common Options

Available for all commands:

| Option | Description |
|--------|-------------|
| --help, -h | Show help message |
| --version | Show version |

## Error Handling

All errors are printed to stderr with "Error: " prefix:

```
Error: <message>
```

Exit code 1 for all errors.

## Status Indicators

| Symbol | Meaning |
|--------|---------|
| [X] | Complete |
| [ ] | Incomplete |
