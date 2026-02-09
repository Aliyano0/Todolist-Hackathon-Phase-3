# Data Model: Multi-User Authentication System

**Feature**: 018-better-auth-jwt
**Date**: 2026-02-08
**Purpose**: Define database schema, entities, relationships, and validation rules

## Overview

This document defines the data model for the multi-user authentication system. The schema uses UUID primary keys for all entities and enforces data isolation through foreign key relationships and query-level filtering.

---

## Entity Relationship Diagram

```
┌─────────────────────────────────────┐
│             User                     │
├─────────────────────────────────────┤
│ id: UUID (PK)                       │
│ email: string (unique, indexed)     │
│ password_hash: string               │
│ email_verified: boolean             │
│ verification_token: string?         │
│ reset_token: string?                │
│ reset_token_expires: datetime?      │
│ created_at: datetime                │
│ updated_at: datetime                │
└─────────────────────────────────────┘
              │
              │ 1:N
              │
              ▼
┌─────────────────────────────────────┐
│           TodoTask                   │
├─────────────────────────────────────┤
│ id: UUID (PK)                       │
│ user_id: UUID (FK → User.id)       │
│ title: string                       │
│ description: string?                │
│ completed: boolean                  │
│ priority: enum(high,medium,low)     │
│ category: string                    │
│ created_at: datetime                │
│ updated_at: datetime                │
└─────────────────────────────────────┘
```

**Relationship**: One User has many TodoTasks (1:N)
**Cascade**: ON DELETE CASCADE (when user deleted, all their tasks deleted)
**Isolation**: All TodoTask queries filtered by user_id

---

## Entity: User

### Purpose
Represents an authenticated user account with credentials and profile information.

### Fields

| Field | Type | Constraints | Default | Description |
|-------|------|-------------|---------|-------------|
| id | UUID | PRIMARY KEY, NOT NULL | uuid.uuid4() | Unique identifier for the user |
| email | string(255) | UNIQUE, NOT NULL, INDEXED | - | User's email address (case-insensitive) |
| password_hash | string | NOT NULL | - | bcrypt hashed password (never store plain text) |
| email_verified | boolean | NOT NULL | false | Email verification status (reserved for Phase 3) |
| verification_token | string | NULLABLE | null | Email verification token (reserved for Phase 3) |
| reset_token | string | NULLABLE | null | Password reset token (reserved for Phase 3) |
| reset_token_expires | datetime | NULLABLE | null | Reset token expiration (reserved for Phase 3) |
| created_at | datetime | NOT NULL | datetime.utcnow() | Account creation timestamp |
| updated_at | datetime | NOT NULL | datetime.utcnow() | Last update timestamp |

### Validation Rules

**Email**:
- Must be valid email format (RFC 5322)
- Case-insensitive (normalize to lowercase before storage)
- Maximum 255 characters
- Must be unique across all users

**Password** (before hashing):
- Minimum 8 characters
- Must contain at least one uppercase letter (A-Z)
- Must contain at least one lowercase letter (a-z)
- Must contain at least one digit (0-9)
- Must contain at least one special character (!@#$%^&*()_+-=[]{}|;:,.<>?)

**Password Hash**:
- Generated using bcrypt with cost factor 12
- Stored as string (bcrypt output format)
- Never log or expose in API responses

### Indexes

- **Primary Index**: `id` (UUID, clustered)
- **Unique Index**: `email` (for uniqueness constraint and login queries)

### State Transitions

```
[New User] --register--> [Unverified] --verify--> [Verified]
                              │
                              └--login--> [Active Session]
```

**Note**: Email verification is optional in Phase 2. Users can login immediately after registration. The `email_verified` field is reserved for future Phase 3 chatbot features.

### Security Considerations

- Password hash must never be included in API responses
- Email should be normalized (lowercase) before queries
- verification_token and reset_token must be cryptographically secure random strings
- reset_token_expires should be short-lived (e.g., 1 hour)

---

## Entity: TodoTask

### Purpose
Represents a todo item owned by a specific user with priority and category classification.

### Fields

| Field | Type | Constraints | Default | Description |
|-------|------|-------------|---------|-------------|
| id | UUID | PRIMARY KEY, NOT NULL | uuid.uuid4() | Unique identifier for the task |
| user_id | UUID | FOREIGN KEY (User.id), NOT NULL, INDEXED | - | Owner of the task |
| title | string(255) | NOT NULL, MIN_LENGTH=1 | - | Task title/summary |
| description | string(1000) | NULLABLE | null | Detailed task description |
| completed | boolean | NOT NULL | false | Completion status |
| priority | enum | NOT NULL, CHECK IN ('high','medium','low') | 'medium' | Task priority level |
| category | string(50) | NOT NULL | 'personal' | Task category/tag |
| created_at | datetime | NOT NULL | datetime.utcnow() | Task creation timestamp |
| updated_at | datetime | NOT NULL | datetime.utcnow() | Last update timestamp |

### Validation Rules

**Title**:
- Required (cannot be empty or whitespace-only)
- Minimum 1 character (after trimming)
- Maximum 255 characters
- Should be trimmed of leading/trailing whitespace

**Description**:
- Optional (can be null or empty)
- Maximum 1000 characters
- Should be trimmed of leading/trailing whitespace

**Priority**:
- Must be one of: 'high', 'medium', 'low'
- Case-sensitive (stored as lowercase)
- Default: 'medium'

**Category**:
- Required (cannot be empty)
- Maximum 50 characters
- Default: 'personal'
- Examples: 'personal', 'work', 'shopping', 'health'

**Completed**:
- Boolean (true/false)
- Default: false
- Cannot be null

### Indexes

- **Primary Index**: `id` (UUID, clustered)
- **Foreign Key Index**: `user_id` (for join performance and data isolation queries)
- **Composite Index**: `(user_id, created_at DESC)` (for user's task list sorted by creation date)

### Relationships

**User → TodoTask (1:N)**:
- One user can have many tasks
- Each task belongs to exactly one user
- Foreign key: `TodoTask.user_id` → `User.id`
- Cascade: ON DELETE CASCADE (delete all tasks when user deleted)
- Isolation: All queries must filter by `user_id`

### State Transitions

```
[New Task] --create--> [Active (completed=false)]
                              │
                              ├--complete--> [Completed (completed=true)]
                              │
                              ├--update--> [Active (modified)]
                              │
                              └--delete--> [Deleted]
```

### Data Isolation Rules

**Critical**: All TodoTask queries MUST include `WHERE user_id = authenticated_user_id`

```sql
-- ✅ CORRECT: Filtered by user_id
SELECT * FROM todotask WHERE user_id = ? AND completed = false;

-- ❌ INCORRECT: Missing user_id filter (security vulnerability)
SELECT * FROM todotask WHERE completed = false;
```

**Enforcement**:
- FastAPI dependency extracts user_id from JWT token
- Route handlers validate path user_id matches JWT user_id
- Database queries always include user_id filter
- Integration tests verify cross-user access is blocked

---

## Database Schema (SQLModel)

### User Model

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid

class User(SQLModel, table=True):
    """User model for database storage"""
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, nullable=False, max_length=255, index=True)
    password_hash: str = Field(nullable=False)
    email_verified: bool = Field(default=False)
    verification_token: Optional[str] = Field(default=None)
    reset_token: Optional[str] = Field(default=None)
    reset_token_expires: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### TodoTask Model

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid
from sqlalchemy import Index

class TodoTask(SQLModel, table=True):
    """TodoTask model for database storage"""
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False, index=True)
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    priority: str = Field(default="medium", regex="^(high|medium|low)$")
    category: str = Field(default="personal", max_length=50)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    __table_args__ = (
        Index('idx_todotask_user_created', 'user_id', 'created_at'),
    )
```

---

## Migration Strategy

### Clean Slate Approach

**Rationale**: Development environment allows data loss. Simplifies UUID migration.

**Steps**:
1. Drop all existing tables (User, TodoTask, Category, AuthToken, etc.)
2. Create new tables with UUID primary keys
3. Apply indexes and constraints
4. Verify schema with SQLModel metadata

**Migration Script** (`migrations/uuid_migration.py`):

```python
from sqlmodel import SQLModel, create_engine
from models.user import User
from models.todo import TodoTask
import os

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def migrate():
    """Drop all tables and recreate with UUID schema"""
    print("Dropping all existing tables...")
    SQLModel.metadata.drop_all(engine)

    print("Creating new tables with UUID schema...")
    SQLModel.metadata.create_all(engine)

    print("Migration complete!")

if __name__ == "__main__":
    migrate()
```

**Execution**:
```bash
cd backend
python migrations/uuid_migration.py
```

---

## Data Access Patterns

### User Operations

**Create User (Registration)**:
```python
async def create_user(email: str, password: str, session: AsyncSession) -> User:
    # Validate email format
    # Check email uniqueness
    # Hash password with bcrypt
    # Create user with email_verified=False
    # Return user (without password_hash)
```

**Find User by Email (Login)**:
```python
async def get_user_by_email(email: str, session: AsyncSession) -> Optional[User]:
    # Normalize email to lowercase
    # Query user by email
    # Return user with password_hash (for verification)
```

**Verify Password**:
```python
def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Use bcrypt.checkpw to compare
    # Return boolean result
```

### TodoTask Operations

**Create Task**:
```python
async def create_task(
    user_id: uuid.UUID,
    title: str,
    description: Optional[str],
    priority: str,
    category: str,
    session: AsyncSession
) -> TodoTask:
    # Validate title (non-empty, max length)
    # Validate priority (enum)
    # Create task with user_id
    # Return created task
```

**List User's Tasks**:
```python
async def get_user_tasks(
    user_id: uuid.UUID,
    session: AsyncSession
) -> List[TodoTask]:
    # Query tasks WHERE user_id = user_id
    # Order by created_at DESC
    # Return list of tasks
```

**Update Task**:
```python
async def update_task(
    task_id: uuid.UUID,
    user_id: uuid.UUID,
    updates: dict,
    session: AsyncSession
) -> TodoTask:
    # Query task WHERE id = task_id AND user_id = user_id
    # If not found, raise 404
    # Apply updates
    # Update updated_at timestamp
    # Return updated task
```

**Delete Task**:
```python
async def delete_task(
    task_id: uuid.UUID,
    user_id: uuid.UUID,
    session: AsyncSession
) -> None:
    # Query task WHERE id = task_id AND user_id = user_id
    # If not found, raise 404
    # Delete task
    # Commit transaction
```

---

## Performance Considerations

### Indexes

**User Table**:
- Primary key index on `id` (automatic)
- Unique index on `email` (for login queries)

**TodoTask Table**:
- Primary key index on `id` (automatic)
- Foreign key index on `user_id` (for data isolation queries)
- Composite index on `(user_id, created_at)` (for sorted task lists)

### Query Optimization

**Avoid N+1 Queries**:
- Use eager loading for user-task relationships if needed
- Batch queries when fetching multiple tasks

**Connection Pooling**:
- Use SQLModel's async engine with connection pool
- Configure pool size based on expected concurrency

**Pagination**:
- Implement LIMIT/OFFSET for large task lists
- Consider cursor-based pagination for better performance

---

## Testing Data

### Test Users

```python
TEST_USERS = [
    {
        "email": "alice@example.com",
        "password": "Alice123!",
        "id": "550e8400-e29b-41d4-a716-446655440001"
    },
    {
        "email": "bob@example.com",
        "password": "Bob456!@",
        "id": "550e8400-e29b-41d4-a716-446655440002"
    }
]
```

### Test Tasks

```python
TEST_TASKS = [
    {
        "id": "650e8400-e29b-41d4-a716-446655440001",
        "user_id": "550e8400-e29b-41d4-a716-446655440001",  # Alice
        "title": "Buy groceries",
        "description": "Milk, eggs, bread",
        "priority": "high",
        "category": "shopping",
        "completed": False
    },
    {
        "id": "650e8400-e29b-41d4-a716-446655440002",
        "user_id": "550e8400-e29b-41d4-a716-446655440002",  # Bob
        "title": "Finish project",
        "description": "Complete authentication feature",
        "priority": "high",
        "category": "work",
        "completed": False
    }
]
```

---

## Summary

**Entities**: 2 (User, TodoTask)
**Relationships**: 1 (User 1:N TodoTask)
**Primary Keys**: UUID for all entities
**Foreign Keys**: TodoTask.user_id → User.id (CASCADE DELETE)
**Indexes**: 4 total (2 primary, 1 unique, 1 composite)
**Validation**: Email format, password strength, title length, priority enum
**Isolation**: Query-level user_id filtering enforced
**Migration**: Clean slate (drop and recreate)
