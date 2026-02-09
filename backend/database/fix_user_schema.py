"""
Migration script to fix user table schema - convert id from VARCHAR to UUID
This script drops and recreates the user and authentication_token tables with correct types
"""
from sqlmodel import Session, text
from database.session import engine
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def fix_user_schema():
    """
    Drop and recreate user and authentication_token tables with correct UUID types
    WARNING: This will delete all existing user data
    """
    try:
        with Session(engine) as session:
            logger.info("Starting schema fix for user and authentication_token tables...")

            # Drop authentication_token table first (has foreign key to user)
            logger.info("Dropping authentication_token table if exists...")
            session.exec(text("DROP TABLE IF EXISTS authentication_token CASCADE"))

            # Drop user table
            logger.info("Dropping user table if exists...")
            session.exec(text('DROP TABLE IF EXISTS "user" CASCADE'))

            session.commit()
            logger.info("Successfully dropped existing tables")

            # Now recreate tables using SQLModel
            logger.info("Recreating tables with correct schema...")
            from models.user import User
            from models.auth_token import AuthenticationToken
            from sqlmodel import SQLModel

            # Create all tables
            SQLModel.metadata.create_all(engine)

            session.commit()
            logger.info("Successfully recreated user and authentication_token tables with UUID types")

    except Exception as e:
        logger.error(f"Error during schema fix: {str(e)}")
        raise

if __name__ == "__main__":
    print("WARNING: This will delete all existing user and authentication data!")
    print("Press Ctrl+C to cancel, or Enter to continue...")
    input()
    fix_user_schema()
    print("Schema fix completed successfully!")
