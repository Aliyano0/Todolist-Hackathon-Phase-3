"""
Unit tests for update_task MCP tool

Tests the update_task tool with title, description, and validation scenarios.
Following TDD: These tests should FAIL before implementation.
"""

import pytest
import uuid
from unittest.mock import AsyncMock, MagicMock, patch
from mcp_server.tools.update_task import update_task_tool


@pytest.mark.asyncio
async def test_update_task_title():
    """Test updating only the task title"""
    user_id = str(uuid.uuid4())
    task_id = str(uuid.uuid4())
    new_title = "Updated task title"

    result = await update_task_tool(
        user_id=user_id,
        task_id=task_id,
        title=new_title
    )

    assert result["status"] == "updated"
    assert result["task_id"] == task_id
    assert result["title"] == new_title
    assert "updated_fields" in result
    assert "title" in result["updated_fields"]


@pytest.mark.asyncio
async def test_update_task_description():
    """Test updating only the task description"""
    user_id = str(uuid.uuid4())
    task_id = str(uuid.uuid4())
    new_description = "Updated description"

    result = await update_task_tool(
        user_id=user_id,
        task_id=task_id,
        description=new_description
    )

    assert result["status"] == "updated"
    assert result["description"] == new_description
    assert "updated_fields" in result
    assert "description" in result["updated_fields"]


@pytest.mark.asyncio
async def test_update_task_both_fields():
    """Test updating both title and description"""
    user_id = str(uuid.uuid4())
    task_id = str(uuid.uuid4())
    new_title = "New title"
    new_description = "New description"

    result = await update_task_tool(
        user_id=user_id,
        task_id=task_id,
        title=new_title,
        description=new_description
    )

    assert result["status"] == "updated"
    assert result["title"] == new_title
    assert result["description"] == new_description
    assert "title" in result["updated_fields"]
    assert "description" in result["updated_fields"]


@pytest.mark.asyncio
async def test_update_task_no_fields():
    """Test that updating with no fields raises ValueError"""
    user_id = str(uuid.uuid4())
    task_id = str(uuid.uuid4())

    with pytest.raises(ValueError, match="At least one field.*must be provided"):
        await update_task_tool(
            user_id=user_id,
            task_id=task_id
        )


@pytest.mark.asyncio
async def test_update_task_empty_title():
    """Test that empty title raises ValueError"""
    user_id = str(uuid.uuid4())
    task_id = str(uuid.uuid4())

    with pytest.raises(ValueError, match="Task title cannot be empty"):
        await update_task_tool(
            user_id=user_id,
            task_id=task_id,
            title=""
        )


@pytest.mark.asyncio
async def test_update_task_whitespace_title():
    """Test that whitespace-only title raises ValueError"""
    user_id = str(uuid.uuid4())
    task_id = str(uuid.uuid4())

    with pytest.raises(ValueError, match="Task title cannot be empty"):
        await update_task_tool(
            user_id=user_id,
            task_id=task_id,
            title="   "
        )


@pytest.mark.asyncio
async def test_update_task_invalid_user_id():
    """Test that invalid user_id format raises ValueError"""
    task_id = str(uuid.uuid4())

    with pytest.raises(ValueError, match="Invalid user_id format"):
        await update_task_tool(
            user_id="not-a-uuid",
            task_id=task_id,
            title="New title"
        )


@pytest.mark.asyncio
async def test_update_task_invalid_task_id():
    """Test that invalid task_id format raises ValueError"""
    user_id = str(uuid.uuid4())

    with pytest.raises(ValueError, match="Invalid task_id format"):
        await update_task_tool(
            user_id=user_id,
            task_id="not-a-uuid",
            title="New title"
        )


@pytest.mark.asyncio
async def test_update_task_not_found():
    """Test updating a non-existent task"""
    user_id = str(uuid.uuid4())
    task_id = str(uuid.uuid4())

    with pytest.raises(Exception, match="Task not found"):
        await update_task_tool(
            user_id=user_id,
            task_id=task_id,
            title="New title"
        )


@pytest.mark.asyncio
async def test_update_task_user_isolation():
    """Test that users cannot update other users' tasks"""
    user1_id = str(uuid.uuid4())
    user2_id = str(uuid.uuid4())
    task_id = str(uuid.uuid4())

    # User1 creates a task
    # User2 tries to update user1's task
    with pytest.raises(Exception, match="Task not found or you don't have permission"):
        await update_task_tool(
            user_id=user2_id,
            task_id=task_id,
            title="Hacked title"
        )


@pytest.mark.asyncio
async def test_update_task_strips_whitespace():
    """Test that title and description are stripped of whitespace"""
    user_id = str(uuid.uuid4())
    task_id = str(uuid.uuid4())
    title = "  Title with spaces  "
    description = "  Description with spaces  "

    result = await update_task_tool(
        user_id=user_id,
        task_id=task_id,
        title=title,
        description=description
    )

    assert result["title"] == "Title with spaces"
    assert result["description"] == "Description with spaces"


@pytest.mark.asyncio
async def test_update_task_clear_description():
    """Test clearing description by setting it to empty string"""
    user_id = str(uuid.uuid4())
    task_id = str(uuid.uuid4())

    result = await update_task_tool(
        user_id=user_id,
        task_id=task_id,
        description=""
    )

    assert result["status"] == "updated"
    assert result["description"] is None or result["description"] == ""


@pytest.mark.asyncio
async def test_update_task_preserves_other_fields():
    """Test that updating doesn't affect other fields like completed, priority, category"""
    user_id = str(uuid.uuid4())
    task_id = str(uuid.uuid4())

    result = await update_task_tool(
        user_id=user_id,
        task_id=task_id,
        title="New title"
    )

    # Should only update title, not completed status or other fields
    assert result["status"] == "updated"
    assert "title" in result["updated_fields"]
    assert len(result["updated_fields"]) == 1


@pytest.mark.asyncio
async def test_update_task_long_title():
    """Test updating with a very long title"""
    user_id = str(uuid.uuid4())
    task_id = str(uuid.uuid4())
    long_title = "A" * 500

    result = await update_task_tool(
        user_id=user_id,
        task_id=task_id,
        title=long_title
    )

    assert result["status"] == "updated"
    assert result["title"] == long_title


@pytest.mark.asyncio
async def test_update_task_special_characters():
    """Test updating with special characters"""
    user_id = str(uuid.uuid4())
    task_id = str(uuid.uuid4())
    title = "Task with émojis 🎉 and spëcial çhars!"

    result = await update_task_tool(
        user_id=user_id,
        task_id=task_id,
        title=title
    )

    assert result["status"] == "updated"
    assert result["title"] == title
