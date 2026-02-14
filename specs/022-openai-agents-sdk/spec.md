# Feature Specification: OpenAI Agents SDK Integration

**Feature Branch**: `022-openai-agents-sdk`
**Created**: 2026-02-12
**Status**: Draft
**Input**: User description: "Reimplement AI agent system using OpenAI Agents SDK for proper agentic workflow instead of basic function calling. Current implementation (021-ai-chatbot) uses direct OpenRouter API calls with manual tool orchestration in agent_service.py, which does not leverage the OpenAI Agents SDK's capabilities for agent state management, multi-turn reasoning, and tool orchestration."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Agent SDK Tool Orchestration (Priority: P1) 🎯 MVP

The system must use OpenAI Agents SDK to automatically orchestrate tool calls based on user intent, replacing the current manual function calling implementation.

**Why this priority**: This is the core requirement and primary reason for this feature. Without proper SDK integration, the agent lacks state management, multi-turn reasoning, and automatic tool orchestration capabilities. This is the foundation that enables all other improvements.

**Independent Test**: Can be fully tested by sending a task management request (e.g., "add task: buy groceries") and verifying that the Agents SDK Agent class handles tool selection, execution, and response generation automatically. Delivers immediate value by providing proper agentic workflow with state management.

**Acceptance Scenarios**:

1. **Given** a user sends "add task: buy groceries", **When** the agent processes the message, **Then** the Agents SDK automatically selects and executes the add_task tool without manual orchestration code
2. **Given** a user sends "show my tasks", **When** the agent processes the message, **Then** the Agents SDK automatically selects and executes the list_tasks tool
3. **Given** a user sends an ambiguous request, **When** the agent processes the message, **Then** the Agents SDK manages the conversation state and asks clarifying questions
4. **Given** a tool execution fails, **When** the agent handles the error, **Then** the Agents SDK manages error recovery and provides user-friendly feedback
5. **Given** multiple tool calls are needed, **When** the agent processes the request, **Then** the Agents SDK orchestrates the sequence automatically
6. **Given** the agent is processing a request, **When** checking the implementation, **Then** agent_service.py uses the Agent class from openai-agents SDK, not manual function calling

---

### User Story 2 - OpenRouter LLM Provider Configuration (Priority: P1) 🎯 MVP

The OpenAI Agents SDK must be configured to use OpenRouter API as the LLM provider instead of OpenAI API, using the OPENROUTER_API_KEY environment variable.

**Why this priority**: This is a critical requirement because the system must use OpenRouter for cost efficiency (gpt-4o-mini model) rather than paid OpenAI API. Without this configuration, the feature cannot be deployed.

**Independent Test**: Can be fully tested by verifying that all LLM calls go to OpenRouter's API endpoint (https://openrouter.ai/api/v1) using the OPENROUTER_API_KEY, and that no calls are made to OpenAI's API. Delivers value by maintaining cost-effective LLM usage.

**Acceptance Scenarios**:

1. **Given** the agent is initialized, **When** checking the LLM client configuration, **Then** it points to OpenRouter's API endpoint
2. **Given** the agent makes an LLM call, **When** monitoring network requests, **Then** the request goes to openrouter.ai, not api.openai.com
3. **Given** the OPENROUTER_API_KEY is set, **When** the agent initializes, **Then** it uses this key for authentication
4. **Given** the OPENROUTER_API_KEY is missing, **When** the agent initializes, **Then** it fails with a clear error message
5. **Given** the agent processes a message, **When** the LLM responds, **Then** the response comes from the gpt-4o-mini model via OpenRouter

---

### User Story 3 - Multi-Turn Conversation State Management (Priority: P2)

The agent must handle multi-turn conversations with proper state management, enabling it to ask clarifying questions, remember context, and handle complex multi-step interactions.

**Why this priority**: This enhances the agent's capabilities beyond basic single-turn interactions. While not critical for MVP, it significantly improves user experience by enabling natural conversational flows.

**Independent Test**: Can be fully tested by initiating a multi-turn conversation (e.g., "update task 1" → agent asks "what do you want to change?" → user responds "change title to X") and verifying that the agent maintains context across turns.

**Acceptance Scenarios**:

1. **Given** a user sends an incomplete request, **When** the agent processes it, **Then** the agent asks a clarifying question and waits for response
2. **Given** the agent asked a clarifying question, **When** the user responds, **Then** the agent remembers the original intent and completes the action
3. **Given** a user sends "delete task 2", **When** the agent processes it, **Then** the agent asks for confirmation and waits for user response
4. **Given** the agent asked for confirmation, **When** the user confirms, **Then** the agent executes the deletion using the remembered task ID
5. **Given** a multi-step task operation, **When** the agent processes it, **Then** the agent maintains state across multiple tool calls

---

### User Story 4 - Existing Functionality Preservation (Priority: P2)

All existing chat functionality must work identically from the user's perspective, including conversation persistence, rate limiting, email verification, multilingual support, and user isolation.

**Why this priority**: This ensures no regression in existing features. Users should not notice any difference in functionality, only improvements in agent behavior.

**Independent Test**: Can be fully tested by running the existing test suite and verifying that all tests pass without modification. Delivers value by ensuring backward compatibility.

**Acceptance Scenarios**:

1. **Given** a user with unverified email, **When** they try to use chat, **Then** they receive a 403 error requiring email verification
2. **Given** a user sends 11 messages in one minute, **When** the rate limiter checks, **Then** the 11th message is rejected with 429 error
3. **Given** a user sends a message in Roman Urdu, **When** the agent responds, **Then** the response is in Roman Urdu
4. **Given** a user sends a message in Urdu script, **When** the agent responds, **Then** the response is in Urdu script
5. **Given** a user's conversation, **When** they close and reopen chat, **Then** the conversation history is loaded from database
6. **Given** user A and user B both have tasks, **When** user A asks for tasks, **Then** only user A's tasks are returned (user isolation verified)

---

### User Story 5 - MCP Tools Integration (Priority: P3)

All existing MCP tools (add_task, list_tasks, complete_task, delete_task, update_task) must be registered with the Agents SDK and work seamlessly.

**Why this priority**: This ensures the agent can perform all task management operations. While critical for functionality, it's P3 because the tools themselves don't change, only how they're registered.

**Independent Test**: Can be fully tested by verifying that each MCP tool can be called by the agent and returns expected results. Delivers value by maintaining all task management capabilities.

**Acceptance Scenarios**:

1. **Given** the agent is initialized, **When** checking registered tools, **Then** all 5 MCP tools are registered with the Agents SDK
2. **Given** a user requests to add a task, **When** the agent processes it, **Then** the add_task tool is called with correct parameters
3. **Given** a user requests to list tasks, **When** the agent processes it, **Then** the list_tasks tool is called with user_id for isolation
4. **Given** a user requests to complete a task, **When** the agent processes it, **Then** the complete_task tool is called with correct task_id
5. **Given** a user requests to delete a task, **When** the agent processes it, **Then** the delete_task tool is called after confirmation
6. **Given** a user requests to update a task, **When** the agent processes it, **Then** the update_task tool is called with new values

---

### Edge Cases

- What happens when the OpenAI Agents SDK encounters an unexpected error during tool orchestration?
- How does the agent handle tool calls that timeout or fail to respond?
- What happens when the agent needs to call multiple tools in sequence but one fails midway?
- How does the system handle conversation state when the agent is restarted mid-conversation?
- What happens when the OpenRouter API rate limit is exceeded?
- How does the agent handle malformed tool responses from MCP tools?
- What happens when a user sends a message while the agent is still processing a previous message?
- How does the agent handle very long conversation histories that exceed context window limits?

## Requirements *(mandatory)*

### Functional Requirements

**OpenAI Agents SDK Integration:**

- **FR-001**: System MUST use OpenAI Agents SDK (openai-agents==0.8.3) Agent class for all agent operations
- **FR-002**: System MUST NOT use manual function calling or tool orchestration code in agent_service.py
- **FR-003**: Agent MUST be initialized with proper configuration for tool registration and state management
- **FR-004**: Agent MUST handle tool selection, execution, and response generation automatically via the SDK

**OpenRouter LLM Provider Configuration:**

- **FR-005**: System MUST configure OpenAI Agents SDK to use OpenRouter API as the LLM provider
- **FR-006**: System MUST use OPENROUTER_API_KEY environment variable for authentication
- **FR-007**: System MUST point all LLM calls to OpenRouter's API endpoint (https://openrouter.ai/api/v1)
- **FR-008**: System MUST use gpt-4o-mini model via OpenRouter for all LLM inference
- **FR-009**: System MUST NOT make any calls to OpenAI's API (api.openai.com)
- **FR-010**: System MUST fail gracefully with clear error message if OPENROUTER_API_KEY is not set

**MCP Tools Registration:**

- **FR-011**: System MUST register add_task tool with the Agents SDK
- **FR-012**: System MUST register list_tasks tool with the Agents SDK
- **FR-013**: System MUST register complete_task tool with the Agents SDK
- **FR-014**: System MUST register delete_task tool with the Agents SDK
- **FR-015**: System MUST register update_task tool with the Agents SDK
- **FR-016**: All tool registrations MUST include proper parameter schemas and descriptions
- **FR-017**: All tools MUST maintain user_id parameter for user isolation

**Conversation State Management:**

- **FR-018**: Agent MUST maintain conversation state across multiple turns within a single request
- **FR-019**: Agent MUST be able to ask clarifying questions and wait for user responses
- **FR-020**: Agent MUST remember context from previous turns in the same conversation
- **FR-021**: Agent MUST handle confirmation flows (e.g., delete confirmation) with state preservation
- **FR-022**: Agent MUST reconstruct conversation history from database on each request (stateless architecture)

**Existing Functionality Preservation:**

- **FR-023**: System MUST maintain conversation persistence in database (Conversation and Message models)
- **FR-024**: System MUST maintain rate limiting (10 messages per minute per user)
- **FR-025**: System MUST maintain email verification requirement (403 if not verified)
- **FR-026**: System MUST maintain multilingual support (English, Roman Urdu, Urdu)
- **FR-027**: System MUST maintain user isolation (all tool calls filtered by user_id)
- **FR-028**: System MUST preserve existing chat endpoint (POST /api/{user_id}/chat)
- **FR-029**: System MUST preserve existing request/response schemas (ChatRequest, ChatResponse)
- **FR-030**: System MUST load last 5 messages from conversation history on each request (optimized for performance)

**Implementation Constraints:**

- **FR-031**: System SHOULD minimize changes to files outside agent_service.py where possible
- **FR-032**: System MAY modify MCP tools if required for feature enhancements (e.g., priority/category support)
- **FR-033**: System MAY modify chat endpoint for performance optimizations (e.g., singleton service, history limit)
- **FR-034**: System MUST NOT modify database models (Conversation, Message)
- **FR-035**: System MUST NOT modify chat schemas (backend/schemas/chat.py)

**Performance Requirements:**

- **FR-036**: System MUST optimize conversation history loading (reduced from 20 to 5 messages)
- **FR-037**: System MUST optimize agent instructions for token efficiency (target: <600 tokens)
- **FR-038**: System MUST use singleton AgentService instance to avoid per-request initialization
- **FR-039**: System MUST optimize database queries (use JOIN instead of multiple queries)
- **FR-040**: System MUST disable unnecessary SDK features (e.g., tracing) for performance

**Error Handling:**

- **FR-041**: Agent MUST handle tool execution errors gracefully with user-friendly messages
- **FR-042**: Agent MUST handle OpenRouter API errors with retry logic and fallback responses
- **FR-043**: Agent MUST handle conversation state errors without crashing
- **FR-044**: Agent MUST log all errors with sufficient context for debugging
- **FR-045**: Agent MUST handle timeout errors from tools or LLM calls

### Key Entities

- **Agent**: The OpenAI Agents SDK Agent instance that manages conversation state, tool orchestration, and LLM interactions. Configured to use OpenRouter API as LLM provider and registered with all MCP tools.

- **LLM Client**: The configured client that connects the Agents SDK to OpenRouter's API endpoint, using OPENROUTER_API_KEY for authentication and gpt-4o-mini model for inference.

- **Tool Registry**: The collection of MCP tools registered with the Agents SDK, including their parameter schemas, descriptions, and execution functions.

- **Conversation State**: The agent's internal state that tracks multi-turn conversations, pending confirmations, and context across turns within a single request.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Agent successfully orchestrates tool calls using OpenAI Agents SDK without manual function calling code in 100% of cases
- **SC-002**: All LLM calls go to OpenRouter API endpoint (verified through network monitoring) in 100% of cases
- **SC-003**: All existing chat functionality tests pass without modification (100% backward compatibility)
- **SC-004**: Agent handles multi-turn conversations with proper state management in 95%+ of test scenarios
- **SC-005**: Agent response time remains under 5 seconds for simple queries (no performance regression)
- **SC-006**: All 5 MCP tools are successfully registered and callable by the agent (verified through tool registry inspection)
- **SC-007**: User isolation is maintained across all tool calls (verified through automated tests)
- **SC-008**: Multilingual support works correctly for English, Roman Urdu, and Urdu with 90%+ accuracy
- **SC-009**: Rate limiting and email verification enforcement work identically to current implementation (100% of cases)
- **SC-010**: Agent handles tool execution errors gracefully without crashing in 100% of cases

## Scope *(mandatory)*

### In Scope

- Reimplementing agent_service.py to use OpenAI Agents SDK Agent class
- Configuring Agents SDK to use OpenRouter API as LLM provider
- Registering all 5 MCP tools with the Agents SDK
- Implementing proper conversation state management within the SDK
- Maintaining all existing functionality (conversation persistence, rate limiting, email verification, multilingual support, user isolation)
- Error handling and logging for SDK-related operations
- Testing and validation of SDK integration

### Out of Scope

- Modifying MCP server package or tools
- Modifying chat endpoint or API routes
- Modifying database models or schemas
- Modifying frontend components
- Adding new MCP tools or capabilities
- Changing conversation persistence mechanism
- Changing rate limiting implementation
- Changing email verification logic
- Changing multilingual support mechanism
- Performance optimization beyond maintaining current levels
- Adding new features beyond SDK integration

## Assumptions *(mandatory)*

1. **OpenAI Agents SDK Compatibility**: The openai-agents==0.8.3 package supports custom LLM providers and can be configured to use OpenRouter API
2. **OpenRouter API Compatibility**: OpenRouter's API is compatible with OpenAI's API format and can be used as a drop-in replacement
3. **Tool Registration Format**: The Agents SDK supports registering async Python functions as tools with parameter schemas
4. **State Management**: The Agents SDK's state management is compatible with the stateless architecture (reconstructing from database)
5. **Conversation History**: The Agents SDK can accept conversation history as input for context reconstruction
6. **Error Handling**: The Agents SDK provides hooks or mechanisms for custom error handling
7. **Multilingual Support**: The Agents SDK does not interfere with multilingual prompt engineering
8. **Performance**: The Agents SDK does not introduce significant performance overhead compared to direct API calls
9. **Environment Variables**: The OPENROUTER_API_KEY environment variable is already configured in production
10. **Testing**: Existing test suite can be used to validate backward compatibility

## Dependencies *(mandatory)*

### External Dependencies

- **OpenAI Agents SDK**: openai-agents==0.8.3 (already installed)
- **OpenRouter API**: External LLM provider service (already in use)
- **MCP Tools**: Existing 5 tools in backend/mcp_server/tools/ (no changes needed)

### Internal Dependencies

- **Chat Service**: backend/core/services/chat_service.py (loads conversation history)
- **OpenRouter Client**: backend/core/services/openrouter_client.py (may need modification for SDK integration)
- **Chat Endpoint**: backend/api/chat.py (calls agent_service, no changes needed)
- **Database Models**: Conversation and Message models (no changes needed)
- **Rate Limiter**: backend/api/middleware/rate_limit.py (no changes needed)
- **Email Verification**: Authentication dependency (no changes needed)

### Blocking Dependencies

None - all dependencies are already in place and functional.

## Non-Functional Requirements *(optional)*

### Performance

- Agent response time must remain under 5 seconds for simple queries (no regression)
- Agent response time must remain under 10 seconds for complex multi-tool queries (no regression)
- Memory usage must not increase significantly (< 20% increase acceptable)

### Reliability

- Agent must handle 100% of tool execution errors gracefully without crashing
- Agent must maintain 99.9% uptime (same as current implementation)
- Agent must recover from transient OpenRouter API errors with retry logic

### Maintainability

- Code must be well-documented with clear explanations of SDK usage
- Agent initialization and configuration must be centralized and easy to modify

---

## Implementation Notes *(post-implementation)*

### Additional Work Completed (Outside Original Scope)

#### 1. Priority and Category Update Support

**Issue Identified**: During user testing, it was discovered that the chatbot couldn't update task priority or category fields - it would write these values into the description field instead.

**Root Cause**: The `update_task` MCP tool only supported updating `title` and `description` fields, not `priority` or `category`.

**Solution Implemented**:
- Extended `update_task_tool` in `backend/mcp_server/tools/update_task.py` to support priority and category parameters
- Added priority validation (low/medium/high)
- Updated agent wrapper function in `backend/core/services/agent_service.py` with new parameters
- Enhanced agent instructions with priority/category usage examples

**Impact**: Users can now update priority and category via natural language:
- "Change task 1 priority to high"
- "Set task 2 category to work"
- "Add high priority task: finish report"

**Validation**: ✅ User confirmed working correctly

#### 2. Performance Optimizations

**Issue Identified**: Response time increased from 11s to 23-25s after priority/category feature was added.

**Root Cause**: Verbose agent instructions (1,400 tokens) were being sent with every request to the LLM.

**Optimizations Applied**:
1. **Streamlined Agent Instructions**: Reduced from 1,400 to 550 tokens (60% reduction)
   - Removed verbose examples and explanations
   - Used concise arrow notation for examples
   - Maintained all functionality with less verbosity

2. **Reduced Conversation History**: Changed from 20 to 5 messages (75% reduction)
   - Files: `chat_service.py`, `chat.py`
   - Most conversations don't need 20 messages of context
   - 5 messages sufficient for task management operations

3. **Optimized Database Query**: Combined 2 queries into 1 JOIN query
   - File: `chat_service.py`
   - Eliminated separate conversation verification query
   - User isolation maintained via JOIN condition

4. **Singleton AgentService**: Module-level initialization instead of per-request
   - File: `chat.py`
   - Eliminated initialization overhead on every request
   - Agent instance already initialized at module load

5. **Disabled SDK Tracing**: Eliminated 401 errors to api.openai.com
   - File: `agent_service.py`
   - Added `disable_tracing()` call at module load
   - Removed unnecessary telemetry calls

**Expected Impact**: 70-80% improvement from 23-25s baseline
**Validation**: Awaiting production testing

#### 3. Files Modified (Beyond Original Scope)

**Originally Planned**:
- `backend/core/services/agent_service.py` (complete rewrite)

**Actually Modified**:
- `backend/core/services/agent_service.py` (complete rewrite + priority/category + optimizations)
- `backend/mcp_server/tools/update_task.py` (added priority/category support)
- `backend/core/services/chat_service.py` (optimized query, reduced history limit)
- `backend/api/chat.py` (singleton service, reduced history limit)
- `backend/core/services/openrouter_client.py` (deleted - replaced by SDK's AsyncOpenAI client)

**Rationale**: Performance optimizations and user-requested features required changes beyond the original scope to deliver a production-ready implementation.

---
- Tool registration must be modular and easy to extend

### Security

- OPENROUTER_API_KEY must be stored securely in environment variables
- User isolation must be maintained across all tool calls (no cross-user data access)
- Error messages must not expose sensitive information or API keys

## Open Questions *(optional)*

None - all requirements are clear and well-defined based on the feature description and existing implementation.
