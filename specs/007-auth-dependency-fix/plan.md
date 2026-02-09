# Implementation Plan: Auth Dependency Fix

**Branch**: `007-auth-dependency-fix` | **Date**: 2026-01-28 | **Spec**: [link to spec.md](specs/007-auth-dependency-fix/spec.md)
**Input**: Feature specification from `/specs/007-auth-dependency-fix/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Fix the authentication system dependency issues by implementing the missing verify_user_owns_resource function in dependencies/auth.py and updating todos.py to work with the new User object interface instead of the old dictionary interface. This resolves the ImportError and interface mismatch that prevents the application from starting.

## Technical Context

**Language/Version**: Python 3.13+ (backend), TypeScript 5.0+ (frontend)
**Primary Dependencies**: FastAPI, SQLModel, python-jose[cryptography], Better Auth, Neon Serverless PostgreSQL
**Storage**: Neon Serverless PostgreSQL database (postgres version 17) with SQLModel ORM
**Testing**: pytest (backend), Jest/React Testing Library (frontend)
**Target Platform**: Web application (Linux server backend, cross-platform frontend)
**Project Type**: Full-stack web application with separate frontend and backend
**Performance Goals**: Application starts without ImportError exceptions, authentication flows complete within 3 seconds
**Constraints**: Must maintain backward compatibility or proper migration path for auth interface changes
**Scale/Scope**: Single application instance supporting multiple users with proper authentication and authorization

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
specs/007-auth-dependency-fix/
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
├── main.py                  # FastAPI app entry point
├── models/                  # SQLModel database models
│   └── user.py              # User model for authentication
├── api/                     # API routes
│   ├── auth.py              # Authentication routes
│   └── todos.py             # Todo CRUD routes
├── core/                    # Core business logic
├── database/                # Database configuration
│   └── session.py           # Database session management
├── dependencies/            # FastAPI dependencies
│   └── auth.py              # Current user dependency with verify_user_owns_resource
├── schemas/                 # Pydantic schemas
│   └── user.py              # User request/response schemas
└── tests/                   # Backend tests

frontend/
├── app/                     # Next.js App Router pages
│   ├── layout.tsx
│   ├── page.tsx             # Home/Dashboard page
│   ├── (auth)/
│   │   ├── login/page.tsx   # Login page
│   │   └── register/page.tsx # Registration page
│   └── dashboard/page.tsx   # Protected dashboard
├── components/              # React components
├── lib/                     # Utility functions
│   └── api.ts               # API client utilities
├── providers/               # Context providers
│   └── AuthProvider.tsx     # Authentication context
└── tests/                   # Frontend tests
```

**Structure Decision**: Web application with separate backend and frontend directories as specified in the feature requirements. Backend uses FastAPI with SQLModel and Neon PostgreSQL, frontend uses Next.js 16+ with Better Auth integration. The fix focuses on updating backend/dependencies/auth.py and backend/api/todos.py to resolve the interface mismatch.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
