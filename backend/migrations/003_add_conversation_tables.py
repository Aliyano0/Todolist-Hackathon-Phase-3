"""
Database Migration Script: Add Conversation and Message Tables

This script adds conversation and message tables for the AI chatbot feature (Phase 3).
This is a non-destructive migration - existing tables are preserved.

Usage:
    python migrations/003_add_conversation_tables.py

Requirements:
    - DATABASE_URL environment variable must be set
    - asyncpg==0.30.0 must be installed
    - User table must already exist
"""

import asyncio
import os
from dotenv import load_dotenv
import asyncpg

# Load environment variables
load_dotenv()


async def create_conversation_tables(conn):
    """
    Create conversation and message tables for AI chatbot feature
    """
    print("Creating conversation and message tables...")

    # Enable UUID extension (if not already enabled)
    await conn.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')

    # Create Conversation table
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS conversation (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            user_id UUID NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("  Created table: conversation")

    # Create Message table
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS message (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            conversation_id UUID NOT NULL REFERENCES conversation(id) ON DELETE CASCADE,
            user_id UUID NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
            role VARCHAR(20) NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("  Created table: message")

    # Create indexes for performance
    await conn.execute('CREATE INDEX IF NOT EXISTS idx_conversation_user_id ON conversation(user_id)')
    await conn.execute('CREATE INDEX IF NOT EXISTS idx_conversation_updated_at ON conversation(updated_at)')
    await conn.execute('CREATE INDEX IF NOT EXISTS idx_message_conversation_id ON message(conversation_id)')
    await conn.execute('CREATE INDEX IF NOT EXISTS idx_message_user_id ON message(user_id)')
    await conn.execute('CREATE INDEX IF NOT EXISTS idx_message_created_at ON message(created_at)')
    print("  Created indexes")

    print("\nMigration complete!")


async def main():
    """
    Main migration function
    """
    # Get database URL from environment
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("ERROR: DATABASE_URL environment variable not set")
        return

    # Convert SQLAlchemy URL format to asyncpg format if needed
    if database_url.startswith("postgresql+asyncpg://"):
        database_url = database_url.replace("postgresql+asyncpg://", "postgresql://")
    elif database_url.startswith("postgresql://"):
        pass  # Already in correct format
    else:
        print(f"ERROR: Unsupported database URL format: {database_url}")
        return

    print(f"Connecting to database...")
    print(f"Database URL: {database_url[:30]}...")

    try:
        # Connect to database
        conn = await asyncpg.connect(database_url)

        try:
            # Create conversation and message tables
            await create_conversation_tables(conn)

            print("\n✅ Migration completed successfully!")
            print("\nConversation and message tables are now ready for AI chatbot feature.")

        finally:
            # Close connection
            await conn.close()

    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
