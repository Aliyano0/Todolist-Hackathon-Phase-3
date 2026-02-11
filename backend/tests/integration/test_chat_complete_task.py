"""
Integration test for chat endpoint task completion

Tests the full flow of natural language task completion through the chat endpoint.
Following TDD: These tests should FAIL before implementation.
"""

import pytest
import uuid
from httpx import AsyncClient
from datetime import datetime, timedelta
from jose import jwt
import os

from main import app
from database.session import get_session
from models.user import User
from models.todo import TodoTask
from sqlmodel import select


@pytest.fixture
async def verified_user_with_tasks(session):
    """Create a verified user with sample tasks"""
    user = User(
        email="test@example.com",
        password_hash="hashed_password",
        email_verified=True,
        verification_token=None
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)

    # Add sample tasks
    tasks = [
        TodoTask(
            user_id=user.id,
            title="Buy groceries",
            completed=False
        ),
        TodoTask(
            user_id=user.id,
            title="Finish report",
            completed=False
        ),
        TodoTask(
            user_id=user.id,
            title="Call dentist",
            completed=False
        )
    ]
    
    for task in tasks:
        session.add(task)
    
    await session.commit()
    
    return user


@pytest.fixture
def auth_token(verified_user_with_tasks):
    """Create a valid JWT token for the verified user"""
    secret = os.getenv("BETTER_AUTH_SECRET", "test-secret-key-for-testing-only")
    payload = {
        "sub": str(verified_user_with_tasks.id),
        "email": verified_user_with_tasks.email,
        "email_verified": True,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    token = jwt.encode(payload, secret, algorithm="HS256")
    return token


@pytest.mark.asyncio
async def test_chat_complete_task_by_position(verified_user_with_tasks, auth_token):
    """Test completing a task by position number"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # First, list tasks to establish context
        response1 = await client.post(
            f"/api/{verified_user_with_tasks.id}/chat",
            json={"message": "Show my tasks"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        
        conversation_id = response1.json()["conversation_id"]
        
        # Complete task 1
        response2 = await client.post(
            f"/api/{verified_user_with_tasks.id}/chat",
            json={
                "message": "Mark task 1 as done",
                "conversation_id": conversation_id
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response2.status_code == 200
    data = response2.json()

    # Verify response mentions completion
    message_lower = data["message"].lower()
    assert any(keyword in message_lower for keyword in ["completed", "done", "marked", "finished"])
    
    # Verify task is actually completed in database
    async with get_session() as session:
        result = await session.execute(
            select(TodoTask).where(
                TodoTask.user_id == verified_user_with_tasks.id,
                TodoTask.title == "Buy groceries"
            )
        )
        task = result.scalar_one_or_none()
        assert task is not None
        assert task.completed is True


@pytest.mark.asyncio
async def test_chat_complete_task_by_name(verified_user_with_tasks, auth_token):
    """Test completing a task by name"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            f"/api/{verified_user_with_tasks.id}/chat",
            json={"message": "Mark 'Buy groceries' as complete"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response.status_code == 200
    data = response.json()

    message_lower = data["message"].lower()
    assert "completed" in message_lower or "done" in message_lower
    
    # Verify in database
    async with get_session() as session:
        result = await session.execute(
            select(TodoTask).where(
                TodoTask.user_id == verified_user_with_tasks.id,
                TodoTask.title == "Buy groceries"
            )
        )
        task = result.scalar_one_or_none()
        assert task.completed is True


@pytest.mark.asyncio
async def test_chat_complete_task_variations(verified_user_with_tasks, auth_token):
    """Test different natural language variations for completing tasks"""
    variations = [
        "Complete task 1",
        "Mark task 1 as done",
        "Task 1 is finished",
        "I finished task 1",
        "Done with task 1"
    ]
    
    for idx, message in enumerate(variations):
        # Create a new task for each variation
        async with get_session() as session:
            task = TodoTask(
                user_id=verified_user_with_tasks.id,
                title=f"Test task {idx}",
                completed=False
            )
            session.add(task)
            await session.commit()
        
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                f"/api/{verified_user_with_tasks.id}/chat",
                json={"message": message},
                headers={"Authorization": f"Bearer {auth_token}"}
            )

        assert response.status_code == 200


@pytest.mark.asyncio
async def test_chat_complete_nonexistent_task(verified_user_with_tasks, auth_token):
    """Test completing a task that doesn't exist"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            f"/api/{verified_user_with_tasks.id}/chat",
            json={"message": "Complete task 999"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response.status_code == 200
    data = response.json()

    # Agent should indicate task not found
    message_lower = data["message"].lower()
    assert any(keyword in message_lower for keyword in ["not found", "doesn't exist", "can't find"])


@pytest.mark.asyncio
async def test_chat_complete_already_completed_task(verified_user_with_tasks, auth_token):
    """Test completing a task that is already completed"""
    # First completion
    async with AsyncClient(app=app, base_url="http://test") as client:
        response1 = await client.post(
            f"/api/{verified_user_with_tasks.id}/chat",
            json={"message": "Complete task 1"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )
    
    assert response1.status_code == 200
    
    # Second completion (already completed)
    async with AsyncClient(app=app, base_url="http://test") as client:
        response2 = await client.post(
            f"/api/{verified_user_with_tasks.id}/chat",
            json={"message": "Complete task 1"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response2.status_code == 200
    data = response2.json()

    # Agent should indicate task is already completed
    message_lower = data["message"].lower()
    assert "already" in message_lower or "completed" in message_lower


@pytest.mark.asyncio
async def test_chat_complete_task_with_confirmation(verified_user_with_tasks, auth_token):
    """Test that agent provides confirmation with task title"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            f"/api/{verified_user_with_tasks.id}/chat",
            json={"message": "Mark task 1 as done"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response.status_code == 200
    data = response.json()

    # Agent should mention the task title in confirmation
    message_lower = data["message"].lower()
    assert "groceries" in message_lower or "buy" in message_lower


@pytest.mark.asyncio
async def test_chat_complete_multiple_tasks(verified_user_with_tasks, auth_token):
    """Test completing multiple tasks in sequence"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Complete task 1
        response1 = await client.post(
            f"/api/{verified_user_with_tasks.id}/chat",
            json={"message": "Complete task 1"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        
        conversation_id = response1.json()["conversation_id"]
        
        # Complete task 2
        response2 = await client.post(
            f"/api/{verified_user_with_tasks.id}/chat",
            json={
                "message": "Complete task 2",
                "conversation_id": conversation_id
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response1.status_code == 200
    assert response2.status_code == 200
    
    # Verify both tasks are completed
    async with get_session() as session:
        result = await session.execute(
            select(TodoTask).where(
                TodoTask.user_id == verified_user_with_tasks.id,
                TodoTask.completed == True
            )
        )
        completed_tasks = result.scalars().all()
        assert len(completed_tasks) >= 2


@pytest.mark.asyncio
async def test_chat_complete_task_multilingual_roman_urdu(verified_user_with_tasks, auth_token):
    """Test completing task in Roman Urdu"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            f"/api/{verified_user_with_tasks.id}/chat",
            json={"message": "Task 1 complete karo"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response.status_code == 200
    
    # Verify task is completed
    async with get_session() as session:
        result = await session.execute(
            select(TodoTask).where(
                TodoTask.user_id == verified_user_with_tasks.id,
                TodoTask.title == "Buy groceries"
            )
        )
        task = result.scalar_one_or_none()
        assert task.completed is True


@pytest.mark.asyncio
async def test_chat_complete_task_user_isolation(verified_user_with_tasks, auth_token):
    """Test that users cannot complete other users' tasks"""
    # Create another user with a task
    async with get_session() as session:
        other_user = User(
            email="other@example.com",
            password_hash="hashed",
            email_verified=True
        )
        session.add(other_user)
        await session.commit()
        await session.refresh(other_user)
        
        other_task = TodoTask(
            user_id=other_user.id,
            title="Other user's task",
            completed=False
        )
        session.add(other_task)
        await session.commit()
        await session.refresh(other_task)
        other_task_id = other_task.id
    
    # Try to complete other user's task
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            f"/api/{verified_user_with_tasks.id}/chat",
            json={"message": f"Complete task {other_task_id}"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response.status_code == 200
    
    # Task should NOT be completed (user isolation)
    async with get_session() as session:
        result = await session.execute(
            select(TodoTask).where(TodoTask.id == other_task_id)
        )
        task = result.scalar_one_or_none()
        assert task.completed is False
