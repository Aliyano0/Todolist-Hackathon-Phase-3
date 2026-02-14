# Tasks: Phase III - AI Chatbot Integration

**Input**: Design documents from `/specs/021-ai-chatbot/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: TDD is mandatory per constitution - all test tasks are REQUIRED and must be written FIRST (Red-Green-Refactor)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/` (FastAPI, SQLModel, asyncpg)
- **MCP Server**: `backend/mcp_server/` (MCP SDK, tools - runs in-process as Python package)
- **Frontend**: `frontend/` (Next.js, ChatKit)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create backend/mcp_server directory structure with tools/, tests/ subdirectories and __init__.py files
- [X] T002 Install backend dependencies: uv add openrouter agents mcp (OpenRouter SDK, OpenAI Agents SDK, MCP SDK)
- [X] T003 [P] Install frontend dependencies: npm install @openai/chatkit-react
- [X] T004 [P] Configure environment variables in backend/.env (OPENROUTER_API_KEY, DATABASE_URL)
- [X] T005 [P] Update backend/CLAUDE.md with Phase 3 context (chat service, agent integration, MCP tools in mcp_server package)
- [X] T006 [P] Update frontend/CLAUDE.md with ChatKit integration and email verification UI guidelines

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

**Note**: Authentication system (018-better-auth-jwt), SMTP email service (019-production-deployment), and production infrastructure (019) are already implemented. This phase focuses on NEW Phase 3 requirements: email verification extension, chat infrastructure, and MCP server.

### Email Verification Extension (Extends Existing Auth System)

**Context**: User model already has `email_verified` and `verification_token` fields (018). JWT creation and SMTP email service already exist (018, 019). We need to add the verification flow.

- [X] T013 Add send verification email logic to registration endpoint in backend/api/auth.py (generate token, send email via existing SMTP service)
- [X] T014 Create verify email endpoint POST /api/auth/verify-email in backend/api/auth.py (validate token, update email_verified)
- [X] T015 Create resend verification email endpoint POST /api/auth/resend-verification in backend/api/auth.py
- [X] T016 Update JWT creation in backend/core/security/jwt.py to include email_verified claim in token payload

### Database Schema (New for Phase 3)

- [X] T017 Create Conversation model in backend/models/conversation.py with UUID, user_id, timestamps
- [X] T018 Create Message model in backend/models/message.py with UUID, conversation_id, user_id, role, content, timestamp
- [X] T019 Create Alembic migration script for conversation and message tables in backend/alembic/versions/003_add_conversation_tables.py
- [X] T020 Run database migration and verify tables created with proper indexes

### MCP Server Infrastructure (New for Phase 3)

- [ ] T021 Create MCP server entry point in backend/mcp_server/server.py with tool registration
- [ ] T022 [P] Implement add_task tool in backend/mcp_server/tools/add_task.py with user_id isolation
- [ ] T023 [P] Implement list_tasks tool in backend/mcp_server/tools/list_tasks.py with status filtering
- [ ] T024 [P] Implement complete_task tool in backend/mcp_server/tools/complete_task.py with user_id validation
- [X] T025 [P] Implement delete_task tool in backend/mcp_server/tools/delete_task.py with user_id validation
- [X] T026 [P] Implement update_task tool in backend/mcp_server/tools/update_task.py with user_id validation

### Chat Service Infrastructure (New for Phase 3)

- [X] T027 Create chat service in backend/core/services/chat_service.py with conversation history loading
- [X] T028 Implement OpenRouter API client wrapper in backend/core/services/openrouter_client.py
- [X] T029 Implement OpenAI Agents SDK integration in backend/core/services/agent_service.py with MCP tool registration
- [X] T030 Create chat request/response schemas in backend/schemas/chat.py

### Chat Endpoint & Rate Limiting (New for Phase 3)

- [X] T031 Create email verification dependency in backend/dependencies/auth.py (check email_verified claim from JWT)
- [X] T032 Implement rate limiting middleware in backend/api/middleware/rate_limit.py (10 messages/minute per user)
- [X] T033 Create chat endpoint in backend/api/chat.py with POST /api/{user_id}/chat route

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Natural Language Task Creation (Priority: P1) 🎯 MVP

**Goal**: Verified users can add tasks using natural language, enabling rapid task capture through conversational interface

**Independent Test**: Send message "Add task: buy groceries" and verify task is created in database with correct user isolation

### Tests for User Story 1 (TDD - Write FIRST)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T034 [P] [US1] Write unit test for add_task MCP tool in backend/mcp_server/tests/test_add_task.py (happy path, validation, isolation)
- [X] T035 [P] [US1] Write integration test for chat endpoint task creation in backend/tests/integration/test_chat_add_task.py
- [X] T036 [P] [US1] Write E2E test for natural language task creation in frontend/tests/chat/ChatInterface.test.tsx

### Implementation for User Story 1

- [X] T037 [US1] Implement agent prompt with task creation intent recognition in backend/core/services/agent_service.py
- [X] T038 [US1] Add conversation creation logic in backend/core/services/chat_service.py
- [X] T039 [US1] Add message persistence logic in backend/core/services/chat_service.py
- [X] T040 [US1] Implement chat endpoint handler for new conversations in backend/api/chat.py
- [X] T041 [US1] Create ChatInterface component in frontend/components/chat/ChatInterface.tsx using ChatKit
- [X] T042 [US1] Create chat API client in frontend/lib/chatApi.ts with JWT token attachment
- [X] T043 [US1] Create chat page in frontend/app/chat/page.tsx with email verification check
- [X] T044 [US1] Add error handling for unverified email in frontend/components/chat/EmailVerificationPrompt.tsx

**Checkpoint**: At this point, User Story 1 should be fully functional - users can add tasks via natural language

---

## Phase 4: User Story 2 - Task Listing and Querying (Priority: P2)

**Goal**: Users can view their tasks through natural language queries, enabling quick status checks without navigating the web UI

**Independent Test**: Create tasks for a user, send "Show my tasks", verify correct filtered results are returned

### Tests for User Story 2 (TDD - Write FIRST)

- [X] T045 [P] [US2] Write unit test for list_tasks MCP tool in backend/mcp_server/tests/test_list_tasks.py (all, pending, completed filters)
- [X] T046 [P] [US2] Write integration test for chat endpoint task listing in backend/tests/integration/test_chat_list_tasks.py
- [X] T047 [P] [US2] Write E2E test for natural language task queries in frontend/tests/chat/chat-list-tasks.test.tsx

### Implementation for User Story 2

- [X] T048 [US2] Add list tasks intent recognition to agent prompt in backend/core/services/agent_service.py
- [X] T049 [US2] Implement task list formatting in agent responses (numbered positions 1, 2, 3...)
- [X] T050 [US2] Add conversation history context to agent for follow-up queries
- [X] T051 [US2] Update ChatInterface to display task lists with proper formatting in frontend/components/chat/ChatInterface.tsx

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Task Completion via Natural Language (Priority: P3)

**Goal**: Users can mark tasks as complete using natural language, enabling quick status updates through conversation

**Independent Test**: Create a task, send "Mark task 1 as done", verify task's completed status is updated in database

### Tests for User Story 3 (TDD - Write FIRST)

- [X] T052 [P] [US3] Write unit test for complete_task MCP tool in backend/mcp_server/tests/test_complete_task.py (success, not found, isolation)
- [X] T053 [P] [US3] Write integration test for chat endpoint task completion in backend/tests/integration/test_chat_complete_task.py
- [X] T054 [P] [US3] Write E2E test for natural language task completion in frontend/tests/chat/chat-complete-task.test.tsx

### Implementation for User Story 3

- [X] T055 [US3] Add complete task intent recognition to agent prompt in backend/core/services/agent_service.py
- [X] T056 [US3] Implement task position to UUID mapping in agent context
- [X] T057 [US3] Add confirmation messages for task completion in agent responses

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently

---

## Phase 6: User Story 4 - Task Deletion with Confirmation (Priority: P4)

**Goal**: Users can delete tasks using natural language, with the system requiring confirmation for this destructive action

**Independent Test**: Create a task, request deletion, verify confirmation prompt appears, confirm deletion, verify task is removed

### Tests for User Story 4 (TDD - Write FIRST)

- [X] T058 [P] [US4] Write unit test for delete_task MCP tool in backend/mcp_server/tests/test_delete_task.py (success, not found, isolation)
- [X] T059 [P] [US4] Write integration test for chat endpoint task deletion with confirmation in backend/tests/integration/test_chat_delete_task.py
- [X] T060 [P] [US4] Write E2E test for natural language task deletion flow in frontend/tests/chat/chat-delete-task.test.tsx

### Implementation for User Story 4

- [X] T061 [US4] Add delete task intent recognition to agent prompt in backend/core/services/agent_service.py
- [X] T062 [US4] Implement confirmation prompt logic for destructive actions in agent
- [X] T063 [US4] Add conversation state tracking for pending confirmations
- [X] T064 [US4] Handle explicit confirmation detection ("I'm sure", "yes", "confirm")

**Checkpoint**: At this point, User Stories 1-4 should all work independently

---

## Phase 7: User Story 5 - Task Update and Modification (Priority: P5)

**Goal**: Users can update task details (title, description) using natural language, enabling task refinement through conversation

**Independent Test**: Create a task, send "Change task 1 title to 'New Title'", verify task is updated in database

### Tests for User Story 5 (TDD - Write FIRST)

- [X] T065 [P] [US5] Write unit test for update_task MCP tool in backend/mcp_server/tests/test_update_task.py (title, description, validation)
- [X] T066 [P] [US5] Write integration test for chat endpoint task updates in backend/tests/integration/test_chat_update_task.py
- [X] T067 [P] [US5] Write E2E test for natural language task updates in frontend/tests/chat/chat-update-task.test.tsx

### Implementation for User Story 5

- [X] T068 [US5] Add update task intent recognition to agent prompt in backend/core/services/agent_service.py
- [X] T069 [US5] Implement ambiguity detection for update requests ("Update task 1" → ask what to update)
- [X] T070 [US5] Add field extraction logic for title and description updates

**Checkpoint**: At this point, User Stories 1-5 should all work independently

---

## Phase 8: User Story 6 - Conversation Persistence and Resumption (Priority: P6)

**Goal**: Users' chat conversations persist across sessions, enabling them to resume conversations after closing and reopening the app

**Independent Test**: Have a conversation, close the app, reopen it, verify conversation history is loaded and displayed

### Tests for User Story 6 (TDD - Write FIRST)

- [X] T071 [P] [US6] Write unit test for conversation history loading in backend/tests/unit/test_chat_service.py (last 20 messages)
- [X] T072 [P] [US6] Write integration test for conversation resumption in backend/tests/integration/test_chat_resume.py
- [X] T073 [P] [US6] Write E2E test for conversation persistence in frontend/tests/chat/chat-persistence.test.tsx

### Implementation for User Story 6

- [X] T074 [US6] Implement conversation list query in backend/core/services/chat_service.py
- [X] T075 [US6] Create ConversationList component in frontend/components/chat/ConversationList.tsx
- [X] T076 [US6] Add conversation selection logic in frontend/app/chat/page.tsx
- [X] T077 [US6] Implement conversation history display in ChatInterface with last message preview in frontend/components/chat/ChatInterface.tsx
- [X] T078 [US6] Add conversation_id persistence in frontend (localStorage or state)

**Checkpoint**: At this point, User Stories 1-6 should all work independently

---

## Phase 9: User Story 7 - Multilingual Support (Priority: P7)

**Goal**: Users can interact with the chatbot in their preferred language (English, Roman Urdu, or Urdu), with automatic detection and response

**Independent Test**: Send messages in different languages and verify agent responds in the detected language while maintaining correct tool invocations

### Tests for User Story 7 (TDD - Write FIRST)

- [X] T079 [P] [US7] Write integration test for English language detection in backend/tests/integration/test_chat_multilingual.py
- [X] T080 [P] [US7] Write integration test for Roman Urdu language detection in backend/tests/integration/test_chat_multilingual.py
- [X] T081 [P] [US7] Write integration test for Urdu language detection in backend/tests/integration/test_chat_multilingual.py
- [X] T082 [P] [US7] Write E2E test for language switching mid-conversation in frontend/tests/chat/chat-multilingual.test.tsx

### Implementation for User Story 7

- [X] T083 [US7] Update agent system prompt with multilingual instructions in backend/core/services/agent_service.py
- [X] T084 [US7] Add language detection examples to agent prompt (English, Roman Urdu, Urdu)
- [X] T085 [US7] Verify tool parameters remain in English regardless of input language
- [X] T086 [US7] Test language switching with native speakers and adjust prompt if needed

**Checkpoint**: All user stories should now be independently functional

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T087 [P] Add comprehensive error handling for OpenRouter API failures in backend/core/services/openrouter_client.py
- [X] T088 [P] Implement retry logic with exponential backoff for API calls
- [X] T089 [P] Add logging for all chat interactions in backend/api/chat.py
- [X] T090 [P] Add logging for MCP tool invocations in backend/mcp_server/server.py
- [X] T091 [P] Optimize conversation history query with proper indexing
- [X] T092 [P] Add rate limit error handling in frontend with user-friendly messages
- [X] T093 [P] Add loading states and animations to ChatInterface in frontend/components/chat/ChatInterface.tsx
- [X] T094 [P] Ensure dark mode consistency with existing UI in frontend/components/chat/ChatInterface.tsx
- [X] T095 [P] Add conversation deletion functionality (optional enhancement) in frontend/components/chat/ConversationList.tsx
- [X] T096 [P] Update backend/CLAUDE.md with MCP server package documentation
- [ ] T097 Run quickstart.md validation and verify all setup steps work
- [ ] T098 Create deployment documentation for Hugging Face Spaces (backend) and Vercel (frontend)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-9)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4 → P5 → P6 → P7)
- **Polish (Phase 10)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories (independently testable)
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - No dependencies on other stories (independently testable)
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - No dependencies on other stories (independently testable)
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - No dependencies on other stories (independently testable)
- **User Story 6 (P6)**: Can start after Foundational (Phase 2) - No dependencies on other stories (independently testable)
- **User Story 7 (P7)**: Can start after Foundational (Phase 2) - No dependencies on other stories (independently testable)

### Within Each User Story

- Tests MUST be written and FAIL before implementation (TDD)
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- MCP tools (T022-T026) can all be implemented in parallel
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (TDD - write first):
Task: "Write unit test for add_task MCP tool in backend/mcp_server/tests/test_add_task.py"
Task: "Write integration test for chat endpoint task creation in backend/tests/integration/test_chat_add_task.py"
Task: "Write E2E test for natural language task creation in frontend/tests/chat-e2e.test.tsx"

# After tests fail, implement in sequence:
# 1. Agent prompt updates
# 2. Chat service logic
# 3. Chat endpoint handler
# 4. Frontend components
```

---

## Parallel Example: Foundational Phase

```bash
# Launch all MCP tools together (after database setup):
Task: "Implement add_task tool in backend/mcp_server/tools/add_task.py"
Task: "Implement list_tasks tool in backend/mcp_server/tools/list_tasks.py"
Task: "Implement complete_task tool in backend/mcp_server/tools/complete_task.py"
Task: "Implement delete_task tool in backend/mcp_server/tools/delete_task.py"
Task: "Implement update_task tool in backend/mcp_server/tools/update_task.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Natural Language Task Creation)
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

**MVP Deliverable**: Verified users can add tasks via natural language chat interface

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Add User Story 6 → Test independently → Deploy/Demo
8. Add User Story 7 → Test independently → Deploy/Demo
9. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (P1) - Natural Language Task Creation
   - Developer B: User Story 2 (P2) - Task Listing and Querying
   - Developer C: User Story 3 (P3) - Task Completion
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- TDD is mandatory: Write tests FIRST, ensure they FAIL, then implement
- Verify tests fail before implementing (Red-Green-Refactor)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- All MCP tools MUST enforce user_id isolation for security
- Email verification is MANDATORY for chat access (403 if not verified)
- Rate limiting is MANDATORY (10 messages/minute per user)
- Conversation history limited to last 20 messages for performance
- Stateless architecture: Agent reconstructs context from database on each request
