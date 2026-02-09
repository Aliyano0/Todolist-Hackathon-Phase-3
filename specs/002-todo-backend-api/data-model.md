# Data Model: Todo Backend API

## Task Entity

### Fields
- **id**: Integer (Auto-increment primary key)
- **title**: String (Required, max 255 characters)
- **description**: String (Optional, max 1000 characters)
- **completed**: Boolean (Default: False)
- **user_id**: String (Required, represents authenticated user ID from JWT)
- **created_at**: DateTime (Auto-populated timestamp)
- **updated_at**: DateTime (Auto-populated and updated timestamp)

### Relationships
- **Owner**: Each task is associated with a single user identified by user_id

### Validation Rules
- Title must not be empty or whitespace only
- Title must be between 1 and 255 characters
- Description must be 1000 characters or less if provided
- User_id must match the authenticated user's ID from JWT token
- Task can only be accessed by the user who owns it

### State Transitions
- **Created**: When POST /{user_id}/tasks is called with valid data
- **Updated**: When PUT /{user_id}/tasks/{id} is called with new data
- **Completed**: When PATCH /{user_id}/tasks/{id}/complete is called to mark as complete
- **Reopened**: When PATCH /{user_id}/tasks/{id}/complete is called to mark as incomplete
- **Deleted**: When DELETE /{user_id}/tasks/{id} is called

## User Representation

### Fields
- **user_id**: String (Unique identifier extracted from JWT token)
- **email**: String (Email associated with the user account, from Better Auth)

### Notes
- User data is not stored in this backend; it's extracted from JWT tokens issued by Better Auth
- All task operations are filtered by the authenticated user's ID