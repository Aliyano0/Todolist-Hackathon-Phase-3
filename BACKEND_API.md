# Todo Backend API Documentation

## Overview
The Todo Backend API is a FastAPI-based RESTful service for managing todo tasks with JWT-based authentication. The API provides full CRUD operations for todo items while enforcing strict multi-user data isolation.

## Base URL
All API endpoints are prefixed with `/api/` and require a user ID in the path.

## Authentication
- All API endpoints require JWT authentication
- Include the JWT token in the Authorization header: `Authorization: Bearer {jwt_token}`
- The user ID in the JWT token must match the user ID in the URL path
- Tokens are obtained from Better Auth frontend integration

## API Endpoints

### Health Check
```
GET /
GET /health
```

Returns a welcome message or health status.

### Task Operations

#### Create a Task
```
POST /api/{user_id}/tasks
```

**Headers:**
- `Authorization: Bearer {jwt_token}`
- `Content-Type: application/json`

**Request Body:**
```json
{
  "title": "Task title",
  "description": "Optional description"
}
```

**Response:**
- `201 Created` with the created task object
- `400 Bad Request` for invalid input
- `401 Unauthorized` for invalid/missing token
- `403 Forbidden` for user ID mismatch

**Response Body:**
```json
{
  "id": 123,
  "title": "Task title",
  "description": "Optional description",
  "completed": false,
  "user_id": "user_identifier",
  "created_at": "2023-01-01T12:00:00Z",
  "updated_at": "2023-01-01T12:00:00Z"
}
```

#### List User's Tasks
```
GET /api/{user_id}/tasks
```

**Headers:**
- `Authorization: Bearer {jwt_token}`

**Response:**
- `200 OK` with an array of task objects
- `401 Unauthorized` for invalid/missing token
- `403 Forbidden` for user ID mismatch

**Response Body:**
```json
[
  {
    "id": 123,
    "title": "Task title",
    "description": "Optional description",
    "completed": false,
    "user_id": "user_identifier",
    "created_at": "2023-01-01T12:00:00Z",
    "updated_at": "2023-01-01T12:00:00Z"
  }
]
```

#### Get Specific Task
```
GET /api/{user_id}/tasks/{task_id}
```

**Headers:**
- `Authorization: Bearer {jwt_token}`

**Response:**
- `200 OK` with the task object
- `401 Unauthorized` for invalid/missing token
- `403 Forbidden` for user ID mismatch
- `404 Not Found` if task doesn't exist

#### Update Task
```
PUT /api/{user_id}/tasks/{task_id}
```

**Headers:**
- `Authorization: Bearer {jwt_token}`
- `Content-Type: application/json`

**Request Body:**
```json
{
  "title": "Updated title",
  "description": "Updated description",
  "completed": true
}
```

All fields are optional.

**Response:**
- `200 OK` with the updated task object
- `400 Bad Request` for invalid input
- `401 Unauthorized` for invalid/missing token
- `403 Forbidden` for user ID mismatch
- `404 Not Found` if task doesn't exist

#### Delete Task
```
DELETE /api/{user_id}/tasks/{task_id}
```

**Headers:**
- `Authorization: Bearer {jwt_token}`

**Response:**
- `204 No Content` on success
- `401 Unauthorized` for invalid/missing token
- `403 Forbidden` for user ID mismatch
- `404 Not Found` if task doesn't exist

#### Toggle Task Completion
```
PATCH /api/{user_id}/tasks/{task_id}/complete
```

**Headers:**
- `Authorization: Bearer {jwt_token}`

**Response:**
- `200 OK` with the updated task object
- `401 Unauthorized` for invalid/missing token
- `403 Forbidden` for user ID mismatch
- `404 Not Found` if task doesn't exist

## Error Responses
All error responses follow the format:
```json
{
  "detail": "Error message"
}
```

## Frontend Integration Guidelines

### Authentication Flow
1. Obtain JWT token from Better Auth on login/signup
2. Store token securely (preferably in memory)
3. Include token in Authorization header for all API requests
4. Handle 401/403 responses by redirecting to login
5. Verify that user ID in JWT matches the user ID in API paths

### Common Headers
- `Authorization: Bearer {jwt_token}`
- `Content-Type: application/json` (for POST, PUT, PATCH requests)

### Data Model
Task objects returned by the API contain:
- `id`: Unique identifier (integer)
- `title`: Task title (string, 1-255 characters)
- `description`: Optional task description (string, max 1000 characters)
- `completed`: Completion status (boolean)
- `user_id`: Associated user ID (string)
- `created_at`: Creation timestamp (ISO format)
- `updated_at`: Last update timestamp (ISO format)

### Error Handling
- Handle 401/403 for authentication issues
- Handle 404 for resource not found
- Handle 400 for validation errors
- Provide user-friendly error messages from API responses

## Testing Notes
- All endpoints require valid JWT tokens
- User ID in JWT must match the user ID in the URL path
- The API enforces strict data isolation between users
- Test with multiple users to verify data isolation works correctly

## Health Check
- Use `GET /health` endpoint to verify API is running
- Returns `{"status": "healthy", "message": "Todo Backend API is running"}` when operational