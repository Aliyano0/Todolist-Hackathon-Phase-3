# Feature Specification: Backend Database Schema Fix

**Feature Branch**: `016-backend-db-fix`
**Created**: 2026-02-02
**Status**: Draft
**Input**: User description: "Fix FastAPI backend database schema mismatch issues after adding priority and category features to NextJS todo app. The backend is trying to access priority and category columns in the todotask table that don't exist in the current database. Requires database migration and API fixes."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Fix Database Schema Mismatch (Priority: P1)

As a user of the todo application, I want the API to work correctly so that I can manage my tasks with priority and category features without encountering database errors.

**Why this priority**: This is the highest priority because the core functionality is broken - the API throws database errors when trying to access priority and category columns that don't exist in the current database table.

**Independent Test**: Can be fully tested by making API calls to list, create, update, and retrieve todo items and verifying that no database errors occur, delivering the core functionality of the enhanced todo app.

**Acceptance Scenarios**:

1. **Given** a user accesses the todo API endpoints, **When** they request todo data, **Then** the API should return data without "column does not exist" errors
2. **Given** a user creates or updates a todo item with priority and category, **When** the request is processed, **Then** the operation should complete successfully without database errors

---

### User Story 2 - Restore API Functionality (Priority: P2)

As a user, I want all todo API endpoints to work properly so that I can use all the enhanced features (priority, category, completion status) seamlessly.

**Why this priority**: Important to restore full functionality after the database fix to ensure all features work as expected.

**Independent Test**: Can be fully tested by exercising all API endpoints (GET, POST, PUT, PATCH) and verifying they return proper responses without errors.

**Acceptance Scenarios**:

1. **Given** a user makes API calls to todo endpoints, **When** they perform CRUD operations, **Then** all operations should complete successfully with proper responses
2. **Given** a user tries to filter or sort by priority/category, **When** they make API requests, **Then** the API should handle these operations properly

---

### User Story 3 - Maintain Data Consistency (Priority: P3)

As a system administrator, I want to ensure data consistency and proper migration so that existing todo data remains intact while new features are enabled.

**Why this priority**: Ensuring data integrity is important for long-term stability and user trust.

**Independent Test**: Can be fully tested by verifying that existing todo items are properly updated with default priority/category values and that no data is lost during the migration.

**Acceptance Scenarios**:

1. **Given** existing todo items in the database, **When** the migration is applied, **Then** all existing items should have valid priority and category values
2. **Given** the migration process, **When** it runs, **Then** no existing data should be lost or corrupted

---

### Edge Cases

- What happens when the database migration fails during execution?
- How does the system handle concurrent requests during migration?
- What happens when there are connectivity issues during the migration process?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST add priority and category columns to the todotask table in the database
- **FR-002**: System MUST provide proper database migration to update existing schema without data loss
- **FR-003**: System MUST handle existing records by assigning default priority ('medium') and category ('personal') values
- **FR-004**: System MUST ensure all API endpoints work correctly with the updated schema
- **FR-005**: System MUST maintain backward compatibility with existing todo items
- **FR-006**: System MUST provide error handling for database migration failures
- **FR-007**: System MUST validate priority values ('high', 'medium', 'low') and category values
- **FR-008**: System MUST run database migrations automatically on application startup

### Key Entities *(include if feature involves data)*

- **Todo Task**: Represents a todo item with properties including id, title, description, completion status, priority (high, medium, low), and category
- **Database Schema**: The structure of the todotask table including all required columns for the enhanced features

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: API endpoints return 200 OK responses without database errors 100% of the time
- **SC-002**: Database migration completes successfully without data loss in under 30 seconds
- **SC-003**: All existing todo items are updated with valid priority and category values
- **SC-004**: New todo items can be created with priority and category fields successfully
- **SC-005**: All API endpoints (GET, POST, PUT, PATCH, DELETE) function properly with the updated schema

## Implementation Summary

### Implemented Solutions

- **Database Migration Script**: Created `database/migrations.py` containing an `ALTER TABLE` statement to add `priority VARCHAR(20)` and `category VARCHAR(50)` columns with default values ('medium' and 'personal' respectively)
- **Model Updates**: Updated `models/todo.py` to include `priority` and `category` fields in the `TodoTask` SQLModel with proper validation and default values
- **API Consistency**: Updated `backend/api/tasks.py` to properly handle the new fields, including camelCase conversion and proper response formatting
- **Duplicate Directory Cleanup**: Removed duplicate nested `backend/backend` directory structure to eliminate code duplication and maintain clean architecture
- **Test Updates**: Updated `test-backend-apiendpoints/test_api_endpoints.py` to include priority and category fields in test requests to ensure API compatibility
- **API Endpoint Alignment**: Fixed 404 errors by aligning backend API endpoints with frontend expectations - added `/toggle` endpoint to match frontend API calls, plus maintained `/complete` for backward compatibility

### Files Modified

- `database/migrations.py` - Added migration script for priority and category columns
- `models/todo.py` - Updated TodoTask model with new fields and validation
- `backend/api/tasks.py` - Updated API endpoints to handle new fields and maintain consistency
- `test-backend-apiendpoints/test_api_endpoints.py` - Updated test suite to include new fields
- Removed `backend/backend/` directory (duplicate structure)

### Verification

- Database migration runs successfully without errors
- API endpoints work correctly with new priority and category fields
- Existing data maintains integrity with default values applied appropriately
- All CRUD operations function properly with the enhanced schema
- Duplicate directory structure eliminated, maintaining clean project architecture
