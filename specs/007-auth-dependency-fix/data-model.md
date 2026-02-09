# Data Model: Auth Dependency Fix

## Overview
This document defines the data structures and relationships relevant to fixing the authentication system dependency issues. The focus is on the User entity and authentication-related objects that are involved in the interface mismatch between the auth system and dependent modules.

## User Entity

### User Model
- **id**: UUID (Primary Key) - Unique identifier for the user
- **email**: String (Unique, Required) - User's email address for authentication
- **name**: String (Required) - User's full name
- **password_hash**: String (Required) - Hashed password for authentication
- **created_at**: DateTime - Timestamp when user account was created
- **updated_at**: DateTime - Timestamp when user account was last updated
- **is_active**: Boolean (Default: True) - Whether the account is active
- **email_verified**: Boolean (Default: False) - Whether the email has been verified

### Validation Rules
- Email: Must be valid email format, unique across all users
- Name: Must be 1-100 characters
- Password: Must be minimum 8 characters with uppercase, lowercase, and number
- Is Active: Cannot be set to false by user, only by admin or system

## Authentication Interface

### User Object Properties
- **id**: String - Unique identifier for the authenticated user
- **email**: String - Email address of the authenticated user
- **name**: String - Full name of the authenticated user
- **is_active**: Boolean - Whether the account is active
- **email_verified**: Boolean - Whether the email has been verified
- **created_at**: DateTime - When the user account was created
- **updated_at**: DateTime - When the user account was last updated

### Access Pattern
- **Direct Property Access**: `user.id`, `user.email`, `user.name` (NEW APPROACH)
- ~~Dictionary Access~~: `user["user_id"]`, `user["email"]` (OLD APPROACH - DEPRECATED)

## Session Entity

### Session Model
- **id**: UUID (Primary Key) - Unique identifier for the session
- **user_id**: UUID (Foreign Key) - Reference to the user
- **token**: String (Unique, Required) - JWT token identifier
- **expires_at**: DateTime - When the session expires
- **created_at**: DateTime - When the session was created
- **last_accessed_at**: DateTime - Last time the session was used
- **device_info**: String (Optional) - Information about the device used
- **ip_address**: String (Optional) - IP address of the session

### Validation Rules
- Expires At: Must be in the future
- User ID: Must reference an existing active user
- Token: Must be unique across all sessions

## Token Entity

### JWT Token Model
- **id**: UUID (Primary Key) - Unique identifier for the token
- **user_id**: UUID (Foreign Key) - Reference to the user
- **token_type**: String (Enum: 'access', 'refresh') - Type of token
- **token_value**: String (Required) - The actual JWT token
- **expires_at**: DateTime - When the token expires
- **revoked**: Boolean (Default: False) - Whether the token has been revoked
- **created_at**: DateTime - When the token was created

### Validation Rules
- Expires At: Must be in the future
- Token Type: Must be either 'access' or 'refresh'
- User ID: Must reference an existing active user

## Relationship Diagram

```
User (1) <---> (Many) Session
User (1) <---> (Many) Token
```

## State Transitions

### User States
- **Pending**: User created but email not verified
- **Active**: User email verified and account active
- **Suspended**: Account temporarily deactivated
- **Deactivated**: Account permanently deactivated

### Session States
- **Active**: Session is valid and can be used
- **Expired**: Session has passed its expiry time
- **Revoked**: Session was manually invalidated

## Database Indexes

### Required Indexes
- User.email (Unique)
- User.created_at
- Session.token (Unique)
- Session.expires_at
- Session.user_id
- Token.user_id
- Token.expires_at

## Constraints

### Referential Integrity
- Session.user_id must reference User.id
- Token.user_id must reference User.id

### Data Integrity
- Passwords must be hashed before storage
- Email addresses must be unique
- Session tokens must be unique
- Tokens must expire within defined time limits

## API Contract Implications

### User Creation
- Requires: email, name, password
- Returns: user id, email, name, created timestamp
- Validates: email format, password strength, name length

### Authentication
- Requires: email, password
- Returns: JWT token, user id, expiration
- Validates: user exists, password matches, account active

## Authentication Interface Changes

### Old Interface (Dictionary-based)
- `get_current_user` returned: `{"user_id": "...", "email": "...", "name": "..."}`
- Access pattern: `user["user_id"]`, `user["email"]`

### New Interface (Object-based)
- `get_current_user` returns: User object with properties
- Access pattern: `user.id`, `user.email`, `user.name`

### Ownership Validation
- `verify_user_owns_resource` validates that JWT user_id matches path parameter
- Returns appropriate HTTP error responses (403 Forbidden) when validation fails