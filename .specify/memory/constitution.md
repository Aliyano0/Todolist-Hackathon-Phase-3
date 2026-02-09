<!--
Sync Impact Report
==================
Version change: 2.3.0 → 2.4.0 (minor update - Better Auth JWT integration)
Modified principles: Updated authentication section to reflect Better Auth-centric JWT authentication with stateless backend verification
Templates requiring updates: ✅ Updated (authentication simplified to Better Auth + JWT verification model)
-->

# The Evolution of Todo - Phase II: Multi-User Web Application with Persistent Storage Constitution

## Core Principles

### I. Product Architect Mindset

Every contributor operates as a Product Architect, not a code implementer. This means:
- All decisions must be justified by explicit product value or future evolution benefit
- Technical choices must consider Phase III and beyond implications
- Architecture diagrams and decision rationale must be documented
- Questions are welcomed; assumptions must be surfaced and challenged

**Rationale**: "The Evolution of Todo" is an intentional multi-phase evolution project. Every
Phase II decision shapes the migration path forward. Treating contributors as architects
ensures decisions are reversible, traceable, and evolution-aware.

### II. Clean Architecture Mandatory

The application MUST follow clean architecture principles:
- Domain logic is isolated from I/O and presentation concerns
- Core entities and use cases reside in shared modules with minimal external dependencies
- Ports (interfaces) define all external interactions; adapters implement them
- Dependencies point inward; no layer may import from an outer layer

**Rationale**: Phase II introduces web APIs, databases, and authentication. Clean architecture ensures
each evolution remains modular and maintainable as complexity increases.

### III. Simplicity First (Non-Negotiable)

Complexity must be justified before being introduced. For every feature or abstraction:
- Ask: "What specific problem does this solve today?"
- If no immediate problem: do not introduce
- Prefer the simplest implementation that satisfies current requirements
- Defer decisions to the last responsible moment

**Rationale**: This is an evolution project. Over-engineering Phase II creates debt for
Phase III. The YAGNI principle ("You Aren't Gonna Need It") applies aggressively.

### IV. Five Core Features Only

Phase II MUST implement exactly these five features converted to a web application:
1. **Add**: Create a new todo item with title and optional description via web interface
2. **View**: List all todos for authenticated user; show individual todo details
3. **Update**: Modify title or description of an existing todo via web interface
4. **Delete**: Remove a todo item permanently via web interface
5. **Mark Complete**: Toggle completion status on a todo via web interface

**Rationale**: Constraining scope ensures a focused, complete Phase II. Feature creep
in early phases compounds through the evolution timeline. The web interface provides
modern UX while maintaining the same core functionality.

### V. Persistent Storage Mandate

Phase II MUST implement persistent storage:
- Use Neon Serverless PostgreSQL database (postgres version 17) for data storage
- Use SQLModel ORM with asyncpg driver for database interactions
- Data persists beyond user sessions
- Database schema supports multi-user data isolation

**Rationale**: Persistence is Phase II's core concern. The transition from in-memory to
persistent storage requires careful architecture to maintain clean separation of concerns.
The persistence mandate forces proper data modeling and repository patterns.

### VI. Modern Tech Stack Compliance

Phase II MUST use the specified technology stack:
- Backend: FastAPI with Python 3.13+ in UV venv environment
- Frontend: Next.js 16.1 with App Router and with Shadcn UI and tailwindcss
- Database: Neon Serverless PostgreSQL with SQLModel ORM and asyncpg driver
- Authentication: Better Auth with JWT token integration
- Package management: UV for Python dependencies

**Rationale**: The specified tech stack ensures compatibility, scalability, and modern
development practices. Using these technologies creates a robust foundation for future
evolution phases.

### VII. Documentation-First Approach with MCP Servers

Phase II development MUST prioritize documentation from official sources using MCP servers and Context7:
- Use context7 MCP server to retrieve up-to-date documentation and code examples for any library
- Use nextjs mcp server for Next.js-specific documentation and tooling
- Prioritize official documentation over internal knowledge or assumptions
- Follow authoritative documentation for API usage, configuration, and best practices

**Rationale**: Using official, up-to-date documentation ensures that development follows
current best practices and avoids deprecated patterns. MCP servers provide verified,
curated information that reduces risk of implementing outdated approaches.

### VIII. Context-Specific Documentation with CLAUDE.md

Each major component (e.g., `backend/`, `frontend/`) MUST contain its own `CLAUDE.md` file for context-specific instructions, guidelines, and tool usage. The root `CLAUDE.md` file SHOULD contain global instructions applicable to the entire project and refer to component-specific `CLAUDE.md` files for detailed context.

**Rationale**: As the project evolves into a full-stack application, maintaining a single, monolithic `CLAUDE.md` becomes unwieldy. Dedicated `CLAUDE.md` files improve clarity, reduce cognitive load for developers working on specific parts of the codebase, and ensure that context is always co-located with the code it describes.

### IX. Multi-User Authentication & Authorization

Phase II MUST implement secure multi-user functionality using Better Auth with JWT:

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
- All API routes require valid JWT token
- User ID extracted from JWT token (sub claim) for authorization
- API routes use user ID in path (/api/{user_id}/tasks) validated against token
- User ID mismatch between token and path results in 403 Forbidden
- Missing or invalid token results in 401 Unauthorized
- Proper data isolation between users at database level
- All database queries filtered by authenticated user_id
- Cross-user data access always fails

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
- Referential integrity between tasks and users
- Indexed fields for performance (email, user_id)

**Rationale**: Multi-user support with Better Auth provides a robust, industry-standard
authentication solution. The stateless JWT approach simplifies backend architecture while
maintaining security. Better Auth handles token issuance complexity, allowing the backend
to focus on verification and authorization. Proper data isolation prevents cross-user
data leakage and ensures security compliance.

### X. Test-Driven Development (Non-Negotiable)

Phase II MUST use TDD for all implementation:
- Write failing test first for every feature
- Test must fail for a clear, specific reason
- Implement minimal code to pass the test
- Refactor while tests remain green
- Red-Green-Refactor cycle strictly enforced

**Rationale**: TDD ensures design discipline, regression safety, and evolution
readiness. Tests from Phase II will validate future migrations.

## Goals

### Primary Goal
Deliver a working, tested, clean-architecture multi-user web todo application
that implements all five core features with persistent storage and authentication,
serving as a solid foundation for future evolution phases.

### Secondary Goals
- Establish secure authentication and authorization patterns
- Create comprehensive test coverage that enables confident refactoring
- Document architectural decisions for traceability
- Demonstrate modern web development practices with the specified tech stack
- Implement proper data isolation between users

### Non-Goals
- Advanced UI/UX features beyond core functionality
- Real-time collaboration or notifications
- Email integrations or advanced notification systems
- Admin panels or user management beyond basic auth
- Advanced search or filtering capabilities
- Export/import functionality
- Mobile app development (web app should be responsive)

## Success Criteria

### Functional Criteria
- All five features (add, view, update, delete, mark complete) work correctly in web interface
- User authentication (signup/signin) works seamlessly
- Data persists across sessions and user logins
- Error handling provides clear, actionable messages
- Multi-user data isolation prevents cross-user access

### Architectural Criteria
- Core domain has minimal imports from outer layers (API, UI, Infrastructure)
- All dependencies point inward toward the domain
- New features can be added without modifying domain code
- Tests can run independently of UI layer
- Proper separation between frontend and backend concerns

### Quality Criteria
- Unit test coverage for core domain entities and use cases (target 80%+)
- API endpoints properly validated and secured
- Type hints used throughout (Python and TypeScript)
- Proper error handling and validation for all inputs
- Security best practices implemented (JWT, input sanitization, etc.)

### Evolution Criteria
- Domain code contains no references to "Phase II" or web-specific constraints
- Additional features can be added without modifying core domain code
- Authentication system can be extended without changing domain logic
- Database schema can be evolved without breaking existing functionality

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
│   │   └── pages.md
├── CLAUDE.md                    # Root Claude Code instructions
├── backend/
│   ├── CLAUDE.md
│   ├── main.py                  # FastAPI app entry point
│   ├── models/                  # SQLModel database models
│   │   └── todo.py              # Todo model with user relationship
│   ├── api/                     # API routes
│   │   ├── auth.py              # Authentication routes
│   │   └── todos.py             # Todo CRUD routes
│   ├── core/                    # Core business logic
│   │   ├── services/            # Service layer
│   │   │   └── todo_service.py  # Todo business logic
│   │   └── security/            # Security utilities
│   │       └── jwt.py           # JWT utilities
│   ├── database/                # Database configuration
│   │   └── session.py           # Database session management
│   ├── dependencies/            # FastAPI dependencies
│   │   └── auth.py              # Current user dependency
│   ├── schemas/                 # Pydantic schemas
│   │   ├── todo.py              # Todo request/response schemas
│   │   └── user.py              # User schemas
│   ├── tests/                   # Backend tests
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
│   │   └── globals.css
│   ├── components/              # React components
│   │   ├── TodoForm.tsx         # Todo creation/update form
│   │   ├── TodoList.tsx         # Todo display component
│   │   ├── TodoItem.tsx         # Individual todo item
│   │   └── Navbar.tsx           # Navigation component
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
- Python 3.13+ required for backend
- Next.js 16+ with App Router for frontend
- Use Shadcn UI components and tailwindcss for styling
- Neon Serverless PostgreSQL for database with asyncpg driver
- Better Auth for authentication with JWT integration
- SQLModel ORM for database interactions with asyncpg compatibility
- Use context7 and nextjs mcp servers for documentation and code examples

### Process Constraints
- All features must follow TDD (Red-Green-Refactor)
- All architectural decisions must be documented as ADRs
- All changes must be traceable to a user story in spec.md
- Spec-Kit Plus workflow must be followed for all work
- API endpoints must be properly documented with OpenAPI
- Use official documentation accessed through MCP servers and Context7
- Component-specific `CLAUDE.md` files must be maintained for context

### Quality Constraints
- No TODO comments left in production code
- Maximum cyclomatic complexity: 10 per function
- Maximum function length: 50 lines
- All public APIs must have docstrings
- Type hints required for all function signatures
- Proper error handling for all user inputs

## Additional Constraints

### Forbidden Patterns
- Direct database queries in UI components (use API endpoints)
- Hardcoded secrets or credentials in source code
- Sharing of data between authenticated users
- Storing sensitive data in client-side storage without encryption
- Bypassing authentication for protected routes
- Hardcoded strings in domain logic (use constants or enums)
- Relying on outdated documentation or internal knowledge without verification

### Required Patterns
- Explicit is better than implicit (PEP 20 and TypeScript best practices)
- Composition over inheritance
- Single responsibility per class/function/component
- Dependency injection for all external concerns
- Proper error handling with user-friendly messages
- JWT token validation for all protected API routes
- SQL injection prevention through ORM usage
- Use of MCP servers and Context7 for documentation verification
- Use of dedicated `CLAUDE.md` files for component-specific context

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
10. **Repeat**: Continue until all tasks complete

### Code Review Standards
- All PRs must have passing tests before review
- Review must verify constitution compliance
- Review must verify clean architecture boundaries
- Review must verify TDD workflow was followed
- Review must verify authentication and data isolation requirements
- Review must verify use of official documentation from MCP servers and Context7
- Review must verify `CLAUDE.md` files are up-to-date and provide relevant context

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

**Version**: 2.4.0 | **Ratified**: 2026-01-14 | **Last Amended**: 2026-02-08