from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CategoryBase(BaseModel):
    name: str
    is_custom: bool = False


class CategoryCreate(CategoryBase):
    name: str


class CategoryRead(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    is_custom: Optional[bool] = None


class CategoryResponse(BaseModel):
    id: str
    name: str
    isCustom: bool  # camelCase for frontend
    createdAt: str  # camelCase for frontend
    updatedAt: str  # camelCase for frontend

    class Config:
        from_attributes = True


class ErrorResponse(BaseModel):
    """
    Standardized error response schema.
    """
    detail: str