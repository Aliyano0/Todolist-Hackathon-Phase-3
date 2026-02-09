# Authentication System Documentation

## Overview
This document describes the unified authentication system using Better Auth with JWT token integration for the FastAPI backend. This system resolves the previous 400 Bad Request error on the POST /auth/register endpoint by properly integrating Better Auth with the FastAPI backend.

## Architecture

### Frontend (Next.js)
- Uses Better Auth for user authentication and session management
- Handles registration, login, and logout operations via Better Auth client
- Stores JWT tokens in browser storage and includes them in API requests

### Backend (FastAPI)
- Implements JWT token verification compatible with Better Auth tokens
- Provides authentication endpoints for registration, login, logout, and token refresh
- Validates tokens and protects API routes using JWT middleware

## API Endpoints

### Authentication Endpoints

#### POST /auth/register
Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "user-uuid-string",
    "email": "user@example.com",
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z",
    "email_verified": false,
    "is_active": true
  }
}
```

#### POST /auth/login
Authenticate user and return JWT token.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "user-uuid-string",
    "email": "user@example.com",
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z",
    "email_verified": false,
    "is_active": true
  }
}
```

#### POST /auth/logout
Logout user (client-side operation).

**Response:**
```json
{
  "message": "Successfully logged out"
}
```

#### POST /auth/refresh
Refresh JWT token.

**Headers:**
```
Authorization: Bearer <valid_refresh_token>
```

**Response:**
```json
{
  "token": "new-jwt-token-string",
  "token_type": "bearer",
  "user": {
    "id": "user-uuid-string",
    "email": "user@example.com",
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z",
    "email_verified": false,
    "is_active": true
  }
}
```

## Security Features

### Password Validation
- Minimum 8 characters
- Mixed case (uppercase and lowercase)
- Numbers
- Special symbols

### Input Sanitization
- All user inputs are sanitized to prevent injection attacks
- Email format validation
- Special character filtering

### JWT Token Security
- Tokens expire after 30 minutes
- Proper token verification using HS256 algorithm
- Secure token storage and transmission

## Error Handling

### Standard Error Format
All error responses follow the standardized format:
```json
{
  "error": "Error Type",
  "message": "Human-readable error message"
}
```

### Common Error Codes
- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Invalid or expired token
- `409 Conflict`: User already exists
- `500 Internal Server Error`: Server-side error

## Integration with Better Auth

The system is designed to work seamlessly with Better Auth on the frontend while maintaining compatibility with the FastAPI backend. Better Auth tokens are verified by the FastAPI JWT middleware ensuring consistent authentication protocols between frontend and backend services.

## Testing

### End-to-End Authentication Flow
1. User registers via `/auth/register`
2. User logs in via `/auth/login` to receive JWT token
3. JWT token is included in `Authorization: Bearer <token>` header for protected endpoints
4. Tokens can be refreshed via `/auth/refresh` endpoint
5. User logs out via client-side operation

### Error Scenarios Covered
- Invalid email format during registration
- Weak password during registration
- Duplicate email registration attempt
- Invalid credentials during login
- Expired token access to protected resources
- Invalid refresh token

## Deployment Notes

### Environment Variables
Backend requires the following environment variables:
- `JWT_SECRET_KEY`: Secret key for JWT token signing
- `ALGORITHM`: Algorithm for JWT signing (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time (default: 30 minutes)

Frontend requires:
- `NEXT_PUBLIC_API_URL`: Base URL for backend API
- `NEXT_PUBLIC_BETTER_AUTH_URL`: Base URL for Better Auth

## Troubleshooting

### Common Issues
1. **400 Bad Request on registration**: Check email format and password strength requirements
2. **401 Unauthorized on protected endpoints**: Verify JWT token is properly included in request headers
3. **Token compatibility issues**: Ensure Better Auth and FastAPI use compatible token formats

### Resolution Steps
1. Verify environment variables are correctly set
2. Check that Better Auth is properly configured on the frontend
3. Confirm JWT verification middleware is working on the backend
4. Validate that API endpoints are accessible and responding correctly