from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from utils.format_utils import convert_dict_keys_to_camel, snake_to_camel
from database.session import get_session
from models.todo import TodoTask
from schemas.todo import (
    TodoTaskRead,
    TodoTaskCreate,
    TodoTaskUpdate,
    TodoTaskToggleComplete,
    ErrorResponse
)
from core.services.todo_service import (
    create_task,
    update_task,
    delete_task,
    toggle_task_completion,
    get_all_tasks_for_user,
    get_task_by_id_for_user
)
from dependencies.auth import get_current_user
from models.user import User
import uuid

# Create API router for task endpoints with user_id in path
router = APIRouter(prefix="/{user_id}/tasks", tags=["tasks"])


def verify_user_access(user_id: str, current_user: User) -> uuid.UUID:
    """
    Verify that the user_id in the path matches the authenticated user.
    Returns the validated UUID or raises 403 Forbidden.
    """
    try:
        path_user_id = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user_id format"
        )

    if path_user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot access another user's tasks"
        )

    return path_user_id


@router.get("")
async def list_tasks(
    user_id: str,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Get all tasks for the authenticated user
    """
    # Verify user_id in path matches authenticated user
    verified_user_id = verify_user_access(user_id, current_user)

    # Filter tasks by current user's ID
    tasks = await get_all_tasks_for_user(session, verified_user_id)

    # Convert snake_case to camelCase
    converted_tasks = []
    for task in tasks:
        task_dict = task.dict()
        # Convert UUID to string for JSON serialization
        task_dict['id'] = str(task_dict['id'])
        task_dict['user_id'] = str(task_dict['user_id'])
        # Convert to camelCase
        converted_task = convert_dict_keys_to_camel(task_dict)
        converted_tasks.append(converted_task)

    return {"data": converted_tasks}


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_new_task(
    user_id: str,
    task: TodoTaskCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new task for the authenticated user
    """
    # Verify user_id in path matches authenticated user
    verified_user_id = verify_user_access(user_id, current_user)

    # Validate that title is provided
    if not task.title or len(task.title.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title is required and cannot be empty"
        )

    # Validate title length
    if len(task.title) > 255:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title must be less than 255 characters"
        )

    created_task = await create_task(session, task, verified_user_id)

    # Convert to dict and convert to camelCase
    task_dict = created_task.dict()
    task_dict['id'] = str(task_dict['id'])
    task_dict['user_id'] = str(task_dict['user_id'])
    converted_task = convert_dict_keys_to_camel(task_dict)

    return {"data": converted_task}


@router.get("/{task_id}")
async def get_task(
    user_id: str,
    task_id: str,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific task by ID for the authenticated user
    """
    # Verify user_id in path matches authenticated user
    verified_user_id = verify_user_access(user_id, current_user)

    # Convert task_id string to UUID
    try:
        task_uuid = uuid.UUID(task_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task_id format"
        )

    task = await get_task_by_id_for_user(session, task_uuid, verified_user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found or not owned by user"
        )

    # Convert to dict and convert to camelCase
    task_dict = task.dict()
    task_dict['id'] = str(task_dict['id'])
    task_dict['user_id'] = str(task_dict['user_id'])
    converted_task = convert_dict_keys_to_camel(task_dict)

    return {"data": converted_task}


@router.put("/{task_id}")
async def update_existing_task(
    user_id: str,
    task_id: str,
    task_update: TodoTaskUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Update an existing task for the authenticated user
    """
    # Verify user_id in path matches authenticated user
    verified_user_id = verify_user_access(user_id, current_user)

    # Convert task_id string to UUID
    try:
        task_uuid = uuid.UUID(task_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task_id format"
        )

    # Validate title if provided
    if task_update.title is not None:
        if len(task_update.title) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Title cannot be empty"
            )
        if len(task_update.title) > 255:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Title must be less than 255 characters"
            )

    updated_task = await update_task(session, task_uuid, task_update, verified_user_id)
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found or not owned by user"
        )

    # Convert to dict and convert to camelCase
    task_dict = updated_task.dict()
    task_dict['id'] = str(task_dict['id'])
    task_dict['user_id'] = str(task_dict['user_id'])
    converted_task = convert_dict_keys_to_camel(task_dict)

    return {"data": converted_task}


@router.delete("/{task_id}")
async def delete_existing_task(
    user_id: str,
    task_id: str,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a task for the authenticated user
    """
    # Verify user_id in path matches authenticated user
    verified_user_id = verify_user_access(user_id, current_user)

    # Convert task_id string to UUID
    try:
        task_uuid = uuid.UUID(task_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task_id format"
        )

    # First get the task to return it
    task = await get_task_by_id_for_user(session, task_uuid, verified_user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found or not owned by user"
        )

    success = await delete_task(session, task_uuid, verified_user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found or not owned by user"
        )

    # Convert to dict and convert to camelCase
    task_dict = task.dict()
    task_dict['id'] = str(task_dict['id'])
    task_dict['user_id'] = str(task_dict['user_id'])
    converted_task = convert_dict_keys_to_camel(task_dict)

    return {"data": converted_task}


@router.patch("/{task_id}/toggle")
async def toggle_task_complete_status(
    user_id: str,
    task_id: str,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Toggle the completion status of a task for the authenticated user
    """
    # Verify user_id in path matches authenticated user
    verified_user_id = verify_user_access(user_id, current_user)

    # Convert task_id string to UUID
    try:
        task_uuid = uuid.UUID(task_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task_id format"
        )

    toggled_task = await toggle_task_completion(session, task_uuid, verified_user_id)
    if not toggled_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found or not owned by user"
        )

    # Convert to dict and convert to camelCase
    task_dict = toggled_task.dict()
    task_dict['id'] = str(task_dict['id'])
    task_dict['user_id'] = str(task_dict['user_id'])
    converted_task = convert_dict_keys_to_camel(task_dict)

    return {"data": converted_task}


@router.patch("/{task_id}/complete")
async def toggle_task_completion_alt(
    user_id: str,
    task_id: str,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Toggle the completion status of a task (alternative endpoint) for the authenticated user
    """
    # Verify user_id in path matches authenticated user
    verified_user_id = verify_user_access(user_id, current_user)

    # Convert task_id string to UUID
    try:
        task_uuid = uuid.UUID(task_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task_id format"
        )

    toggled_task = await toggle_task_completion(session, task_uuid, verified_user_id)
    if not toggled_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found or not owned by user"
        )

    # Convert to dict and convert to camelCase
    task_dict = toggled_task.dict()
    task_dict['id'] = str(task_dict['id'])
    task_dict['user_id'] = str(task_dict['user_id'])
    converted_task = convert_dict_keys_to_camel(task_dict)

    return {"data": converted_task}
