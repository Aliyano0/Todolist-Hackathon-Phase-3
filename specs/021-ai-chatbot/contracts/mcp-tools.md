# MCP Tools Contract Specification

**Date**: 2026-02-10
**Feature**: [spec.md](../spec.md)
**Status**: Complete

## Overview

This document defines the contract for 5 MCP (Model Context Protocol) tools that enable the AI agent to perform task management operations. All tools require `user_id` parameter for multi-user isolation and perform async database operations.

## Tool Definitions

### 1. add_task

**Purpose**: Create a new task for the user

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "user_id": {
      "type": "string",
      "format": "uuid",
      "description": "UUID of the user creating the task"
    },
    "title": {
      "type": "string",
      "minLength": 1,
      "maxLength": 200,
      "description": "Task title (can be in any supported language)"
    },
    "description": {
      "type": "string",
      "maxLength": 1000,
      "description": "Optional task description"
    }
  },
  "required": ["user_id", "title"]
}
```

**Output Schema**:
```json
{
  "type": "object",
  "properties": {
    "task_id": {
      "type": "string",
      "format": "uuid",
      "description": "UUID of the created task"
    },
    "status": {
      "type": "string",
      "enum": ["created"],
      "description": "Operation status"
    },
    "title": {
      "type": "string",
      "description": "Task title as stored"
    }
  },
  "required": ["task_id", "status", "title"]
}
```

**Example Invocation**:
```python
result = await add_task(
    user_id="550e8400-e29b-41d4-a716-446655440000",
    title="Buy groceries",
    description="Get milk, eggs, and bread"
)
# Returns: {
#   "task_id": "770e8400-e29b-41d4-a716-446655440002",
#   "status": "created",
#   "title": "Buy groceries"
# }
```

**Error Conditions**:
- Invalid `user_id` format → ValidationError
- Empty `title` → ValidationError
- Database connection failure → DatabaseError

---

### 2. list_tasks

**Purpose**: Retrieve tasks for the user with optional filtering

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "user_id": {
      "type": "string",
      "format": "uuid",
      "description": "UUID of the user"
    },
    "status": {
      "type": "string",
      "enum": ["all", "pending", "completed"],
      "default": "all",
      "description": "Filter tasks by completion status"
    }
  },
  "required": ["user_id"]
}
```

**Output Schema**:
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "id": {
        "type": "string",
        "format": "uuid",
        "description": "Task UUID"
      },
      "title": {
        "type": "string",
        "description": "Task title"
      },
      "description": {
        "type": "string",
        "nullable": true,
        "description": "Task description"
      },
      "completed": {
        "type": "boolean",
        "description": "Completion status"
      },
      "priority": {
        "type": "string",
        "nullable": true,
        "description": "Task priority"
      },
      "category": {
        "type": "string",
        "nullable": true,
        "description": "Task category"
      },
      "created_at": {
        "type": "string",
        "format": "date-time",
        "description": "Creation timestamp"
      }
    },
    "required": ["id", "title", "completed", "created_at"]
  }
}
```

**Example Invocation**:
```python
result = await list_tasks(
    user_id="550e8400-e29b-41d4-a716-446655440000",
    status="pending"
)
# Returns: [
#   {
#     "id": "770e8400-e29b-41d4-a716-446655440002",
#     "title": "Buy groceries",
#     "description": "Get milk, eggs, and bread",
#     "completed": false,
#     "priority": "high",
#     "category": "shopping",
#     "created_at": "2026-02-10T10:30:00Z"
#   },
#   ...
# ]
```

**Error Conditions**:
- Invalid `user_id` format → ValidationError
- Invalid `status` value → ValidationError
- Database connection failure → DatabaseError

---

### 3. complete_task

**Purpose**: Mark a task as completed

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "user_id": {
      "type": "string",
      "format": "uuid",
      "description": "UUID of the user"
    },
    "task_id": {
      "type": "string",
      "format": "uuid",
      "description": "UUID of the task to complete"
    }
  },
  "required": ["user_id", "task_id"]
}
```

**Output Schema**:
```json
{
  "type": "object",
  "properties": {
    "task_id": {
      "type": "string",
      "format": "uuid",
      "description": "UUID of the completed task"
    },
    "status": {
      "type": "string",
      "enum": ["completed"],
      "description": "Operation status"
    },
    "title": {
      "type": "string",
      "description": "Task title"
    }
  },
  "required": ["task_id", "status", "title"]
}
```

**Example Invocation**:
```python
result = await complete_task(
    user_id="550e8400-e29b-41d4-a716-446655440000",
    task_id="770e8400-e29b-41d4-a716-446655440002"
)
# Returns: {
#   "task_id": "770e8400-e29b-41d4-a716-446655440002",
#   "status": "completed",
#   "title": "Buy groceries"
# }
```

**Error Conditions**:
- Invalid `user_id` or `task_id` format → ValidationError
- Task not found → NotFoundError
- Task belongs to different user → NotFoundError (for security)
- Database connection failure → DatabaseError

---

### 4. delete_task

**Purpose**: Delete a task permanently

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "user_id": {
      "type": "string",
      "format": "uuid",
      "description": "UUID of the user"
    },
    "task_id": {
      "type": "string",
      "format": "uuid",
      "description": "UUID of the task to delete"
    }
  },
  "required": ["user_id", "task_id"]
}
```

**Output Schema**:
```json
{
  "type": "object",
  "properties": {
    "task_id": {
      "type": "string",
      "format": "uuid",
      "description": "UUID of the deleted task"
    },
    "status": {
      "type": "string",
      "enum": ["deleted"],
      "description": "Operation status"
    },
    "title": {
      "type": "string",
      "description": "Task title (before deletion)"
    }
  },
  "required": ["task_id", "status", "title"]
}
```

**Example Invocation**:
```python
result = await delete_task(
    user_id="550e8400-e29b-41d4-a716-446655440000",
    task_id="770e8400-e29b-41d4-a716-446655440002"
)
# Returns: {
#   "task_id": "770e8400-e29b-41d4-a716-446655440002",
#   "status": "deleted",
#   "title": "Buy groceries"
# }
```

**Error Conditions**:
- Invalid `user_id` or `task_id` format → ValidationError
- Task not found → NotFoundError
- Task belongs to different user → NotFoundError (for security)
- Database connection failure → DatabaseError

---

### 5. update_task

**Purpose**: Update task title and/or description

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "user_id": {
      "type": "string",
      "format": "uuid",
      "description": "UUID of the user"
    },
    "task_id": {
      "type": "string",
      "format": "uuid",
      "description": "UUID of the task to update"
    },
    "title": {
      "type": "string",
      "minLength": 1,
      "maxLength": 200,
      "description": "New task title (optional)"
    },
    "description": {
      "type": "string",
      "maxLength": 1000,
      "nullable": true,
      "description": "New task description (optional)"
    }
  },
  "required": ["user_id", "task_id"],
  "minProperties": 3
}
```

**Output Schema**:
```json
{
  "type": "object",
  "properties": {
    "task_id": {
      "type": "string",
      "format": "uuid",
      "description": "UUID of the updated task"
    },
    "status": {
      "type": "string",
      "enum": ["updated"],
      "description": "Operation status"
    },
    "title": {
      "type": "string",
      "description": "Updated task title"
    },
    "description": {
      "type": "string",
      "nullable": true,
      "description": "Updated task description"
    }
  },
  "required": ["task_id", "status", "title"]
}
```

**Example Invocation**:
```python
result = await update_task(
    user_id="550e8400-e29b-41d4-a716-446655440000",
    task_id="770e8400-e29b-41d4-a716-446655440002",
    title="Buy organic groceries"
)
# Returns: {
#   "task_id": "770e8400-e29b-41d4-a716-446655440002",
#   "status": "updated",
#   "title": "Buy organic groceries",
#   "description": "Get milk, eggs, and bread"
# }
```

**Error Conditions**:
- Invalid `user_id` or `task_id` format → ValidationError
- No fields to update (only user_id and task_id provided) → ValidationError
- Empty `title` → ValidationError
- Task not found → NotFoundError
- Task belongs to different user → NotFoundError (for security)
- Database connection failure → DatabaseError

---

## Common Patterns

### Multi-User Isolation

All tools MUST enforce user isolation by:
1. Accepting `user_id` as required parameter
2. Filtering database queries by `user_id`
3. Returning NotFoundError (not PermissionError) when task belongs to different user

**Example**:
```python
# ✅ CORRECT - Enforces isolation
task = await session.execute(
    select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id  # Isolation check
    )
)

# ❌ INCORRECT - No isolation check
task = await session.execute(
    select(Task).where(Task.id == task_id)
)
```

### Error Handling

All tools MUST return structured errors:

```python
# Success response
{
    "task_id": "...",
    "status": "created",
    "title": "..."
}

# Error response (raised as exception, caught by MCP server)
raise NotFoundError("Task not found")
raise ValidationError("Invalid task_id format")
raise DatabaseError("Database connection failed")
```

### Async Operations

All tools MUST use async/await for database operations:

```python
@server.call_tool()
async def handle_tool(name: str, arguments: dict) -> CallToolResult:
    if name == "add_task":
        return await handle_add_task(arguments)
    # ...

async def handle_add_task(arguments: dict) -> CallToolResult:
    async with get_async_session() as session:
        task = Task(...)
        session.add(task)
        await session.commit()  # Async commit
        await session.refresh(task)  # Async refresh
        return CallToolResult(...)
```

## Integration with AI Agent

The AI agent invokes MCP tools through the OpenAI Agents SDK:

```python
from agents import Agent, function_tool

@function_tool
def add_task(user_id: str, title: str, description: str = None) -> dict:
    """Add a new task for the user."""
    # This function wraps the MCP tool invocation
    result = mcp_server.call_tool("add_task", {
        "user_id": user_id,
        "title": title,
        "description": description
    })
    return result

agent = Agent(
    name="TaskAssistant",
    instructions="...",
    tools=[add_task, list_tasks, complete_task, delete_task, update_task]
)
```

## Testing Requirements

Each tool MUST have comprehensive tests covering:

1. **Happy Path**: Valid inputs, successful operation
2. **Validation**: Invalid inputs, missing required fields
3. **Isolation**: Cross-user access attempts
4. **Not Found**: Non-existent task IDs
5. **Database Errors**: Connection failures, transaction rollbacks

**Example Test**:
```python
async def test_add_task_success():
    result = await add_task(
        user_id="550e8400-e29b-41d4-a716-446655440000",
        title="Test task"
    )
    assert result["status"] == "created"
    assert result["title"] == "Test task"
    assert "task_id" in result

async def test_add_task_isolation():
    # Create task for user A
    task = await add_task(
        user_id=user_a_id,
        title="User A task"
    )

    # Try to access with user B
    with pytest.raises(NotFoundError):
        await complete_task(
            user_id=user_b_id,
            task_id=task["task_id"]
        )
```

## Performance Considerations

- All database operations use connection pooling (asyncpg)
- Queries are indexed on `user_id` and `id` fields
- List operations should be limited to reasonable page sizes
- No N+1 query problems (use proper joins/eager loading)

## Security Considerations

- Never expose internal error details to users
- Always validate UUID formats before database queries
- Use parameterized queries (SQLModel handles this)
- Return generic "Not Found" for both missing and unauthorized access
- Log security events (cross-user access attempts)
