from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class CategoryBase(SQLModel):
    """Base model for Category with common fields"""
    name: str = Field(min_length=1, max_length=50)
    is_custom: bool = Field(default=False)


class Category(CategoryBase, table=True):
    """Category model for database storage"""
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class CategoryRead(CategoryBase):
    """Model for reading Category data"""
    id: int
    created_at: datetime
    updated_at: datetime


class CategoryUpdate(SQLModel):
    """Model for updating Category data"""
    name: Optional[str] = Field(default=None, min_length=1, max_length=50)
    is_custom: Optional[bool] = None