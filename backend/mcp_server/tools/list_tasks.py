"""
List Tasks MCP Tool

Provides functionality to list tasks for a user with optional status filtering.
Enforces user_id isolation and returns tasks in numbered order.
"""

from typing import Optional, List
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from models.todo import TodoTask
from database.session import get_async_session
import logging

logger = logging.getLogger(__name__)


async def list_tasks_tool(
    user_id: str,
    status: Optional[str] = "all"
) -> dict:
    """
    List tasks for the user with optional status filtering

    Args:
        user_id: UUID of the user (for isolation)
        status: Filter by status - "all", "pending", or "completed" (default: "all")

    Returns:
        Dictionary with tasks list and count

    Raises:
        ValueError: If user_id is invalid or status is unknown
    """
    try:
        # Validate user_id format
        try:
            user_uuid = uuid.UUID(user_id)
        except (ValueError, AttributeError):
            raise ValueError(f"Invalid user_id format: {user_id}")

        # Validate status parameter
        valid_statuses = ["all", "pending", "completed"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status: {status}. Must be one of {valid_statuses}")

        # Query tasks with user isolation
        async with get_async_session() as session:
            statement = select(TodoTask).where(TodoTask.user_id == user_uuid)

            # Apply status filter
            if status == "pending":
                statement = statement.where(TodoTask.completed == False)
            elif status == "completed":
                statement = statement.where(TodoTask.completed == True)

            # Order by creation date (oldest first)
            statement = statement.order_by(TodoTask.created_at)

            result = await session.execute(statement)
            tasks = result.scalars().all()

            # Format tasks with numbered positions
            formatted_tasks = [
                {
                    "position": idx + 1,  # 1-indexed for user-friendly display
                    "task_id": str(task.id),
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "priority": task.priority,
                    "category": task.category,
                    "created_at": task.created_at.isoformat()
                }
                for idx, task in enumerate(tasks)
            ]

            logger.info(f"Listed {len(formatted_tasks)} tasks for user: {user_id} (status: {status})")

            return {
                "tasks": formatted_tasks,
                "count": len(formatted_tasks),
                "status_filter": status
            }

    except ValueError as e:
        logger.warning(f"Validation error in list_tasks: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error listing tasks for user {user_id}: {str(e)}")
        raise Exception(f"Failed to list tasks: {str(e)}")


__all__ = ['list_tasks_tool']
