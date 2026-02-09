# Implementation Plan: Backend Database Schema Fix

**Branch**: `016-backend-db-fix` | **Date**: 2026-02-02 | **Spec**: [../specs/016-backend-db-fix/spec.md](../specs/016-backend-db-fix/spec.md)
**Input**: Feature specification from `/specs/016-backend-db-fix/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of backend database schema fix to resolve the critical issue where the FastAPI backend is trying to access priority and category columns in the todotask table that don't exist in the current database. The approach includes: 1) creating proper database migration to add missing columns, 2) handling existing records with default values, 3) ensuring all API endpoints work correctly with the updated schema, and 4) maintaining backward compatibility with existing todo items.

## Technical Context

**Language/Version**: Python 3.13+ for backend, TypeScript 5.0+ for frontend
**Primary Dependencies**: FastAPI, SQLModel, Neon Serverless PostgreSQL, Next.js 16.1+
**Storage**: Neon Serverless PostgreSQL database with SQLModel ORM
**Testing**: pytest for backend, Jest for frontend
**Target Platform**: Web application (Next.js 16.1+)
**Project Type**: Web application with frontend and backend
**Performance Goals**: Database migration completes successfully without data loss in under 30 seconds, API endpoints return 200 OK responses without database errors 100% of the time
**Constraints**: Maintain backward compatibility with existing todo items, ensure data integrity during migration, follow clean architecture principles
**Scale/Scope**: Single-user todo application with priority and category features

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] Verify documentation-first approach using MCP servers and Context7
- [x] Confirm adherence to clean architecture principles
- [x] Validate tech stack compliance with specified technologies
- [x] Ensure TDD workflow will be followed
- [x] Confirm multi-user authentication & authorization requirements
- [x] Ensure `CLAUDE.md` files exist for each major component (`backend/`, `frontend/`) and adhere to context-specific guidelines

## Project Structure

### Documentation (this feature)

```text
specs/016-backend-db-fix/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── main.py
├── models/
│   └── todo.py
├── api/
│   └── tasks.py
├── core/
│   └── services/
│       └── todo_service.py
├── database/
│   ├── session.py
│   └── migrations.py
├── dependencies/
│   └── auth.py
└── schemas/
    └── todo.py

frontend/
├── app/
│   └── page.tsx
├── components/
│   ├── todo/
│   │   ├── TodoItem.tsx
│   │   ├── TodoForm.tsx
│   │   └── TodoList.tsx
│   └── ui/
│       ├── Button.tsx
│       └── Card.tsx
├── hooks/
│   └── useTodos.ts
├── lib/
│   └── api.ts
└── types/
    └── todo.ts

tests/
├── frontend/
│   ├── __tests__/
│   └── setup.ts
└── backend/
    ├── conftest.py
    └── test_todos.py
```

**Structure Decision**: Web application with separate frontend and backend components. Backend uses FastAPI with SQLModel ORM for database interactions. The structure supports the database migration and API fixes needed to resolve the schema mismatch issue.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [N/A] | [No violations identified] | [All constitution requirements met] |

## Architectural Decisions

### AD-001: Database Migration Approach
**Decision**: Use ALTER TABLE with ADD COLUMN to add priority and category columns to existing todotask table
**Context**: The database schema was missing columns that the application code was trying to access
**Option Considered**: Complete table recreation vs. ALTER TABLE approach
**Option Chosen**: ALTER TABLE with ADD COLUMN
**Consequences**: Minimal downtime, preserves existing data, maintains referential integrity

### AD-002: Default Value Strategy
**Decision**: Assign default values ('medium' for priority, 'personal' for category) to existing records
**Context**: Need to handle existing records that don't have priority/category values
**Option Considered**: NULL values vs. default values approach
**Option Chosen**: Default values approach
**Consequences**: Maintains data consistency, ensures all records have valid values, prevents NULL-related errors

### AD-003: API Response Format Consistency
**Decision**: Standardize API responses to use camelCase and wrapped format (`{"data": ...}`)
**Context**: Inconsistent response formats between different API implementations
**Option Considered**: Keep existing formats vs. standardize across all endpoints
**Option Chosen**: Standardize to camelCase with wrapped responses
**Consequences**: Consistent API contract, easier frontend integration, improved maintainability

### AD-004: Project Structure Cleanup
**Decision**: Remove duplicate nested backend directory structure
**Context**: Found duplicate `backend/backend` directory causing confusion and code duplication
**Option Considered**: Keep both structures vs. consolidate to single structure
**Option Chosen**: Consolidate to single canonical structure
**Consequences**: Cleaner architecture, eliminates confusion, reduces maintenance overhead

### AD-005: API Endpoint Compatibility
**Decision**: Align backend API endpoints with frontend expectations to fix 404 errors
**Context**: Frontend was calling `/api/todos/{id}/toggle` but backend had `/api/todos/{id}/complete`
**Option Considered**: Update frontend vs. update backend vs. support both endpoints
**Option Chosen**: Support both endpoints for maximum compatibility
**Consequences**: Maintains backward compatibility while supporting frontend requirements

## Implementation Architecture

### Database Layer
- **Models**: Updated `TodoTask` SQLModel with `priority` (VARCHAR(20), default='medium') and `category` (VARCHAR(50), default='personal') fields
- **Migration**: Database migration script using ALTER TABLE to add columns with default values
- **Validation**: Proper validation constraints for allowed priority values ('high', 'medium', 'low')

### API Layer
- **Endpoints**: All CRUD operations updated to handle new priority and category fields
- **Response Format**: Standardized to camelCase with wrapped responses (`{"data": ...}`)
- **ID Handling**: Integer IDs converted to strings for frontend compatibility

### Service Layer
- **Business Logic**: Updated service methods to properly handle new fields
- **Data Consistency**: Ensured all operations maintain data integrity across new fields
