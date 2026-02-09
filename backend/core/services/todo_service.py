from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from typing import List, Optional
import uuid
from datetime import datetime
from models.todo import TodoTask
from schemas.todo import TodoTaskCreate, TodoTaskUpdate


async def get_all_tasks_for_user(session: AsyncSession, user_id: uuid.UUID) -> List[TodoTask]:
    """
    Retrieve all tasks for a specific user
    """
    statement = select(TodoTask).where(TodoTask.user_id == user_id)
    result = await session.execute(statement)
    tasks = result.scalars().all()
    return list(tasks)


async def get_task_by_id_for_user(session: AsyncSession, task_id: uuid.UUID, user_id: uuid.UUID) -> Optional[TodoTask]:
    """
    Retrieve a specific task by ID for a specific user
    """
    statement = select(TodoTask).where(TodoTask.id == task_id, TodoTask.user_id == user_id)
    result = await session.execute(statement)
    task = result.scalar_one_or_none()
    return task


async def create_task(session: AsyncSession, task_data: TodoTaskCreate, user_id: uuid.UUID) -> TodoTask:
    """
    Create a new task in the database for a specific user
    """
    task = TodoTask(
        title=task_data.title,
        description=task_data.description,
        completed=getattr(task_data, 'completed', False),
        priority=getattr(task_data, 'priority', 'medium'),  # Default priority
        category=getattr(task_data, 'category', 'personal'),  # Default category
        user_id=user_id
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


async def update_task(session: AsyncSession, task_id: uuid.UUID, task_update: TodoTaskUpdate, user_id: uuid.UUID) -> Optional[TodoTask]:
    """
    Update an existing task in the database for a specific user
    """
    task = await get_task_by_id_for_user(session, task_id, user_id)
    if not task:
        return None

    # Update the task with provided fields
    update_data = task_update.dict(exclude_unset=True)

    for field, value in update_data.items():
        setattr(task, field, value)

    task.updated_at = datetime.utcnow()
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


async def delete_task(session: AsyncSession, task_id: uuid.UUID, user_id: uuid.UUID) -> bool:
    """
    Delete a task from the database for a specific user
    """
    task = await get_task_by_id_for_user(session, task_id, user_id)
    if not task:
        return False

    await session.delete(task)
    await session.commit()
    return True


async def toggle_task_completion(session: AsyncSession, task_id: uuid.UUID, user_id: uuid.UUID) -> Optional[TodoTask]:
    """
    Toggle the completion status of a task for a specific user
    """
    task = await get_task_by_id_for_user(session, task_id, user_id)
    if not task:
        return None

    task.completed = not task.completed
    task.updated_at = datetime.utcnow()
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task