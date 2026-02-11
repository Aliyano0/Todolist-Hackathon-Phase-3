"""
Integration test for chat endpoint task listing

Tests the full flow of natural language task queries through the chat endpoint.
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
            description="Milk, eggs, bread",
            completed=False,
            priority="high",
            category="shopping"
        ),
        TodoTask(
            user_id=user.id,
            title="Finish report",
            description="Q4 financial report",
            completed=True,
            priority="high",
            category="work"
        ),
        TodoTask(
            user_id=user.id,
            title="Call dentist",
            description="Schedule appointment",
            completed=False,
            priority="medium",
            category="health"
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
async def test_chat_list_all_tasks(verified_user_with_tasks, auth_token):
    """Test listing all tasks through natural language"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            f"/api/{verified_user_with_tasks.id}/chat",
            json={
                "message": "Show my tasks"
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response.status_code == 200
    data = response.json()

    # Verify response structure
    assert "message" in data
    
    # Agent response should mention tasks
    message_lower = data["message"].lower()
    assert any(keyword in message_lower for keyword in ["task", "todo", "list"])
    
    # Response should mention task titles
    assert "groceries" in message_lower or "report" in message_lower or "dentist" in message_lower


@pytest.mark.asyncio
async def test_chat_list_pending_tasks(verified_user_with_tasks, auth_token):
    """Test listing only pending tasks"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            f"/api/{verified_user_with_tasks.id}/chat",
            json={
                "message": "Show my pending tasks"
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response.status_code == 200
    data = response.json()

    message_lower = data["message"].lower()
    
    # Should mention pending tasks
    assert "groceries" in message_lower or "dentist" in message_lower
    
    # Should NOT mention completed tasks
    assert "finish report" not in message_lower


@pytest.mark.asyncio
async def test_chat_list_completed_tasks(verified_user_with_tasks, auth_token):
    """Test listing only completed tasks"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            f"/api/{verified_user_with_tasks.id}/chat",
            json={
                "message": "Show my completed tasks"
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response.status_code == 200
    data = response.json()

    message_lower = data["message"].lower()
    
    # Should mention completed task
    assert "report" in message_lower or "finish" in message_lower
    
    # Should indicate completion status
    assert any(keyword in message_lower for keyword in ["completed", "done", "finished"])


@pytest.mark.asyncio
async def test_chat_list_tasks_with_numbers(verified_user_with_tasks, auth_token):
    """Test that tasks are listed with numbered positions"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            f"/api/{verified_user_with_tasks.id}/chat",
            json={
                "message": "List all my tasks"
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response.status_code == 200
    data = response.json()

    message = data["message"]
    
    # Should contain numbered list (1, 2, 3, etc.)
    assert "1" in message or "1." in message
    assert "2" in message or "2." in message


@pytest.mark.asyncio
async def test_chat_list_tasks_empty(verified_user, auth_token):
    """Test listing tasks when user has no tasks"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            f"/api/{verified_user.id}/chat",
            json={
                "message": "Show my tasks"
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response.status_code == 200
    data = response.json()

    message_lower = data["message"].lower()
    
    # Should indicate no tasks
    assert any(keyword in message_lower for keyword in ["no tasks", "empty", "don't have any"])


@pytest.mark.asyncio
async def test_chat_list_tasks_variations(verified_user_with_tasks, auth_token):
    """Test different natural language variations for listing tasks"""
    variations = [
        "What are my tasks?",
        "Show me my todo list",
        "What do I need to do?",
        "List my tasks",
        "What's on my list?"
    ]
    
    for message in variations:
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                f"/api/{verified_user_with_tasks.id}/chat",
                json={"message": message},
                headers={"Authorization": f"Bearer {auth_token}"}
            )

        assert response.status_code == 200
        data = response.json()
        
        # Should return task information
        message_lower = data["message"].lower()
        assert any(keyword in message_lower for keyword in ["task", "groceries", "report", "dentist"])


@pytest.mark.asyncio
async def test_chat_list_tasks_follow_up(verified_user_with_tasks, auth_token):
    """Test follow-up queries in same conversation"""
    # First message: list all tasks
    async with AsyncClient(app=app, base_url="http://test") as client:
        response1 = await client.post(
            f"/api/{verified_user_with_tasks.id}/chat",
            json={
                "message": "Show my tasks"
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response1.status_code == 200
    conversation_id = response1.json()["conversation_id"]

    # Second message: ask about pending tasks (follow-up)
    async with AsyncClient(app=app, base_url="http://test") as client:
        response2 = await client.post(
            f"/api/{verified_user_with_tasks.id}/chat",
            json={
                "message": "Which ones are pending?",
                "conversation_id": conversation_id
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response2.status_code == 200
    data = response2.json()

    # Should understand context and show pending tasks
    message_lower = data["message"].lower()
    assert "groceries" in message_lower or "dentist" in message_lower


@pytest.mark.asyncio
async def test_chat_list_tasks_multilingual_roman_urdu(verified_user_with_tasks, auth_token):
    """Test listing tasks in Roman Urdu"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            f"/api/{verified_user_with_tasks.id}/chat",
            json={
                "message": "Mere tasks dikhao"
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response.status_code == 200
    data = response.json()

    # Agent should respond (possibly in Roman Urdu)
    # But should still list the tasks
    assert "message" in data
    assert len(data["message"]) > 0


@pytest.mark.asyncio
async def test_chat_list_tasks_by_category(verified_user_with_tasks, auth_token):
    """Test listing tasks filtered by category"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            f"/api/{verified_user_with_tasks.id}/chat",
            json={
                "message": "Show my shopping tasks"
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response.status_code == 200
    data = response.json()

    message_lower = data["message"].lower()
    
    # Should mention shopping task
    assert "groceries" in message_lower
    
    # Should NOT mention other categories
    assert "report" not in message_lower and "dentist" not in message_lower
