# Data Model: Better Auth Integration with FastAPI Backend

## User Entity

**Fields**:
- `id`: String (Primary identifier from Better Auth)
- `email`: String (User's email address, unique)
- `password_hash`: String (Hashed password for legacy compatibility)
- `created_at`: DateTime (Account creation timestamp)
- `updated_at`: DateTime (Last update timestamp)
- `email_verified`: Boolean (Whether email has been verified)
- `is_active`: Boolean (Whether account is active)

**Validation Rules**:
- Email must be valid format
- Email must be unique
- Password must meet strength requirements (8+ chars, mixed case, numbers, symbols)
- ID must match Better Auth user ID format

**Relationships**:
- One-to-many with Todo entity (user has many todos)

## AuthenticationToken Entity

**Fields**:
- `token`: String (JWT token string)
- `user_id`: String (Reference to User.id)
- `expires_at`: DateTime (Token expiration time)
- `created_at`: DateTime (Token creation time)
- `is_revoked`: Boolean (Whether token has been revoked)

**Validation Rules**:
- Token must be valid JWT format
- User ID must reference existing user
- Expiration time must be in the future

## Todo Entity

**Fields**:
- `id`: Integer (Auto-incrementing primary key)
- `title`: String (Todo title, required)
- `description`: String (Optional description)
- `completed`: Boolean (Whether todo is completed)
- `user_id`: String (Reference to User.id)
- `created_at`: DateTime (Creation timestamp)
- `updated_at`: DateTime (Last update timestamp)

**Validation Rules**:
- Title must not be empty
- User ID must reference existing user
- Completed defaults to false

**Relationships**:
- Many-to-one with User entity (todo belongs to one user)