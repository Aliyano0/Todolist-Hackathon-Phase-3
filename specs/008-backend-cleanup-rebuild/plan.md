# Implementation Plan: Backend Cleanup and Rebuild (Phase 2a)

**Branch**: `008-backend-cleanup-rebuild` | **Date**: 2026-01-30 | **Spec**: [Backend Cleanup and Rebuild Spec](./spec.md)
**Input**: Feature specification from `/specs/008-backend-cleanup-rebuild/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a FastAPI backend with SQLModel ORM connected to Neon PostgreSQL database to provide a REST API for todo management. The backend will include 6 API endpoints for basic todo operations (list, create, get, update, delete, toggle completion) without authentication as a temporary single-user implementation. This phase also includes cleaning up existing Phase 2 code and setting up proper project structure with environment configuration.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: FastAPI, SQLModel, uvicorn, psycopg2-binary, python-jose[cryptography]
**Storage**: Neon Serverless PostgreSQL database with SQLModel ORM
**Testing**: pytest for backend API and database operations
**Target Platform**: Linux server environment with UV virtual environment
**Project Type**: web backend API service
**Performance Goals**: API endpoints respond within 1 second for all basic operations (GET, POST, PUT, DELETE, PATCH) when database is accessible
**Constraints**: Single-user temporary implementation without authentication; must follow clean architecture principles; use MCP servers and Context7 for documentation verification
**Scale/Scope**: Single user todo management system with basic CRUD operations

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] Verify documentation-first approach using MCP servers and Context7
- [x] Confirm adherence to clean architecture principles
- [x] Validate tech stack compliance with specified technologies
- [x] Ensure TDD workflow will be followed
- [x] Confirm multi-user authentication & authorization requirements (not applicable for this temporary single-user implementation)
- [x] Ensure `CLAUDE.md` files exist for each major component (`backend/`, `frontend/`) and adhere to context-specific guidelines

## Project Structure

### Documentation (this feature)

```text
specs/008-backend-cleanup-rebuild/
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
├── CLAUDE.md                    # Backend-specific Claude Code instructions
├── main.py                    # FastAPI app entry point
├── models/                    # SQLModel database models
│   └── todo.py                # Todo model definition
├── api/                       # API routes
│   └── tasks.py               # Task CRUD routes
├── core/                      # Core business logic (services, utils)
│   └── services/
│       └── todo_service.py    # Todo business logic
├── database/                  # Database configuration
│   └── session.py             # Database session management
├── schemas/                   # Pydantic schemas
│   └── todo.py                # Task request/response schemas
├── dependencies/              # FastAPI dependencies
├── tests/                     # Backend tests
├── .env.example              # Environment variables template
├── pyproject.toml            # Project dependencies
├── requirements.txt          # Python dependencies
└── todo_backend.db           # SQLite database file (if needed for dev)
```

**Structure Decision**: Backend API service structure selected with FastAPI, SQLModel ORM, and Neon PostgreSQL as specified in the feature requirements. This structure follows clean architecture principles with separation of concerns between models, API routes, business logic, database configuration, and schemas.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [N/A] | [No violations found] | [All constitution requirements met] |
