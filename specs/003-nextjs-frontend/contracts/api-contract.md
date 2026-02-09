# API Contract: Frontend-Backend Integration

## Overview
This document defines the API contracts between the Next.js frontend and FastAPI backend for the multi-user Todo application.

## Authentication Endpoints

### POST /auth/register
Register a new user account.

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response (200)**:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "uuid-string",
    "email": "user@example.com",
    "created_at": "2026-01-21T10:30:00Z",
    "updated_at": "2026-01-21T10:30:00Z"
  }
}
```

**Validation**:
- Email must be valid format
- Password must meet strength requirements (8+ chars, mixed case, numbers, symbols)

**Errors**:
- `400 Bad Request`: Invalid email format or password requirements not met
- `409 Conflict`: User with this email already exists

### POST /auth/login
Authenticate a user and return JWT token.

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response (200)**:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "uuid-string",
    "email": "user@example.com",
    "created_at": "2026-01-21T10:30:00Z",
    "updated_at": "2026-01-21T10:30:00Z"
  }
}
```

**Errors**:
- `400 Bad Request`: Invalid email format or missing password
- `401 Unauthorized`: Incorrect email or password

### POST /auth/logout
Logout the current user.

**Headers**:
```
Authorization: Bearer {jwt-token}
```

**Response (200)**:
```json
{
  "message": "Successfully logged out"
}
```

### POST /auth/refresh
Refresh JWT token (future implementation).

**Headers**:
```
Authorization: Bearer {jwt-token}
```

**Response (501)**:
```json
{
  "detail": "Token refresh functionality not fully implemented in this version. For now, users need to re-login when access token expires."
}
```

**Note**: This endpoint is currently not implemented and returns a 501 Not Implemented error.

## Todo Endpoints

All todo endpoints require authentication via JWT token in the Authorization header.

### GET /api/todos
Retrieve all todos for the authenticated user.

**Headers**:
```
Authorization: Bearer {jwt-token}
```

**Response (200)**:
```json
{
  "todos": [
    {
      "id": "uuid-string",
      "title": "Todo title",
      "description": "Optional description",
      "completed": false,
      "userId": "user-uuid",
      "createdAt": "2026-01-16T10:00:00Z",
      "updatedAt": "2026-01-16T10:00:00Z"
    }
  ]
}
```

### POST /api/todos
Create a new todo for the authenticated user.

**Headers**:
```
Authorization: Bearer {jwt-token}
```

**Request Body**:
```json
{
  "title": "New todo title",
  "description": "Optional description (max 500 chars)",
  "completed": false
}
```

**Response (201)**:
```json
{
  "todo": {
    "id": "uuid-string",
    "title": "New todo title",
    "description": "Optional description",
    "completed": false,
    "userId": "user-uuid",
    "createdAt": "2026-01-16T10:00:00Z",
    "updatedAt": "2026-01-16T10:00:00Z"
  }
}
```

### PUT /api/todos/{id}
Update an existing todo.

**Headers**:
```
Authorization: Bearer {jwt-token}
```

**Request Body**:
```json
{
  "title": "Updated title",
  "description": "Updated description",
  "completed": true
}
```

**Response (200)**:
```json
{
  "todo": {
    "id": "uuid-string",
    "title": "Updated title",
    "description": "Updated description",
    "completed": true,
    "userId": "user-uuid",
    "createdAt": "2026-01-16T10:00:00Z",
    "updatedAt": "2026-01-16T11:00:00Z"
  }
}
```

### PATCH /api/todos/{id}/toggle
Toggle the completion status of a todo.

**Headers**:
```
Authorization: Bearer {jwt-token}
```

**Response (200)**:
```json
{
  "todo": {
    "id": "uuid-string",
    "title": "Todo title",
    "description": "Optional description",
    "completed": true,
    "userId": "user-uuid",
    "createdAt": "2026-01-16T10:00:00Z",
    "updatedAt": "2026-01-16T11:00:00Z"
  }
}
```

### DELETE /api/todos/{id}
Delete a todo.

**Headers**:
```
Authorization: Bearer {jwt-token}
```

**Response (200)**:
```json
{
  "success": true,
  "message": "Todo deleted successfully"
}
```

## User Profile Endpoints

### GET /api/users/me
Get the authenticated user's profile information.

**Headers**:
```
Authorization: Bearer {jwt-token}
```

**Response (200)**:
```json
{
  "user": {
    "id": "uuid-string",
    "email": "user@example.com",
    "createdAt": "2026-01-16T10:00:00Z",
    "updatedAt": "2026-01-16T10:00:00Z"
  }
}
```

### PUT /api/users/me
Update the authenticated user's profile information.

**Headers**:
```
Authorization: Bearer {jwt-token}
```

**Request Body**:
```json
{
  "email": "newemail@example.com"
}
```

**Response (200)**:
```json
{
  "user": {
    "id": "uuid-string",
    "email": "newemail@example.com",
    "createdAt": "2026-01-16T10:00:00Z",
    "updatedAt": "2026-01-16T11:00:00Z"
  }
}
```

## Error Responses

All error responses follow the same structure:

**Response (4xx/5xx)**:
```json
{
  "success": false,
  "error": "Error message",
  "details": "Additional details if applicable"
}
```

## Authentication Requirements

- All `/api/*` endpoints require a valid JWT token in the `Authorization: Bearer {token}` header
- Invalid/expired tokens will result in a 401 Unauthorized response
- Tokens are automatically refreshed using silent refresh mechanism
- Users are logged out after 30 minutes of inactivity