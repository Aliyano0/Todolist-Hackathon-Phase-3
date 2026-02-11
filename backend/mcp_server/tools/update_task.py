"""
Update Task MCP Tool

Provides functionality to update a task's title and/or description.
Enforces user_id isolation and validates task ownership.
"""

from typing import Optional
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from models.todo import TodoTask
from database.session import get_async_session
import logging

logger = logging.getLogger(__name__)


async def update_task_tool(
    user_id: str,
    task_id: str,
    title: Optional[str] = None,
    description: Optional[str] = None
) -> dict:
    """
    Update a task's title and/or description

    Args:
        user_id: UUID of the user (for isolation)
        task_id: UUID of the task to update
        title: New task title (optional)
        description: New task description (optional)

    Returns:
        Dictionary with task_id, status, title, and description

    Raises:
        ValueError: If user_id or task_id is invalid, or no fields to update
        Exception: If task not found or unauthorized access
    """
    try:
        # Validate user_id format
        try:
            user_uuid = uuid.UUID(user_id)
        except (ValueError, AttributeError):
            raise ValueError(f"Invalid user_id format: {user_id}")

        # Validate task_id format
        try:
            task_uuid = uuid.UUID(task_id)
        except (ValueError, AttributeError):
            raise ValueError(f"Invalid task_id format: {task_id}")

        # Check if at least one field is provided for update
        if title is None and description is None:
            raise ValueError("At least one field (title or description) must be provided for update")

        # Validate title if provided
        if title is not None and not title.strip():
            raise ValueError("Task title cannot be empty")

        # Find and update task with user isolation
        async with get_async_session() as session:
            statement = select(TodoTask).where(
                TodoTask.id == task_uuid,
                TodoTask.user_id == user_uuid
            )
            result = await session.execute(statement)
            task = result.scalar_one_or_none()

            if not task:
                logger.warning(f"Task not found or unauthorized: {task_id} for user: {user_id}")
                raise Exception(f"Task not found or you don't have permission to access it")

            # Update fields
            updated_fields = []
            if title is not None:
                task.title = title.strip()
                updated_fields.append("title")

            if description is not None:
                task.description = description.strip() if description else None
                updated_fields.append("description")

            await session.commit()
            await session.refresh(task)

            logger.info(f"Task updated: {task_id} for user: {user_id} (fields: {', '.join(updated_fields)})")

            return {
                "task_id": str(task.id),
                "status": "updated",
                "title": task.title,
                "description": task.description,
                "updated_fields": updated_fields
            }

    except ValueError as e:
        logger.warning(f"Validation error in update_task: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error updating task {task_id} for user {user_id}: {str(e)}")
        raise


__all__ = ['update_task_tool']
