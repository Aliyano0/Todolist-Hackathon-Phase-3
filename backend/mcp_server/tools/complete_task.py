"""
Complete Task MCP Tool

Provides functionality to mark a task as completed.
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


async def complete_task_tool(
    user_id: str,
    task_id: str
) -> dict:
    """
    Mark a task as completed

    Args:
        user_id: UUID of the user (for isolation)
        task_id: UUID of the task to complete

    Returns:
        Dictionary with task_id, status, and title

    Raises:
        ValueError: If user_id or task_id is invalid
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

            # Check if already completed
            if task.completed:
                logger.info(f"Task already completed: {task_id}")
                return {
                    "task_id": str(task.id),
                    "status": "already_completed",
                    "title": task.title
                }

            # Mark as completed
            task.completed = True
            await session.commit()

            logger.info(f"Task completed: {task_id} for user: {user_id}")

            return {
                "task_id": str(task.id),
                "status": "completed",
                "title": task.title
            }

    except ValueError as e:
        logger.warning(f"Validation error in complete_task: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error completing task {task_id} for user {user_id}: {str(e)}")
        raise


__all__ = ['complete_task_tool']
