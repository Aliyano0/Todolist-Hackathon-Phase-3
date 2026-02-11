"""
Integration test for chat endpoint task updates

Tests the full flow of natural language task updates through the chat endpoint.
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
            description="Milk and eggs",
            completed=False
        ),
        TodoTask(
            user_id=user.id,
            title="Finish report",
            description="Q4 report",
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
async def test_chat_update_task_title(verified_user_with_tasks, auth_token):
    """Test updating task title through natural language"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            f"/api/{verified_user_with_tasks.id}/chat",
            json={"message": "Change task 1 title to 'Buy groceries and snacks'"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response.status_code == 200
    data = response.json()

    # Verify response mentions update
    message_lower = data["message"].lower()
    assert any(keyword in message_lower for keyword in ["updated", "changed", "renamed"])
    
    # Verify task is updated in database
    async with get_session() as session:
        result = await session.execute(
            select(TodoTask).where(
                TodoTask.user_id == verified_user_with_tasks.id,
                TodoTask.title.contains("snacks")
            )
        )
        task = result.scalar_one_or_none()
        assert task is not None
        assert "snacks" in task.title.lower()


@pytest.mark.asyncio
async def test_chat_update_task_description(verified_user_with_tasks, auth_token):
    """Test updating task description through natural language"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            f"/api/{verified_user_with_tasks.id}/chat",
            json={"message": "Update task 1 description to 'Milk, eggs, bread, and butter'"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response.status_code == 200
    
    # Verify in database
    async with get_session() as session:
        result = await session.execute(
            select(TodoTask).where(
                TodoTask.user_id == verified_user_with_tasks.id,
                TodoTask.title == "Buy groceries"
            )
        )
        task = result.scalar_one_or_none()
        assert task is not None
        assert "butter" in task.description.lower()


@pytest.mark.asyncio
async def test_chat_update_task_ambiguous_request(verified_user_with_tasks, auth_token):
    """Test that agent asks for clarification on ambiguous update requests"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            f"/api/{verified_user_with_tasks.id}/chat",
            json={"message": "Update task 1"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response.status_code == 200
    data = response.json()

    # Agent should ask what to update
    message_lower = data["message"].lower()
    assert any(keyword in message_lower for keyword in ["what", "which", "title", "description", "change"])


@pytest.mark.asyncio
async def test_chat_update_task_not_found(verified_user_with_tasks, auth_token):
    """Test updating a non-existent task"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            f"/api/{verified_user_with_tasks.id}/chat",
            json={"message": "Update task 999 title to 'New title'"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response.status_code == 200
    data = response.json()

    # Agent should indicate task not found
    message_lower = data["message"].lower()
    assert any(keyword in message_lower for keyword in ["not found", "doesn't exist", "can't find"])


@pytest.mark.asyncio
async def test_chat_update_task_variations(verified_user_with_tasks, auth_token):
    """Test different natural language variations for updating tasks"""
    variations = [
        "Change task 1 title to 'New title'",
        "Rename task 1 to 'New title'",
        "Update task 1 name to 'New title'",
        "Modify task 1 title to 'New title'"
    ]
    
    for message in variations:
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                f"/api/{verified_user_with_tasks.id}/chat",
                json={"message": message},
                headers={"Authorization": f"Bearer {auth_token}"}
            )

        assert response.status_code == 200


@pytest.mark.asyncio
async def test_chat_update_task_with_confirmation(verified_user_with_tasks, auth_token):
    """Test that agent provides confirmation with old and new values"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            f"/api/{verified_user_with_tasks.id}/chat",
            json={"message": "Change task 1 title to 'Buy groceries and snacks'"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response.status_code == 200
    data = response.json()

    # Agent should mention the update
    message_lower = data["message"].lower()
    assert "updated" in message_lower or "changed" in message_lower


@pytest.mark.asyncio
async def test_chat_update_task_by_name(verified_user_with_tasks, auth_token):
    """Test updating task by name instead of position"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            f"/api/{verified_user_with_tasks.id}/chat",
            json={"message": "Change 'Buy groceries' to 'Buy groceries and snacks'"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response.status_code == 200
    
    # Verify in database
    async with get_session() as session:
        result = await session.execute(
            select(TodoTask).where(
                TodoTask.user_id == verified_user_with_tasks.id,
                TodoTask.title.contains("snacks")
            )
        )
        task = result.scalar_one_or_none()
        assert task is not None


@pytest.mark.asyncio
async def test_chat_update_task_user_isolation(verified_user_with_tasks, auth_token):
    """Test that users cannot update other users' tasks"""
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
        original_title = other_task.title
    
    # Try to update other user's task
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            f"/api/{verified_user_with_tasks.id}/chat",
            json={"message": f"Update task {other_task_id} title to 'Hacked'"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response.status_code == 200
    
    # Task should NOT be updated (user isolation)
    async with get_session() as session:
        result = await session.execute(
            select(TodoTask).where(TodoTask.id == other_task_id)
        )
        task = result.scalar_one_or_none()
        assert task.title == original_title  # Title unchanged


@pytest.mark.asyncio
async def test_chat_update_task_multilingual_roman_urdu(verified_user_with_tasks, auth_token):
    """Test updating task in Roman Urdu"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            f"/api/{verified_user_with_tasks.id}/chat",
            json={"message": "Task 1 ka title change karo 'Groceries khareedna'"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response.status_code == 200
    
    # Verify task is updated
    async with get_session() as session:
        result = await session.execute(
            select(TodoTask).where(
                TodoTask.user_id == verified_user_with_tasks.id
            )
        )
        tasks = result.scalars().all()
        # At least one task should have been updated
        assert len(tasks) > 0


@pytest.mark.asyncio
async def test_chat_update_task_preserves_other_fields(verified_user_with_tasks, auth_token):
    """Test that updating title doesn't affect other fields"""
    # Get original task state
    async with get_session() as session:
        result = await session.execute(
            select(TodoTask).where(
                TodoTask.user_id == verified_user_with_tasks.id,
                TodoTask.title == "Buy groceries"
            )
        )
        original_task = result.scalar_one_or_none()
        original_description = original_task.description
        original_completed = original_task.completed
    
    # Update title
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            f"/api/{verified_user_with_tasks.id}/chat",
            json={"message": "Change task 1 title to 'Buy groceries and snacks'"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response.status_code == 200
    
    # Verify other fields unchanged
    async with get_session() as session:
        result = await session.execute(
            select(TodoTask).where(
                TodoTask.user_id == verified_user_with_tasks.id,
                TodoTask.title.contains("snacks")
            )
        )
        updated_task = result.scalar_one_or_none()
        assert updated_task.description == original_description
        assert updated_task.completed == original_completed
