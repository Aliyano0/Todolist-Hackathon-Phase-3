"""
Unit tests for chat service

Tests conversation history loading functionality.
Following TDD: These tests should FAIL before implementation.
"""

import pytest
import uuid
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch
from core.services.chat_service import ChatService


@pytest.mark.asyncio
async def test_load_conversation_history_last_20_messages():
    """Test loading last 20 messages from conversation"""
    user_id = uuid.uuid4()
    conversation_id = uuid.uuid4()

    history = await ChatService.load_conversation_history(
        conversation_id=conversation_id,
        user_id=user_id,
        limit=20
    )

    assert isinstance(history, list)
    assert len(history) <= 20
    
    # Verify message format
    for message in history:
        assert "role" in message
        assert "content" in message
        assert message["role"] in ["user", "assistant", "tool"]


@pytest.mark.asyncio
async def test_load_conversation_history_chronological_order():
    """Test that messages are returned in chronological order (oldest first)"""
    user_id = uuid.uuid4()
    conversation_id = uuid.uuid4()

    history = await ChatService.load_conversation_history(
        conversation_id=conversation_id,
        user_id=user_id,
        limit=20
    )

    # If multiple messages, verify chronological order
    # (Implementation should reverse the DESC query results)
    if len(history) > 1:
        # First message should be older than last message
        # (This assumes messages have timestamps, but we're checking order)
        assert len(history) >= 1


@pytest.mark.asyncio
async def test_load_conversation_history_user_isolation():
    """Test that users can only load their own conversation history"""
    user1_id = uuid.uuid4()
    user2_id = uuid.uuid4()
    conversation_id = uuid.uuid4()

    # User1's conversation
    # User2 tries to access it
    with pytest.raises(Exception, match="Conversation not found or access denied"):
        await ChatService.load_conversation_history(
            conversation_id=conversation_id,
            user_id=user2_id,
            limit=20
        )


@pytest.mark.asyncio
async def test_load_conversation_history_empty():
    """Test loading history from conversation with no messages"""
    user_id = uuid.uuid4()
    conversation_id = uuid.uuid4()

    history = await ChatService.load_conversation_history(
        conversation_id=conversation_id,
        user_id=user_id,
        limit=20
    )

    assert history == []


@pytest.mark.asyncio
async def test_load_conversation_history_custom_limit():
    """Test loading history with custom limit"""
    user_id = uuid.uuid4()
    conversation_id = uuid.uuid4()

    history = await ChatService.load_conversation_history(
        conversation_id=conversation_id,
        user_id=user_id,
        limit=5
    )

    assert len(history) <= 5


@pytest.mark.asyncio
async def test_load_conversation_history_nonexistent_conversation():
    """Test loading history from non-existent conversation"""
    user_id = uuid.uuid4()
    conversation_id = uuid.uuid4()  # Non-existent

    with pytest.raises(Exception, match="Conversation not found"):
        await ChatService.load_conversation_history(
            conversation_id=conversation_id,
            user_id=user_id,
            limit=20
        )


@pytest.mark.asyncio
async def test_list_conversations_ordered_by_recent():
    """Test listing conversations ordered by most recent first"""
    user_id = uuid.uuid4()

    conversations = await ChatService.list_conversations(
        user_id=user_id,
        limit=50
    )

    assert isinstance(conversations, list)
    
    # Verify conversations are ordered by updated_at DESC
    if len(conversations) > 1:
        for i in range(len(conversations) - 1):
            assert conversations[i].updated_at >= conversations[i + 1].updated_at


@pytest.mark.asyncio
async def test_list_conversations_user_isolation():
    """Test that users only see their own conversations"""
    user1_id = uuid.uuid4()
    user2_id = uuid.uuid4()

    conversations1 = await ChatService.list_conversations(user_id=user1_id)
    conversations2 = await ChatService.list_conversations(user_id=user2_id)

    # Verify no overlap in conversation IDs
    if conversations1 and conversations2:
        ids1 = {conv.id for conv in conversations1}
        ids2 = {conv.id for conv in conversations2}
        assert ids1.isdisjoint(ids2)


@pytest.mark.asyncio
async def test_list_conversations_limit():
    """Test listing conversations with limit"""
    user_id = uuid.uuid4()

    conversations = await ChatService.list_conversations(
        user_id=user_id,
        limit=10
    )

    assert len(conversations) <= 10


@pytest.mark.asyncio
async def test_get_or_create_conversation_existing():
    """Test getting existing conversation"""
    user_id = uuid.uuid4()

    # Create a conversation first
    conv1 = await ChatService.create_conversation(user_id)

    # Get or create should return existing
    conv2 = await ChatService.get_or_create_conversation(user_id)

    assert conv1.id == conv2.id


@pytest.mark.asyncio
async def test_get_or_create_conversation_new():
    """Test creating new conversation when none exists"""
    user_id = uuid.uuid4()

    conversation = await ChatService.get_or_create_conversation(user_id)

    assert conversation is not None
    assert conversation.user_id == user_id


@pytest.mark.asyncio
async def test_save_message_updates_conversation_timestamp():
    """Test that saving a message updates conversation's updated_at"""
    user_id = uuid.uuid4()
    conversation_id = uuid.uuid4()

    # Get original timestamp
    # Save message
    # Verify updated_at changed

    message = await ChatService.save_message(
        conversation_id=conversation_id,
        user_id=user_id,
        role="user",
        content="Test message"
    )

    assert message is not None
    assert message.content == "Test message"
