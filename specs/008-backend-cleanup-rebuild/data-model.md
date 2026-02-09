# Data Model: Backend Cleanup and Rebuild (Phase 2a)

## Entity: Todo Task

**Description:** Represents a single user's todo item

**Attributes:**
- `id` (Integer, Primary Key, Auto-increment): Unique identifier for the task
- `title` (String, Required): Title/name of the task
- `description` (String, Optional): Detailed description of the task
- `completed` (Boolean, Default: False): Completion status of the task
- `created_at` (DateTime, Auto-generated): Timestamp when task was created
- `updated_at` (DateTime, Auto-generated): Timestamp when task was last modified

**Relationships:**
- No user relationship needed as this is a single-user temporary system

**Validation Rules:**
- `title` must not be empty or null
- `title` must be less than 255 characters
- `description` can be null or up to 1000 characters
- `completed` must be a boolean value

**State Transitions:**
- `completed` can transition from `false` to `true` (mark complete)
- `completed` can transition from `true` to `false` (mark incomplete)

## Entity: Task Collection

**Description:** Represents the collection of all tasks in the system managed by the database

**Operations:**
- Create new task
- Retrieve all tasks
- Retrieve single task by ID
- Update task details
- Delete task
- Toggle completion status