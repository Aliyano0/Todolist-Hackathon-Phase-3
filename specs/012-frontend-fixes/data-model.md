# Data Model: Frontend Fixes and Improvements

## Todo Item
Represents a task with properties such as title, description, completion status, and timestamps
- **Fields**:
  - id: string (unique identifier)
  - title: string (required, max 255 chars)
  - description: string (optional, max 1000 chars)
  - completed: boolean (default: false)
  - createdAt: string (ISO date string)
  - updatedAt: string (ISO date string)
  - userId: string (foreign key to user)

## Task List
Collection of todo items displayed in the "Your Tasks" section
- **Relationships**:
  - Contains multiple Todo Items
  - Belongs to a User

## Validation Rules
- Todo title must be 1-255 characters
- Todo description must be 0-1000 characters if provided
- Completed status must be boolean
- Timestamps must be valid ISO date strings
- User ID must reference an existing user

## State Transitions
- Todo Item: pending → completed (via toggleComplete)
- Todo Item: pending ← completed (via toggleComplete)
- Todo Item: created → active (via createTodo)
- Todo Item: active → deleted (via deleteTodo)