# Data Model: Backend Database Schema Fix

## Overview
This document defines the data structures and relationships for the backend database schema fix, specifically addressing the addition of priority and category fields to the todo task entity.

## Core Entities

### Todo Task
The primary entity representing a user task that needs to be updated with additional fields.

**Fields**:
- `id`: integer - Unique identifier for the todo task (primary key)
- `title`: string (max 255) - The title or description of the task
- `description`: string (optional, max 1000) - Additional details about the task
- `completed`: boolean - Whether the task is marked as complete
- `priority`: string (max 20) - Priority level of the task ('high', 'medium', 'low'), defaults to 'medium'
- `category`: string (max 50) - Category assigned to the task (e.g., 'work', 'personal', 'shopping'), defaults to 'personal'
- `created_at`: datetime - Timestamp when the task was created
- `updated_at`: datetime - Timestamp when the task was last updated

**Validation Rules**:
- `title` is required and must be between 1-255 characters
- `priority` must be one of the allowed values: 'high', 'medium', 'low'
- `category` is required and must be between 1-50 characters
- `completed` defaults to false
- `created_at` and `updated_at` are automatically managed by the database

**State Transitions**:
- `incomplete` → `complete`: When user marks task as done
- `complete` → `incomplete`: When user unmarks completed task

## Database Schema Changes

### Migration Requirements
The existing `todotask` table needs to be updated to include two new columns:

**New Columns**:
- `priority`: VARCHAR(20) DEFAULT 'medium' NOT NULL
- `category`: VARCHAR(50) DEFAULT 'personal' NOT NULL

**Migration Steps**:
1. Add `priority` column with default value 'medium'
2. Add `category` column with default value 'personal'
3. Update existing records to ensure they have valid values
4. Set both columns as NOT NULL to enforce data integrity

### SQL Migration Script
```sql
-- Add priority and category columns with default values
ALTER TABLE todotask
ADD COLUMN IF NOT EXISTS priority VARCHAR(20) DEFAULT 'medium',
ADD COLUMN IF NOT EXISTS category VARCHAR(50) DEFAULT 'personal';

-- Update existing records that might have NULL values
UPDATE todotask
SET priority = 'medium', category = 'personal'
WHERE priority IS NULL OR category IS NULL;

-- Ensure columns are NOT NULL
-- (This may require separate alter statements depending on database)
```

## API Contract Elements

### Todo Operations (Updated)
With the new fields, the following API endpoints need to be updated:

- GET /api/tasks - Retrieve all todos with priority and category fields
- POST /api/tasks - Create a new todo with optional priority and category
- PUT /api/tasks/{id} - Update an existing todo including priority and category
- PATCH /api/tasks/{id}/toggle-complete - Toggle completion status (now includes priority/category in response)

### Request/Response Examples

**Create Todo Request**:
```json
{
  "title": "New task",
  "description": "Task description",
  "priority": "high",
  "category": "work"
}
```

**Todo Response**:
```json
{
  "id": 1,
  "title": "New task",
  "description": "Task description",
  "completed": false,
  "priority": "high",
  "category": "work",
  "created_at": "2026-02-02T10:00:00Z",
  "updated_at": "2026-02-02T10:00:00Z"
}
```

## Relationships
- No new relationships are introduced by this change
- The existing user-to-todo relationship remains unchanged