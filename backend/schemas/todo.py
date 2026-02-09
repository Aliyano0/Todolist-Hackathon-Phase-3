from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TodoTaskCreate(BaseModel):
    """Schema for creating a new TodoTask (user_id comes from auth, not request body)"""
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: str = "medium"  # Priority levels: high, medium, low
    category: str = "personal"  # Category for the task


class TodoTaskBase(BaseModel):
    """Base schema for TodoTask with common fields"""
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: str = "medium"  # Priority levels: high, medium, low
    category: str = "personal"  # Category for the task
    user_id: str  # Foreign key to User


class TodoTaskRead(TodoTaskBase):
    """Schema for reading TodoTask data with ID and timestamps"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TodoTaskReadResponse(TodoTaskBase):
    """Schema for reading TodoTask data with string ID for frontend compatibility"""
    id: str
    createdAt: str  # camelCase for frontend
    updatedAt: str  # camelCase for frontend

    class Config:
        from_attributes = True


class TodoTaskUpdate(BaseModel):
    """Schema for updating TodoTask data"""
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None  # Priority levels: high, medium, low
    category: Optional[str] = None  # Category for the task


class TodoTaskToggleComplete(BaseModel):
    """Schema for toggling completion status"""
    completed: bool


class ErrorResponse(BaseModel):
    """
    Standardized error response schema.
    """
    detail: str