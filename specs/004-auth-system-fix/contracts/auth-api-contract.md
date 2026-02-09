# Authentication API Contract

## Overview
API contract for the unified authentication system using Better Auth with JWT token integration for the FastAPI backend.

## Base URL
`http://localhost:8000` (development) or configured API URL

## Authentication Flow
1. User registers via `/auth/register`
2. User logs in via `/auth/login` to receive JWT token
3. JWT token is included in `Authorization: Bearer <token>` header for protected endpoints
4. Tokens can be refreshed via `/auth/refresh` endpoint

## API Endpoints

### Registration
#### POST /auth/register
Register a new user account.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Request Headers:**
- `Content-Type: application/json`

**Responses:**
- `200 OK`: Registration successful
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "user-uuid-string",
    "email": "user@example.com",
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z"
  }
}
```

- `400 Bad Request`: Invalid input data
```json
{
  "error": "Bad Request",
  "message": "Invalid email format or password requirements not met"
}
```

- `409 Conflict`: User already exists
```json
{
  "error": "Conflict",
  "message": "User with this email already exists"
}
```

### Login
#### POST /auth/login
Authenticate user and return JWT token.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Request Headers:**
- `Content-Type: application/json`

**Responses:**
- `200 OK`: Login successful
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "user-uuid-string",
    "email": "user@example.com",
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z"
  }
}
```

- `400 Bad Request`: Invalid input data
```json
{
  "error": "Bad Request",
  "message": "Invalid email format or password not provided"
}
```

- `401 Unauthorized`: Incorrect credentials
```json
{
  "error": "Unauthorized",
  "message": "Incorrect email or password"
}
```

### Logout
#### POST /auth/logout
Logout user (client-side operation).

**Request Headers:**
- `Authorization: Bearer <valid-jwt-token>`

**Responses:**
- `200 OK`: Logout successful
```json
{
  "message": "Successfully logged out"
}
```

### Token Refresh
#### POST /auth/refresh
Refresh JWT token before expiration.

**Request Headers:**
- `Authorization: Bearer <valid-refresh-token>`

**Responses:**
- `200 OK`: Token refresh successful
```json
{
  "token": "new-jwt-token-string",
  "token_type": "bearer"
}
```

- `401 Unauthorized`: Invalid or expired refresh token
```json
{
  "error": "Unauthorized",
  "message": "Invalid or expired refresh token"
}
```

## Error Response Format
All error responses follow the standardized format:

```json
{
  "error": "Error Type",
  "message": "Human-readable error message"
}
```

## JWT Token Format
JWT tokens follow the standard format with the following claims:
- `sub`: User ID (string)
- `email`: User email (string)
- `exp`: Expiration time (Unix timestamp)
- `iat`: Issued at time (Unix timestamp)

## Security Requirements
- All authentication requests must use HTTPS in production
- Passwords must meet complexity requirements (8+ characters with mixed case, numbers, symbols)
- JWT tokens must be validated on all protected endpoints
- Token expiration must be enforced
- Rate limiting should be applied to authentication endpoints