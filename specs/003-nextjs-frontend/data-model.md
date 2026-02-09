# Data Model: Next.js Frontend for Multi-User Todo Web App

## Frontend-Specific Models

### User Model
- **id**: string - Unique identifier for the user
- **email**: string - User's email address
- **createdAt**: Date - Account creation timestamp
- **updatedAt**: Date - Last update timestamp

**Validation**:
- Email must be valid email format
- Email must be unique

### Todo Model
- **id**: string - Unique identifier for the todo
- **title**: string - Title of the todo (required, max 255 characters)
- **description**: string - Optional description (max 500 characters)
- **completed**: boolean - Completion status
- **userId**: string - Owner of the todo
- **createdAt**: Date - Creation timestamp
- **updatedAt**: Date - Last update timestamp

**Validation**:
- Title must not be empty
- Description length must be ≤ 500 characters
- userId must match authenticated user

### Auth Session Model
- **token**: string - JWT token
- **expiresAt**: Date - Token expiration time
- **user**: User - Associated user data

## State Management
- **AuthState**: Manages authentication status and user info
- **TodoState**: Manages todo list and operations
- **ThemeState**: Manages light/dark theme preference

## Relationships
- **User 1 -> * Todo**: One user can have multiple todos
- **Todo * -> 1 User**: Each todo belongs to one user