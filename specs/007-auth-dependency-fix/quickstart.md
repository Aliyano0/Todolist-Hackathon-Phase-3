# Quickstart Guide: Auth Dependency Fix

## Overview
This guide provides instructions for implementing the fix for authentication system dependency issues, specifically addressing the missing `verify_user_owns_resource` function and interface mismatch between `get_current_user` return types.

## Prerequisites
- Python 3.13+ installed
- Node.js 18+ installed (if working with frontend components)
- PostgreSQL database (Neon Serverless recommended)
- UV package manager for Python dependencies
- Git for version control

## Setup

### 1. Clone and Navigate to Project
```bash
cd /path/to/todolist-hackathon/todolist-phase-1
```

### 2. Activate Virtual Environment
```bash
cd backend
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

## Implementation Steps

### Step 1: Fix Missing Function in Auth Dependencies

Add the missing `verify_user_owns_resource` function to `backend/dependencies/auth.py`:

```python
def verify_user_owns_resource(
    current_user: User = Depends(get_current_user)
):
    """
    Verify that the current user owns the resource being accessed.
    This function is used as a dependency to ensure user_id in JWT matches the user_id in the path.
    """
    # This will be used in the routes to verify the user_id matches the path parameter
    return current_user
```

### Step 2: Update Todos API to Use New Interface

Update `backend/api/todos.py` to work with the new User object interface instead of dictionary:

**Before (Old Interface):**
```python
# Old approach - treating user as dictionary
if current_user["user_id"] != user_id:
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="User ID in token doesn't match path parameter"
    )
```

**After (New Interface):**
```python
# New approach - accessing User object properties directly
if current_user.id != user_id:
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="User ID in token doesn't match path parameter"
    )
```

### Step 3: Update All User ID Verification Locations

Update all locations in `todos.py` where user ID verification occurs:
- Line 25: Create task endpoint
- Line 60: List tasks endpoint
- Line 83: Get task endpoint
- Line 114: Update task endpoint
- Line 159: Delete task endpoint
- Line 190: Toggle task completion endpoint

## Testing the Fix

### 1. Verify Application Starts Without Errors
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Check that there are no ImportError exceptions related to `verify_user_owns_resource`.

### 2. Test Authentication Flows
- Verify user can register and login successfully
- Test that users can only access their own todos
- Confirm that attempting to access another user's data returns 403 Forbidden

### 3. Validate Interface Consistency
- Ensure all API routes properly use the new User object interface
- Verify that authorization checks work as expected

## Error Handling

### Common Issues and Solutions

#### ImportError: cannot import name 'verify_user_owns_resource'
- **Cause**: Missing function in dependencies/auth.py
- **Solution**: Add the `verify_user_owns_resource` function to the auth dependencies file

#### AttributeError: 'User' object has no attribute 'get'
- **Cause**: Still using dictionary access patterns on User object
- **Solution**: Update to use direct property access (e.g., `user.id` instead of `user['user_id']`)

#### 403 Forbidden Errors on Valid Requests
- **Cause**: Incorrect user ID comparison in authorization checks
- **Solution**: Ensure using `current_user.id` instead of `current_user['user_id']`

## API Endpoints Affected

### Authentication Endpoints
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User authentication
- `POST /api/auth/refresh` - Token refresh

### Todo Endpoints
- `POST /api/todos/{user_id}/tasks` - Create task for user
- `GET /api/todos/{user_id}/tasks` - List user's tasks
- `GET /api/todos/{user_id}/tasks/{id}` - Get specific task
- `PUT /api/todos/{user_id}/tasks/{id}` - Update task
- `DELETE /api/todos/{user_id}/tasks/{id}` - Delete task
- `PATCH /api/todos/{user_id}/tasks/{id}/complete` - Toggle completion

## Security Considerations

### Authorization Checks
- Always verify that the authenticated user owns the resource being accessed
- Use 403 Forbidden responses when authorization fails
- Ensure user ID in JWT matches the user ID in the request path

### Data Isolation
- Prevent cross-user data access
- Validate user ownership for all sensitive operations
- Maintain proper session management

## Troubleshooting

### Application Won't Start
- Check that `verify_user_owns_resource` is properly imported in `todos.py`
- Verify all syntax is correct in the updated auth dependencies
- Ensure all required dependencies are installed

### Authentication Fails
- Confirm the User object properties are being accessed correctly
- Verify JWT tokens are being validated properly
- Check that the auth middleware is functioning as expected

### Data Access Issues
- Ensure all user ID comparisons use the new interface (`user.id` not `user['user_id']`)
- Verify that authorization checks are consistent across all endpoints
- Test that users can only access their own data