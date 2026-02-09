from sqlmodel import Session, select
from typing import List, Optional
from backend.models.category import Category, CategoryCreate, CategoryUpdate
from datetime import datetime


def get_all_categories(session: Session) -> List[Category]:
    """
    Retrieve all categories from the database
    """
    statement = select(Category)
    categories = session.exec(statement).all()
    return categories


def get_category_by_id(session: Session, category_id: int) -> Optional[Category]:
    """
    Retrieve a specific category by ID
    """
    statement = select(Category).where(Category.id == category_id)
    category = session.exec(statement).first()
    return category


def get_category_by_name(session: Session, name: str) -> Optional[Category]:
    """
    Retrieve a category by its name
    """
    statement = select(Category).where(Category.name == name)
    category = session.exec(statement).first()
    return category


def create_category(session: Session, category_data: CategoryCreate) -> Category:
    """
    Create a new category in the database
    """
    category = Category(
        name=category_data.name,
        is_custom=category_data.is_custom
    )
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


def update_category(session: Session, category_id: int, category_update: CategoryUpdate) -> Optional[Category]:
    """
    Update an existing category in the database
    """
    category = get_category_by_id(session, category_id)
    if not category:
        return None

    # Update the category with provided fields
    update_data = category_update.dict(exclude_unset=True)

    for field, value in update_data.items():
        setattr(category, field, value)

    category.updated_at = datetime.utcnow()
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


def delete_category(session: Session, category_id: int) -> bool:
    """
    Delete a category from the database
    """
    category = get_category_by_id(session, category_id)
    if not category:
        return False

    session.delete(category)
    session.commit()
    return True