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
    description: Optional[str] = None,
    priority: Optional[str] = None,
    category: Optional[str] = None
) -> dict:
    """
    Update a task's title, description, priority, and/or category

    Args:
        user_id: UUID of the user (for isolation)
        task_id: UUID of the task to update
        title: New task title (optional)
        description: New task description (optional)
        priority: New task priority - "low", "medium", or "high" (optional)
        category: New task category (optional)

    Returns:
        Dictionary with task_id, status, and updated fields

    Raises:
        ValueError: If user_id or task_id is invalid, invalid priority, or no fields to update
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
        if title is None and description is None and priority is None and category is None:
            raise ValueError("At least one field (title, description, priority, or category) must be provided for update")

        # Validate title if provided
        if title is not None and not title.strip():
            raise ValueError("Task title cannot be empty")

        # Validate priority if provided
        if priority is not None:
            valid_priorities = ["low", "medium", "high"]
            priority_lower = priority.lower().strip()
            if priority_lower not in valid_priorities:
                raise ValueError(f"Invalid priority: {priority}. Must be one of: {', '.join(valid_priorities)}")
            priority = priority_lower

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

            if priority is not None:
                task.priority = priority
                updated_fields.append("priority")

            if category is not None:
                task.category = category.strip() if category else None
                updated_fields.append("category")

            await session.commit()
            await session.refresh(task)

            logger.info(f"Task updated: {task_id} for user: {user_id} (fields: {', '.join(updated_fields)})")

            return {
                "task_id": str(task.id),
                "status": "updated",
                "title": task.title,
                "description": task.description,
                "priority": task.priority,
                "category": task.category,
                "updated_fields": updated_fields
            }

    except ValueError as e:
        logger.warning(f"Validation error in update_task: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error updating task {task_id} for user {user_id}: {str(e)}")
        raise


__all__ = ['update_task_tool']
