# Feature Specification: Todo Console App

**Feature Branch**: `001-todo-console-app`
**Created**: 2026-01-02
**Status**: Draft
**Input**: User description: "Project: Todo In-Memory Python Console App (Phase I)\n\nObjective: Build a command-line todo application that stores tasks in memory using Claude Code and Spec-Kit Plus.\n\nRequirements:\n- Implement all 5 Basic Level features: Add, Delete, Update, View, Mark Complete.\n- Follow clean code principles and proper Python project structure.\n\nTechnology Stack:\n- UV\n- Python 3.13+\n\nDeliverables:\n1. GitHub repository with:\n   - Constitution file\n   - specs history folder containing all specification files\n   - /src folder with Python source code\n   - README.md with setup instructions\n2. Working console application demonstrating:\n   - Adding tasks with title and description\n   - Listing all tasks with status indicators\n   - Updating task details\n   - Deleting tasks by ID\n   - Marking tasks as complete/incomplete"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Add Tasks (Priority: P1)

As a user, I want to add new tasks with a title and optional description so that I can capture what I need to do.

**Why this priority**: Creating tasks is the fundamental operation of any todo application. Without this feature, nothing else matters.

**Independent Test**: Can be fully tested by running the "add" command with title and optional description, then verifying the task appears in the list.

**Acceptance Scenarios**:

1. **Given** the todo list is empty, **When** the user adds a task with title "Buy groceries", **Then** the task is created with the title "Buy groceries" and no description.
2. **Given** the todo list has existing tasks, **When** the user adds a task with title "Call mom" and description "Discuss weekend plans", **Then** the new task appears at the end of the list with both title and description.
3. **Given** the user provides an empty title, **When** attempting to add a task, **Then** the system shows "Error: Title cannot be empty" and no task is created.
4. **Given** the user provides a title with only whitespace, **When** attempting to add a task, **Then** the system shows "Error: Title cannot be empty" and no task is created.

---

### User Story 2 - View Tasks (Priority: P1)

As a user, I want to see all my tasks with their status indicators so that I can quickly understand what needs to be done.

**Why this priority**: Visibility into tasks is essential for task management. Users need to see what exists and which tasks are complete.

**Independent Test**: Can be fully tested by adding multiple tasks with different completion statuses and verifying the list command shows them correctly.

**Acceptance Scenarios**:

1. **Given** the todo list has three tasks (two incomplete, one complete), **When** the user lists all tasks, **Then** all three tasks are displayed with [X] for complete and [ ] for incomplete.
2. **Given** the todo list is empty, **When** the user lists all tasks, **Then** a friendly message indicates no tasks exist.
3. **Given** the user requests details for a specific task by ID, **When** the task exists, **Then** the full details (title, description, status, creation date) are displayed.
4. **Given** the user requests details for a non-existent task ID, **When** the ID is a valid number but not found, **Then** an error message indicates "Task not found".

---

### User Story 3 - Mark Tasks Complete (Priority: P1)

As a user, I want to mark tasks as complete or incomplete so that I can track my progress on what I need to do.

**Why this priority**: Task completion tracking is core to todo management and directly impacts user satisfaction with the application.

**Independent Test**: Can be fully tested by creating tasks and toggling their completion status, verifying the status changes correctly.

**Acceptance Scenarios**:

1. **Given** a task exists and is incomplete, **When** the user marks it as complete, **Then** the task status changes to complete.
2. **Given** a task exists and is complete, **When** the user marks it as incomplete, **Then** the task status changes to incomplete.
3. **Given** the user attempts to mark a non-existent task as complete, **When** the ID is invalid format, **Then** the system shows "Error: Invalid ID format".
4. **Given** the user marks multiple tasks as complete, **When** listing tasks, **Then** the completion status is correctly reflected for each task.

---

### User Story 4 - Update Tasks (Priority: P2)

As a user, I want to modify the title and description of existing tasks so that I can correct or refine task details.

**Why this priority**: Tasks often need updates after creation. This is a common user need but not as fundamental as creation and viewing.

**Independent Test**: Can be fully tested by creating a task and updating its title and/or description, verifying the changes persist.

**Acceptance Scenarios**:

1. **Given** a task exists with title "Buy milk", **When** the user updates the title to "Buy almond milk", **Then** the task now has title "Buy almond milk" and other fields remain unchanged.
2. **Given** a task exists with title "Buy groceries" and no description, **When** the user adds a description "Get eggs, bread, cheese", **Then** the task now has the description "Get eggs, bread, cheese".
3. **Given** a task exists, **When** the user updates the title to empty whitespace, **Then** the system shows "Error: Title cannot be empty" and no changes are made.
4. **Given** the user attempts to update a non-existent task, **When** the ID is invalid format, **Then** the system shows "Error: Invalid ID format".

---

### User Story 5 - Delete Tasks (Priority: P2)

As a user, I want to remove tasks that are no longer needed so that I can keep my todo list focused on relevant items.

**Why this priority**: Deleting tasks is important for list management but less critical than core CRUD operations. It can be implemented after core features.

**Independent Test**: Can be fully tested by creating tasks, deleting one, and verifying it no longer appears in the list.

**Acceptance Scenarios**:

1. **Given** a todo list has three tasks, **When** the user deletes the second task, **Then** the list now has two tasks and the remaining tasks preserve their original order.
2. **Given** the user attempts to delete a non-existent task, **When** the ID is invalid format, **Then** the system shows "Error: Invalid ID format".
3. **Given** a task is deleted, **When** the user lists tasks, **Then** the deleted task no longer appears in the list.

---

### User Story 6 - Interactive Mode (Priority: P1)

As a user, I want an interactive menu-driven session so that I can manage tasks without typing full commands for each operation.

**Why this priority**: Interactive mode improves usability by allowing users to stay in a single session and navigate features through a simple numbered menu. Tasks persist within the session, eliminating the need to re-enter commands.

**Independent Test**: Can be fully tested by starting interactive mode, selecting options from the menu, and verifying all operations work correctly within the session.

**Acceptance Scenarios**:

1. **Given** the user runs `todolist interactive` or `todolist --interactive`, **When** the session starts, **Then** a menu is displayed with options 1-6 and instructions to select a number.
2. **Given** the interactive menu is displayed, **When** the user selects option 1 (Add Task), **Then** the user is prompted for title and description, and the task is added with confirmation.
3. **Given** the interactive menu is displayed, **When** the user selects option 2 (List Tasks), **Then** all tasks are displayed with status indicators.
4. **Given** the interactive menu is displayed, **When** the user selects option 3 (Get Task Details), **Then** the user is prompted for a task ID, and full details are displayed.
5. **Given** the interactive menu is displayed, **When** the user selects option 4 (Update Task), **Then** the user is prompted for ID, title, and description, and the task is updated.
6. **Given** the interactive menu is displayed, **When** the user selects option 5 (Mark Complete/Incomplete), **Then** the user is prompted for ID and completion status, and the task is updated.
7. **Given** the interactive menu is displayed, **When** the user selects option 6 (Delete Task), **Then** the user is prompted for ID, and the task is deleted.
8. **Given** the interactive menu is displayed, **When** the user selects option 7 (Exit), **Then** the session ends with a goodbye message.
9. **Given** the user enters an invalid menu option, **When** the selection is processed, **Then** an error message is shown and the menu is redisplayed.
10. **Given** the user enters an invalid task ID, **When** an operation requiring ID is performed, **Then** an error message is shown and the menu is redisplayed.

---

### Edge Cases

- What happens when adding a task with a title longer than 200 characters? → Reject with error
- What happens when attempting to mark, update, or delete a task that was just added in the same session? → Works normally (tasks persist in memory)
- What happens when the user provides a task ID that is not a valid number (e.g., text or special characters)? → "Invalid ID format" error
- How does the system handle task IDs after deletions (do they get reassigned or stay unique)? → IDs are never reused (sequential, unique per session)
- What happens when the user tries to add a duplicate task with the exact same title? → Warn but allow

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to create new tasks with a title and optional description.
- **FR-002**: System MUST assign a unique identifier to each task upon creation.
- **FR-003**: System MUST track the completion status (complete/incomplete) for each task.
- **FR-004**: System MUST allow users to list all tasks with clear status indicators.
- **FR-005**: System MUST allow users to view detailed information for a specific task by ID.
- **FR-006**: System MUST allow users to update the title and/or description of an existing task.
- **FR-007**: System MUST allow users to mark a task as complete.
- **FR-008**: System MUST allow users to mark a complete task as incomplete.
- **FR-009**: System MUST allow users to delete a task by its ID.
- **FR-010**: System MUST validate that task titles are non-empty and contain non-whitespace characters.
- **FR-011**: System MUST provide clear error messages prefixed with "Error: " for all error conditions.
- **FR-012**: System MUST store all data in memory for the duration of the session only.
- **FR-013**: System MUST maintain task order based on creation time (newest at the end).
- **FR-014**: System MUST provide an interactive menu mode for task management within a single session.

### Key Entities

- **Todo**: Represents a single task item with the following attributes:
  - `id`: Unique identifier (integer, auto-incrementing)
  - `title`: Short text describing the task (required, non-empty)
  - `description`: Optional detailed text about the task
  - `completed`: Boolean indicating if the task is done
  - `created_at`: Timestamp when the task was created

- **TodoList**: Represents the collection of todos with the following capabilities:
  - Add a new todo
  - Get all todos
  - Get a todo by ID
  - Update a todo
  - Delete a todo by ID
  - Mark a todo as complete/incomplete

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can add a new task and see it appear in the list within 5 seconds of command execution.
- **SC-002**: Users can view all tasks and clearly distinguish between complete ([X]) and incomplete ([ ]) items.
- **SC-003**: Users can successfully complete the six core operations (add, view, update, delete, mark complete, interactive mode) without encountering unhandled errors.
- **SC-004**: Error messages for invalid inputs (empty title, non-existent ID) are clear and actionable.
- **SC-005**: The application provides a consistent and intuitive command-line interface that users can learn quickly.
- **SC-006**: All task data is preserved for the duration of a single session (until the application exits).
- **SC-007**: Users can enter interactive mode and perform multiple operations without restarting the application.

## Clarifications

### Session 2026-01-02

- Q: Duplicate task handling → A: Warn but allow duplicates
- Q: Title length limit → A: 200 characters maximum
- Q: Status indicator format → A: [X] / [ ] format
- Q: Invalid ID error handling → A: Different errors for invalid format vs not found
- Q: Error message style → A: Prefix with "Error: " for all errors

## Assumptions

- Users interact with the application via a command-line interface.
- The application runs as a single-user session with no concurrent access concerns.
- Task IDs are assigned sequentially starting from 1 and increment with each new task.
- Deleted task IDs are not reused for new tasks to maintain referential integrity.
- Task titles have a maximum length of 200 characters.
- Description field is optional and can be empty or omitted entirely.
- The application does not require any form of authentication or user accounts.
