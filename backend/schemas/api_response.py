"""
API Response schemas for frontend compatibility
"""
from pydantic import BaseModel
from typing import Generic, TypeVar, List, Optional, Union
from datetime import datetime


T = TypeVar('T')


class ApiResponse(BaseModel, Generic[T]):
    """Generic API response wrapper"""
    data: Union[T, List[T]]


class TodoApiResponse(BaseModel):
    """Schema matching frontend TodoItem interface"""
    id: str
    title: str
    description: Optional[str] = None
    completed: bool
    createdAt: str  # camelCase for frontend
    updatedAt: str  # camelCase for frontend
    userId: Optional[str] = "1"  # temporary single-user implementation