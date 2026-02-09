# Database Schema Fix Instructions

## Problem
The existing `user` table in the database has `id` column as VARCHAR (string type), but the User model defines it as UUID. This creates a type mismatch when trying to create foreign key constraints in the `authentication_token` table.

## Solution
Run the schema fix migration script to drop and recreate the tables with correct UUID types.

## Steps to Fix

### 1. Run the Schema Fix Migration

```bash
cd backend
python database/fix_user_schema.py
```

**WARNING**: This will delete all existing user and authentication data. Press Enter to confirm or Ctrl+C to cancel.

### 2. Start the Backend Server

After the migration completes successfully:

```bash
uvicorn main:app --reload
```

The server should now start without errors and create all tables with correct schema.

## What the Migration Does

1. Drops `authentication_token` table (if exists)
2. Drops `user` table (if exists)
3. Recreates both tables using SQLModel with correct UUID types
4. All foreign key constraints will work correctly

## Alternative: Fresh Database

If you prefer to start with a completely fresh database, you can:

1. Drop all tables in your Neon database
2. Start the backend server - it will automatically create all tables with correct schema

## Verification

After running the migration, verify the schema:

```sql
-- Check user table schema
\d "user"

-- Check authentication_token table schema
\d authentication_token
```

Both tables should have `id` and `user_id` columns as UUID type.
