"""
Integration test for chat endpoint task creation

Tests the full flow of natural language task creation through the chat endpoint.
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
async def verified_user(session):
    """Create a verified user for testing"""
    user = User(
        email="test@example.com",
        password_hash="hashed_password",
        email_verified=True,
        verification_token=None
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@pytest.fixture
def auth_token(verified_user):
    """Create a valid JWT token for the verified user"""
    secret = os.getenv("BETTER_AUTH_SECRET", "test-secret-key-for-testing-only")
    payload = {
        "sub": str(verified_user.id),
        "email": verified_user.email,
        "email_verified": True,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    token = jwt.encode(payload, secret, algorithm="HS256")
    return token


@pytest.mark.asyncio
async def test_chat_add_task_simple(verified_user, auth_token):
    """Test adding a simple task through natural language"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            f"/api/{verified_user.id}/chat",
            json={
                "message": "Add task: buy groceries"
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response.status_code == 200
    data = response.json()

    # Verify response structure
    assert "conversation_id" in data
    assert "message" in data
    assert "timestamp" in data

    # Verify conversation_id is a valid UUID
    uuid.UUID(data["conversation_id"])

    # Verify agent response mentions task creation
    assert "buy groceries" in data["message"].lower() or "added" in data["message"].lower()

    # Verify task was created in database
    async with get_session() as session:
        result = await session.execute(
            select(TodoTask).where(
                TodoTask.user_id == verified_user.id,
                TodoTask.title.contains("groceries")
            )
        )
        task = result.scalar_one_or_none()
        assert task is not None
        assert "groceries" in task.title.lower()
        assert task.completed is False


@pytest.mark.asyncio
async def test_chat_add_task_with_description(verified_user, auth_token):
    """Test adding a task with description through natural language"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            f"/api/{verified_user.id}/chat",
            json={
                "message": "Add a task to buy milk and eggs from the store"
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response.status_code == 200
    data = response.json()

    # Verify task was created
    async with get_session() as session:
        result = await session.execute(
            select(TodoTask).where(TodoTask.user_id == verified_user.id)
        )
        tasks = result.scalars().all()
        assert len(tasks) > 0
        # At least one task should mention milk or eggs
        assert any("milk" in task.title.lower() or "eggs" in task.title.lower() for task in tasks)


@pytest.mark.asyncio
async def test_chat_add_task_unverified_email(verified_user, auth_token):
    """Test that unverified users cannot access chat"""
    # Update user to unverified
    async with get_session() as session:
        result = await session.execute(
            select(User).where(User.id == verified_user.id)
        )
        user = result.scalar_one()
        user.email_verified = False
        await session.commit()

    # Create token with email_verified=False
    secret = os.getenv("BETTER_AUTH_SECRET", "test-secret-key-for-testing-only")
    payload = {
        "sub": str(verified_user.id),
        "email": verified_user.email,
        "email_verified": False,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    unverified_token = jwt.encode(payload, secret, algorithm="HS256")

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            f"/api/{verified_user.id}/chat",
            json={
                "message": "Add task: test"
            },
            headers={"Authorization": f"Bearer {unverified_token}"}
        )

    assert response.status_code == 403
    assert "email verification" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_chat_add_task_no_auth(verified_user):
    """Test that unauthenticated requests are rejected"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            f"/api/{verified_user.id}/chat",
            json={
                "message": "Add task: test"
            }
        )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_chat_add_task_wrong_user(verified_user, auth_token):
    """Test that users cannot access other users' chat"""
    other_user_id = str(uuid.uuid4())

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            f"/api/{other_user_id}/chat",
            json={
                "message": "Add task: test"
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_chat_add_task_conversation_persistence(verified_user, auth_token):
    """Test that conversation is persisted and can be resumed"""
    # First message
    async with AsyncClient(app=app, base_url="http://test") as client:
        response1 = await client.post(
            f"/api/{verified_user.id}/chat",
            json={
                "message": "Add task: first task"
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response1.status_code == 200
    conversation_id = response1.json()["conversation_id"]

    # Second message in same conversation
    async with AsyncClient(app=app, base_url="http://test") as client:
        response2 = await client.post(
            f"/api/{verified_user.id}/chat",
            json={
                "message": "Add task: second task",
                "conversation_id": conversation_id
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response2.status_code == 200
    assert response2.json()["conversation_id"] == conversation_id

    # Verify both tasks were created
    async with get_session() as session:
        result = await session.execute(
            select(TodoTask).where(TodoTask.user_id == verified_user.id)
        )
        tasks = result.scalars().all()
        assert len(tasks) >= 2


@pytest.mark.asyncio
async def test_chat_add_task_multilingual_roman_urdu(verified_user, auth_token):
    """Test adding task in Roman Urdu"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            f"/api/{verified_user.id}/chat",
            json={
                "message": "Task add karo: doodh khareedna hai"
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response.status_code == 200
    data = response.json()

    # Agent should respond in Roman Urdu
    # But task should still be created
    async with get_session() as session:
        result = await session.execute(
            select(TodoTask).where(TodoTask.user_id == verified_user.id)
        )
        tasks = result.scalars().all()
        assert len(tasks) > 0
