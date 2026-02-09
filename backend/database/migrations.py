from sqlmodel import Session, text
from database.session import engine
from typing import Optional
import logging

logger = logging.getLogger(__name__)

def add_priority_category_columns():
    """
    Add priority and category columns to existing todotask table
    """
    try:
        with Session(engine) as session:
            # Add priority and category columns with default values
            session.exec(text("""
                ALTER TABLE todotask
                ADD COLUMN IF NOT EXISTS priority VARCHAR(20) DEFAULT 'medium',
                ADD COLUMN IF NOT EXISTS category VARCHAR(50) DEFAULT 'personal'
            """))

            # Update existing records that might have NULL values
            session.exec(text("""
                UPDATE todotask
                SET priority = 'medium', category = 'personal'
                WHERE priority IS NULL OR category IS NULL
            """))

            session.commit()
            logger.info("Successfully added priority and category columns to todotask table")
    except Exception as e:
        logger.error(f"Error during migration: {str(e)}")
        raise


def add_user_id_column():
    """
    Add user_id column to existing todotask table for user isolation
    """
    try:
        with Session(engine) as session:
            # Add user_id column with default value for existing records
            session.exec(text("""
                ALTER TABLE todotask
                ADD COLUMN IF NOT EXISTS user_id UUID
            """))

            # Create User table if it doesn't exist
            from models.user import User
            from sqlmodel import SQLModel
            SQLModel.metadata.tables[User.__tablename__].create(bind=session.bind, checkfirst=True)

            # For existing tasks without a user_id, we would typically assign them to a default user
            # In a real migration, you might have different logic for handling existing tasks
            # For now, let's create a default user and assign existing tasks to it

            # For the purpose of this migration, let's not assign existing tasks to any user
            # since in a real authenticated system, existing unassigned tasks would need special handling
            session.commit()
            logger.info("Successfully added user_id column to todotask table for user isolation")
    except Exception as e:
        logger.error(f"Error during user_id migration: {str(e)}")
        raise

def add_authentication_token_table():
    """
    Create authentication_token table for token tracking and revocation
    """
    try:
        with Session(engine) as session:
            # Create authentication_token table
            session.exec(text("""
                CREATE TABLE IF NOT EXISTS authentication_token (
                    id UUID PRIMARY KEY,
                    user_id UUID NOT NULL,
                    token_type VARCHAR(10) NOT NULL,
                    token_value VARCHAR(500) NOT NULL,
                    expires_at TIMESTAMP NOT NULL,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    revoked BOOLEAN NOT NULL DEFAULT FALSE,
                    FOREIGN KEY (user_id) REFERENCES "user"(id) ON DELETE CASCADE
                )
            """))

            # Create index on user_id for faster lookups
            session.exec(text("""
                CREATE INDEX IF NOT EXISTS idx_auth_token_user_id
                ON authentication_token(user_id)
            """))

            # Create index on token_value for faster validation
            session.exec(text("""
                CREATE INDEX IF NOT EXISTS idx_auth_token_value
                ON authentication_token(token_value)
            """))

            session.commit()
            logger.info("Successfully created authentication_token table with indexes")
    except Exception as e:
        logger.error(f"Error creating authentication_token table: {str(e)}")
        raise


def run_migration():
    """
    Run the database migrations to add priority, category, user_id columns, and authentication_token table
    """
    logger.info("Starting database migration for priority, category, user_id columns, and authentication_token table...")
    add_priority_category_columns()
    add_user_id_column()
    add_authentication_token_table()
    logger.info("Database migration completed successfully")

if __name__ == "__main__":
    run_migration()