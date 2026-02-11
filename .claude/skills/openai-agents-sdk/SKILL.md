---
name: openai-agents-sdk
description: Build lightweight AI agents using OpenAI's models for logic, tool invocations, and task handling. Use for creating agents that process user inputs, invoke tools, and maintain sessions in backend applications.
---

# OpenAI Agents SDK Skill

## Description
The OpenAI Agents SDK is a Python library for building AI agents powered by OpenAI models. It provides a lightweight, Python-first approach to creating agents with instructions, tools, and session management. Use this for implementing core agent logic that handles natural language processing, tool calls, and responses in applications like chatbots.

Key features include agent loops for multi-step reasoning, function tools for integrations, session persistence, built-in tracing, guardrails, and support for realtime agents.

## Instructions
- Install: `uv add openai-agents`.
- Setup: Set the `OPENAI_API_KEY` (In user case `OPENROUTER_API_KEY`) environment variable for authentication.
- Import core classes: Use `Agent` to define the agent and `Runner` to execute tasks.
- Define an agent: Provide a name and instructions (system prompt) to guide behavior.
- Run the agent: Use `Runner.run_sync(agent, message)` for synchronous execution or `Runner.run(agent, message)` for async.
- Tool integration: Add function tools to the agent for custom operations (e.g., MCP tools like add_task). Tools are defined as Python functions and passed to the agent.
- Stateless operations: Use sessions for persistence if needed, but for stateless setups, recreate the agent per request and pass full conversation history.
- Guardrails: Incorporate instructions in the agent's prompt for intent mapping, language handling, confirmations, and scope limitations.
- Multilingual support: Handle via prompt instructions, as the SDK relies on the underlying LLM.

Note: For integration with third-party LLM routers like OpenRouter, use a compatible client by customizing the base URL and API key in the OpenAI client configuration (not natively supported in the SDK; requires openai-python adjustments).

## Examples
Basic example for a simple agent:
```python
from agents import Agent, Runner

agent = Agent(name="Assistant", instructions="You are a helpful assistant that manages tasks via tools.")
# Add tools here, e.g., agent.tools = [add_task, list_tasks]
result = Runner.run_sync(agent, "Add a task to buy groceries.")
print(result)
```

For a stateless chat endpoint in FastAPI:
```python
from agents import Agent, Runner
from fastapi import APIRouter

router = APIRouter()

@router.post("/chat")
async def chat(message: str):
    agent = Agent(name="TaskAgent", instructions="Handle task management via tools only.")
    # Reconstruct history from DB if needed
    history = [{"role": "user", "content": "Previous message"}]  # Example
    full_input = history + [{"role": "user", "content": message}]
    result = await Runner.run(agent, full_input)  # Assuming async run
    return {"response": result}
```

## Best Practices
- Keep agents lightweight: Use for focused tasks to avoid token bloat.
- Tracing: Enable built-in tracing for debugging tool calls and loops.
- Error handling: Wrap runs in try-except to manage API errors.
- Sessions: For persistent conversations, use the SDK's session features instead of DB-only storage.
- Updates: Check the official docs for new features like enhanced realtime support or additional guardrails.
- For third-party LLMs: Customize the OpenAI client in the SDK to point to your router's endpoint, ensuring compatibility with the expected API format.