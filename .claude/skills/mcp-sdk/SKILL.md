---
name: mcp-sdk
description: Build MCP servers and clients to expose tools, resources, and prompts to AI agents. Use for defining task operation tools that integrate with databases and agents in backend applications.
---

# MCP SDK Skill

## Description
The MCP (Model Context Protocol) Python SDK is the official library for implementing MCP servers and clients, allowing AI applications (like agents) to access external tools, resources, and prompts in a standardized way. It enables exposing functions as tools for LLMs to invoke, handling structured data, authentication, and more. Use this for creating tools like add_task or list_tasks that perform database operations, integrated with AI agents for task management.

Key features include tool decorators, resource exposure, prompt templates, structured outputs with Pydantic, context injection, lifespan management for dependencies (e.g., DB connections), and support for transports like Streamable HTTP.

## Instructions
- Install: `uv add "mcp[cli]"` (recommended) or `pip install "mcp[cli]"`.
- Setup: Import `MCPServer` from `mcp.server.mcpserver`.
- Define tools: Use `@mcp.tool()` decorator on async or sync functions, with type hints for parameters and returns.
- Integrate with DB: Use lifespan context to initialize DB connections (e.g., AsyncSession with SQLModel), and inject `Context` into tools for accessing DB.
- Validation: Tools automatically handle schemas; add custom validation in function body.
- Expose to agents: Run the server and connect via client or integrate with agent frameworks like OpenAI Agents SDK.
- Multilingual/Guardrails: Handle in tool logic or via agent prompts, as MCP focuses on exposure.
- Run server: Use `mcp.run(transport="streamable-http", stateless_http=True, json_response=True)` for stateless APIs.

For stateless operations in chat endpoints, recreate sessions per request and use DB for persistence.

## Examples
Basic tool definition:
```python
from mcp.server.mcpserver import MCPServer, Context

mcp = MCPServer("Task Manager")

@mcp.tool()
async def add_task(user_id: str, title: str, description: str = None, ctx: Context) -> dict:
    """Add a new task for the user."""
    db = ctx.request_context.lifespan_context.db  # Assuming DB in lifespan
    task = Task(id=uuid.uuid4(), user_id=uuid.UUID(user_id), title=title, description=description, completed=False)
    db.add(task)
    await db.commit()
    return {"task_id": str(task.id), "status": "created", "title": title}
```

Server with lifespan for DB:
```python
from contextlib import asynccontextmanager
from sqlmodel.ext.asyncio.session import AsyncSession

@asynccontextmanager
async def app_lifespan(server: MCPServer):
    engine = create_async_engine(os.getenv("DATABASE_URL"))
    async with AsyncSession(engine) as db:
        yield {"db": db}  # Inject DB into context

mcp = MCPServer("Task App", lifespan=app_lifespan)

# Add tools like above

if __name__ == "__main__":
    mcp.run(transport="streamable-http", stateless_http=True, json_response=True)
```

Integration in FastAPI endpoint (for agent invocation):
```python
from fastapi import APIRouter
from mcp.client.streamable_http import streamable_http_client
from mcp import ClientSession

router = APIRouter()

@router.post("/chat")
async def chat(message: str, user_id: str):
    async with streamable_http_client("http://localhost:8000/mcp") as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            # Invoke tool via session, or pass to agent
            result = await session.call_tool("add_task", {"user_id": user_id, "title": message})
            return {"response": result}
```

## Best Practices
- Use stateless HTTP for scalable, production-ready servers.
- Leverage Pydantic models for structured tool outputs to ensure type safety.
- Implement authentication with TokenVerifier for secure tool access.
- Use elicitation in tools for user confirmations (e.g., destructive actions).
- Handle pagination for list tools like list_tasks.
- Monitor with context logging and progress reporting for long-running tasks.
- For agent integration, use MCP clients to list and call tools dynamically.
- Check the official GitHub for updates: https://github.com/modelcontextprotocol/python-sdk.
