---
id: "014"
title: "Backend Cleanup Frontend Consistency Plan"
stage: "plan"
date_iso: "2026-02-02"
surface: "agent"
model: "Claude Sonnet 4.5"
feature: "backend-cleanup-frontend-consistency"
branch: "014-backend-cleanup-frontend-consistency"
user: "user"
command: "sp.plan"
labels: ["plan", "cleanup", "consistency", "todo", "crud"]
links:
  spec: "specs/014-backend-cleanup-frontend-consistency/spec.md"
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - specs/014-backend-cleanup-frontend-consistency/plan.md
  - specs/014-backend-cleanup-frontend-consistency/research.md
  - specs/014-backend-cleanup-frontend-consistency/data-model.md
  - specs/014-backend-cleanup-frontend-consistency/quickstart.md
  - specs/014-backend-cleanup-frontend-consistency/contracts/todo-api.yaml
tests_yaml: |
  - specs/014-backend-cleanup-frontend-consistency/plan.md validation
  - research summary creation
  - data model documentation
  - API contracts definition
  - quickstart guide creation
prompt_text: |

response_text: |
  Completed implementation plan for backend cleanup and frontend consistency. Created comprehensive documentation including:
  - Implementation plan outlining approach to clean up backend and ensure consistency with frontend
  - Research summary identifying files to remove from 008-backend-cleanup-rebuild feature
  - Data model documentation standardizing entity structures
  - API contracts defining standardized endpoints
  - Quickstart guide for setting up the cleaned up application

  Key findings include identification of unnecessary authentication-related files to remove while preserving core todo functionality. The plan ensures consistent communication between frontend and backend using existing API contracts with the same data model as the frontend, maintaining a temporary single-user implementation without authentication.
outcome: |
  Successfully created comprehensive implementation plan addressing backend cleanup and frontend consistency with research, data models, API contracts, and setup instructions.
evaluation: |
  The plan provides clear direction for removing unnecessary files while maintaining essential functionality and ensuring proper communication between frontend and backend.
---

# Implementation Plan: Backend Cleanup and Frontend Consistency

**Branch**: `014-backend-cleanup-frontend-consistency` | **Date**: 2026-02-02 | **Spec**: [link]
**Input**: Feature specification from `/specs/014-backend-cleanup-frontend-consistency/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Clean up unnecessary files from the backend codebase that were part of the 008-backend-cleanup-rebuild feature while preserving essential functionality for basic todo CRUD operations. Ensure consistent communication between frontend and backend using existing API contracts with the same data model as the frontend. Maintain a temporary single-user implementation without authentication.

## Technical Context

**Language/Version**: Python 3.13+ (backend), TypeScript 5.0+ (frontend)
**Primary Dependencies**: FastAPI, SQLModel, Next.js 16+, Shadcn UI, Tailwind CSS
**Storage**: Neon Serverless PostgreSQL database with SQLModel ORM
**Testing**: pytest (backend), Jest/React Testing Library (frontend)
**Target Platform**: Web application (Linux server for backend, browser for frontend)
**Project Type**: Full-stack web application
**Performance Goals**: Sub-second API response times, responsive UI with optimistic updates
**Constraints**: Single-user implementation (authentication temporarily disabled), consistent API contracts between frontend and backend
**Scale/Scope**: Individual user todo application with core CRUD functionality

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] Verify documentation-first approach using MCP servers and Context7
- [x] Confirm adherence to clean architecture principles
- [x] Validate tech stack compliance with specified technologies
- [x] Ensure TDD workflow will be followed
- [x] Confirm multi-user authentication & authorization requirements (temporarily disabled per clarifications)
- [x] Ensure `CLAUDE.md` files exist for each major component (`backend/`, `frontend/`) and adhere to context-specific guidelines

## Project Structure

### Documentation (this feature)

```text
specs/014-backend-cleanup-frontend-consistency/
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
├── main.py              # FastAPI app entry point
├── api/
│   ├── tasks.py         # Current API routes (todo-related endpoints only)
│   └── todos.py         # Alternative API routes
├── models/
│   └── todo.py          # SQLModel database models (todo only)
├── schemas/
│   └── todo.py          # Pydantic request/response schemas (todo only)
├── core/
│   └── services/
│       └── todo_service.py  # Todo business logic only
├── database/
│   └── session.py       # Database session management
├── tests/               # Backend tests
└── requirements.txt     # Python dependencies

frontend/
├── app/                 # Next.js App Router pages
│   ├── page.tsx         # Main dashboard
│   └── globals.css
├── components/          # React components
│   └── todo/
│       ├── TodoList.tsx
│       ├── TodoItem.tsx
│       └── TodoForm.tsx
├── lib/
│   └── api.ts           # API client for backend communication
├── hooks/
│   └── useTodos.ts      # Todo state management
└── tests/               # Frontend tests
```

**Structure Decision**: Full-stack web application with separate backend (FastAPI) and frontend (Next.js) components following clean architecture principles. Backend handles API and data persistence, frontend manages UI and user interactions. Unnecessary authentication-related files have been removed to maintain single-user implementation.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| API Contract Consistency | Backend uses /api/todos, frontend expects /api/todos | Critical for proper communication between frontend and backend |
| Data Model Alignment | Different field naming (snake_case vs camelCase), ID types (int vs string) | Would cause serialization/deserialization errors |
| Authentication Removal | Keeping auth code not needed for single-user implementation | Would add unnecessary complexity for current requirements |