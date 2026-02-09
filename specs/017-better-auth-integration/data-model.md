# Data Model: JWT-Based Authentication Integration

**Status**: Implemented

## User Entity
- **id**: UUID (Primary Key)
- **email**: String (Unique, Indexed)
- **password_hash**: String (Bcrypt hashed)
- **created_at**: DateTime (Timestamp)
- **updated_at**: DateTime (Timestamp)
- **email_verified**: Boolean (Default: false)
- **verification_token**: String (Nullable, for email verification, 24-hour expiry)
- **reset_token**: String (Nullable, for password reset, 1-hour expiry)
- **reset_token_expires**: DateTime (Nullable, for password reset)

## TodoTask Entity (Enhanced)
- **id**: Integer (Primary Key)
- **title**: String (Min: 1, Max: 255)
- **description**: String (Nullable, Max: 1000)
- **completed**: Boolean (Default: false)
- **priority**: String (Enum: high|medium|low, Default: medium)
- **category**: String (Max: 50, Default: personal)
- **user_id**: UUID (Foreign Key to User.id, Indexed)
- **created_at**: DateTime (Timestamp)
- **updated_at**: DateTime (Timestamp)

## Authentication Token Entity
- **id**: UUID (Primary Key)
- **user_id**: UUID (Foreign Key to User.id)
- **token_type**: String (Enum: access|refresh)
- **token_value**: String (Hashed)
- **expires_at**: DateTime (Expiration timestamp)
- **created_at**: DateTime (Timestamp)
- **revoked**: Boolean (Default: false)

## Relationships
- User (1) ←→ TodoTask (Many): One user owns many tasks
- User (1) ←→ Authentication Token (Many): One user has many auth tokens