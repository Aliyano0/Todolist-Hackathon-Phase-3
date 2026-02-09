# Feature Specification: Todo Backend API

**Feature Branch**: `002-todo-backend-api`
**Created**: 2026-01-16
**Status**: Draft
**Updated**: 2026-01-21
**Input**: User description: "For Phase 2a (backend only), develop the FastAPI backend in the /backend directory for the multi-user Todo web app with persistent storage. Work exclusively in /backend.

First, ensure the folder structure is set up correctly in /backend, install required technologies using 'uv add' for any Python package installations (including fastapi, sqlmodel, uvicorn, python-jose[cryptography] for JWT, bcrypt for password hashing, etc.), then confirm the working directory is /backend before proceeding.

Set up UV venv Python FastAPI backend with SQLModel ORM connected to Neon Serverless PostgreSQL database. Implement all 5 Basic Level features through RESTful API endpoints.

Create the following RESTful API endpoints (all under /api):

- GET /{user_id}/tasks → List all tasks for the authenticated user
- POST /{user_id}/tasks → Create a new task for the authenticated user
- GET /{user_id}/tasks/{id} → Get details of a specific task
- PUT /{user_id}/tasks/{id} → Update a task
- DELETE /{user_id}/tasks/{id} → Delete a task
- PATCH /{user_id}/tasks/{id}/complete → Toggle task completion

Also implement authentication endpoints under /auth:

- POST /auth/register → Register a new user with email and password
- POST /auth/login → Authenticate user with email and password, return JWT token
- POST /auth/logout → End user session
- POST /auth/refresh → Refresh JWT token (future implementation)

Secure the API with JWT verification: Add FastAPI middleware to extract and verify JWT from Authorization: Bearer header using the shared secret, decode to get user_id/email, validate it matches the {user_id} in the URL path, and filter all database queries by the authenticated user's ID for strict multi-user data isolation.

Implement secure user management with:
- bcrypt password hashing
- Email validation and uniqueness
- Password strength requirements (8+ characters with mixed case, numbers, symbols)
- Protection against timing attacks
- Standardized error responses

Ensure tasks are stored and retrieved per authenticated user via SQLModel models."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create Todo Task (Priority: P1)

A logged-in user wants to create a new todo task with a title and optional description through the web interface. The user fills out the task details and submits the form. The system validates the input and stores the task in the database associated with the authenticated user's account.

**Why this priority**: This is the foundational functionality that enables users to start using the todo app. Without the ability to create tasks, other features become meaningless.

**Independent Test**: Can be fully tested by sending a POST request to the API with valid task data and verifying that the task is stored and retrievable for the authenticated user only.

**Acceptance Scenarios**:

1. **Given** user is authenticated with valid JWT token, **When** user sends POST request with valid task title and optional description, **Then** task is created and returned with a unique ID and timestamp
2. **Given** user is authenticated with valid JWT token, **When** user sends POST request with invalid data (empty title), **Then** appropriate error response is returned with validation details

---

### User Story 2 - View Todo Tasks (Priority: P1)

A logged-in user wants to view all their todo tasks in a list format. The user navigates to the tasks page and the system retrieves and displays all tasks associated with their account, showing completion status and details.

**Why this priority**: Essential for users to see their tasks and understand the state of their todo list. This is core functionality alongside task creation.

**Independent Test**: Can be fully tested by sending a GET request to the API and verifying that only the authenticated user's tasks are returned, not tasks from other users.

**Acceptance Scenarios**:

1. **Given** user is authenticated with valid JWT token and has created tasks, **When** user sends GET request for their tasks, **Then** all tasks for that user are returned with their details
2. **Given** user is authenticated with valid JWT token but has no tasks, **When** user sends GET request for their tasks, **Then** an empty list is returned

---

### User Story 3 - Update and Manage Tasks (Priority: P2)

A logged-in user wants to modify existing tasks by updating details, marking them as complete/incomplete, or deleting them. The user selects a task and performs the desired action through the interface.

**Why this priority**: These are essential management functions that allow users to maintain their todo lists effectively after creating tasks.

**Independent Test**: Can be tested separately for each operation (update, delete, toggle completion) by sending appropriate requests to the API and verifying the changes are persisted correctly.

**Acceptance Scenarios**:

1. **Given** user is authenticated and owns a specific task, **When** user sends PUT request to update task details, **Then** the task is updated and returned with new information
2. **Given** user is authenticated and owns a specific task, **When** user sends PATCH request to toggle completion status, **Then** the task's completion status is updated
3. **Given** user is authenticated and owns a specific task, **When** user sends DELETE request for that task, **Then** the task is removed from their list

---

### Edge Cases

- What happens when a user attempts to access or modify another user's tasks?
- How does system handle expired or invalid JWT tokens?
- What occurs when a user tries to access a non-existent task ID?
- How does the system handle concurrent modifications to the same task?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide RESTful API endpoints for creating, reading, updating, and deleting todo tasks
- **FR-002**: System MUST authenticate all API requests using JWT tokens from Better Auth
- **FR-003**: Users MUST be able to create new todo tasks with title and optional description
- **FR-004**: Users MUST be able to retrieve all their own tasks through the API
- **FR-005**: Users MUST be able to get details of a specific task they own
- **FR-006**: Users MUST be able to update their own tasks (title, description)
- **FR-007**: Users MUST be able to delete their own tasks
- **FR-008**: Users MUST be able to toggle completion status of their own tasks
- **FR-009**: System MUST enforce strict data isolation ensuring users can only access their own tasks
- **FR-010**: System MUST validate JWT tokens and verify user identity matches the requested user ID in the URL
- **FR-011**: System MUST persist all task data to a PostgreSQL database
- **FR-012**: System MUST return appropriate HTTP status codes for all operations
- **FR-013**: System MUST configure CORS to allow requests from the frontend origin
- **FR-014**: System MUST support secure communication via HTTPS in production

### Key Entities

- **Task**: Represents a todo item with title, description, completion status, timestamps, and user association
- **User**: Represents an authenticated user identified by their ID extracted from JWT token

## Clarifications

### Session 2026-01-16

- Q: How should the JWT secret be configured and managed? → A: Environment variable
- Q: What specific attributes should the Task entity include? → A: Core attributes only - title, description, completion status, timestamps (created/updated), and user ID (with extended attributes as optional future enhancement)
- Q: How should API error responses be formatted? → A: Standardized JSON format
- Q: How should database connections be managed? → A: Connection pooling
- Q: How should unique identifiers for tasks be generated? → A: Auto-increment numeric IDs

### Session 2026-01-21

- Q: How should CORS be configured for frontend integration? → A: Use environment variable ALLOWED_ORIGINS with comma-separated origins, default to http://localhost:3000 for development
- Q: Should CORS allow credentials? → A: Yes, to support JWT token transmission via headers
- Q: How should CORS be configured for production? → A: Use environment-specific origins, avoid wildcard configurations

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can create a new task in under 2 seconds from form submission to confirmation
- **SC-002**: System handles at least 1000 concurrent API requests without degradation
- **SC-003**: 99.9% of authenticated requests successfully return the correct user's data without cross-user access
- **SC-004**: API endpoints respond to 95% of requests within 500ms
- **SC-005**: Users can successfully manage their tasks (create, update, delete, toggle completion) with 99% success rate
