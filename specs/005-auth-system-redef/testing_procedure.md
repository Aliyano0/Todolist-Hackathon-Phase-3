# Better Auth Integration Testing Procedure

This document outlines the testing procedures to validate the Better Auth integration with the FastAPI backend.

## Pre-requisites

- Backend server running on http://localhost:8000
- Frontend server running on http://localhost:3000
- Environment variables properly configured with shared JWT secret

## Test Suite 1: User Registration Flow

### Test Case 1.1: Successful Registration
1. Navigate to frontend registration page (`/register`)
2. Fill in valid email and strong password
3. Submit registration form
4. Verify:
   - API call to `/api/auth/sign-up` is made
   - 200 response with JWT token and user data
   - User is redirected to dashboard
   - User entry is created in database with Better Auth ID

### Test Case 1.2: Invalid Registration Data
1. Navigate to frontend registration page
2. Fill in invalid data (invalid email format, weak password)
3. Submit registration form
4. Verify:
   - Error messages are displayed to user
   - No user is created in database

## Test Suite 2: User Login Flow

### Test Case 2.1: Successful Login
1. Navigate to frontend login page (`/login`)
2. Fill in valid email and password for existing user
3. Submit login form
4. Verify:
   - API call to `/api/auth/sign-in` is made
   - 200 response with JWT token and user data
   - User is redirected to dashboard
   - Auth token is stored in local storage

### Test Case 2.2: Failed Login
1. Navigate to frontend login page
2. Fill in invalid credentials
3. Submit login form
4. Verify:
   - 401 Unauthorized response
   - Error message displayed to user
   - No token stored in local storage

## Test Suite 3: Protected API Access

### Test Case 3.1: Valid Token Access
1. Obtain a valid JWT token (via login)
2. Make API request to `/api/todos` with Authorization header
3. Verify:
   - 200 response with user's todos
   - Proper user ID validation from JWT token

### Test Case 3.2: Invalid Token Access
1. Use an invalid or expired JWT token
2. Make API request to `/api/todos` with Authorization header
3. Verify:
   - 401 Unauthorized response
   - Proper error handling

### Test Case 3.3: Wrong User Data Access
1. Obtain a JWT token for user A
2. Attempt to access todos for user B
3. Verify:
   - 403 Forbidden response or appropriate validation
   - User data isolation is maintained

## Test Suite 4: Token Refresh Flow

### Test Case 4.1: Token Refresh
1. Obtain a valid JWT token
2. Call `/api/auth/refresh` endpoint with valid token
3. Verify:
   - 200 response with new JWT token
   - New token has updated expiration time

## Test Suite 5: Logout Flow

### Test Case 5.1: Successful Logout
1. Log in and obtain a JWT token
2. Call `/api/auth/sign-out` endpoint
3. Verify:
   - 200 response
   - Token is cleared from local storage
   - User is redirected to login page

## Test Suite 6: Better Auth Compatibility

### Test Case 6.1: Endpoint Compatibility
1. Make direct API calls to Better Auth compatible endpoints:
   - `POST /api/auth/sign-up`
   - `POST /api/auth/sign-in`
   - `POST /api/auth/sign-out`
   - `POST /api/auth/refresh`
2. Verify:
   - All endpoints respond with expected data structures
   - JWT tokens are properly formatted and validated

### Test Case 6.2: JWT Token Validation
1. Generate a JWT token from Better Auth
2. Send it to any protected backend endpoint
3. Verify:
   - Token is properly validated using shared secret
   - User ID is extracted correctly from token
   - Access is granted based on user permissions

## Test Suite 7: Error Handling

### Test Case 7.1: Malformed JWT Token
1. Send a malformed JWT token to any protected endpoint
2. Verify:
   - Proper error response (401 Unauthorized)
   - No stack traces exposed

### Test Case 7.2: Expired JWT Token
1. Send an expired JWT token to any protected endpoint
2. Verify:
   - Proper error response (401 Unauthorized)
   - User is redirected to login

## Expected Results

All test cases should pass with the following outcomes:
- User registration and login work seamlessly
- JWT tokens are validated consistently between frontend and backend
- User data isolation is maintained across all operations
- Proper error handling for all failure scenarios
- Secure token storage and transmission
- Compatibility with Better Auth client expectations