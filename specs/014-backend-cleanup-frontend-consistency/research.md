# Research Summary: Backend Cleanup and Frontend Consistency

## Current Backend State Analysis

### Files from 008-backend-cleanup-rebuild Feature:
Based on the spec review and current backend files, the following files were created during the 008-backend-cleanup-rebuild feature:

- **Core Application**: `main.py`, `requirements.txt`, `pyproject.toml`
- **API Layer**: `api/tasks.py`, `api/todos.py`, `api/auth.py`, `api/user.py`, `api/better_auth.py`
- **Models**: `models/todo.py`, `models/user.py`, `models/auth_token.py`, `models/session.py`, `models/token.py`
- **Schemas**: `schemas/todo.py`, `schemas/user.py`, `schemas/auth.py`, `api_response.py`
- **Services**: `core/services/todo_service.py`, `core/services/user_service.py`
- **Database**: `database/session.py`, `database/init_db.py`
- **Security**: `core/security/jwt.py`, `core/security/hashing.py`, `core/security/session.py`, `security/jwt.py`
- **Dependencies**: `dependencies/auth.py`
- **Utilities**: `utils/format_utils.py`, `utils/id_converter.py` (from 013-backend-frontend-review)

### Additional Files from Later Features:
- From 013-backend-frontend-review: `utils/format_utils.py`, `utils/id_converter.py`, `schemas/api_response.py`
- Various auth-related files that may be unnecessary for single-user implementation

## Decision: Files to Remove for Cleanup
**Rationale**: Following the minimal approach to remove files that are unnecessary for basic todo CRUD operations without authentication.

**Files to Remove**:
- `api/auth.py` - Authentication endpoints not needed for single-user implementation
- `api/better_auth.py` - Better Auth integration not needed
- `api/user.py` - User management not needed for single-user implementation
- `better-auth-server.ts` - Better Auth server not needed
- `BETTER_AUTH_INTEGRATION.md` - Documentation for unused auth system
- `models/auth_token.py` - Auth tokens not needed
- `models/session.py` - Session management not needed
- `models/token.py` - Token models not needed
- `models/user.py` - User model not needed
- `schemas/auth.py` - Auth schemas not needed
- `schemas/user.py` - User schemas not needed
- `core/security/jwt.py` - JWT security not needed
- `core/security/session.py` - Session security not needed
- `security/jwt.py` - JWT security not needed
- `dependencies/auth.py` - Auth dependencies not needed
- `core/services/user_service.py` - User services not needed
- `core/middleware.py` - May contain auth middleware
- `core/errors.py` - If it contains auth-related errors
- `core/logging.py` - If it contains auth-related logging
- Various test files related to auth

**Files to Keep**:
- `api/tasks.py` - Core todo API endpoints
- `models/todo.py` - Todo model
- `schemas/todo.py` - Todo schemas
- `core/services/todo_service.py` - Todo services
- `database/session.py` - Database session management
- `main.py` - Main application
- `requirements.txt`, `pyproject.toml` - Dependencies
- Essential files for basic CRUD operations

## Decision: Frontend-Backend Communication Protocol
**Rationale**: Use existing API contracts with same data model as frontend. The API endpoints should be consistent with what the frontend expects.

**Confirmed Approach**:
- Backend API endpoints at `/api/todos` (as seen in previous integration work)
- Data model consistency between frontend and backend
- Response format alignment (wrapped responses, camelCase fields, string IDs)

## Decision: Database Schema Preservation
**Rationale**: Keep existing database schema and only clean up code around it to maintain data integrity and compatibility with the frontend.

**Confirmed Approach**:
- Maintain current Todo model structure
- Preserve existing database connection and session management
- Keep SQLModel ORM integration

## Decision: Authentication Approach
**Rationale**: Maintain current temporary single-user implementation without authentication as specified in clarifications.

**Confirmed Approach**:
- Remove all authentication-related code
- Keep single-user functionality
- Simplify API endpoints to not require authentication tokens