"""
Database session management with async support using asyncpg

This module provides async database session management for FastAPI
using SQLModel with asyncpg driver for Neon Serverless PostgreSQL.
"""

from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from typing import AsyncGenerator, Optional
import os
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse


# Get database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Create engine only if DATABASE_URL is set (allows for testing with mock databases)
engine: Optional[any] = None
async_session_maker: Optional[sessionmaker] = None

if DATABASE_URL:
    # Convert to asyncpg URL format if needed
    if DATABASE_URL.startswith("postgresql://"):
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
    elif not DATABASE_URL.startswith("postgresql+asyncpg://"):
        raise ValueError("DATABASE_URL must start with postgresql:// or postgresql+asyncpg://")

    # Parse URL to remove asyncpg-incompatible parameters
    parsed = urlparse(DATABASE_URL)
    query_params = parse_qs(parsed.query)

    # Remove sslmode and channel_binding from query string (asyncpg doesn't support these in URL)
    query_params.pop('sslmode', None)
    query_params.pop('channel_binding', None)

    # Rebuild query string
    new_query = urlencode(query_params, doseq=True)

    # Rebuild URL without incompatible parameters
    clean_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        new_query,
        parsed.fragment
    ))

    # Create async engine for Neon Serverless PostgreSQL
    # Using NullPool for serverless environments (Neon manages connections)
    engine = create_async_engine(
        clean_url,
        echo=False,  # Set to True for SQL query logging
        poolclass=NullPool,  # Neon Serverless manages connection pooling
        future=True,
        connect_args={
            "ssl": "require",  # Enable SSL for Neon (asyncpg format)
        }
    )

    # Create async session factory
    async_session_maker = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Async dependency to get database session for FastAPI routes

    Usage:
        @router.get("/items")
        async def list_items(session: AsyncSession = Depends(get_session)):
            result = await session.execute(select(Item))
            items = result.scalars().all()
            return items
    """
    if not async_session_maker:
        raise ValueError("Database not configured. Set DATABASE_URL environment variable.")

    async with async_session_maker() as session:
        yield session


def get_async_session():
    """
    Context manager to get database session for non-FastAPI code (services, MCP tools)

    Usage:
        async with get_async_session() as session:
            result = await session.execute(select(Item))
            items = result.scalars().all()

    Returns:
        Async context manager that yields AsyncSession
    """
    if not async_session_maker:
        raise ValueError("Database not configured. Set DATABASE_URL environment variable.")

    return async_session_maker()


async def create_db_and_tables():
    """
    Create database tables - should be called on startup

    Note: This uses the migration script instead for clean slate UUID schema.
    This function is kept for compatibility but tables are created via migration.
    """
    if not engine:
        raise ValueError("Database not configured. Set DATABASE_URL environment variable.")

    from models.todo import TodoTask
    from models.user import User

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
