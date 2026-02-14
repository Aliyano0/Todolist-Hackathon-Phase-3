# Quickstart: OpenAI Agents SDK Integration

**Feature**: 022-openai-agents-sdk
**Date**: 2026-02-12
**Audience**: Developers implementing or maintaining the agent service

## Overview

This guide explains how the OpenAI Agents SDK integration works in `backend/core/services/agent_service.py`. The implementation replaces manual function calling with proper SDK-based agent orchestration while maintaining 100% backward compatibility.

## Architecture

```
User Request (POST /api/{user_id}/chat)
    ↓
Chat Endpoint (backend/api/chat.py)
    ↓
Chat Service (loads last 20 messages from DB)
    ↓
Agent Service (NEW: OpenAI Agents SDK) ← This file is modified
    ↓
OpenRouter API (gpt-4o-mini via custom client)
    ↓
MCP Tools (add_task, list_tasks, etc.) ← Unchanged
    ↓
Database (TodoTask operations)
```

## Key Components

### 1. Custom OpenAI Client Configuration

Configure the SDK to use OpenRouter API instead of OpenAI API:

```python
from openai import AsyncOpenAI
from agents import set_default_openai_client
import os

# Initialize custom client for OpenRouter
custom_client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# Set as default client for all agents
set_default_openai_client(custom_client)
```

**Why**: OpenRouter provides cost-effective access to gpt-4o-mini model. The SDK supports any OpenAI-compatible API through custom client configuration.

### 2. Tool Registration with @function_tool

Decorate existing MCP tool functions to register them with the SDK:

```python
from agents import function_tool

@function_tool
async def add_task(
    user_id: str,
    title: str,
    description: str | None = None,
    priority: str | None = None,
    category: str | None = None
) -> str:
    """Add a new task for the user.

    Args:
        user_id: The user ID to add the task for
        title: The task title (required)
        description: Optional task description
        priority: Optional priority (low, medium, high)
        category: Optional category
    """
    # Existing MCP tool implementation
    async with get_session() as session:
        # ... existing logic ...
        return f"Task '{title}' added successfully"
```

**Why**: The `@function_tool` decorator automatically extracts tool name, description, and parameter schema from the function signature and docstring. No manual schema definition needed.

### 3. Agent Initialization

Create the agent with tools and instructions:

```python
from agents import Agent

agent = Agent(
    name="TodoAssistant",
    model="gpt-4o-mini",
    instructions="""You are a helpful task management assistant.

    You help users manage their todo tasks in English, Roman Urdu, and Urdu.
    Always respond in the same language the user uses.

    Available tools:
    - add_task: Add a new task
    - list_tasks: List user's tasks (optionally filter by status)
    - complete_task: Mark a task as completed
    - delete_task: Delete a task
    - update_task: Update task details

    Always confirm actions before executing destructive operations like delete.
    """,
    tools=[add_task, list_tasks, complete_task, delete_task, update_task]
)
```

**Why**: The Agent class encapsulates all agent configuration including model, instructions, and available tools. The SDK handles tool selection and orchestration automatically.

### 4. Conversation History Management

Convert database messages to SDK input format:

```python
from agents import Runner

async def process_message(user_id: str, message: str, conversation_id: str | None):
    # Load conversation history from database (existing logic)
    messages = await chat_service.load_conversation_history(
        user_id, conversation_id, limit=20
    )

    # Convert to SDK input format
    input_list = []
    for msg in messages:
        input_list.append({
            "role": msg.role,  # "user" or "assistant"
            "content": msg.content
        })

    # Add new user message
    input_list.append({
        "role": "user",
        "content": message
    })

    # Run agent with conversation history
    result = await Runner.run(agent, input_list)

    # Extract response
    return result.final_output
```

**Why**: Our stateless architecture requires loading conversation history from PostgreSQL on each request. The SDK accepts a list of messages in OpenAI format, allowing us to maintain existing database schema.

## Complete Flow Example

```python
# 1. User sends message via POST /api/{user_id}/chat
# Request: {"message": "add task: buy groceries", "conversation_id": "uuid"}

# 2. Chat endpoint validates JWT and email verification

# 3. Chat service loads last 20 messages from database
messages = await load_conversation_history(user_id, conversation_id, limit=20)

# 4. Agent service processes message
input_list = convert_messages_to_input_list(messages)
input_list.append({"role": "user", "content": "add task: buy groceries"})

# 5. SDK runs agent with conversation history
result = await Runner.run(agent, input_list)
# SDK automatically:
# - Analyzes user intent
# - Selects add_task tool
# - Executes tool with parameters: user_id, title="buy groceries"
# - Generates natural language response

# 6. Response returned to user
# Response: {"response": "Task 'buy groceries' added successfully", "conversation_id": "uuid"}
```

## Multi-turn Conversation Example

```python
# Turn 1
User: "add task: buy groceries"
Agent: "Task 'buy groceries' added successfully"

# Turn 2 (agent remembers context)
User: "mark it as high priority"
Agent: [SDK automatically understands "it" refers to the last task]
       [Calls update_task with task_id and priority="high"]
       "Task updated to high priority"

# Turn 3 (agent asks clarifying question)
User: "delete task 2"
Agent: "Are you sure you want to delete task 'buy groceries'? This cannot be undone."
User: "yes"
Agent: [Calls delete_task with task_id=2]
       "Task deleted successfully"
```

**Why**: The SDK maintains conversation state automatically within a single `Runner.run()` call, enabling natural multi-turn interactions.

## Error Handling

```python
try:
    result = await Runner.run(agent, input_list)
    return result.final_output
except Exception as e:
    logger.error(f"Agent processing error: {e}")
    return "I encountered an error processing your request. Please try again."
```

**Why**: Graceful error handling ensures the chat endpoint always returns a user-friendly response even if the agent or tools fail.

## Testing

### Unit Tests
```python
# Test agent initialization
def test_agent_initialization():
    assert agent.name == "TodoAssistant"
    assert len(agent.tools) == 5

# Test tool registration
def test_tools_registered():
    tool_names = [t.name for t in agent.tools if isinstance(t, FunctionTool)]
    assert "add_task" in tool_names
    assert "list_tasks" in tool_names
```

### Integration Tests
```python
# Test end-to-end flow
async def test_add_task_flow():
    result = await Runner.run(agent, [
        {"role": "user", "content": "add task: test task"}
    ])
    assert "added successfully" in result.final_output.lower()
```

### Backward Compatibility Tests
```python
# Existing test suite must pass without modification
async def test_chat_endpoint():
    response = await client.post(
        f"/api/{user_id}/chat",
        json={"message": "add task: test", "conversation_id": None},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "response" in response.json()
```

## Environment Variables

```bash
# Required
OPENROUTER_API_KEY=your_openrouter_api_key

# Already configured (no changes)
DATABASE_URL=postgresql+asyncpg://...
JWT_SECRET_KEY=your_jwt_secret
```

## Deployment Checklist

- [ ] Verify OPENROUTER_API_KEY is set in production environment
- [ ] Run existing test suite - all tests must pass
- [ ] Test chat functionality manually from frontend
- [ ] Verify multilingual support (English, Roman Urdu, Urdu)
- [ ] Confirm rate limiting works (10 messages/minute)
- [ ] Check error handling and logging
- [ ] Monitor OpenRouter API usage and costs

## Troubleshooting

### Issue: Agent not using OpenRouter API
**Solution**: Verify `set_default_openai_client()` is called before agent initialization

### Issue: Tools not being called
**Solution**: Check tool docstrings are properly formatted and parameters have type hints

### Issue: Conversation history not working
**Solution**: Verify messages are converted to correct format: `[{"role": "user"|"assistant", "content": "..."}]`

### Issue: Performance regression
**Solution**: Check OpenRouter API latency and consider caching or optimization

## Next Steps

After implementation:
1. Run `/sp.tasks` to generate detailed implementation tasks
2. Follow TDD workflow: write tests first, then implement
3. Update `backend/CLAUDE.md` with OpenAI Agents SDK integration details
4. Create PR with comprehensive testing evidence
