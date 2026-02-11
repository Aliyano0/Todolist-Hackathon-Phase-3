"""
Unit tests for add_task MCP tool

Tests the add_task tool with happy path, validation, and user isolation.
Following TDD: These tests should FAIL before implementation.
"""

import pytest
import uuid
from unittest.mock import AsyncMock, MagicMock, patch
from mcp_server.tools.add_task import add_task_tool


@pytest.mark.asyncio
async def test_add_task_happy_path():
    """Test successfully adding a task with all fields"""
    user_id = str(uuid.uuid4())
    title = "Buy groceries"
    description = "Milk, eggs, bread"
    priority = "high"
    category = "shopping"

    result = await add_task_tool(
        user_id=user_id,
        title=title,
        description=description,
        priority=priority,
        category=category
    )

    assert result["status"] == "created"
    assert result["title"] == title
    assert result["description"] == description
    assert result["priority"] == priority
    assert result["category"] == category
    assert "task_id" in result
    # Verify task_id is a valid UUID
    uuid.UUID(result["task_id"])


@pytest.mark.asyncio
async def test_add_task_minimal_fields():
    """Test adding a task with only required fields (title)"""
    user_id = str(uuid.uuid4())
    title = "Simple task"

    result = await add_task_tool(
        user_id=user_id,
        title=title
    )

    assert result["status"] == "created"
    assert result["title"] == title
    assert result["description"] is None
    assert result["priority"] is None
    assert result["category"] is None
    assert "task_id" in result


@pytest.mark.asyncio
async def test_add_task_empty_title():
    """Test that empty title raises ValueError"""
    user_id = str(uuid.uuid4())

    with pytest.raises(ValueError, match="Task title cannot be empty"):
        await add_task_tool(
            user_id=user_id,
            title=""
        )


@pytest.mark.asyncio
async def test_add_task_whitespace_title():
    """Test that whitespace-only title raises ValueError"""
    user_id = str(uuid.uuid4())

    with pytest.raises(ValueError, match="Task title cannot be empty"):
        await add_task_tool(
            user_id=user_id,
            title="   "
        )


@pytest.mark.asyncio
async def test_add_task_invalid_user_id():
    """Test that invalid user_id format raises ValueError"""
    with pytest.raises(ValueError, match="Invalid user_id format"):
        await add_task_tool(
            user_id="not-a-uuid",
            title="Test task"
        )


@pytest.mark.asyncio
async def test_add_task_strips_whitespace():
    """Test that title and description are stripped of whitespace"""
    user_id = str(uuid.uuid4())
    title = "  Task with spaces  "
    description = "  Description with spaces  "

    result = await add_task_tool(
        user_id=user_id,
        title=title,
        description=description
    )

    assert result["title"] == "Task with spaces"
    assert result["description"] == "Description with spaces"


@pytest.mark.asyncio
async def test_add_task_user_isolation():
    """Test that tasks are isolated by user_id"""
    user1_id = str(uuid.uuid4())
    user2_id = str(uuid.uuid4())

    # Add task for user1
    result1 = await add_task_tool(
        user_id=user1_id,
        title="User 1 task"
    )

    # Add task for user2
    result2 = await add_task_tool(
        user_id=user2_id,
        title="User 2 task"
    )

    # Both should succeed with different task IDs
    assert result1["task_id"] != result2["task_id"]
    assert result1["status"] == "created"
    assert result2["status"] == "created"


@pytest.mark.asyncio
async def test_add_task_long_title():
    """Test adding a task with a long title"""
    user_id = str(uuid.uuid4())
    title = "A" * 500  # Very long title

    result = await add_task_tool(
        user_id=user_id,
        title=title
    )

    assert result["status"] == "created"
    assert result["title"] == title


@pytest.mark.asyncio
async def test_add_task_special_characters():
    """Test adding a task with special characters in title"""
    user_id = str(uuid.uuid4())
    title = "Task with émojis 🎉 and spëcial çhars!"

    result = await add_task_tool(
        user_id=user_id,
        title=title
    )

    assert result["status"] == "created"
    assert result["title"] == title
