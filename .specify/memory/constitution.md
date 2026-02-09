<!--
Sync Impact Report
==================
Version change: 2.4.0 → 2.5.0 (minor update - Phase 3 AI Chatbot integration)
Modified principles:
  - Updated title to reflect Phase 3 scope
  - Added Principle XI: AI Conversational Interface
  - Updated tech stack to include OpenAI Agents SDK, MCP SDK, ChatKit
  - Expanded project structure to include MCP server and chat components
  - Updated goals and success criteria for conversational interface
Added sections:
  - AI Chatbot architecture and requirements
  - MCP server implementation guidelines
  - Conversation state management
Templates requiring updates:
  - ✅ spec-template.md (should include AI chatbot feature sections)
  - ✅ plan-template.md (should include MCP server and AI agent design)
  - ✅ tasks-template.md (should include AI/NLP task categories)
Follow-up TODOs: None (all placeholders filled)
-->

# The Evolution of Todo - Phase III: AI Chatbot Integration Constitution

## Core Principles

### I. Product Architect Mindset

Every contributor operates as a Product Architect, not a code implementer. This means:
- All decisions must be justified by explicit product value or future evolution benefit
- Technical choices must consider Phase III and beyond implications
- Architecture diagrams and decision rationale must be documented
- Questions are welcomed; assumptions must be surfaced and challenged

**Rationale**: "The Evolution of Todo" is an intentional multi-phase evolution project. Every
Phase III decision shapes the migration path forward. Treating contributors as architects
ensures decisions are reversible, traceable, and evolution-aware.

### II. Clean Architecture Mandatory

The application MUST follow clean architecture principles:
- Domain logic is isolated from I/O and presentation concerns
- Core entities and use cases reside in shared modules with minimal external dependencies
- Ports (interfaces) define all external interactions; adapters implement them
- Dependencies point inward; no layer may import from an outer layer

**Rationale**: Phase III introduces AI agents, MCP servers, and conversational interfaces. Clean
architecture ensures each evolution remains modular and maintainable as complexity increases.

### III. Simplicity First (Non-Negotiable)

Complexity must be justified before being introduced. For every feature or abstraction:
- Ask: "What specific problem does this solve today?"
- If no immediate problem: do not introduce
- Prefer the simplest implementation that satisfies current requirements
- Defer decisions to the last responsible moment

**Rationale**: This is an evolution project. Over-engineering Phase III creates debt for
future phases. The YAGNI principle ("You Aren't Gonna Need It") applies aggressively.

### IV. Five Core Features with Conversational Interface

Phase III MUST implement the five core features through both web UI and conversational interface:
1. **Add**: Create a new todo item via web interface OR natural language ("Add task: buy groceries")
2. **View**: List all todos via web interface OR natural language ("Show my tasks")
3. **Update**: Modify todo via web interface OR natural language ("Update task 1 to high priority")
4. **Delete**: Remove todo via web interface OR natural language ("Delete completed tasks")
5. **Mark Complete**: Toggle completion via web interface OR natural language ("Mark task 2 as done")

**Rationale**: Phase III extends Phase II capabilities with conversational access. Both interfaces
must coexist and provide equivalent functionality. The conversational interface provides natural
language accessibility while maintaining the web UI for visual task management.

### V. Persistent Storage Mandate

Phase III MUST implement persistent storage for both tasks and conversations:
- Use Neon Serverless PostgreSQL database (postgres version 17) for data storage
- Use SQLModel ORM with asyncpg driver for database interactions
- Data persists beyond user sessions
- Database schema supports multi-user data isolation
- Conversation history and message state stored in database (Conversation and Message models)

**Rationale**: Persistence is critical for both task data and conversation context. Storing
conversation history enables context-aware responses and allows users to resume conversations
after restart. The persistence mandate forces proper data modeling for both domains.

### VI. Modern Tech Stack Compliance

Phase III MUST use the specified technology stack:
- Backend: FastAPI with Python 3.13+ in UV venv environment
- Frontend: Next.js 16.1 with App Router, Shadcn UI, and tailwindcss
- Database: Neon Serverless PostgreSQL with SQLModel ORM and asyncpg driver
- Authentication: Better Auth with JWT token integration
- AI Agent: OpenAI Agents SDK for conversational logic
- MCP Server: Official MCP SDK for tool exposure
- Chat UI: OpenAI ChatKit for Next.js chat interface
- Package management: UV for Python dependencies (use 'uv add' for installations)

**Rationale**: The specified tech stack ensures compatibility, scalability, and modern
development practices. OpenAI Agents SDK provides robust intent recognition and tool
orchestration. MCP SDK enables standardized tool exposure for AI agents.

### VII. Documentation-First Approach with MCP Servers

Phase III development MUST prioritize documentation from official sources using MCP servers and Context7:
- Use context7 MCP server to retrieve up-to-date documentation and code examples for any library
- Use nextjs mcp server for Next.js-specific documentation and tooling
- Prioritize official documentation over internal knowledge or assumptions
- Follow authoritative documentation for API usage, configuration, and best practices

**Rationale**: Using official, up-to-date documentation ensures that development follows
current best practices and avoids deprecated patterns. MCP servers provide verified,
curated information that reduces risk of implementing outdated approaches.

### VIII. Context-Specific Documentation with CLAUDE.md

Each major component (e.g., `backend/`, `frontend/`, `mcp-server/`) MUST contain its own `CLAUDE.md` file for context-specific instructions, guidelines, and tool usage. The root `CLAUDE.md` file SHOULD contain global instructions applicable to the entire project and refer to component-specific `CLAUDE.md` files for detailed context.

**Rationale**: As the project evolves into a full-stack application with AI capabilities, maintaining
a single, monolithic `CLAUDE.md` becomes unwieldy. Dedicated `CLAUDE.md` files improve clarity,
reduce cognitive load for developers working on specific parts of the codebase, and ensure that
context is always co-located with the code it describes.

### IX. Multi-User Authentication & Authorization

Phase III MUST implement secure multi-user functionality using Better Auth with JWT:

**Authentication Architecture:**
- Better Auth (Next.js) is the ONLY authentication authority
- Better Auth issues JWT tokens on user login
- FastAPI backend NEVER issues tokens, only verifies them
- Stateless authentication on backend (no token storage in database)
- JWT tokens valid for 7 days with HS256 signing algorithm
- Shared secret (BETTER_AUTH_SECRET) used by both frontend and backend

**Authentication Features:**
- User registration with email and password validation
- User login with credential verification
- JWT token issuance by Better Auth containing user_id (UUID), email, and expiration
- Automatic token attachment to all API requests (Authorization: Bearer header)
- User logout (client-side session clearing)
- Session persistence for 7-day token validity period

**Security Implementation:**
- Password hashing using industry-standard algorithms (bcrypt)
- Password requirements following industry standards (minimum length, complexity)
- JWT signature verification using shared secret
- Token expiry validation on every request
- Input sanitization and validation at all layers
- Proper error handling without exposing security details

**Authorization & Data Isolation:**
- All API routes (including chat endpoint) require valid JWT token
- User ID extracted from JWT token (sub claim) for authorization
- API routes use user ID in path (/api/{user_id}/tasks, /api/{user_id}/chat) validated against token
- User ID mismatch between token and path results in 403 Forbidden
- Missing or invalid token results in 401 Unauthorized
- Proper data isolation between users at database level
- All database queries filtered by authenticated user_id
- Cross-user data access always fails
- Conversation and message data isolated by user_id

**Frontend Integration:**
- Better Auth configuration with credentials provider and JWT plugin
- Protected routes redirect unauthenticated users to login page
- Login and registration pages with form validation
- Automatic JWT attachment to all API requests via client interceptor
- Clear error messages for authentication failures
- Responsive design for all screen sizes

**Database Schema:**
- User model with UUID primary key, unique email, and password hash
- Task model with UUID primary key and user_id foreign key
- Conversation model with UUID primary key and user_id foreign key
- Message model with UUID primary key and conversation_id foreign key
- Referential integrity between tasks/conversations and users
- Indexed fields for performance (email, user_id, conversation_id)

**Rationale**: Multi-user support with Better Auth provides a robust, industry-standard
authentication solution. The stateless JWT approach simplifies backend architecture while
maintaining security. Better Auth handles token issuance complexity, allowing the backend
to focus on verification and authorization. Proper data isolation prevents cross-user
data leakage and ensures security compliance for both task and conversation data.

### X. Test-Driven Development (Non-Negotiable)

Phase III MUST use TDD for all implementation:
- Write failing test first for every feature
- Test must fail for a clear, specific reason
- Implement minimal code to pass the test
- Refactor while tests remain green
- Red-Green-Refactor cycle strictly enforced
- End-to-end tests for natural language flows (e.g., "add task via chat", "list tasks via chat")

**Rationale**: TDD ensures design discipline, regression safety, and evolution
readiness. Tests from Phase III will validate future migrations. E2E tests for
conversational flows ensure intent recognition and tool execution work correctly.

### XI. AI Conversational Interface (Stateless Architecture)

Phase III MUST implement a conversational interface using OpenAI Agents SDK with stateless architecture:

**AI Agent Architecture:**
- Use OpenAI Agents SDK for intent recognition and tool orchestration
- Agent logic is stateless (no in-memory state between requests)
- All conversation context loaded from database on each request
- Intent-based tool triggers (e.g., "add task" intent → add_task tool)
- Confirmation prompts for destructive actions (e.g., delete, update)
- Proper error handling with user-friendly messages
- Support for Basic Level task management: add, list, complete, delete, update

**MCP Server Implementation:**
- Build MCP server using Official MCP SDK
- Expose stateless tools: add_task, list_tasks, complete_task, delete_task, update_task
- All tools MUST accept user_id UUID parameter for multi-user isolation
- All tools perform async database operations via SQLModel/asyncpg to Neon PostgreSQL
- Tools return structured responses (success/error with details)
- No shared state between tool invocations

**Chat Endpoint:**
- Stateless FastAPI endpoint: POST /api/{user_id}/chat
- Accept message payload with conversation_id (optional for new conversations)
- Validate user_id from JWT token matches path parameter
- Load conversation history from database if conversation_id provided
- Process message through OpenAI Agents SDK
- Execute tools via MCP server with user_id parameter
- Persist conversation and message to database
- Return agent response with tool execution results

**Conversation State Management:**
- Conversation model: UUID id, UUID user_id, timestamp created_at, timestamp updated_at
- Message model: UUID id, UUID conversation_id, string role (user/assistant/tool), string content, timestamp created_at
- All conversation data filtered by user_id for isolation
- Conversation history loaded from database on each request (stateless)
- Support for resuming conversations after restart

**Frontend Chat Interface:**
- Use OpenAI ChatKit UI components in Next.js
- Send messages with JWT token in Authorization header
- Display user messages, assistant responses, and tool execution results
- Handle conversation creation and resumption
- Show loading states during agent processing
- Display errors clearly to users

**Natural Language Capabilities:**
- Support natural language task management (e.g., "Add buy groceries to my list")
- Intent recognition for all five core features
- Context-aware responses using conversation history
- Confirmation for ambiguous or destructive actions
- Graceful handling of unrecognized intents

**Rationale**: The stateless architecture ensures scalability and simplifies deployment.
Storing conversation state in the database enables context-aware responses and allows
users to resume conversations after restart. OpenAI Agents SDK provides robust intent
recognition and tool orchestration. MCP SDK standardizes tool exposure for AI agents.
Multi-user isolation at the tool level ensures security and data privacy.

## Goals

### Primary Goal
Deliver a working, tested, clean-architecture multi-user web todo application with AI
conversational interface that implements all five core features through both web UI and
natural language, with persistent storage for tasks and conversations, serving as a solid
foundation for future evolution phases.

### Secondary Goals
- Establish AI agent patterns with stateless architecture
- Create comprehensive test coverage including e2e natural language flows
- Document architectural decisions for AI integration
- Demonstrate modern AI-powered web development practices
- Implement proper data isolation for both tasks and conversations
- Enable context-aware conversational experiences

### Non-Goals
- Advanced AI features beyond Basic Level task management
- Voice interface or speech recognition
- Multi-modal inputs (images, files) in chat
- Advanced NLP features (sentiment analysis, entity extraction)
- Real-time collaboration or notifications
- Admin panels or user management beyond basic auth
- Advanced search or filtering capabilities beyond natural language
- Export/import functionality
- Mobile app development (web app should be responsive)

## Success Criteria

### Functional Criteria
- All five features work correctly in both web UI and conversational interface
- User authentication (signup/signin) works seamlessly
- Data persists across sessions and user logins
- Conversation history persists and can be resumed after restart
- Error handling provides clear, actionable messages
- Multi-user data isolation prevents cross-user access for tasks and conversations
- Natural language intent recognition works for all five core features

### Architectural Criteria
- Core domain has minimal imports from outer layers (API, UI, Infrastructure, AI)
- All dependencies point inward toward the domain
- New features can be added without modifying domain code
- Tests can run independently of UI layer
- Proper separation between frontend, backend, and AI agent concerns
- Stateless AI agent architecture (no in-memory state)
- MCP server tools are stateless and accept user_id parameter

### Quality Criteria
- Unit test coverage for core domain entities and use cases (target 80%+)
- API endpoints properly validated and secured
- Type hints used throughout (Python and TypeScript)
- Proper error handling and validation for all inputs
- Security best practices implemented (JWT, input sanitization, etc.)
- End-to-end tests for natural language flows (e.g., "add task via chat")

### Evolution Criteria
- Domain code contains no references to "Phase III" or AI-specific constraints
- Additional AI features can be added without modifying core domain code
- Authentication system can be extended without changing domain logic
- Database schema can be evolved without breaking existing functionality
- Conversation state management can be extended for advanced features

## Project Structure

```
todolist-hackathon/
├── .specify/                    # Spec-Kit configuration
│   └── config.yaml
├── specs/                       # Spec-Kit managed specifications
│   ├── overview.md              # Project overview
│   ├── architecture.md          # System architecture
│   ├── features/                # Feature specifications
│   │   ├── task-crud.md
│   │   ├── authentication.md
│   │   └── chatbot.md
│   ├── api/                     # API specifications
│   │   ├── rest-endpoints.md
│   │   └── mcp-tools.md
│   ├── database/                # Database specifications
│   │   └── schema.md
│   ├── ui/                      # UI specifications
│   │   ├── components.md
│   │   └── pages.md
├── CLAUDE.md                    # Root Claude Code instructions
├── backend/
│   ├── CLAUDE.md
│   ├── main.py                  # FastAPI app entry point
│   ├── models/                  # SQLModel database models
│   │   ├── todo.py              # Todo model with user relationship
│   │   ├── conversation.py      # Conversation model
│   │   └── message.py           # Message model
│   ├── api/                     # API routes
│   │   ├── auth.py              # Authentication routes
│   │   ├── todos.py             # Todo CRUD routes
│   │   └── chat.py              # Chat endpoint (POST /api/{user_id}/chat)
│   ├── core/                    # Core business logic
│   │   ├── services/            # Service layer
│   │   │   ├── todo_service.py  # Todo business logic
│   │   │   └── chat_service.py  # Chat orchestration logic
│   │   └── security/            # Security utilities
│   │       └── jwt.py           # JWT utilities
│   ├── database/                # Database configuration
│   │   └── session.py           # Database session management
│   ├── dependencies/            # FastAPI dependencies
│   │   └── auth.py              # Current user dependency
│   ├── schemas/                 # Pydantic schemas
│   │   ├── todo.py              # Todo request/response schemas
│   │   ├── user.py              # User schemas
│   │   └── chat.py              # Chat request/response schemas
│   ├── tests/                   # Backend tests
│   └── requirements.txt         # Python dependencies
├── mcp-server/                  # MCP server for AI agent tools
│   ├── CLAUDE.md
│   ├── server.py                # MCP server entry point
│   ├── tools/                   # MCP tool implementations
│   │   ├── add_task.py          # Add task tool
│   │   ├── list_tasks.py        # List tasks tool
│   │   ├── complete_task.py     # Complete task tool
│   │   ├── delete_task.py       # Delete task tool
│   │   └── update_task.py       # Update task tool
│   ├── tests/                   # MCP server tests
│   └── requirements.txt         # Python dependencies
├── frontend/
│   ├── CLAUDE.md
│   ├── package.json
│   ├── next.config.js
│   ├── tsconfig.json
│   ├── app/                     # Next.js App Router pages
│   │   ├── layout.tsx
│   │   ├── page.tsx             # Home/Dashboard page
│   │   ├── login/page.tsx       # Login page
│   │   ├── register/page.tsx    # Registration page
│   │   ├── dashboard/page.tsx   # Todo dashboard
│   │   ├── chat/page.tsx        # Chat interface page
│   │   └── globals.css
│   ├── components/              # React components
│   │   ├── TodoForm.tsx         # Todo creation/update form
│   │   ├── TodoList.tsx         # Todo display component
│   │   ├── TodoItem.tsx         # Individual todo item
│   │   ├── Navbar.tsx           # Navigation component
│   │   └── ChatInterface.tsx    # Chat UI component (OpenAI ChatKit)
│   ├── lib/                     # Utility functions
│   │   └── api.ts               # API client utilities
│   ├── providers/               # Context providers
│   │   └── AuthProvider.tsx     # Authentication context
│   └── tests/                   # Frontend tests
├── docker-compose.yml
└── README.md
```

## Constraints

### Technical Constraints
- Use UV to initialize and manage the project with UV venv
- Python 3.13+ required for backend and MCP server
- Next.js 16+ with App Router for frontend
- Use Shadcn UI components and tailwindcss for styling
- Neon Serverless PostgreSQL for database with asyncpg driver
- Better Auth for authentication with JWT integration
- SQLModel ORM for database interactions with asyncpg compatibility
- OpenAI Agents SDK for AI agent logic
- Official MCP SDK for MCP server implementation
- OpenAI ChatKit for chat UI components
- Use 'uv add' for Python package installations
- Use context7 and nextjs mcp servers for documentation and code examples

### Process Constraints
- All features must follow TDD (Red-Green-Refactor)
- All architectural decisions must be documented as ADRs
- All changes must be traceable to a user story in spec.md
- Spec-Kit Plus workflow must be followed for all work
- API endpoints must be properly documented with OpenAPI
- Use official documentation accessed through MCP servers and Context7
- Component-specific `CLAUDE.md` files must be maintained for context
- End-to-end tests required for natural language flows

### Quality Constraints
- No TODO comments left in production code
- Maximum cyclomatic complexity: 10 per function
- Maximum function length: 50 lines
- All public APIs must have docstrings
- Type hints required for all function signatures
- Proper error handling for all user inputs
- Stateless architecture for AI agent and MCP server

## Additional Constraints

### Forbidden Patterns
- Direct database queries in UI components (use API endpoints)
- Hardcoded secrets or credentials in source code
- Sharing of data between authenticated users
- Storing sensitive data in client-side storage without encryption
- Bypassing authentication for protected routes (including chat endpoint)
- Hardcoded strings in domain logic (use constants or enums)
- Relying on outdated documentation or internal knowledge without verification
- Stateful AI agent logic (must load context from database)
- MCP tools without user_id parameter (breaks multi-user isolation)

### Required Patterns
- Explicit is better than implicit (PEP 20 and TypeScript best practices)
- Composition over inheritance
- Single responsibility per class/function/component
- Dependency injection for all external concerns
- Proper error handling with user-friendly messages
- JWT token validation for all protected API routes (including chat)
- SQL injection prevention through ORM usage
- Use of MCP servers and Context7 for documentation verification
- Use of dedicated `CLAUDE.md` files for component-specific context
- Stateless architecture for AI agent (load conversation from database)
- User ID parameter in all MCP tools for multi-user isolation

## Development Workflow

### Required Workflow Steps
1. **Spec**: Create feature specification in `specs/features/`
2. **Plan**: Create implementation plan in `specs/architecture.md`
3. **Tasks**: Generate task breakdown in `specs/tasks.md`
4. **Red**: Write failing test for next task
5. **Green**: Implement minimal code to pass test
6. **Refactor**: Improve code while tests stay green
7. **Document**: Update ADR if architectural decisions were made
8. **Verify**: Use context7 and nextjs mcp servers to validate tech stack usage
9. **Context**: Update component-specific `CLAUDE.md` files for relevant context
10. **E2E Test**: Write end-to-end tests for natural language flows (if AI feature)
11. **Repeat**: Continue until all tasks complete

### Code Review Standards
- All PRs must have passing tests before review
- Review must verify constitution compliance
- Review must verify clean architecture boundaries
- Review must verify TDD workflow was followed
- Review must verify authentication and data isolation requirements
- Review must verify use of official documentation from MCP servers and Context7
- Review must verify `CLAUDE.md` files are up-to-date and provide relevant context
- Review must verify stateless architecture for AI components
- Review must verify user_id parameter in all MCP tools

## Governance

### Constitution Supremacy
This constitution supersedes all other development practices, conventions, and
guidelines within the project. When conflicts arise, constitution provisions take
precedence.

### Amendment Process
Constitutional amendments require:
1. Documentation of proposed change with rationale
2. Impact analysis on existing phases
3. Review by at least one other contributor
4. Update to constitution version following semantic versioning

### Versioning Policy
- **MAJOR**: Backward-incompatible changes to principles or removal of constraints
- **MINOR**: Addition of new principles, goals, or significant clarification
- **PATCH**: Typo fixes, wording clarifications, non-semantic refinements

### Compliance Verification
All PRs and commits must verify constitution compliance. Violations must be
documented in an ADR with explicit justification for why the constraint was
intentionally violated.

**Version**: 2.5.0 | **Ratified**: 2026-01-14 | **Last Amended**: 2026-02-09
