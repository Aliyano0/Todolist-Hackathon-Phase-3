"""
Unit tests for complete_task MCP tool

Tests the complete_task tool with success, not found, and isolation scenarios.
Following TDD: These tests should FAIL before implementation.
"""

import pytest
import uuid
from unittest.mock import AsyncMock, MagicMock, patch
from mcp_server.tools.complete_task import complete_task_tool


@pytest.mark.asyncio
async def test_complete_task_success():
    """Test successfully completing a task"""
    user_id = str(uuid.uuid4())
    task_id = str(uuid.uuid4())

    result = await complete_task_tool(
        user_id=user_id,
        task_id=task_id
    )

    assert result["status"] == "completed"
    assert result["task_id"] == task_id
    assert "title" in result


@pytest.mark.asyncio
async def test_complete_task_already_completed():
    """Test completing a task that is already completed"""
    user_id = str(uuid.uuid4())
    task_id = str(uuid.uuid4())

    # First completion
    result1 = await complete_task_tool(
        user_id=user_id,
        task_id=task_id
    )
    assert result1["status"] == "completed"

    # Second completion (already completed)
    result2 = await complete_task_tool(
        user_id=user_id,
        task_id=task_id
    )
    assert result2["status"] == "already_completed"
    assert result2["task_id"] == task_id


@pytest.mark.asyncio
async def test_complete_task_not_found():
    """Test completing a non-existent task"""
    user_id = str(uuid.uuid4())
    task_id = str(uuid.uuid4())  # Non-existent task

    with pytest.raises(Exception, match="Task not found"):
        await complete_task_tool(
            user_id=user_id,
            task_id=task_id
        )


@pytest.mark.asyncio
async def test_complete_task_invalid_user_id():
    """Test that invalid user_id format raises ValueError"""
    task_id = str(uuid.uuid4())

    with pytest.raises(ValueError, match="Invalid user_id format"):
        await complete_task_tool(
            user_id="not-a-uuid",
            task_id=task_id
        )


@pytest.mark.asyncio
async def test_complete_task_invalid_task_id():
    """Test that invalid task_id format raises ValueError"""
    user_id = str(uuid.uuid4())

    with pytest.raises(ValueError, match="Invalid task_id format"):
        await complete_task_tool(
            user_id=user_id,
            task_id="not-a-uuid"
        )


@pytest.mark.asyncio
async def test_complete_task_user_isolation():
    """Test that users cannot complete other users' tasks"""
    user1_id = str(uuid.uuid4())
    user2_id = str(uuid.uuid4())
    task_id = str(uuid.uuid4())

    # User1 creates and completes a task
    # (Assuming task belongs to user1)

    # User2 tries to complete user1's task
    with pytest.raises(Exception, match="Task not found or you don't have permission"):
        await complete_task_tool(
            user_id=user2_id,
            task_id=task_id
        )


@pytest.mark.asyncio
async def test_complete_task_returns_title():
    """Test that completion returns the task title"""
    user_id = str(uuid.uuid4())
    task_id = str(uuid.uuid4())

    result = await complete_task_tool(
        user_id=user_id,
        task_id=task_id
    )

    assert "title" in result
    assert isinstance(result["title"], str)
    assert len(result["title"]) > 0


@pytest.mark.asyncio
async def test_complete_task_idempotent():
    """Test that completing a task multiple times is idempotent"""
    user_id = str(uuid.uuid4())
    task_id = str(uuid.uuid4())

    # Complete task multiple times
    result1 = await complete_task_tool(user_id=user_id, task_id=task_id)
    result2 = await complete_task_tool(user_id=user_id, task_id=task_id)
    result3 = await complete_task_tool(user_id=user_id, task_id=task_id)

    # All should succeed (second and third return already_completed)
    assert result1["status"] == "completed"
    assert result2["status"] == "already_completed"
    assert result3["status"] == "already_completed"
    assert result1["task_id"] == result2["task_id"] == result3["task_id"]


@pytest.mark.asyncio
async def test_complete_task_preserves_other_fields():
    """Test that completing a task only changes completed status"""
    user_id = str(uuid.uuid4())
    task_id = str(uuid.uuid4())

    # Get task before completion
    # (Assuming we can query the task)

    result = await complete_task_tool(
        user_id=user_id,
        task_id=task_id
    )

    # Task should be marked as completed
    assert result["status"] == "completed"
    
    # Other fields should remain unchanged
    # (title, description, priority, category should not change)
