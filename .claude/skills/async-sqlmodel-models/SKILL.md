---
name: async-sqlmodel-models
description: Provides the async SQLModel models (Task, Conversation, Message + User.email_verified) for Phase III with UUIDs and Neon.
---

# Async SQLModel Models Skill

When the user needs the database models for the Todo AI Chatbot (Phase III), output this exact file.

## File location
`backend/models.py`

## Code
```python
# models.py
from sqlmodel import SQLModel, Field
from sqlalchemy.ext.asyncio import AsyncAttrs
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional

class BaseModel(SQLModel, AsyncAttrs):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})

class User(BaseModel, table=True):
    email: str = Field(unique=True)
    password_hash: str
    email_verified: bool = Field(default=False)

class Task(BaseModel, table=True):
    user_id: UUID = Field(foreign_key="user.id")
    title: str
    description: Optional[str] = None
    completed: bool = Field(default=False)

class Conversation(BaseModel, table=True):
    user_id: UUID = Field(foreign_key="user.id")

class Message(BaseModel, table=True):
    user_id: UUID = Field(foreign_key="user.id")
    conversation_id: UUID = Field(foreign_key="conversation.id")
    role: str
    content: str
```

Run `await engine.begin()` with `SQLModel.metadata.create_all` on startup.


