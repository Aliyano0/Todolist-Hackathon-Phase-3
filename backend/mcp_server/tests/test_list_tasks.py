"""
Unit tests for list_tasks MCP tool

Tests the list_tasks tool with all, pending, and completed filters.
Following TDD: These tests should FAIL before implementation.
"""

import pytest
import uuid
from unittest.mock import AsyncMock, MagicMock, patch
from mcp_server.tools.list_tasks import list_tasks_tool


@pytest.mark.asyncio
async def test_list_tasks_all_status():
    """Test listing all tasks regardless of completion status"""
    user_id = str(uuid.uuid4())

    result = await list_tasks_tool(
        user_id=user_id,
        status="all"
    )

    assert result["status_filter"] == "all"
    assert "tasks" in result
    assert "count" in result
    assert isinstance(result["tasks"], list)
    assert result["count"] == len(result["tasks"])


@pytest.mark.asyncio
async def test_list_tasks_pending_only():
    """Test listing only pending (incomplete) tasks"""
    user_id = str(uuid.uuid4())

    result = await list_tasks_tool(
        user_id=user_id,
        status="pending"
    )

    assert result["status_filter"] == "pending"
    assert "tasks" in result
    # All returned tasks should be incomplete
    for task in result["tasks"]:
        assert task["completed"] is False


@pytest.mark.asyncio
async def test_list_tasks_completed_only():
    """Test listing only completed tasks"""
    user_id = str(uuid.uuid4())

    result = await list_tasks_tool(
        user_id=user_id,
        status="completed"
    )

    assert result["status_filter"] == "completed"
    assert "tasks" in result
    # All returned tasks should be completed
    for task in result["tasks"]:
        assert task["completed"] is True


@pytest.mark.asyncio
async def test_list_tasks_default_status():
    """Test that default status is 'all'"""
    user_id = str(uuid.uuid4())

    result = await list_tasks_tool(user_id=user_id)

    assert result["status_filter"] == "all"


@pytest.mark.asyncio
async def test_list_tasks_invalid_status():
    """Test that invalid status raises ValueError"""
    user_id = str(uuid.uuid4())

    with pytest.raises(ValueError, match="Invalid status"):
        await list_tasks_tool(
            user_id=user_id,
            status="invalid_status"
        )


@pytest.mark.asyncio
async def test_list_tasks_invalid_user_id():
    """Test that invalid user_id format raises ValueError"""
    with pytest.raises(ValueError, match="Invalid user_id format"):
        await list_tasks_tool(
            user_id="not-a-uuid",
            status="all"
        )


@pytest.mark.asyncio
async def test_list_tasks_numbered_positions():
    """Test that tasks are returned with numbered positions (1-indexed)"""
    user_id = str(uuid.uuid4())

    result = await list_tasks_tool(
        user_id=user_id,
        status="all"
    )

    # Check that positions are 1-indexed and sequential
    for idx, task in enumerate(result["tasks"]):
        assert task["position"] == idx + 1
        assert "task_id" in task
        assert "title" in task
        assert "completed" in task


@pytest.mark.asyncio
async def test_list_tasks_ordered_by_creation():
    """Test that tasks are ordered by creation date (oldest first)"""
    user_id = str(uuid.uuid4())

    result = await list_tasks_tool(
        user_id=user_id,
        status="all"
    )

    # Verify tasks have created_at timestamps
    for task in result["tasks"]:
        assert "created_at" in task

    # If multiple tasks, verify chronological order
    if len(result["tasks"]) > 1:
        for i in range(len(result["tasks"]) - 1):
            current_time = task["created_at"]
            next_time = result["tasks"][i + 1]["created_at"]
            assert current_time <= next_time


@pytest.mark.asyncio
async def test_list_tasks_user_isolation():
    """Test that tasks are isolated by user_id"""
    user1_id = str(uuid.uuid4())
    user2_id = str(uuid.uuid4())

    # List tasks for user1
    result1 = await list_tasks_tool(
        user_id=user1_id,
        status="all"
    )

    # List tasks for user2
    result2 = await list_tasks_tool(
        user_id=user2_id,
        status="all"
    )

    # Both should succeed
    assert "tasks" in result1
    assert "tasks" in result2

    # Task IDs should not overlap (if both have tasks)
    if result1["tasks"] and result2["tasks"]:
        user1_task_ids = {task["task_id"] for task in result1["tasks"]}
        user2_task_ids = {task["task_id"] for task in result2["tasks"]}
        assert user1_task_ids.isdisjoint(user2_task_ids)


@pytest.mark.asyncio
async def test_list_tasks_empty_result():
    """Test listing tasks when user has no tasks"""
    user_id = str(uuid.uuid4())

    result = await list_tasks_tool(
        user_id=user_id,
        status="all"
    )

    assert result["tasks"] == []
    assert result["count"] == 0


@pytest.mark.asyncio
async def test_list_tasks_includes_all_fields():
    """Test that all task fields are included in response"""
    user_id = str(uuid.uuid4())

    result = await list_tasks_tool(
        user_id=user_id,
        status="all"
    )

    # Check that each task has all required fields
    for task in result["tasks"]:
        assert "position" in task
        assert "task_id" in task
        assert "title" in task
        assert "description" in task
        assert "completed" in task
        assert "priority" in task
        assert "category" in task
        assert "created_at" in task
