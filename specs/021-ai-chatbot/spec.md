# Feature Specification: Phase III - AI Chatbot Integration

**Feature Branch**: `021-ai-chatbot`
**Created**: 2026-02-10
**Updated**: 2026-02-11
**Status**: Complete
**Input**: User description: "Phase III – Todo AI Chatbot (Basic Level) - Integrate an AI-powered conversational chatbot into the Phase 2 Todo web app, enabling users to manage Basic Level tasks (add, list, complete, delete, update) through natural language. The system uses a stateless agent architecture with DB-backed conversation persistence, MCP tools for task operations, OpenAI Agents SDK for logic, and OpenRouter for LLM inference. Ensure multi-user isolation, email verification enforcement, and multilingual support (English, Roman Urdu, Urdu). Include floating chatbot widget with real-time task updates."

## Building on Existing Foundation

**Phase 3 extends the existing Todo web app with AI chatbot capabilities. The following are already implemented:**

### Already Complete (018-better-auth-jwt)
- ✅ User registration with password validation
- ✅ User login with JWT tokens (7-day validity, HS256 algorithm)
- ✅ Password reset with secure tokens and email delivery
- ✅ JWT verification middleware
- ✅ User model with `email_verified` and `verification_token` fields
- ✅ Protected API routes with user isolation (`/api/{user_id}/tasks`)

### Already Complete (019-production-deployment)
- ✅ SMTP email service with aiosmtplib (supports Gmail, SendGrid, AWS SES)
- ✅ Docker containerization with multi-stage builds
- ✅ Production configuration management (centralized in backend/core/config.py)
- ✅ Security headers middleware (HSTS, CSP, X-Frame-Options, etc.)
- ✅ Health check endpoint for container monitoring
- ✅ Structured JSON logging

### Already Complete (020-frontend-ui-upgrade)
- ✅ Modern UI with Framer Motion animations
- ✅ Homepage with hero section and feature showcase
- ✅ Dashboard with task management interface
- ✅ Dark mode support
- ✅ Responsive design for mobile and desktop

### Phase 3 Adds (NEW - Complete)
- 🆕 **Email Verification Flow** (4 tasks): Send verification email on registration, verify endpoint, resend endpoint (added to profile page), JWT claim update, verify-email page for handling verification links
- 🆕 **Chat Infrastructure** (29 tasks): Conversation/Message models, MCP server with 5 tools, OpenAI Agents SDK integration, OpenRouter API client, chat service, chat endpoint, rate limiting
- 🆕 **Chat UI** (11 tasks): Full chat page, ChatKit components, email verification prompt, conversation list, chat page
- 🆕 **Chatbot Widget** (NEW): Floating widget in bottom-right corner with theme matching, animations, expand to full chat, real-time task updates, chat history persistence, Info icon with command guide
- 🆕 **Chat History Persistence**: Messages and conversation IDs saved to localStorage per user, persists across page refreshes and widget open/close
- 🆕 **Task Numbering System**: Tasks display numbered badges (#1, #2, etc.) for easy chatbot reference, consistent numbering between dashboard and chatbot (oldest = #1), newest tasks displayed at top
- 🆕 **Command Guide**: Info icon in both widget and full chat page showing available commands, supported languages, and task number usage
- 🆕 **User Stories** (36 tasks): 7 independent user stories (task creation, listing, completion, deletion, update, conversation persistence, multilingual support)
- 🆕 **Polish** (12 tasks): Error handling, retry logic, logging, loading states, dark mode consistency, documentation
- 🆕 **Real-time Updates**: Event-based task synchronization between chat and dashboard
- 🆕 **Bug Fixes**: Email verification resend (422/500 errors), chat API authentication (401 error), datetime import, email service instantiation

## Clarifications

### Session 2026-02-10

- Q: How many recent messages should the agent load from the database when reconstructing conversation context? → A: Last 20 messages per conversation (balanced context and performance)
- Q: What rate limiting should be applied to chat messages per user? → A: 10 messages per minute per user (balanced protection and usability)
- Q: How should task IDs be presented to users in chat responses for easy reference? → A: Numbered list positions (1, 2, 3...) - agent maps position to UUID internally
- Q: How should conversations be displayed in the conversation list? → A: Show last message preview with timestamp, sorted by most recent activity
- Q: How should the agent handle task position references when no recent task list exists in the conversation? → A: Auto-fetch and display task list, then ask for confirmation (balanced safety and convenience)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Natural Language Task Creation (Priority: P1) 🎯 MVP

A verified user wants to quickly add tasks using natural language without navigating through forms, enabling rapid task capture through conversational interface.

**Why this priority**: Task creation is the most fundamental operation. Without the ability to add tasks via natural language, the chatbot provides no value. This is the core MVP feature that demonstrates AI integration.

**Independent Test**: Can be fully tested by sending natural language messages like "Add a task to buy groceries" and verifying the task is created in the database with correct user isolation. Delivers immediate value by enabling hands-free task creation.

**Acceptance Scenarios**:

1. **Given** a verified user is on the chat page, **When** they type "Add a task to buy groceries", **Then** the system creates a new task with title "buy groceries" and responds with confirmation
2. **Given** a verified user sends "Create task: finish project report", **When** the agent processes the message, **Then** a task is created and the user receives confirmation with task ID
3. **Given** a user types in Roman Urdu "task add karo buy milk", **When** the agent detects the language, **Then** the task is created and response is in Roman Urdu
4. **Given** a user types in Urdu script, **When** the agent processes the message, **Then** the task is created and response is in Urdu
5. **Given** an unverified user tries to use chat, **When** they send any message, **Then** they receive a 403 error with message "Please verify your email to use the chatbot"
6. **Given** a verified user adds a task, **When** the task is created, **Then** it is associated with their user_id and isolated from other users

---

### User Story 2 - Task Listing and Querying (Priority: P2)

A verified user wants to view their tasks through natural language queries, enabling quick status checks without navigating the web UI.

**Why this priority**: After creating tasks, users need to view them. This completes the basic read operation and enables users to understand their task status through conversation.

**Independent Test**: Can be fully tested by creating tasks for a user, then sending queries like "Show my tasks" or "What's pending?" and verifying correct filtered results are returned.

**Acceptance Scenarios**:

1. **Given** a user has 5 tasks (3 pending, 2 completed), **When** they ask "Show my tasks", **Then** all 5 tasks are listed with their status
2. **Given** a user asks "What's pending?", **When** the agent processes the query, **Then** only incomplete tasks are returned
3. **Given** a user asks "Show completed tasks", **When** the agent processes the query, **Then** only completed tasks are returned
4. **Given** a user has no tasks, **When** they ask "Show my tasks", **Then** the agent responds "You have no tasks yet. Want to add one?"
5. **Given** a user asks in Roman Urdu "mere tasks dikhao", **When** the agent processes the query, **Then** tasks are listed with response in Roman Urdu
6. **Given** multiple users have tasks, **When** user A asks for tasks, **Then** only user A's tasks are returned (isolation verified)

---

### User Story 3 - Task Completion via Natural Language (Priority: P3)

A verified user wants to mark tasks as complete using natural language, enabling quick status updates through conversation.

**Why this priority**: Completing tasks is a core workflow. This enables users to update task status without switching to the web UI, maintaining conversational flow.

**Independent Test**: Can be fully tested by creating a task, then sending messages like "Mark task 1 as done" and verifying the task's completed status is updated in the database.

**Acceptance Scenarios**:

1. **Given** a user has a pending task with ID "abc-123", **When** they say "Mark task abc-123 as done", **Then** the task is marked complete and confirmation is sent
2. **Given** a user says "Complete task 2", **When** the agent processes the command, **Then** the task is marked complete
3. **Given** a user says "Task 3 is finished", **When** the agent recognizes the intent, **Then** the task is marked complete
4. **Given** a user tries to complete a non-existent task, **When** they say "Complete task xyz", **Then** the agent responds "Task not found. Please check the task ID."
5. **Given** a user tries to complete another user's task, **When** they provide a task ID from another user, **Then** the operation fails with "Task not found" (isolation enforced)
6. **Given** a user completes a task in Roman Urdu "task 1 complete karo", **When** the agent processes it, **Then** the task is completed with confirmation in Roman Urdu

---

### User Story 4 - Task Deletion with Confirmation (Priority: P4)

A verified user wants to delete tasks using natural language, with the system requiring confirmation for this destructive action to prevent accidental data loss.

**Why this priority**: Deletion is a destructive operation that requires safeguards. While important, it's less critical than creation, viewing, and completion.

**Independent Test**: Can be fully tested by creating a task, requesting deletion, verifying confirmation prompt appears, confirming deletion, and verifying task is removed from database.

**Acceptance Scenarios**:

1. **Given** a user says "Delete task abc-123", **When** the agent processes the command, **Then** the agent asks "Are you sure you want to delete this task?" before proceeding
2. **Given** a user confirms deletion, **When** they respond "Yes", **Then** the task is deleted and confirmation is sent
3. **Given** a user cancels deletion, **When** they respond "No" or "Cancel", **Then** the task is not deleted
4. **Given** a user says "Delete task abc-123" with explicit confirmation like "Delete task abc-123, I'm sure", **When** the agent detects explicit confirmation, **Then** the task is deleted immediately without additional prompt
5. **Given** a user tries to delete a non-existent task, **When** they provide an invalid task ID, **Then** the agent responds "Task not found"
6. **Given** a user tries to delete another user's task, **When** they provide a task ID from another user, **Then** the operation fails with "Task not found" (isolation enforced)

---

### User Story 5 - Task Update and Modification (Priority: P5)

A verified user wants to update task details (title, description) using natural language, enabling task refinement through conversation.

**Why this priority**: Updating tasks is useful but less critical than core CRUD operations. Users can work around this by deleting and recreating tasks if needed.

**Independent Test**: Can be fully tested by creating a task, sending update commands like "Change task 1 title to 'New Title'", and verifying the task is updated in the database.

**Acceptance Scenarios**:

1. **Given** a user has a task with title "Buy milk", **When** they say "Change task abc-123 title to 'Buy organic milk'", **Then** the task title is updated
2. **Given** a user says "Update task 2 description to 'Get it from the store'", **When** the agent processes the command, **Then** the task description is updated
3. **Given** a user says "Rename task 3 to 'Finish report'", **When** the agent recognizes the intent, **Then** the task title is updated
4. **Given** a user tries to update a non-existent task, **When** they provide an invalid task ID, **Then** the agent responds "Task not found"
5. **Given** a user tries to update another user's task, **When** they provide a task ID from another user, **Then** the operation fails with "Task not found" (isolation enforced)
6. **Given** an ambiguous update request, **When** the user says "Update task 1", **Then** the agent asks "What would you like to update about this task?"

---

### User Story 6 - Conversation Persistence and Resumption (Priority: P6)

A verified user wants their chat conversations to persist across sessions, enabling them to resume conversations after closing and reopening the app.

**Why this priority**: Conversation persistence improves user experience but is not critical for core functionality. Users can still perform all task operations without conversation history.

**Independent Test**: Can be fully tested by having a conversation, closing the app, reopening it, and verifying the conversation history is loaded and displayed.

**Acceptance Scenarios**:

1. **Given** a user has an active conversation, **When** they close and reopen the app, **Then** the conversation history is loaded and displayed
2. **Given** a user sends a message, **When** the message is processed, **Then** it is stored in the database with user_id and conversation_id
3. **Given** a user has multiple conversations, **When** they open the chat page, **Then** they can see their conversation list
4. **Given** a user starts a new conversation, **When** they send the first message, **Then** a new conversation record is created with a unique UUID
5. **Given** a user resumes a conversation, **When** they send a new message, **Then** the agent has access to previous conversation context
6. **Given** the server restarts, **When** a user sends a message, **Then** the agent reconstructs conversation history from the database (stateless architecture verified)

---

### User Story 7 - Multilingual Support (Priority: P7)

A verified user wants to interact with the chatbot in their preferred language (English, Roman Urdu, or Urdu), with the system automatically detecting and responding in the same language.

**Why this priority**: Multilingual support expands accessibility but is not critical for core functionality. English-only would still provide full task management capabilities.

**Independent Test**: Can be fully tested by sending messages in different languages and verifying the agent responds in the detected language while maintaining correct tool invocations.

**Acceptance Scenarios**:

1. **Given** a user sends a message in English, **When** the agent processes it, **Then** the response is in English
2. **Given** a user sends a message in Roman Urdu, **When** the agent detects the language, **Then** the response is in Roman Urdu
3. **Given** a user sends a message in Urdu script, **When** the agent detects the language, **Then** the response is in Urdu
4. **Given** a user switches languages mid-conversation, **When** they send a message in a different language, **Then** the agent responds in the new language
5. **Given** a user sends a message in any supported language, **When** the agent invokes MCP tools, **Then** tool parameters remain in English/structured format
6. **Given** a user sends a message with mixed languages, **When** the agent processes it, **Then** the agent responds in the dominant detected language

---

### Edge Cases

- What happens when a user sends an ambiguous message that could map to multiple intents (e.g., "task 1")?
- How does the system handle messages that are completely off-topic (e.g., "What's the weather?")?
- What happens when the OpenRouter API is unavailable or returns an error?
- How does the system handle extremely long messages (>1000 characters)?
- What happens when a user tries to perform operations on tasks that were just deleted by another session?
- How does the system handle rapid successive messages (rate limiting)?
- What happens when the database connection fails during a conversation?
- How does the system handle malformed task IDs or invalid UUIDs?
- What happens when a user's email verification status changes mid-conversation?
- How does the system handle conversations with >100 messages (context window limits)?
- What happens when a user sends a message with special characters or code injection attempts?
- How does the system handle concurrent requests from the same user?

## Requirements *(mandatory)*

### Functional Requirements

**Authentication & Authorization:**

- **FR-001**: System MUST verify JWT token for all chat endpoint requests
- **FR-002**: System MUST extract user_id from JWT token and validate it matches the path parameter
- **FR-003**: System MUST check user.email_verified field before allowing chatbot access
- **FR-004**: System MUST return 403 error with message "Please verify your email to use the chatbot" if email is not verified
- **FR-005**: System MUST provide a "Resend verification email" button in the frontend when email is not verified
- **FR-006**: Frontend MUST block chat input and show verification prompt for unverified users

**Chat Endpoint:**

- **FR-007**: System MUST provide POST /api/{user_id}/chat endpoint protected by JWT middleware
- **FR-008**: Endpoint MUST accept request payload: {conversation_id?: string (UUID), message: string}
- **FR-009**: Endpoint MUST return response: {conversation_id: string (UUID), response: string, tool_calls: array}
- **FR-010**: System MUST create a new conversation if conversation_id is not provided
- **FR-011**: System MUST fetch existing conversation if conversation_id is provided
- **FR-012**: System MUST validate that conversation belongs to the authenticated user

**Database Models:**

- **FR-013**: System MUST use UUID primary keys for all models (Task, Conversation, Message)
- **FR-014**: Conversation model MUST have: id (UUID), user_id (UUID FK), created_at, updated_at
- **FR-015**: Message model MUST have: id (UUID), user_id (UUID FK), conversation_id (UUID FK), role (user/assistant), content (string), created_at
- **FR-016**: System MUST store all messages in the database for conversation persistence
- **FR-017**: System MUST filter all database queries by user_id for multi-user isolation

**MCP Tools:**

- **FR-018**: System MUST implement add_task tool: add_task(user_id: str, title: str, description?: str) → {task_id, status, title}
- **FR-019**: System MUST implement list_tasks tool: list_tasks(user_id: str, status?: "all"/"pending"/"completed") → [{id, title, completed}, ...]
- **FR-020**: System MUST implement complete_task tool: complete_task(user_id: str, task_id: str) → {task_id, status, title}
- **FR-021**: System MUST implement delete_task tool: delete_task(user_id: str, task_id: str) → {task_id, status, title}
- **FR-022**: System MUST implement update_task tool: update_task(user_id: str, task_id: str, title?: str, description?: str) → {task_id, status, title}
- **FR-023**: All MCP tools MUST require user_id parameter for multi-user isolation
- **FR-024**: All MCP tools MUST perform async database operations using SQLModel with asyncpg
- **FR-025**: All MCP tools MUST validate user_id matches the authenticated user
- **FR-026**: All MCP tools MUST return structured responses with success/error status
- **FR-027**: Agent MUST present tasks to users with numbered list positions (1, 2, 3...) for easy reference
- **FR-028**: Agent MUST maintain internal mapping between list positions and task UUIDs within conversation context
- **FR-029**: Agent MUST auto-fetch and display current task list when user references a task position without recent context, then ask for confirmation before executing operations

**AI Agent Behavior:**

- **FR-030**: System MUST use OpenAI Agents SDK for intent recognition and tool orchestration
- **FR-031**: System MUST use OpenRouter API with gpt-4o-mini model for all LLM inference
- **FR-032**: System MUST use OPENROUTER_API_KEY environment variable for API authentication
- **FR-033**: Agent MUST map natural language intents to MCP tools: "add/create/remember" → add_task, "show/list/see" → list_tasks, "done/complete/finished" → complete_task, "delete/remove/cancel" → delete_task, "change/update/rename" → update_task
- **FR-034**: Agent MUST detect input language (English, Roman Urdu, Urdu) and respond in the same language
- **FR-035**: Agent MUST keep tool parameters in English/structured format regardless of input language
- **FR-036**: Agent MUST use MCP tools for all task operations and NEVER fabricate task IDs or data
- **FR-037**: Agent MUST ask clarification questions for ambiguous intents
- **FR-038**: Agent MUST require user confirmation for destructive actions (delete, complete, update) unless explicit confirmation is in the message
- **FR-039**: Agent MUST confirm all successful actions (e.g., "Task added!", "Task completed!")
- **FR-040**: Agent MUST handle errors gracefully with user-friendly messages (e.g., "Task not found—check ID?")
- **FR-041**: Agent MUST limit scope to task management only and redirect off-topic queries (e.g., "I'm here for tasks—want to add one?")
- **FR-042**: Agent MUST be stateless and reconstruct conversation history from database on each request

**Stateless Architecture:**

- **FR-043**: System MUST NOT maintain any server-side state between requests
- **FR-044**: System MUST load the last 20 messages from conversation history from database on each request
- **FR-045**: System MUST store user message in database before processing
- **FR-046**: System MUST store assistant response in database after processing
- **FR-047**: System MUST support conversation resumption after server restart

**Frontend Integration:**

- **FR-048**: Frontend MUST use OpenAI ChatKit components for chat UI
- **FR-049**: Frontend MUST persist conversation_id in component state or localStorage
- **FR-050**: Frontend MUST send JWT token in Authorization header with all chat requests
- **FR-051**: Frontend MUST handle email verification status and show appropriate prompts
- **FR-052**: Frontend MUST maintain dark mode and animation consistency with existing UI
- **FR-053**: Frontend MUST display user messages, assistant responses, and tool execution results
- **FR-054**: Frontend MUST display conversation list showing last message preview with timestamp, sorted by most recent activity
- **FR-055**: Frontend MUST provide floating chatbot widget in bottom-right corner for quick access
- **FR-056**: Chatbot widget MUST only appear for authenticated users with verified email
- **FR-057**: Chatbot widget MUST use Framer Motion for smooth open/close animations
- **FR-058**: Chatbot widget MUST match application theme (primary color for button, card background for widget)
- **FR-059**: Chatbot widget MUST provide "Expand to full chat" button that redirects to /chat route
- **FR-060**: Chatbot widget MUST be compact (96px width button, 500px height widget window)
- **FR-061**: Chatbot widget MUST persist conversation across widget open/close cycles
- **FR-062**: Frontend MUST dispatch 'taskUpdated' event after successful chat operations
- **FR-063**: Dashboard MUST listen for 'taskUpdated' events and automatically refetch tasks
- **FR-064**: Real-time updates MUST work without manual page refresh
- **FR-065**: Profile page MUST show "Resend Verification Email" button for unverified users
- **FR-066**: System MUST provide /verify-email page to handle email verification links from emails
- **FR-067**: Verify-email page MUST extract token from URL query parameter and call backend verification endpoint
- **FR-068**: Verify-email page MUST show loading, success, and error states with appropriate icons
- **FR-069**: Verify-email page MUST auto-redirect to login after successful verification (3 seconds)

**Chat History Persistence:**

- **FR-070**: ChatWidget MUST save messages and conversationId to localStorage per user
- **FR-071**: ChatInterface MUST save messages and conversationId to localStorage per user
- **FR-072**: Chat history MUST persist across page refreshes and widget open/close cycles
- **FR-073**: Chat history MUST use separate storage keys per user to prevent data mixing
- **FR-074**: Chat history MUST load automatically on component mount if available

**Task Numbering System:**

- **FR-075**: TaskCard MUST display task number badge (#1, #2, etc.) next to task title
- **FR-076**: Task numbers MUST be calculated based on creation date (oldest = #1)
- **FR-077**: Task numbers MUST be consistent between dashboard and chatbot
- **FR-078**: Dashboard MUST display newest tasks at top while maintaining stable numbering
- **FR-079**: Chatbot list_tasks tool MUST return tasks ordered by creation date (oldest first)
- **FR-080**: Task numbers MUST remain stable and not change when tasks are added or deleted

**Command Guide:**

- **FR-081**: ChatWidget MUST provide Info icon in header next to "AI Assistant" title
- **FR-082**: ChatInterface MUST provide Info icon in header next to "AI Assistant" title
- **FR-083**: Info icon MUST toggle collapsible panel showing available commands
- **FR-084**: Command guide MUST list all available commands (add, list, complete, delete, update)
- **FR-085**: Command guide MUST show supported languages (English, Roman Urdu, Urdu)
- **FR-086**: Command guide MUST explain task number usage for referencing tasks

**Error Handling:**

- **FR-087**: System MUST handle OpenRouter API errors gracefully and inform user
- **FR-088**: System MUST handle database connection errors and retry with exponential backoff
- **FR-089**: System MUST handle MCP tool errors and provide user-friendly error messages
- **FR-090**: System MUST log all errors with sufficient context for debugging
- **FR-091**: System MUST handle rate limiting from OpenRouter API
- **FR-092**: System MUST enforce rate limit of 10 messages per minute per user to prevent abuse and manage API costs

### Key Entities

- **Conversation**: Represents a chat session between a user and the AI agent. Contains unique UUID identifier, user_id for ownership, and timestamps for creation and last update. Enables conversation persistence and resumption across sessions.

- **Message**: Represents a single message in a conversation. Contains unique UUID identifier, user_id for ownership, conversation_id for grouping, role (user/assistant) for sender identification, content (text), and timestamp. Enables conversation history reconstruction for stateless agent.

- **MCP Tool**: Represents a task management operation exposed to the AI agent. Each tool accepts user_id for isolation, performs async database operations, and returns structured responses. Tools include: add_task, list_tasks, complete_task, delete_task, update_task.

- **AI Agent**: Stateless component that processes natural language input, detects intent and language, invokes appropriate MCP tools, and generates responses. Uses OpenRouter API (gpt-4o-mini) for LLM inference and OpenAI Agents SDK for orchestration.

- **Chat Session**: Frontend component that manages conversation UI, persists conversation_id, sends messages with JWT authentication, and displays conversation history. Uses OpenAI ChatKit for UI components.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Verified users can create tasks via natural language in under 3 seconds from message send to confirmation
- **SC-002**: System correctly maps natural language intents to MCP tools with 95%+ accuracy for common phrases
- **SC-003**: Multilingual support works correctly for English, Roman Urdu, and Urdu with language detection accuracy >90%
- **SC-004**: Conversation history persists and can be resumed after server restart in 100% of cases
- **SC-005**: Multi-user isolation prevents cross-user data access in 100% of cases (verified through testing)
- **SC-006**: Email verification enforcement blocks unverified users from chatbot access in 100% of cases
- **SC-007**: Destructive actions (delete, complete, update) require confirmation in 100% of cases unless explicit confirmation is provided
- **SC-008**: Agent stays within task management scope and redirects off-topic queries in 95%+ of cases
- **SC-009**: System handles OpenRouter API errors gracefully without crashing in 100% of cases
- **SC-010**: Stateless architecture verified: agent reconstructs conversation from database on each request with no server-side state
- **SC-011**: Chat endpoint response time is under 2 seconds for simple queries (list tasks) and under 5 seconds for complex operations
- **SC-012**: System supports at least 50 concurrent users without performance degradation
- **SC-013**: All MCP tools execute with proper user_id isolation verified through automated tests
- **SC-014**: Frontend chat UI maintains consistency with existing design system (dark mode, animations, responsiveness)

## Scope *(mandatory)*

### In Scope

- Natural language task management (add, list, complete, delete, update)
- Stateless AI agent architecture with database-backed conversation persistence
- MCP server with 5 task management tools (all require user_id)
- OpenAI Agents SDK integration for intent recognition and tool orchestration
- OpenRouter API integration with gpt-4o-mini model
- JWT authentication with email verification enforcement
- Multi-user isolation at database and tool level
- Multilingual support (English, Roman Urdu, Urdu) with automatic language detection
- Conversation history persistence and resumption
- Confirmation prompts for destructive actions
- Graceful error handling with user-friendly messages
- Scope limiting (task management only, redirect off-topic queries)
- Frontend chat UI using OpenAI ChatKit
- Email verification status checking and resend functionality
- Dark mode and animation consistency with existing UI

### Out of Scope

- Third-party authentication providers (OAuth, social login)
- Advanced AI features beyond basic task management (sentiment analysis, recommendations, smart scheduling)
- Free-form database access (agent limited to MCP tools only)
- Off-topic conversations (weather, news, general knowledge)
- Server-side state or session management
- Real-time notifications or push alerts
- Voice input or speech-to-text
- Multi-modal inputs (images, files, attachments)
- Task sharing or collaboration features
- Advanced search or filtering beyond basic status queries
- Task categories, tags, or custom fields via chat
- Bulk operations (e.g., "delete all completed tasks")
- Task scheduling or reminders
- Export/import functionality via chat
- Admin or moderation features
- Analytics or usage tracking beyond basic logging

## Assumptions *(mandatory)*

1. **OpenRouter API Availability**: OpenRouter API is available and reliable for gpt-4o-mini model inference with acceptable latency (<2s for most requests)
2. **Email Verification**: Phase 2 Better Auth implementation includes email verification functionality that can be extended for chatbot access control
3. **Database Performance**: Neon Serverless PostgreSQL with asyncpg driver provides sufficient performance for conversation history queries (<100ms for typical conversation loads)
4. **User Behavior**: Users will primarily use short, conversational messages (<200 words) rather than extremely long inputs
5. **Conversation Length**: Most conversations will have <50 messages, fitting within typical LLM context windows
6. **Language Detection**: OpenRouter's gpt-4o-mini model can accurately detect and respond in English, Roman Urdu, and Urdu
7. **Concurrent Users**: System will support up to 50 concurrent users initially, with horizontal scaling possible if needed
8. **Network Reliability**: Users have reasonably stable internet connections for real-time chat interactions
9. **Browser Support**: Users access the chat interface with modern browsers supporting WebSocket or long-polling for real-time updates
10. **Task Volume**: Users typically have <1000 tasks, making list operations performant without pagination
11. **MCP Tool Reliability**: MCP tools execute reliably with <1% failure rate under normal conditions
12. **Stateless Architecture**: Reconstructing conversation history from database on each request is performant enough for good UX (<500ms overhead)

## Dependencies *(mandatory)*

### External Dependencies

- OpenRouter API account and OPENROUTER_API_KEY for LLM inference
- OpenAI Agents SDK (Python package) for agent orchestration
- Official MCP SDK (Python package) for MCP server implementation
- OpenAI ChatKit (npm package) for frontend chat UI components
- Neon Serverless PostgreSQL database (existing from Phase 2)
- Better Auth JWT authentication system (existing from Phase 2)
- asyncpg==0.30.0 driver for async database operations

### Internal Dependencies

- Phase 2 Task model must be compatible with MCP tool operations
- Phase 2 User model must include email_verified field (add if missing)
- Phase 2 JWT token must include user_id and email_verified claims
- Phase 2 authentication middleware must be reusable for chat endpoint
- Frontend design system (dark mode, animations) must be maintained
- Existing API client utilities must support chat endpoint integration

## Constraints *(mandatory)*

### Technical Constraints

- Must use Python 3.13+ for backend and MCP server
- Must use Next.js 16+ with App Router for frontend
- Must use OpenRouter API (not direct OpenAI API) for cost efficiency
- Must use gpt-4o-mini model (not larger models) for performance and cost
- Must use asyncpg==0.30.0 driver for Neon PostgreSQL compatibility
- Must use UV package manager for Python dependencies (uv add command)
- Must maintain stateless architecture (no server-side session state)
- Must use UUIDs for all primary keys (consistency with Phase 2)
- Must support only 3 languages: English, Roman Urdu, Urdu
- Must limit conversation history to prevent context window overflow
- Backend must run on Hugging Face Spaces deployment environment
- Frontend must run on Vercel deployment environment

### Business Constraints

- Must complete Phase III before hackathon deadline
- Must not introduce breaking changes to Phase 2 functionality
- Must maintain existing user authentication and authorization
- Must not require additional paid services beyond OpenRouter API
- Must work within OpenRouter API rate limits and quotas
- Must maintain data privacy and user isolation requirements
- Must comply with email verification requirements for chatbot access

### Design Constraints

- Must maintain consistency with existing UI design system
- Must support dark mode for chat interface
- Must maintain responsive design for mobile and desktop
- Must follow existing animation and transition patterns
- Must integrate seamlessly with existing navigation and layout
- Chat UI must not obscure or interfere with existing task management UI

## Risks *(mandatory)*

### High Risk

- **OpenRouter API Dependency**: Single point of failure for all AI functionality
  - **Mitigation**: Implement retry logic with exponential backoff, provide clear error messages to users, consider fallback to cached responses for common queries

- **Stateless Architecture Performance**: Reconstructing conversation history from database on every request may cause latency
  - **Mitigation**: Optimize database queries with proper indexing, limit conversation history to recent N messages, implement caching layer if needed

- **Email Verification Enforcement**: Users may be frustrated by mandatory email verification for chatbot access
  - **Mitigation**: Provide clear messaging about why verification is required, make resend verification email prominent and easy to use, ensure verification emails are delivered reliably

### Medium Risk

- **Language Detection Accuracy**: gpt-4o-mini may not accurately detect Roman Urdu or Urdu in all cases
  - **Mitigation**: Test extensively with native speakers, provide language selection option as fallback, log detection failures for improvement

- **Intent Recognition Accuracy**: Natural language is ambiguous and may lead to incorrect tool invocations
  - **Mitigation**: Implement confirmation prompts for ambiguous intents, provide clear error messages, log misrecognitions for model improvement

- **MCP Tool Complexity**: Building and maintaining 5 MCP tools with proper isolation and error handling is complex
  - **Mitigation**: Start with comprehensive tests for each tool, use code generation where possible, follow MCP SDK best practices

### Low Risk

- **Conversation Context Limits**: Very long conversations may exceed LLM context windows
  - **Mitigation**: Limit conversation history to recent 20-30 messages, implement conversation summarization if needed

- **User Adoption**: Users may prefer traditional UI over conversational interface
  - **Mitigation**: Maintain both interfaces (web UI and chat), provide onboarding/tutorial for chat features, gather user feedback

## Open Questions

All requirements are sufficiently specified based on the detailed feature description provided. No critical clarifications needed at this time.

**Note**: Implementation details (exact prompt engineering, error message wording, UI component styling) will be determined during the planning phase based on technical constraints and user testing.
