---
id: 0001
title: todo-backend-api-spec
stage: spec
date: 2026-01-16
surface: agent
model: claude-sonnet-4-5-20250929
feature: 002a-todo-backend-api
branch: 002a-todo-backend-api
user: claude
command: sp.specify
labels: ["spec", "todo", "backend", "api", "fastapi"]
links:
  spec: specs/002a-todo-backend-api/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002a-todo-backend-api/spec.md
  - specs/002a-todo-backend-api/checklists/requirements.md
tests: []
---

## Prompt

For Phase 2a (backend only), develop the FastAPI backend in the /backend directory for the multi-user Todo web app with persistent storage. Work exclusively in /backend.

First, ensure the folder structure is set up correctly in /backend, install required technologies using 'uv add' for any Python package installations (including fastapi, sqlmodel, uvicorn, python-jose[cryptography] for JWT, etc.), then confirm the working directory is /backend before proceeding.

Set up UV venv Python FastAPI backend with SQLModel ORM connected to Neon Serverless PostgreSQL database. Implement all 5 Basic Level features through RESTful API endpoints.

Create the following RESTful API endpoints (all under /api):

- GET /{user_id}/tasks → List all tasks for the authenticated user
- POST /{user_id}/tasks → Create a new task for the authenticated user
- GET /{user_id}/tasks/{id} → Get details of a specific task
- PUT /{user_id}/tasks/{id} → Update a task
- DELETE /{user_id}/tasks/{id} → Delete a task
- PATCH /{user_id}/tasks/{id}/complete → Toggle task completion

Secure the API with JWT verification (since Better Auth on frontend issues JWT tokens on email signup/signin): Add FastAPI middleware to extract and verify JWT from Authorization: Bearer header using the shared secret, decode to get user_id/email, validate it matches the {user_id} in the URL path, and filter all database queries by the authenticated user's ID for strict multi-user data isolation.

User signup/signin is handled by Better Auth on the frontend with email authentication (third-party providers to be added later); backend only verifies JWT for API requests and does not implement signup/signin routes. Ensure tasks are stored and retrieved per authenticated user via SQLModel models.

## Response snapshot

Successfully created the feature specification for the Todo Backend API. Created feature branch 001-todo-backend-api and comprehensive spec file at specs/001-todo-backend-api/spec.md with user stories, functional requirements, key entities, and success criteria. Also created a quality checklist to validate the specification.

The specification includes:
- User stories for creating, viewing, and managing todo tasks
- Functional requirements for the API endpoints
- Key entities (Task and User)
- Success criteria with measurable outcomes
- Edge cases consideration

The spec is complete and ready for the next phase (/sp.clarify or /sp.plan). The specification focuses on the user needs and business value while avoiding implementation details, making it suitable for stakeholders to understand the feature requirements.

## Outcome

- ✅ Impact: Successfully created comprehensive feature specification for Todo Backend API with all required sections
- 🧪 Tests: No tests created yet (spec phase)
- 📁 Files: Created spec file and quality checklist in the feature directory
- 🔁 Next prompts: Ready for /sp.clarify or /sp.plan to continue development
- 🧠 Reflection: Specification follows proper format and covers all necessary requirements from user input

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin implementation planning
