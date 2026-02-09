# API Contract: Better Auth Integration with FastAPI Backend

## Authentication Endpoints

### POST /api/auth/sign-up
**Description**: Register a new user via Better Auth compatible endpoint

**Request**:
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response (200)**:
```json
{
  "token": "jwt-token-string",
  "user": {
    "id": "user-id-from-better-auth",
    "email": "user@example.com",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z",
    "email_verified": false,
    "is_active": true
  }
}
```

### POST /api/auth/sign-in
**Description**: Authenticate user via Better Auth compatible endpoint

**Request**:
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response (200)**:
```json
{
  "token": "jwt-token-string",
  "user": {
    "id": "user-id-from-better-auth",
    "email": "user@example.com",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z",
    "email_verified": false,
    "is_active": true
  }
}
```

### POST /api/auth/sign-out
**Description**: Logout user via Better Auth compatible endpoint

**Response (200)**:
```json
{
  "message": "Successfully signed out"
}
```

### POST /api/auth/refresh
**Description**: Refresh JWT token via Better Auth compatible endpoint

**Headers**:
- Authorization: Bearer {valid-jwt-token}

**Response (200)**:
```json
{
  "token": "new-jwt-token-string",
  "token_type": "bearer",
  "user": {
    "id": "user-id-from-better-auth",
    "email": "user@example.com",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z",
    "email_verified": false,
    "is_active": true
  }
}
```

## Protected API Endpoints

### GET /api/todos
**Description**: Get all todos for authenticated user

**Headers**:
- Authorization: Bearer {valid-jwt-token}

**Response (200)**:
```json
{
  "todos": [
    {
      "id": 1,
      "title": "Sample Todo",
      "description": "Sample description",
      "completed": false,
      "user_id": "user-id-from-better-auth",
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

### POST /api/todos
**Description**: Create a new todo for authenticated user

**Headers**:
- Authorization: Bearer {valid-jwt-token}

**Request**:
```json
{
  "title": "New Todo",
  "description": "Todo description",
  "completed": false
}
```

**Response (200)**:
```json
{
  "id": 1,
  "title": "New Todo",
  "description": "Todo description",
  "completed": false,
  "user_id": "user-id-from-better-auth",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### PUT /api/todos/{id}
**Description**: Update an existing todo for authenticated user

**Headers**:
- Authorization: Bearer {valid-jwt-token}

**Request**:
```json
{
  "title": "Updated Todo Title",
  "description": "Updated description",
  "completed": true
}
```

**Response (200)**:
```json
{
  "id": 1,
  "title": "Updated Todo Title",
  "description": "Updated description",
  "completed": true,
  "user_id": "user-id-from-better-auth",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### DELETE /api/todos/{id}
**Description**: Delete a todo for authenticated user

**Headers**:
- Authorization: Bearer {valid-jwt-token}

**Response (200)**:
```json
{
  "message": "Todo deleted successfully"
}
```

## Error Responses

### 401 Unauthorized
```json
{
  "detail": "Unauthorized: Please log in to continue"
}
```

### 400 Bad Request
```json
{
  "detail": "Error message describing the issue"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Server error: Please try again later"
}
```