---
name: neon-postgresql-asyncpg
description: Provides the Neon Serverless PostgreSQL async connection setup (asyncpg==0.30.0 + SQLModel session) for Phase III.
---

# Neon PostgreSQL + asyncpg Skill

When the user needs the database connection layer for the stateless FastAPI backend, output this file.

## Directory location
`backend/database/`

## Code
```python
# db.py
import os
from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

DATABASE_URL = os.environ["DATABASE_URL"]  # postgresql+asyncpg://...

engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=True)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session():
    async with AsyncSession(engine) as session:
        yield session

# Example usage (store_message, fetch_tasks, etc.)
async def store_message(user_id: str, conversation_id: str, role: str, content: str):
    async with AsyncSession(engine) as session:
        message = Message(...)  # use models from async-sqlmodel-models skill
        session.add(message)
        await session.commit()
        return message
```

Always filter queries by `user_id` for multi-user isolation.


