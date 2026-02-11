# Implementation Plan: Phase III - AI Chatbot Integration

**Branch**: `021-ai-chatbot` | **Date**: 2026-02-10 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/021-ai-chatbot/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Integrate an AI-powered conversational chatbot into the existing Todo web app (Phase 2 with 018-better-auth-jwt, 019-production-deployment, 020-frontend-ui-upgrade), enabling verified users to manage tasks (add, list, complete, delete, update) through natural language in English, Roman Urdu, or Urdu. The system uses a stateless agent architecture with database-backed conversation persistence, MCP tools for task operations, OpenAI Agents SDK for intent recognition, and OpenRouter API (gpt-4o-mini) for LLM inference. All chatbot access requires email verification (extending existing Better Auth JWT system), and multi-user isolation is enforced at all layers (database, MCP tools, API endpoints).

**Note**: Authentication system with JWT tokens (018), SMTP email service (019), and production infrastructure (019) are already implemented. Phase 3 adds email verification flow and chat infrastructure.

## Technical Context

**Language/Version**: Python 3.13+ (backend/MCP server), TypeScript 5.0+ (frontend)
**Primary Dependencies**: FastAPI, SQLModel, asyncpg==0.30.0, OpenAI Agents SDK, Official MCP SDK, OpenRouter API (gpt-4o-mini), OpenAI ChatKit, Next.js 16.1+, Better Auth, Shadcn UI
**Storage**: Neon Serverless PostgreSQL (postgres 17) with asyncpg driver and SQLModel ORM
**Testing**: pytest (backend/MCP), Jest + React Testing Library (frontend), end-to-end tests for natural language flows
**Target Platform**: Hugging Face Spaces (backend), Vercel (frontend), Linux server environment
**Project Type**: Web application (backend + frontend + mcp-server)
**Performance Goals**: <3s task creation via chat, <2s simple queries (list tasks), <5s complex operations, 95%+ intent recognition accuracy, 90%+ language detection accuracy
**Constraints**: Stateless architecture (no server-side state), email verification mandatory for chat access, 10 messages/minute rate limit per user, last 20 messages conversation history, UUIDs for all primary keys
**Scale/Scope**: 50 concurrent users initially, 5 MCP tools, 3 languages (English, Roman Urdu, Urdu), 7 user stories (P1-P7), 92 tasks total (4 email verification extension + 88 new Phase 3 features)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] Verify documentation-first approach using MCP servers and Context7 - Will use context7 for OpenAI Agents SDK, MCP SDK, OpenRouter API, and ChatKit documentation
- [x] Confirm adherence to clean architecture principles - Stateless agent architecture, MCP tools as ports, database isolation at all layers
- [x] Validate tech stack compliance with specified technologies - Python 3.13+, FastAPI, SQLModel, asyncpg==0.30.0, Next.js 16.1+, Better Auth, OpenAI Agents SDK, MCP SDK, ChatKit
- [x] Ensure TDD workflow will be followed - Red-Green-Refactor for all MCP tools, agent logic, and frontend components; E2E tests for natural language flows
- [x] Confirm multi-user authentication & authorization requirements - JWT with email_verified enforcement, user_id in all MCP tools, path validation, 403 for unverified users
- [x] Ensure `CLAUDE.md` files exist for each major component - Will create/update `backend/CLAUDE.md`, `frontend/CLAUDE.md`, `mcp-server/CLAUDE.md` with context-specific instructions

## Project Structure

### Documentation (this feature)

```text
specs/021-ai-chatbot/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   ├── chat-endpoint.yaml       # OpenAPI spec for POST /api/{user_id}/chat
│   ├── mcp-tools.yaml           # MCP tool definitions (5 tools)
│   └── database-schema.sql      # Conversation and Message table schemas
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── CLAUDE.md                    # Backend-specific context and guidelines
├── main.py                      # FastAPI app entry point
├── models/
│   ├── todo.py                  # Existing Task model (Phase 2)
│   ├── user.py                  # Existing User model with email_verified (Phase 2)
│   ├── conversation.py          # NEW: Conversation model (Phase 3)
│   └── message.py               # NEW: Message model (Phase 3)
├── api/
│   ├── auth.py                  # Existing auth routes (Phase 2)
│   ├── todos.py                 # Existing todo CRUD routes (Phase 2)
│   └── chat.py                  # NEW: Chat endpoint POST /api/{user_id}/chat (Phase 3)
├── core/
│   ├── services/
│   │   ├── todo_service.py      # Existing todo business logic (Phase 2)
│   │   └── chat_service.py      # NEW: Chat orchestration logic (Phase 3)
│   └── security/
│       └── jwt.py               # Existing JWT utilities (Phase 2)
├── database/
│   └── session.py               # Existing database session management (Phase 2)
├── dependencies/
│   └── auth.py                  # Existing current user dependency (Phase 2)
├── schemas/
│   ├── todo.py                  # Existing todo schemas (Phase 2)
│   ├── user.py                  # Existing user schemas (Phase 2)
│   └── chat.py                  # NEW: Chat request/response schemas (Phase 3)
├── mcp_server/                  # NEW: MCP server package (Phase 3) - runs in-process
│   ├── __init__.py
│   ├── server.py                # MCP server entry point
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── add_task.py          # Add task tool
│   │   ├── list_tasks.py        # List tasks tool
│   │   ├── complete_task.py     # Complete task tool
│   │   ├── delete_task.py       # Delete task tool
│   │   └── update_task.py       # Update task tool
│   └── tests/
│       ├── test_add_task.py
│       ├── test_list_tasks.py
│       ├── test_complete_task.py
│       ├── test_delete_task.py
│       └── test_update_task.py
└── tests/
    ├── test_chat_endpoint.py    # NEW: Chat endpoint tests (Phase 3)
    └── test_chat_service.py     # NEW: Chat service tests (Phase 3)

frontend/
├── CLAUDE.md                    # Frontend-specific context and guidelines
├── package.json                 # Dependencies and scripts
├── next.config.ts               # Next.js configuration
├── tsconfig.json                # TypeScript configuration
├── app/
│   ├── layout.tsx               # Existing root layout (Phase 2)
│   ├── page.tsx                 # Existing home page (Phase 2)
│   ├── login/page.tsx           # Existing login page (Phase 2)
│   ├── register/page.tsx        # Existing registration page (Phase 2)
│   ├── todos/page.tsx           # Existing todo dashboard (Phase 2)
│   ├── profile/page.tsx         # Existing profile page (Phase 2)
│   ├── forgot-password/page.tsx # Existing forgot password (Phase 2)
│   ├── reset-password/page.tsx  # Existing reset password (Phase 2)
│   └── chat/page.tsx            # NEW: Chat interface page (Phase 3)
├── components/
│   ├── todo/                    # Existing todo components (Phase 2)
│   │   ├── TodoForm.tsx
│   │   ├── TodoList.tsx
│   │   ├── TodoItem.tsx
│   │   ├── TodoActions.tsx
│   │   ├── CategorySelector.tsx
│   │   ├── PrioritySelector.tsx
│   │   └── CategoryManager.tsx
│   ├── navigation/              # Existing navigation (Phase 2)
│   │   └── Navbar.tsx
│   ├── dashboard/               # Existing dashboard components (Phase 2)
│   │   ├── TaskCard.tsx
│   │   ├── TaskForm.tsx
│   │   ├── TaskList.tsx
│   │   ├── CategoryTag.tsx
│   │   └── PriorityBadge.tsx
│   ├── auth/                    # Existing auth components (Phase 2)
│   │   ├── LoginForm.tsx
│   │   ├── RegisterForm.tsx
│   │   ├── ProtectedRoute.tsx
│   │   └── PasswordStrength.tsx
│   ├── chat/                    # NEW: Chat components (Phase 3)
│   │   ├── ChatInterface.tsx    # Chat UI using ChatKit
│   │   ├── ConversationList.tsx # Conversation list
│   │   └── EmailVerificationPrompt.tsx # Email verification prompt
│   ├── animations/              # Existing animation components (Phase 2)
│   ├── homepage/                # Existing homepage components (Phase 2)
│   ├── layout/                  # Existing layout components (Phase 2)
│   ├── theme/                   # Existing theme components (Phase 2)
│   └── ui/                      # Existing Shadcn UI components (Phase 2)
├── lib/
│   ├── api.ts                   # Existing API client utilities (Phase 2)
│   ├── auth.ts                  # Existing auth utilities (Phase 2)
│   ├── validation.ts            # Existing validation utilities (Phase 2)
│   ├── storage.ts               # Existing storage utilities (Phase 2)
│   ├── utils.ts                 # Existing utility functions (Phase 2)
│   ├── animations.ts            # Existing animation utilities (Phase 2)
│   ├── design-tokens.ts         # Existing design tokens (Phase 2)
│   └── chatApi.ts               # NEW: Chat API client (Phase 3)
├── hooks/
│   ├── useTodos.ts              # Existing todo hook (Phase 2)
│   ├── useReducedMotion.ts      # Existing animation hook (Phase 2)
│   └── useChat.ts               # NEW: Chat hook (Phase 3) - optional
├── providers/
│   └── AuthProvider.tsx         # Existing authentication context (Phase 2)
├── contexts/                    # Existing React contexts (Phase 2)
├── types/                       # Existing TypeScript types (Phase 2)
└── tests/
    ├── ChatInterface.test.tsx   # NEW: Chat interface tests (Phase 3)
    └── chat-e2e.test.tsx        # NEW: E2E natural language flow tests (Phase 3)
```

**Vercel Deployment Configuration**:
- **Root Directory**: `frontend` (selected in Vercel dashboard)
- **Build Command**: `npm run build` (default)
- **Output Directory**: `.next` (default)
- **Install Command**: `npm install` (default)
- **Framework Preset**: Next.js (auto-detected)

**Environment Variables for Vercel**:
```bash
NEXT_PUBLIC_API_URL=https://your-backend.hf.space
BETTER_AUTH_SECRET=your-secret-key-here
BETTER_AUTH_URL=https://your-frontend.vercel.app
```

**Structure Decision**: Web application structure with backend (FastAPI with embedded mcp_server package) and frontend (Next.js). The backend and frontend directories already exist from Phase 2. Phase 3 adds the mcp_server package inside backend/ (since only backend/ is deployed to Hugging Face Spaces) and extends frontend with chat-related modules in `components/chat/` subdirectory. This structure maintains clean separation between API layer (backend), tool layer (backend/mcp_server), and presentation layer (frontend), following clean architecture principles and the existing component organization pattern.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations detected. All design decisions comply with constitution principles:
- ✅ Documentation-first approach using MCP servers and Context7
- ✅ Clean architecture with stateless agent and MCP tools as ports
- ✅ Tech stack compliance (Python 3.13+, FastAPI, SQLModel, asyncpg, Next.js 16.1+, Better Auth)
- ✅ TDD workflow planned for all components
- ✅ Multi-user authentication with JWT and email verification enforcement
- ✅ Component-specific CLAUDE.md files planned for backend, mcp-server, and frontend

## Post-Design Constitution Re-Check

*Re-evaluated after Phase 1 design completion*

- [x] Documentation-first approach verified - Used context7 to research OpenRouter API, OpenAI Agents SDK, MCP SDK, SQLModel, asyncpg, and ChatKit
- [x] Clean architecture maintained - Stateless agent architecture, MCP tools as ports, database isolation at all layers, no business logic in UI
- [x] Tech stack compliance confirmed - All specified technologies researched and integrated: Python 3.13+, FastAPI, SQLModel, asyncpg==0.30.0, OpenAI Agents SDK, MCP SDK, OpenRouter API, ChatKit, Next.js 16.1+, Better Auth
- [x] TDD workflow defined - Red-Green-Refactor cycle documented in quickstart.md with clear implementation order
- [x] Multi-user authentication & authorization designed - JWT with email_verified claim, user_id in all MCP tools, path validation, 403 for unverified users, data isolation at database level
- [x] Component-specific CLAUDE.md files planned - Will create/update backend/CLAUDE.md, mcp-server/CLAUDE.md, frontend/CLAUDE.md with context-specific instructions

**Design Quality Assessment**: All design artifacts (data-model.md, contracts, quickstart.md) follow constitution principles. No violations or compromises detected.

## Planning Phase Complete

**Artifacts Generated**:
1. ✅ research.md - Technology decisions and architectural patterns
2. ✅ data-model.md - Database schema for Conversation and Message models
3. ✅ contracts/chat-endpoint.yaml - OpenAPI specification for chat endpoint
4. ✅ contracts/mcp-tools.md - MCP tool contracts and specifications
5. ✅ quickstart.md - Developer setup and implementation guide
6. ✅ Agent context updated - CLAUDE.md updated with Phase 3 technologies

**Next Command**: `/sp.tasks` - Generate actionable, dependency-ordered tasks.md for implementation
