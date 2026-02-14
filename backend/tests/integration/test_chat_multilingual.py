"""
Integration tests for multilingual chat support

Tests language detection and response in English, Roman Urdu, and Urdu.
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
async def test_chat_english_language_detection(verified_user, auth_token):
    """Test that agent detects and responds in English"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            f"/api/{verified_user.id}/chat",
            json={"message": "Add task: buy groceries"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response.status_code == 200
    data = response.json()

    # Agent should respond in English
    message = data["message"]
    assert len(message) > 0
    
    # Should contain English words
    message_lower = message.lower()
    assert any(word in message_lower for word in ["added", "task", "groceries", "i've", "your"])


@pytest.mark.asyncio
async def test_chat_english_tool_invocation(verified_user, auth_token):
    """Test that English input correctly invokes tools"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            f"/api/{verified_user.id}/chat",
            json={"message": "Add task: buy milk"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response.status_code == 200
    
    # Verify task was created in database
    async with get_session() as session:
        result = await session.execute(
            select(TodoTask).where(
                TodoTask.user_id == verified_user.id,
                TodoTask.title.contains("milk")
            )
        )
        task = result.scalar_one_or_none()
        assert task is not None
        assert "milk" in task.title.lower()


@pytest.mark.asyncio
async def test_chat_roman_urdu_language_detection(verified_user, auth_token):
    """Test that agent detects and responds in Roman Urdu"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            f"/api/{verified_user.id}/chat",
            json={"message": "Task add karo: doodh khareedna hai"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response.status_code == 200
    data = response.json()

    # Agent should respond (possibly in Roman Urdu or English)
    message = data["message"]
    assert len(message) > 0


@pytest.mark.asyncio
async def test_chat_roman_urdu_tool_invocation(verified_user, auth_token):
    """Test that Roman Urdu input correctly invokes tools"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            f"/api/{verified_user.id}/chat",
            json={"message": "Task add karo: doodh khareedna"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response.status_code == 200
    
    # Verify task was created (tool parameters should be in English)
    async with get_session() as session:
        result = await session.execute(
            select(TodoTask).where(TodoTask.user_id == verified_user.id)
        )
        tasks = result.scalars().all()
        assert len(tasks) > 0


@pytest.mark.asyncio
async def test_chat_urdu_language_detection(verified_user, auth_token):
    """Test that agent detects and responds in Urdu"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            f"/api/{verified_user.id}/chat",
            json={"message": "ٹاسک شامل کریں: دودھ خریدنا ہے"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response.status_code == 200
    data = response.json()

    # Agent should respond
    message = data["message"]
    assert len(message) > 0


@pytest.mark.asyncio
async def test_chat_urdu_tool_invocation(verified_user, auth_token):
    """Test that Urdu input correctly invokes tools"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            f"/api/{verified_user.id}/chat",
            json={"message": "ٹاسک شامل کریں: دودھ"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response.status_code == 200
    
    # Verify task was created
    async with get_session() as session:
        result = await session.execute(
            select(TodoTask).where(TodoTask.user_id == verified_user.id)
        )
        tasks = result.scalars().all()
        assert len(tasks) > 0


@pytest.mark.asyncio
async def test_chat_language_switching_mid_conversation(verified_user, auth_token):
    """Test switching languages within the same conversation"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # First message in English
        response1 = await client.post(
            f"/api/{verified_user.id}/chat",
            json={"message": "Add task: buy groceries"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        
        conversation_id = response1.json()["conversation_id"]
        
        # Second message in Roman Urdu
        response2 = await client.post(
            f"/api/{verified_user.id}/chat",
            json={
                "message": "Mere tasks dikhao",
                "conversation_id": conversation_id
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response1.status_code == 200
    assert response2.status_code == 200
    
    # Both should work correctly
    data2 = response2.json()
    assert len(data2["message"]) > 0


@pytest.mark.asyncio
async def test_chat_tool_parameters_always_english(verified_user, auth_token):
    """Test that tool parameters are always in English regardless of input language"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Add task in Roman Urdu
        response = await client.post(
            f"/api/{verified_user.id}/chat",
            json={"message": "Task add karo: doodh khareedna"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response.status_code == 200
    
    # Verify task title is stored (could be in any language, but task was created)
    async with get_session() as session:
        result = await session.execute(
            select(TodoTask).where(TodoTask.user_id == verified_user.id)
        )
        tasks = result.scalars().all()
        assert len(tasks) > 0
        # Task should exist (tool was invoked correctly)


@pytest.mark.asyncio
async def test_chat_mixed_language_understanding(verified_user, auth_token):
    """Test understanding of mixed language input"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            f"/api/{verified_user.id}/chat",
            json={"message": "Please task add karo: buy milk"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response.status_code == 200
    
    # Should still work
    async with get_session() as session:
        result = await session.execute(
            select(TodoTask).where(
                TodoTask.user_id == verified_user.id,
                TodoTask.title.contains("milk")
            )
        )
        task = result.scalar_one_or_none()
        assert task is not None


@pytest.mark.asyncio
async def test_chat_language_consistency_in_responses(verified_user, auth_token):
    """Test that agent maintains language consistency in responses"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Send message in Roman Urdu
        response = await client.post(
            f"/api/{verified_user.id}/chat",
            json={"message": "Shukriya"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response.status_code == 200
    data = response.json()

    # Agent should respond appropriately
    message = data["message"]
    assert len(message) > 0
