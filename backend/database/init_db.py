from sqlmodel import SQLModel
from .session import engine
from models.todo import TodoTask


def create_db_and_tables():
    """
    Create database tables if they don't exist.
    This function should be called at application startup.
    """
    print("Initializing database tables...")
    SQLModel.metadata.create_all(engine)
    print("Database tables initialized successfully.")


if __name__ == "__main__":
    create_db_and_tables()