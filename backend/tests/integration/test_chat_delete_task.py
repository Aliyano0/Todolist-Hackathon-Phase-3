"""
Integration test for chat endpoint task deletion with confirmation

Tests the full flow of natural language task deletion with confirmation prompts.
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
async def test_chat_delete_task_requires_confirmation(verified_user_with_tasks, auth_token):
    """Test that deleting a task requires confirmation"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            f"/api/{verified_user_with_tasks.id}/chat",
            json={"message": "Delete task 1"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response.status_code == 200
    data = response.json()

    # Agent should ask for confirmation
    message_lower = data["message"].lower()
    assert any(keyword in message_lower for keyword in ["sure", "confirm", "delete", "certain"])
    
    # Task should NOT be deleted yet
    async with get_session() as session:
        result = await session.execute(
            select(TodoTask).where(
                TodoTask.user_id == verified_user_with_tasks.id,
                TodoTask.title == "Buy groceries"
            )
        )
        task = result.scalar_one_or_none()
        assert task is not None  # Task still exists


@pytest.mark.asyncio
async def test_chat_delete_task_with_confirmation(verified_user_with_tasks, auth_token):
    """Test deleting a task after confirmation"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Request deletion
        response1 = await client.post(
            f"/api/{verified_user_with_tasks.id}/chat",
            json={"message": "Delete task 1"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        
        conversation_id = response1.json()["conversation_id"]
        
        # Confirm deletion
        response2 = await client.post(
            f"/api/{verified_user_with_tasks.id}/chat",
            json={
                "message": "Yes, I'm sure",
                "conversation_id": conversation_id
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response2.status_code == 200
    data = response2.json()

    # Agent should confirm deletion
    message_lower = data["message"].lower()
    assert "deleted" in message_lower or "removed" in message_lower
    
    # Task should be deleted
    async with get_session() as session:
        result = await session.execute(
            select(TodoTask).where(
                TodoTask.user_id == verified_user_with_tasks.id,
                TodoTask.title == "Buy groceries"
            )
        )
        task = result.scalar_one_or_none()
        assert task is None  # Task deleted


@pytest.mark.asyncio
async def test_chat_delete_task_cancel_confirmation(verified_user_with_tasks, auth_token):
    """Test canceling task deletion"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Request deletion
        response1 = await client.post(
            f"/api/{verified_user_with_tasks.id}/chat",
            json={"message": "Delete task 1"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        
        conversation_id = response1.json()["conversation_id"]
        
        # Cancel deletion
        response2 = await client.post(
            f"/api/{verified_user_with_tasks.id}/chat",
            json={
                "message": "No, cancel that",
                "conversation_id": conversation_id
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response2.status_code == 200
    data = response2.json()

    # Agent should acknowledge cancellation
    message_lower = data["message"].lower()
    assert any(keyword in message_lower for keyword in ["cancelled", "canceled", "kept", "not deleted"])
    
    # Task should still exist
    async with get_session() as session:
        result = await session.execute(
            select(TodoTask).where(
                TodoTask.user_id == verified_user_with_tasks.id,
                TodoTask.title == "Buy groceries"
            )
        )
        task = result.scalar_one_or_none()
        assert task is not None  # Task still exists


@pytest.mark.asyncio
async def test_chat_delete_task_confirmation_variations(verified_user_with_tasks, auth_token):
    """Test different confirmation phrases"""
    confirmation_phrases = [
        "Yes",
        "Yes, delete it",
        "I'm sure",
        "Confirm",
        "Go ahead"
    ]
    
    for phrase in confirmation_phrases:
        # Create a new task for each test
        async with get_session() as session:
            task = TodoTask(
                user_id=verified_user_with_tasks.id,
                title=f"Test task {phrase}",
                completed=False
            )
            session.add(task)
            await session.commit()
        
        async with AsyncClient(app=app, base_url="http://test") as client:
            # Request deletion
            response1 = await client.post(
                f"/api/{verified_user_with_tasks.id}/chat",
                json={"message": "Delete the test task"},
                headers={"Authorization": f"Bearer {auth_token}"}
            )
            
            conversation_id = response1.json()["conversation_id"]
            
            # Confirm with variation
            response2 = await client.post(
                f"/api/{verified_user_with_tasks.id}/chat",
                json={
                    "message": phrase,
                    "conversation_id": conversation_id
                },
                headers={"Authorization": f"Bearer {auth_token}"}
            )

        assert response2.status_code == 200


@pytest.mark.asyncio
async def test_chat_delete_task_not_found(verified_user_with_tasks, auth_token):
    """Test deleting a non-existent task"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            f"/api/{verified_user_with_tasks.id}/chat",
            json={"message": "Delete task 999"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response.status_code == 200
    data = response.json()

    # Agent should indicate task not found
    message_lower = data["message"].lower()
    assert any(keyword in message_lower for keyword in ["not found", "doesn't exist", "can't find"])


@pytest.mark.asyncio
async def test_chat_delete_task_mentions_title_in_confirmation(verified_user_with_tasks, auth_token):
    """Test that confirmation prompt mentions the task title"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            f"/api/{verified_user_with_tasks.id}/chat",
            json={"message": "Delete task 1"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response.status_code == 200
    data = response.json()

    # Confirmation should mention task title
    message_lower = data["message"].lower()
    assert "groceries" in message_lower or "buy" in message_lower


@pytest.mark.asyncio
async def test_chat_delete_task_user_isolation(verified_user_with_tasks, auth_token):
    """Test that users cannot delete other users' tasks"""
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
    
    # Try to delete other user's task
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            f"/api/{verified_user_with_tasks.id}/chat",
            json={"message": f"Delete task {other_task_id}"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response.status_code == 200
    
    # Task should NOT be deleted (user isolation)
    async with get_session() as session:
        result = await session.execute(
            select(TodoTask).where(TodoTask.id == other_task_id)
        )
        task = result.scalar_one_or_none()
        assert task is not None  # Task still exists


@pytest.mark.asyncio
async def test_chat_delete_task_multilingual_roman_urdu(verified_user_with_tasks, auth_token):
    """Test deleting task in Roman Urdu with confirmation"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Request deletion in Roman Urdu
        response1 = await client.post(
            f"/api/{verified_user_with_tasks.id}/chat",
            json={"message": "Task 1 delete karo"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        
        conversation_id = response1.json()["conversation_id"]
        
        # Confirm in Roman Urdu
        response2 = await client.post(
            f"/api/{verified_user_with_tasks.id}/chat",
            json={
                "message": "Haan, delete karo",
                "conversation_id": conversation_id
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response2.status_code == 200
    
    # Task should be deleted
    async with get_session() as session:
        result = await session.execute(
            select(TodoTask).where(
                TodoTask.user_id == verified_user_with_tasks.id,
                TodoTask.title == "Buy groceries"
            )
        )
        task = result.scalar_one_or_none()
        assert task is None


@pytest.mark.asyncio
async def test_chat_delete_task_timeout_confirmation(verified_user_with_tasks, auth_token):
    """Test that confirmation context expires after unrelated messages"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Request deletion
        response1 = await client.post(
            f"/api/{verified_user_with_tasks.id}/chat",
            json={"message": "Delete task 1"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        
        conversation_id = response1.json()["conversation_id"]
        
        # Send unrelated message
        await client.post(
            f"/api/{verified_user_with_tasks.id}/chat",
            json={
                "message": "Show my tasks",
                "conversation_id": conversation_id
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        
        # Try to confirm (context should be lost)
        response3 = await client.post(
            f"/api/{verified_user_with_tasks.id}/chat",
            json={
                "message": "Yes, I'm sure",
                "conversation_id": conversation_id
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response3.status_code == 200
    
    # Task should still exist (confirmation expired)
    async with get_session() as session:
        result = await session.execute(
            select(TodoTask).where(
                TodoTask.user_id == verified_user_with_tasks.id,
                TodoTask.title == "Buy groceries"
            )
        )
        task = result.scalar_one_or_none()
        assert task is not None
