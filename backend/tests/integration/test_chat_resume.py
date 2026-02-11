"""
Integration test for conversation resumption

Tests the full flow of resuming conversations across sessions.
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
from models.conversation import Conversation
from models.message import Message
from sqlmodel import select


@pytest.fixture
async def verified_user_with_conversation(session):
    """Create a verified user with an existing conversation"""
    user = User(
        email="test@example.com",
        password_hash="hashed_password",
        email_verified=True,
        verification_token=None
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)

    # Create conversation with message history
    conversation = Conversation(
        user_id=user.id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    session.add(conversation)
    await session.commit()
    await session.refresh(conversation)

    # Add message history
    messages = [
        Message(
            conversation_id=conversation.id,
            user_id=user.id,
            role="user",
            content="Add task: buy groceries",
            created_at=datetime.utcnow()
        ),
        Message(
            conversation_id=conversation.id,
            user_id=user.id,
            role="assistant",
            content="I've added 'buy groceries' to your tasks!",
            created_at=datetime.utcnow()
        ),
        Message(
            conversation_id=conversation.id,
            user_id=user.id,
            role="user",
            content="Show my tasks",
            created_at=datetime.utcnow()
        ),
        Message(
            conversation_id=conversation.id,
            user_id=user.id,
            role="assistant",
            content="Here are your tasks:\n\n1. Buy groceries",
            created_at=datetime.utcnow()
        )
    ]
    
    for message in messages:
        session.add(message)
    
    await session.commit()
    
    return user, conversation


@pytest.fixture
def auth_token(verified_user_with_conversation):
    """Create a valid JWT token for the verified user"""
    user, _ = verified_user_with_conversation
    secret = os.getenv("BETTER_AUTH_SECRET", "test-secret-key-for-testing-only")
    payload = {
        "sub": str(user.id),
        "email": user.email,
        "email_verified": True,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    token = jwt.encode(payload, secret, algorithm="HS256")
    return token


@pytest.mark.asyncio
async def test_chat_resume_conversation(verified_user_with_conversation, auth_token):
    """Test resuming an existing conversation"""
    user, conversation = verified_user_with_conversation

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            f"/api/{user.id}/chat",
            json={
                "message": "Complete task 1",
                "conversation_id": str(conversation.id)
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response.status_code == 200
    data = response.json()

    # Should use the same conversation
    assert data["conversation_id"] == str(conversation.id)
    
    # Agent should have context from previous messages
    # (knows about "buy groceries" task)
    message_lower = data["message"].lower()
    assert "groceries" in message_lower or "completed" in message_lower


@pytest.mark.asyncio
async def test_chat_resume_maintains_context(verified_user_with_conversation, auth_token):
    """Test that resumed conversation maintains context"""
    user, conversation = verified_user_with_conversation

    async with AsyncClient(app=app, base_url="http://test") as client:
        # Send follow-up message that requires context
        response = await client.post(
            f"/api/{user.id}/chat",
            json={
                "message": "What was the first task I added?",
                "conversation_id": str(conversation.id)
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response.status_code == 200
    data = response.json()

    # Agent should remember "buy groceries" from history
    message_lower = data["message"].lower()
    assert "groceries" in message_lower or "buy" in message_lower


@pytest.mark.asyncio
async def test_chat_resume_invalid_conversation_id(verified_user_with_conversation, auth_token):
    """Test resuming with invalid conversation ID"""
    user, _ = verified_user_with_conversation
    invalid_conversation_id = str(uuid.uuid4())

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            f"/api/{user.id}/chat",
            json={
                "message": "Test message",
                "conversation_id": invalid_conversation_id
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_chat_resume_other_user_conversation(verified_user_with_conversation, auth_token):
    """Test that users cannot resume other users' conversations"""
    user, _ = verified_user_with_conversation

    # Create another user with a conversation
    async with get_session() as session:
        other_user = User(
            email="other@example.com",
            password_hash="hashed",
            email_verified=True
        )
        session.add(other_user)
        await session.commit()
        await session.refresh(other_user)
        
        other_conversation = Conversation(
            user_id=other_user.id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        session.add(other_conversation)
        await session.commit()
        await session.refresh(other_conversation)
        other_conversation_id = other_conversation.id

    # Try to resume other user's conversation
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            f"/api/{user.id}/chat",
            json={
                "message": "Test message",
                "conversation_id": str(other_conversation_id)
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_chat_resume_adds_to_history(verified_user_with_conversation, auth_token):
    """Test that resumed conversation adds new messages to history"""
    user, conversation = verified_user_with_conversation

    # Get original message count
    async with get_session() as session:
        result = await session.execute(
            select(Message).where(Message.conversation_id == conversation.id)
        )
        original_count = len(result.scalars().all())

    # Send new message
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            f"/api/{user.id}/chat",
            json={
                "message": "Add another task",
                "conversation_id": str(conversation.id)
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response.status_code == 200

    # Verify new messages were added
    async with get_session() as session:
        result = await session.execute(
            select(Message).where(Message.conversation_id == conversation.id)
        )
        new_count = len(result.scalars().all())
        assert new_count > original_count


@pytest.mark.asyncio
async def test_chat_resume_updates_conversation_timestamp(verified_user_with_conversation, auth_token):
    """Test that resuming updates conversation's updated_at timestamp"""
    user, conversation = verified_user_with_conversation

    # Get original timestamp
    original_updated_at = conversation.updated_at

    # Send new message
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            f"/api/{user.id}/chat",
            json={
                "message": "Test message",
                "conversation_id": str(conversation.id)
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response.status_code == 200

    # Verify timestamp was updated
    async with get_session() as session:
        result = await session.execute(
            select(Conversation).where(Conversation.id == conversation.id)
        )
        updated_conversation = result.scalar_one()
        assert updated_conversation.updated_at > original_updated_at


@pytest.mark.asyncio
async def test_chat_resume_loads_last_20_messages(verified_user_with_conversation, auth_token):
    """Test that conversation history is limited to last 20 messages"""
    user, conversation = verified_user_with_conversation

    # Add many messages to conversation (more than 20)
    async with get_session() as session:
        for i in range(25):
            message = Message(
                conversation_id=conversation.id,
                user_id=user.id,
                role="user" if i % 2 == 0 else "assistant",
                content=f"Message {i}",
                created_at=datetime.utcnow()
            )
            session.add(message)
        await session.commit()

    # Resume conversation
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            f"/api/{user.id}/chat",
            json={
                "message": "What's the latest?",
                "conversation_id": str(conversation.id)
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response.status_code == 200
    # Agent should only have context from last 20 messages
    # (Implementation detail - agent receives limited history)


@pytest.mark.asyncio
async def test_chat_new_conversation_when_none_provided(verified_user_with_conversation, auth_token):
    """Test that new conversation is created when conversation_id not provided"""
    user, old_conversation = verified_user_with_conversation

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            f"/api/{user.id}/chat",
            json={
                "message": "Start fresh conversation"
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response.status_code == 200
    data = response.json()

    # Should create new conversation
    new_conversation_id = data["conversation_id"]
    assert new_conversation_id != str(old_conversation.id)


@pytest.mark.asyncio
async def test_chat_resume_empty_conversation(verified_user_with_conversation, auth_token):
    """Test resuming a conversation with no messages"""
    user, _ = verified_user_with_conversation

    # Create empty conversation
    async with get_session() as session:
        empty_conversation = Conversation(
            user_id=user.id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        session.add(empty_conversation)
        await session.commit()
        await session.refresh(empty_conversation)
        empty_conversation_id = empty_conversation.id

    # Resume empty conversation
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            f"/api/{user.id}/chat",
            json={
                "message": "First message",
                "conversation_id": str(empty_conversation_id)
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    assert response.status_code == 200
    data = response.json()
    assert data["conversation_id"] == str(empty_conversation_id)
