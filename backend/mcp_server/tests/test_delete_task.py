"""
Unit tests for delete_task MCP tool

Tests the delete_task tool with success, not found, and isolation scenarios.
Following TDD: These tests should FAIL before implementation.
"""

import pytest
import uuid
from unittest.mock import AsyncMock, MagicMock, patch
from mcp_server.tools.delete_task import delete_task_tool


@pytest.mark.asyncio
async def test_delete_task_success():
    """Test successfully deleting a task"""
    user_id = str(uuid.uuid4())
    task_id = str(uuid.uuid4())

    result = await delete_task_tool(
        user_id=user_id,
        task_id=task_id
    )

    assert result["status"] == "deleted"
    assert result["task_id"] == task_id
    assert "title" in result


@pytest.mark.asyncio
async def test_delete_task_not_found():
    """Test deleting a non-existent task"""
    user_id = str(uuid.uuid4())
    task_id = str(uuid.uuid4())  # Non-existent task

    with pytest.raises(Exception, match="Task not found"):
        await delete_task_tool(
            user_id=user_id,
            task_id=task_id
        )


@pytest.mark.asyncio
async def test_delete_task_invalid_user_id():
    """Test that invalid user_id format raises ValueError"""
    task_id = str(uuid.uuid4())

    with pytest.raises(ValueError, match="Invalid user_id format"):
        await delete_task_tool(
            user_id="not-a-uuid",
            task_id=task_id
        )


@pytest.mark.asyncio
async def test_delete_task_invalid_task_id():
    """Test that invalid task_id format raises ValueError"""
    user_id = str(uuid.uuid4())

    with pytest.raises(ValueError, match="Invalid task_id format"):
        await delete_task_tool(
            user_id=user_id,
            task_id="not-a-uuid"
        )


@pytest.mark.asyncio
async def test_delete_task_user_isolation():
    """Test that users cannot delete other users' tasks"""
    user1_id = str(uuid.uuid4())
    user2_id = str(uuid.uuid4())
    task_id = str(uuid.uuid4())

    # User1 creates a task
    # (Assuming task belongs to user1)

    # User2 tries to delete user1's task
    with pytest.raises(Exception, match="Task not found or you don't have permission"):
        await delete_task_tool(
            user_id=user2_id,
            task_id=task_id
        )


@pytest.mark.asyncio
async def test_delete_task_returns_title():
    """Test that deletion returns the task title"""
    user_id = str(uuid.uuid4())
    task_id = str(uuid.uuid4())

    result = await delete_task_tool(
        user_id=user_id,
        task_id=task_id
    )

    assert "title" in result
    assert isinstance(result["title"], str)
    assert len(result["title"]) > 0


@pytest.mark.asyncio
async def test_delete_task_permanent():
    """Test that deleted task cannot be retrieved"""
    user_id = str(uuid.uuid4())
    task_id = str(uuid.uuid4())

    # Delete task
    result = await delete_task_tool(
        user_id=user_id,
        task_id=task_id
    )
    assert result["status"] == "deleted"

    # Try to delete again (should fail - task no longer exists)
    with pytest.raises(Exception, match="Task not found"):
        await delete_task_tool(
            user_id=user_id,
            task_id=task_id
        )


@pytest.mark.asyncio
async def test_delete_task_completed_task():
    """Test that completed tasks can be deleted"""
    user_id = str(uuid.uuid4())
    task_id = str(uuid.uuid4())

    # Delete a completed task (should succeed)
    result = await delete_task_tool(
        user_id=user_id,
        task_id=task_id
    )

    assert result["status"] == "deleted"


@pytest.mark.asyncio
async def test_delete_task_with_description():
    """Test deleting a task that has description and other fields"""
    user_id = str(uuid.uuid4())
    task_id = str(uuid.uuid4())

    result = await delete_task_tool(
        user_id=user_id,
        task_id=task_id
    )

    # Should successfully delete regardless of task content
    assert result["status"] == "deleted"
    assert "title" in result
