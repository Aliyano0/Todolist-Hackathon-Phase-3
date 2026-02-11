"""
Add Task MCP Tool

Provides functionality to add a new task for a user.
Enforces user_id isolation and validates input.
"""

from typing import Optional
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from models.todo import TodoTask
from database.session import get_async_session
import logging

logger = logging.getLogger(__name__)


async def add_task_tool(
    user_id: str,
    title: str,
    description: Optional[str] = None,
    priority: Optional[str] = None,
    category: Optional[str] = None
) -> dict:
    """
    Add a new task for the user

    Args:
        user_id: UUID of the user (for isolation)
        title: Task title (required)
        description: Task description (optional)
        priority: Task priority (optional)
        category: Task category (optional)

    Returns:
        Dictionary with task_id, status, and title

    Raises:
        ValueError: If title is empty or user_id is invalid
    """
    try:
        # Validate inputs
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty")

        # Validate user_id format
        try:
            user_uuid = uuid.UUID(user_id)
        except (ValueError, AttributeError):
            raise ValueError(f"Invalid user_id format: {user_id}")

        # Create new task
        async with get_async_session() as session:
            new_task = TodoTask(
                user_id=user_uuid,
                title=title.strip(),
                description=description.strip() if description else None,
                priority=priority,
                category=category,
                completed=False
            )

            session.add(new_task)
            await session.commit()
            await session.refresh(new_task)

            logger.info(f"Task created: {new_task.id} for user: {user_id}")

            return {
                "task_id": str(new_task.id),
                "status": "created",
                "title": new_task.title,
                "description": new_task.description,
                "priority": new_task.priority,
                "category": new_task.category
            }

    except ValueError as e:
        logger.warning(f"Validation error in add_task: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error adding task for user {user_id}: {str(e)}")
        raise Exception(f"Failed to add task: {str(e)}")


__all__ = ['add_task_tool']
