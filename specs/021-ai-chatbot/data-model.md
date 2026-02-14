# Data Model: Phase III - AI Chatbot Integration

**Date**: 2026-02-10
**Feature**: [spec.md](./spec.md)
**Status**: Complete

## Overview

This document defines the database schema for conversation persistence in the AI chatbot feature. All models use UUID primary keys for consistency with Phase 2 architecture.

**Note**: User and Task models already exist from Phase 2 (018-better-auth-jwt). Phase 3 adds Conversation and Message models, and extends User model usage with email verification flow.

## Entity Relationship Diagram

```
User (Phase 2 - 018-better-auth-jwt)
  ├── id: UUID (PK)
  ├── email: string (unique)
  ├── password_hash: string
  ├── email_verified: boolean (Phase 3 extends this)
  ├── verification_token: string (nullable) (Phase 3 extends this)
  └── created_at: timestamp

Task (Phase 2)
  ├── id: UUID (PK)
  ├── user_id: UUID (FK → User.id)
  ├── title: string
  ├── description: string (nullable)
  ├── completed: boolean
  ├── priority: string (nullable)
  ├── category: string (nullable)
  └── created_at: timestamp

Conversation (NEW - Phase 3)
  ├── id: UUID (PK)
  ├── user_id: UUID (FK → User.id)
  ├── created_at: timestamp
  └── updated_at: timestamp

Message (NEW - Phase 3)
  ├── id: UUID (PK)
  ├── conversation_id: UUID (FK → Conversation.id)
  ├── user_id: UUID (FK → User.id)
  ├── role: string (enum: 'user', 'assistant', 'tool')
  ├── content: text
  └── created_at: timestamp
```

## Relationships

- **User → Conversation**: One-to-Many (one user can have multiple conversations)
- **User → Message**: One-to-Many (one user can have multiple messages)
- **Conversation → Message**: One-to-Many (one conversation contains multiple messages)
- **User → Task**: One-to-Many (existing from Phase 2)

## Model Definitions

### Conversation Model

**Purpose**: Represents a chat session between a user and the AI agent. Groups related messages together and enables conversation resumption.

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY, NOT NULL | Unique identifier for the conversation |
| user_id | UUID | FOREIGN KEY (User.id), NOT NULL, INDEXED | Owner of the conversation |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | When conversation was started |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last message timestamp |

**Indexes**:
- PRIMARY KEY on `id`
- INDEX on `user_id` (for filtering conversations by user)
- INDEX on `updated_at` (for sorting by most recent activity)

**Validation Rules**:
- `user_id` must reference existing User
- `updated_at` must be >= `created_at`

**SQLModel Definition**:
```python
from sqlmodel import SQLModel, Field
from datetime import datetime
import uuid

class Conversation(SQLModel, table=True):
    __tablename__ = "conversation"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        nullable=False
    )
    user_id: uuid.UUID = Field(
        foreign_key="user.id",
        nullable=False,
        index=True
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        index=True
    )
```

### Message Model

**Purpose**: Represents a single message in a conversation. Stores user inputs, assistant responses, and tool execution results for conversation history reconstruction.

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY, NOT NULL | Unique identifier for the message |
| conversation_id | UUID | FOREIGN KEY (Conversation.id), NOT NULL, INDEXED | Parent conversation |
| user_id | UUID | FOREIGN KEY (User.id), NOT NULL, INDEXED | Owner of the message |
| role | VARCHAR(20) | NOT NULL, CHECK IN ('user', 'assistant', 'tool') | Message sender role |
| content | TEXT | NOT NULL | Message text content |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | When message was created |

**Indexes**:
- PRIMARY KEY on `id`
- INDEX on `conversation_id` (for fetching conversation history)
- INDEX on `user_id` (for user isolation)
- INDEX on `created_at` (for ordering messages chronologically)

**Validation Rules**:
- `conversation_id` must reference existing Conversation
- `user_id` must reference existing User
- `user_id` must match the `user_id` of the parent Conversation
- `role` must be one of: 'user', 'assistant', 'tool'
- `content` must not be empty

**SQLModel Definition**:
```python
from sqlmodel import SQLModel, Field
from datetime import datetime
import uuid

class Message(SQLModel, table=True):
    __tablename__ = "message"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        nullable=False
    )
    conversation_id: uuid.UUID = Field(
        foreign_key="conversation.id",
        nullable=False,
        index=True
    )
    user_id: uuid.UUID = Field(
        foreign_key="user.id",
        nullable=False,
        index=True
    )
    role: str = Field(
        max_length=20,
        nullable=False
    )
    content: str = Field(
        sa_column_kwargs={"type_": "TEXT"},
        nullable=False
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        index=True
    )
```

## Database Migration

### Migration Script (Alembic)

```python
"""Add conversation and message tables for Phase 3 AI chatbot

Revision ID: 003_add_conversation_tables
Revises: 002_add_priority_category
Create Date: 2026-02-10
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import uuid

# revision identifiers
revision = '003_add_conversation_tables'
down_revision = '002_add_priority_category'
branch_labels = None
depends_on = None

def upgrade():
    # Create conversation table
    op.create_table(
        'conversation',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('user.id'), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP, nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.TIMESTAMP, nullable=False, server_default=sa.func.now()),
    )

    # Create indexes for conversation
    op.create_index('ix_conversation_user_id', 'conversation', ['user_id'])
    op.create_index('ix_conversation_updated_at', 'conversation', ['updated_at'])

    # Create message table
    op.create_table(
        'message',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('conversation_id', UUID(as_uuid=True), sa.ForeignKey('conversation.id'), nullable=False),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('user.id'), nullable=False),
        sa.Column('role', sa.VARCHAR(20), nullable=False),
        sa.Column('content', sa.TEXT, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP, nullable=False, server_default=sa.func.now()),
        sa.CheckConstraint("role IN ('user', 'assistant', 'tool')", name='check_message_role')
    )

    # Create indexes for message
    op.create_index('ix_message_conversation_id', 'message', ['conversation_id'])
    op.create_index('ix_message_user_id', 'message', ['user_id'])
    op.create_index('ix_message_created_at', 'message', ['created_at'])

def downgrade():
    # Drop message table and indexes
    op.drop_index('ix_message_created_at', table_name='message')
    op.drop_index('ix_message_user_id', table_name='message')
    op.drop_index('ix_message_conversation_id', table_name='message')
    op.drop_table('message')

    # Drop conversation table and indexes
    op.drop_index('ix_conversation_updated_at', table_name='conversation')
    op.drop_index('ix_conversation_user_id', table_name='conversation')
    op.drop_table('conversation')
```

## Query Patterns

### Common Queries

**1. Get Conversation History (Last 20 Messages)**
```python
async def get_conversation_history(
    conversation_id: uuid.UUID,
    limit: int = 20
) -> list[Message]:
    async with get_async_session() as session:
        statement = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.desc())
            .limit(limit)
        )
        result = await session.execute(statement)
        messages = result.scalars().all()
        return list(reversed(messages))  # Return oldest first
```

**2. Create New Conversation**
```python
async def create_conversation(user_id: uuid.UUID) -> Conversation:
    async with get_async_session() as session:
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        await session.commit()
        await session.refresh(conversation)
        return conversation
```

**3. Add Message to Conversation**
```python
async def add_message(
    conversation_id: uuid.UUID,
    user_id: uuid.UUID,
    role: str,
    content: str
) -> Message:
    async with get_async_session() as session:
        # Create message
        message = Message(
            conversation_id=conversation_id,
            user_id=user_id,
            role=role,
            content=content
        )
        session.add(message)

        # Update conversation updated_at
        conversation = await session.get(Conversation, conversation_id)
        conversation.updated_at = datetime.utcnow()

        await session.commit()
        await session.refresh(message)
        return message
```

**4. List User Conversations (Most Recent First)**
```python
async def list_user_conversations(
    user_id: uuid.UUID,
    limit: int = 10,
    offset: int = 0
) -> list[Conversation]:
    async with get_async_session() as session:
        statement = (
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await session.execute(statement)
        return result.scalars().all()
```

**5. Get Last Message Preview for Conversation List**
```python
async def get_conversation_with_preview(
    user_id: uuid.UUID
) -> list[dict]:
    async with get_async_session() as session:
        # Get conversations with last message
        statement = """
            SELECT
                c.id,
                c.created_at,
                c.updated_at,
                m.content as last_message,
                m.role as last_message_role,
                m.created_at as last_message_time
            FROM conversation c
            LEFT JOIN LATERAL (
                SELECT content, role, created_at
                FROM message
                WHERE conversation_id = c.id
                ORDER BY created_at DESC
                LIMIT 1
            ) m ON true
            WHERE c.user_id = :user_id
            ORDER BY c.updated_at DESC
        """
        result = await session.execute(
            text(statement),
            {"user_id": user_id}
        )
        return [dict(row) for row in result]
```

## Data Isolation

All queries MUST filter by `user_id` to ensure multi-user isolation:

```python
# ✅ CORRECT - Filters by user_id
messages = await session.execute(
    select(Message)
    .where(Message.conversation_id == conversation_id)
    .where(Message.user_id == user_id)  # Isolation enforced
)

# ❌ INCORRECT - No user_id filter (security vulnerability)
messages = await session.execute(
    select(Message)
    .where(Message.conversation_id == conversation_id)
)
```

## Performance Considerations

### Indexing Strategy

- **conversation.user_id**: Enables fast filtering of conversations by user
- **conversation.updated_at**: Enables fast sorting by most recent activity
- **message.conversation_id**: Enables fast retrieval of conversation history
- **message.user_id**: Enables user isolation checks
- **message.created_at**: Enables chronological ordering of messages

### Query Optimization

- Limit conversation history to 20 messages (prevents large result sets)
- Use `LIMIT` and `OFFSET` for pagination
- Use `LATERAL` join for efficient last message preview
- Consider adding composite index on `(conversation_id, created_at)` if query performance degrades

### Storage Estimates

- Average message size: ~200 bytes (text content)
- 50 users × 100 messages each = 5,000 messages
- Storage: 5,000 × 200 bytes = ~1 MB
- With indexes: ~2-3 MB total

## Validation Rules Summary

### Conversation
- ✅ `user_id` must reference existing User
- ✅ `updated_at` >= `created_at`

### Message
- ✅ `conversation_id` must reference existing Conversation
- ✅ `user_id` must reference existing User
- ✅ `user_id` must match parent Conversation's `user_id`
- ✅ `role` must be 'user', 'assistant', or 'tool'
- ✅ `content` must not be empty
- ✅ `created_at` must be <= current time

## Future Enhancements

Potential schema extensions for future phases:

1. **Message Metadata**: Add JSON field for tool invocation details, language detection results
2. **Conversation Titles**: Add `title` field auto-generated from first message
3. **Message Reactions**: Add `reactions` table for user feedback (thumbs up/down)
4. **Conversation Tags**: Add `tags` field for categorization
5. **Soft Deletes**: Add `deleted_at` field for conversation archiving
6. **Message Edits**: Add `edited_at` and `original_content` fields

These are NOT in scope for Phase 3 but documented for future reference.
