# Feature Specification: Auth Dependency Fix

**Feature Branch**: `007-auth-dependency-fix`
**Created**: 2026-01-28
**Status**: Draft
**Input**: User description: "Critical Issues Identified

1. Missing Function (verify_user_owns_resource)

- Location: backend/api/todos.py line 4
- Issue: The todos API is trying to import verify_user_owns_resource from dependencies.auth, but this function doesn't exist in the current auth dependency file
- Root Cause: During the authentication system overhaul, this function was removed but the todos API still depends on it

2. Interface Mismatch (User Object vs Dictionary)

- Location: backend/api/todos.py throughout the file
- Issue: The old get_current_user function returned a dictionary with \"user_id\" key, but the new implementation returns a User object
- Impact: All user ID verification logic in todos.py (lines 25, 60, 83, 114, 159, 190) is broken

3. Incomplete Updates

- The authentication system was updated successfully, but dependent modules weren't updated to match the new interface
- This created an inconsistent state where some modules use the new interface while others still expect the old one

Recommended Solution

To fix the ImportError, you need to add the missing function to the auth dependencies file. The function should verify that the current user owns the resource being accessed, typically by checking that the user_id in the JWT matches the user_id in the path parameter:

def verify_user_owns_resource(
    current_user: User = Depends(get_current_user)
):
    '''
    Verify that the current user owns the resource being accessed.
    This function is used as a dependency to ensure user_id in JWT matches the user_id in the path.
    '''
    # This will be used in the routes to verify the user_id matches the path parameter
    return current_user

Additionally, you'll need to update the todos.py file to work with the new User object interface instead of the old dictionary interface.

These inconsistencies occurred because the implementation updated the authentication system but didn't update all dependent modules to match the new interface, violating the principle of comprehensive testing and integration."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Application Startup Success (Priority: P1)

As a developer, I want the application to start successfully without ImportError exceptions so that I can access the todo application.

**Why this priority**: This is the foundational requirement that enables all other functionality. Without a successfully starting application, no other features can be used.

**Independent Test**: Can be fully tested by starting the FastAPI application and verifying it runs without import errors, delivering the core value of a functional system.

**Acceptance Scenarios**:

1. **Given** the application dependencies are properly configured, **When** the application starts, **Then** it initializes successfully without ImportError exceptions
2. **Given** the authentication system is properly integrated, **When** users access the application, **Then** they can perform todo operations without errors

---

### User Story 2 - Secure Todo Operations (Priority: P1)

As an authenticated user, I want to perform todo operations securely so that I can only access my own todos.

**Why this priority**: Security is paramount for user data protection. Users must only access their own data, preventing unauthorized access.

**Independent Test**: Can be tested by authenticating as a user, creating todos, and verifying that the user can only access their own todos, delivering the core value of data security.

**Acceptance Scenarios**:

1. **Given** user is authenticated, **When** user performs todo operations, **Then** operations succeed with proper user identification
2. **Given** user attempts to access another user's todos, **When** authorization is checked, **Then** access is properly denied

---

### User Story 3 - Consistent Authentication Interface (Priority: P2)

As a developer, I want consistent authentication interfaces across all modules so that I can maintain the codebase effectively.

**Why this priority**: Essential for maintainability and preventing future integration issues. Consistent interfaces reduce technical debt and improve reliability.

**Independent Test**: Can be tested by verifying that all modules use the same authentication interface, delivering the value of code consistency.

**Acceptance Scenarios**:

1. **Given** authentication system is updated, **When** dependent modules are accessed, **Then** they work with the new interface consistently

---

### Edge Cases

- What happens when the verify_user_owns_resource function is missing from auth dependencies?
- How does system handle interface mismatches between get_current_user return types?
- What occurs when dependent modules expect old dictionary interface but receive User object?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST include verify_user_owns_resource function in dependencies/auth.py module that validates user_id in JWT matches path parameter and returns the current user
- **FR-002**: System MUST update todos.py to work with User object interface by accessing User object properties directly (e.g., user.id, user.email) instead of dictionary keys
- **FR-003**: System MUST ensure proper user identification in JWT token verification
- **FR-004**: System MUST maintain backward compatibility or proper migration path for auth interface changes
- **FR-005**: System MUST handle user ID verification in API routes using new User object properties
- **FR-006**: System MUST prevent cross-user data access through proper authorization checks with appropriate HTTP error responses (403 Forbidden) when validation fails
- **FR-007**: System MUST start successfully without ImportError exceptions
- **FR-008**: System MUST include additional refactoring to improve the overall authentication architecture
- **FR-009**: System MUST verify all existing authentication flows continue to work properly after implementing the fix

### Key Entities *(include if feature involves data)*

- **User Object**: Represents authenticated user with properties for identification and authorization
- **Authentication Interface**: Defines the contract between auth system and dependent modules
- **Todo Resource**: User-specific data that requires proper ownership verification

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Application starts successfully without ImportError exceptions
- **SC-002**: All todo operations properly verify user ownership and prevent cross-user access
- **SC-003**: Authentication interface is consistent across all dependent modules
- **SC-004**: 100% of user-specific operations properly validate user identity
- **SC-005**: All API routes properly handle the new User object interface without errors

## Clarifications

### Session 2026-01-28

- Q: How should the verify_user_owns_resource function be implemented? → A: Implement as a dependency function that validates user_id in JWT matches path parameter and returns the current user
- Q: How should the interface mismatch be resolved? → A: Update todos.py to access User object properties directly (e.g., user.id, user.email) instead of dictionary keys
- Q: What should be the scope of changes? → A: Include additional refactoring to improve the overall authentication architecture
- Q: How should authentication flow validation be handled? → A: Verify all existing authentication flows continue to work properly after implementing the fix
- Q: How should error handling be approached for ownership validation? → A: Return appropriate HTTP error responses (403 Forbidden) when user ownership validation fails
