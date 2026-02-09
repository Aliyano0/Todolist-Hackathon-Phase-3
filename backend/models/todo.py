from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid
from .user import User


from sqlalchemy import Index

class TodoTaskBase(SQLModel):
    """Base model for TodoTask with common fields"""
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    priority: str = Field(default="medium", regex="^(high|medium|low)$")  # Priority levels: high, medium, low
    category: str = Field(default="personal", max_length=50)  # Category for the task
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False, index=True)  # Foreign key to User table with index


class TodoTask(TodoTaskBase, table=True):
    """TodoTask model for database storage"""
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Define index on user_id for better query performance
    __table_args__ = (Index('idx_todo_user_id', 'user_id'),)


class TodoTaskRead(TodoTaskBase):
    """Model for reading TodoTask data (without internal fields)"""
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class TodoTaskUpdate(SQLModel):
    """Model for updating TodoTask data"""
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = None
    priority: Optional[str] = Field(default=None, regex="^(high|medium|low)$")
    category: Optional[str] = Field(default=None, max_length=50)