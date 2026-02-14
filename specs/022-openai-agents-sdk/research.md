# Research: OpenAI Agents SDK Integration

**Feature**: 022-openai-agents-sdk
**Date**: 2026-02-12
**Purpose**: Resolve technical unknowns identified in plan.md Technical Context

## Research Questions

### 1. How to configure OpenAI Agents SDK to use OpenRouter API endpoint instead of OpenAI API?

**Decision**: Use `set_default_openai_client()` with custom `AsyncOpenAI` instance

**Rationale**:
- OpenAI Agents SDK supports custom LLM providers through the `set_default_openai_client()` function
- Any LLM provider with OpenAI-compatible API can be used by setting `base_url` and `api_key`
- OpenRouter API is OpenAI-compatible and can be used as a drop-in replacement

**Implementation Pattern**:
```python
from openai import AsyncOpenAI
from agents import set_default_openai_client

# Configure custom client for OpenRouter
custom_client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)
set_default_openai_client(custom_client)
```

**Alternatives Considered**:
- Environment variables (`EXAMPLE_BASE_URL`, `EXAMPLE_API_KEY`) - Rejected because `set_default_openai_client()` provides more explicit control and better testability
- ModelProvider class - Rejected because it operates at Runner.run level and is more complex than needed for our single-provider use case

**Source**: OpenAI Agents SDK documentation - [config.md](https://github.com/openai/openai-agents-python/blob/main/docs/config.md)

---

### 2. How to register async Python functions (MCP tools) with the Agents SDK tool registry?

**Decision**: Use `@function_tool` decorator for automatic schema extraction

**Rationale**:
- The `@function_tool` decorator automatically extracts tool name, description, and parameter schema from function signature and docstring
- Supports both sync and async functions natively
- Minimal code changes required - just add decorator to existing MCP tool functions
- SDK uses Python's `inspect` module, `griffe` for docstring parsing, and `pydantic` for schema creation

**Implementation Pattern**:
```python
from agents import Agent, function_tool
from typing_extensions import TypedDict

class AddTaskParams(TypedDict):
    user_id: str
    title: str
    description: str | None
    priority: str | None
    category: str | None

@function_tool
async def add_task(user_id: str, title: str, description: str | None = None,
                   priority: str | None = None, category: str | None = None) -> str:
    """Add a new task for the user.

    Args:
        user_id: The user ID to add the task for
        title: The task title (required)
        description: Optional task description
        priority: Optional priority (low, medium, high)
        category: Optional category
    """
    # Existing MCP tool implementation
    pass

# Register tools with agent
agent = Agent(
    name="TodoAssistant",
    tools=[add_task, list_tasks, complete_task, delete_task, update_task]
)
```

**Alternatives Considered**:
- Manual `FunctionTool` instantiation with `params_json_schema` and `on_invoke_tool` - Rejected because it requires more boilerplate code and manual schema definition when decorator approach is simpler
- Wrapping existing MCP tools without modification - Rejected because tools need to be registered directly with Agent class

**Source**: OpenAI Agents SDK documentation - [tools.md](https://github.com/openai/openai-agents-python/blob/main/docs/tools.md)

---

### 3. How does the Agents SDK handle conversation history reconstruction in stateless architecture?

**Decision**: Use manual conversation history management with `Runner.run()` and input list

**Rationale**:
- SDK supports two approaches: automatic (SQLiteSession) and manual (input list)
- Our architecture requires loading last 20 messages from PostgreSQL database (not SQLite)
- Manual approach allows us to maintain existing database schema and conversation loading logic
- We can convert database messages to SDK's input list format: `[{"role": "user"|"assistant", "content": "..."}]`

**Implementation Pattern**:
```python
from agents import Agent, Runner

# Load conversation history from database (existing logic in chat_service.py)
messages = await chat_service.load_conversation_history(user_id, conversation_id, limit=20)

# Convert database messages to SDK input format
input_list = []
for msg in messages:
    input_list.append({
        "role": msg.role,  # "user" or "assistant"
        "content": msg.content
    })

# Add new user message
input_list.append({
    "role": "user",
    "content": user_message
})

# Run agent with conversation history
result = await Runner.run(agent, input_list)

# Extract response
assistant_response = result.final_output
```

**Alternatives Considered**:
- SQLiteSession for automatic history management - Rejected because:
  - Would require migrating conversation storage from PostgreSQL to SQLite
  - Would break existing conversation persistence logic
  - Would require schema changes and data migration
  - Our requirement is to maintain existing database models unchanged
- Custom Session implementation - Rejected because manual approach is simpler and maintains existing architecture

**Source**: OpenAI Agents SDK documentation - [running_agents.md](https://github.com/openai/openai-agents-python/blob/main/docs/running_agents.md)

---

## Additional Findings

### Multi-turn Conversation State Management

**Finding**: SDK's Agent class automatically maintains state within a single `Runner.run()` call

**Implication**:
- For multi-turn conversations within a single request (e.g., agent asks clarifying question, user responds), the SDK handles state automatically
- For conversations across multiple HTTP requests, we use the manual input list approach documented above
- This aligns with our stateless architecture where each request reconstructs history from database

**Source**: OpenAI Agents SDK documentation - [sessions/index.md](https://github.com/openai/openai-agents-python/blob/main/docs/sessions/index.md)

---

### Model Configuration

**Finding**: Model name is specified in Agent initialization or Runner.run()

**Implementation**:
```python
agent = Agent(
    name="TodoAssistant",
    model="gpt-4o-mini",  # OpenRouter model name
    instructions="You are a helpful task management assistant...",
    tools=[...]
)
```

**Note**: When using OpenRouter, the model name should match OpenRouter's model identifier (e.g., "openai/gpt-4o-mini" or "gpt-4o-mini" depending on OpenRouter's API format)

---

## Summary

All three technical unknowns have been resolved:

1. ✅ **OpenRouter Configuration**: Use `set_default_openai_client()` with custom `AsyncOpenAI(base_url="https://openrouter.ai/api/v1", api_key=...)`
2. ✅ **Tool Registration**: Use `@function_tool` decorator on existing MCP tool functions and pass to `Agent(tools=[...])`
3. ✅ **Conversation History**: Use manual input list approach by converting database messages to `[{"role": "...", "content": "..."}]` format

**Next Steps**: Proceed to Phase 1 to create data-model.md, contracts/, and quickstart.md based on these research findings.
