"""
Database Migration Script: Clean Slate UUID Schema

This script drops all existing tables and recreates them with UUID primary keys.
This is a destructive operation - all existing data will be lost.

Usage:
    python migrations/uuid_migration.py

Requirements:
    - DATABASE_URL environment variable must be set
    - asyncpg==0.30.0 must be installed
"""

import asyncio
import os
from dotenv import load_dotenv
import asyncpg

# Load environment variables
load_dotenv()

async def drop_all_tables(conn):
    """
    Drop all tables in the public schema
    """
    print("Dropping all existing tables...")

    # Get all table names
    tables = await conn.fetch("""
        SELECT tablename
        FROM pg_tables
        WHERE schemaname = 'public'
    """)

    # Drop each table with CASCADE
    for table in tables:
        table_name = table['tablename']
        print(f"  Dropping table: {table_name}")
        await conn.execute(f'DROP TABLE IF EXISTS "{table_name}" CASCADE')

    print("All tables dropped successfully.")


async def create_uuid_schema(conn):
    """
    Create new tables with UUID primary keys
    """
    print("\nCreating new tables with UUID schema...")

    # Enable UUID extension
    await conn.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')

    # Create User table
    await conn.execute("""
        CREATE TABLE "user" (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            email_verified BOOLEAN DEFAULT FALSE,
            verification_token VARCHAR(255),
            reset_token VARCHAR(255),
            reset_token_expires TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("  Created table: user")

    # Create TodoTask table
    await conn.execute("""
        CREATE TABLE todotask (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            user_id UUID NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            completed BOOLEAN DEFAULT FALSE,
            priority VARCHAR(50),
            category VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("  Created table: todotask")

    # Create indexes
    await conn.execute('CREATE INDEX idx_todotask_user_id ON todotask(user_id)')
    await conn.execute('CREATE INDEX idx_todotask_user_created ON todotask(user_id, created_at)')
    await conn.execute('CREATE INDEX idx_user_email ON "user"(email)')
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
            # Drop all existing tables
            await drop_all_tables(conn)

            # Create new UUID schema
            await create_uuid_schema(conn)

            print("\n✅ Migration completed successfully!")
            print("\nNext steps:")
            print("1. Start the backend server: uvicorn main:app --reload")
            print("2. Start the frontend server: cd frontend && npm run dev")
            print("3. Register a new user at http://localhost:3000/register")

        finally:
            # Close connection
            await conn.close()

    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
