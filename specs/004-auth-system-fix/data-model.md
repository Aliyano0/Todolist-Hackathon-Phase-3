# Data Model: Authentication System

## Overview
Defines the data structures and relationships for the unified authentication system using Better Auth with JWT token integration for FastAPI backend.

## Key Entities

### User
Represents a registered user account with authentication credentials.

**Fields:**
- `id`: string (primary key, unique identifier from Better Auth)
- `email`: string (unique, validated email address)
- `password_hash`: string (bcrypt hash of user password, stored securely)
- `created_at`: datetime (timestamp when user account was created)
- `updated_at`: datetime (timestamp when user account was last updated)
- `email_verified`: boolean (indicates if email has been verified)
- `is_active`: boolean (indicates if account is active/enabled)

**Validation Rules:**
- Email must be unique across all users
- Email must match standard email format
- Email must be non-empty
- User ID must be unique and immutable
- Account must be active to authenticate

**Relationships:**
- One-to-many with Todo items (user can have multiple todos)
- One-to-many with Sessions (user can have multiple active sessions)

### Authentication Token
Secure token issued upon successful authentication that grants access to protected resources.

**Fields:**
- `token`: string (JWT token string)
- `user_id`: string (foreign key to User.id)
- `token_type`: string (e.g., "bearer", "access", "refresh")
- `expires_at`: datetime (expiration timestamp)
- `created_at`: datetime (issue timestamp)
- `revoked`: boolean (indicates if token has been invalidated)

**Validation Rules:**
- Token must be valid JWT format
- User ID must reference an existing active user
- Token must not be expired
- Revoked tokens must not grant access

**Relationships:**
- Many-to-one with User (multiple tokens per user)
- One-to-one with Session (token associated with specific session)

### Session
Temporary user state maintained during active use of the application.

**Fields:**
- `id`: string (primary key, session identifier)
- `user_id`: string (foreign key to User.id)
- `device_info`: string (information about user's device/browser)
- `ip_address`: string (IP address of the session)
- `created_at`: datetime (session start time)
- `last_activity`: datetime (last interaction time)
- `expires_at`: datetime (session timeout)
- `is_active`: boolean (indicates if session is still valid)

**Validation Rules:**
- Session must be associated with an active user
- Session must not be expired
- Active sessions must have valid authentication tokens
- IP address and device info should be recorded for security

**Relationships:**
- Many-to-one with User (multiple sessions per user)
- One-to-one with Authentication Token (session tied to specific token)

## State Transitions

### User States:
- `Pending Registration` → `Email Verification Required` → `Active` → `Suspended/Deactivated`
- `Active` → `Inactive` (due to inactivity) → `Reactivated`

### Session States:
- `Created` → `Active` → `Expired/Inactive` → `Terminated`
- `Active` → `Paused` (idle timeout) → `Active` (activity resumed)

## Relationships

```
User (1) <---> (Many) Todo
User (1) <---> (Many) Session
User (1) <---> (Many) Authentication Token
Session (1) <---> (1) Authentication Token
```

## Indexes
- User.email (unique index for authentication lookup)
- User.id (primary index)
- Authentication Token.expires_at (for cleanup jobs)
- Session.user_id (for user session management)
- Session.expires_at (for session cleanup)