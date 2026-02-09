# Research: Auth Dependency Fix

## Overview
This research document captures the investigation and decision-making process for fixing the authentication system dependency issues in the backend. The primary issue is an ImportError caused by a missing `verify_user_owns_resource` function in the auth dependencies, and an interface mismatch where `get_current_user` now returns a User object instead of a dictionary.

## Issue Analysis

### Missing Function Issue
The `todos.py` API file is trying to import `verify_user_owns_resource` from `dependencies.auth`, but this function doesn't exist in the current auth dependency file. This occurred during an authentication system overhaul where the function was removed but the todos API still depends on it.

**Decision**: Implement the `verify_user_owns_resource` function in `dependencies/auth.py` as a dependency function that validates user_id in JWT matches path parameter and returns the current user.

**Rationale**: This maintains the expected interface that `todos.py` depends on while ensuring proper user ownership validation.

### Interface Mismatch Issue
The old `get_current_user` function returned a dictionary with "user_id" key, but the new implementation returns a User object. This breaks all user ID verification logic in `todos.py` at lines 25, 60, 83, 114, 159, and 190.

**Decision**: Update `todos.py` to access User object properties directly (e.g., user.id, user.email) instead of dictionary keys.

**Rationale**: This maintains consistency with the new authentication interface while preserving the security functionality of verifying user ownership of resources.

## Technology Research

### FastAPI Dependencies
FastAPI dependency injection system allows for functions that can be used with the `Depends()` decorator to provide shared functionality across endpoints.

**Decision**: Use FastAPI dependency system to implement `verify_user_owns_resource` function that can be injected into routes that need user ownership validation.

**Rationale**: This follows FastAPI best practices and provides a clean, reusable way to implement authorization checks.

### User Object Properties
The User object returned by `get_current_user` contains properties that can be accessed directly (e.g., user.id, user.email) instead of dictionary access (e.g., user["user_id"]).

**Decision**: Access User object properties directly in `todos.py` instead of treating it as a dictionary.

**Rationale**: This matches the new interface and follows proper object-oriented access patterns.

## Architecture Considerations

### Clean Architecture Compliance
The fix maintains separation of concerns by keeping authentication logic in the dependencies layer and authorization checks in the API layer.

**Decision**: Keep the `verify_user_owns_resource` function in the dependencies module while using it in the API routes.

**Rationale**: This preserves the clean architecture boundaries and ensures that authentication/authorization concerns are properly separated.

### Error Handling
When user ownership validation fails, appropriate HTTP error responses (403 Forbidden) should be returned to maintain security.

**Decision**: Implement proper error handling in the `verify_user_owns_resource` function to return 403 Forbidden when validation fails.

**Rationale**: This maintains security by preventing unauthorized access and provides clear feedback to clients about access denial.

## Implementation Approach

### Phase 1: Dependency Fix
1. Add `verify_user_owns_resource` function to `backend/dependencies/auth.py`
2. Ensure the function validates that the current user owns the resource being accessed
3. Verify the function properly returns the current user for authorized access

### Phase 2: Interface Update
1. Update `backend/api/todos.py` to access User object properties directly
2. Replace dictionary-style access patterns with object property access
3. Maintain all existing authorization logic while adapting to the new interface

### Phase 3: Testing and Validation
1. Test that the application starts without ImportError exceptions
2. Verify all todo operations properly validate user ownership
3. Confirm authentication interface is consistent across all dependent modules

## Dependencies and Tools

### Backend Dependencies
- FastAPI: Web framework with dependency injection capabilities
- SQLModel: ORM for database interactions
- python-jose[cryptography]: JWT handling
- Better Auth: Authentication management
- psycopg2-binary: PostgreSQL adapter

## Expected Outcomes
- Application starts successfully without ImportError exceptions
- All todo operations properly verify user ownership and prevent cross-user access
- Authentication interface is consistent across all dependent modules
- All API routes properly handle the new User object interface without errors