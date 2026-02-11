# Research: Phase III - AI Chatbot Integration

**Date**: 2026-02-10
**Feature**: [spec.md](./spec.md)
**Status**: Complete

## Overview

This document consolidates research findings for implementing an AI-powered conversational chatbot with stateless architecture, MCP tools, multilingual support, and email verification enforcement.

## Building on Existing Foundation

**Phase 3 builds on top of completed implementations from previous phases:**

### Already Implemented (018-better-auth-jwt)
- ✅ User registration with password validation
- ✅ User login with JWT token generation (7-day validity)
- ✅ Password reset with secure tokens
- ✅ JWT verification and authentication middleware
- ✅ User model with `email_verified` and `verification_token` fields
- ✅ Protected routes with user isolation (`/api/{user_id}/tasks` pattern)

### Already Implemented (019-production-deployment)
- ✅ SMTP email service with aiosmtplib (Gmail, SendGrid, AWS SES support)
- ✅ Docker containerization with multi-stage builds
- ✅ Production configuration management (backend/core/config.py)
- ✅ Security headers middleware
- ✅ Health check endpoint
- ✅ Structured JSON logging

### Already Implemented (020-frontend-ui-upgrade)
- ✅ Modern UI with Framer Motion animations
- ✅ Homepage with hero section and features
- ✅ Dashboard with task management
- ✅ Dark mode support
- ✅ Responsive design

### Phase 3 Adds (NEW)
- 🆕 Email verification flow (send, verify, resend endpoints + JWT claim)
- 🆕 Chat infrastructure (Conversation/Message models, MCP server, agents)
- 🆕 OpenRouter API integration for LLM inference
- 🆕 OpenAI Agents SDK for intent recognition
- 🆕 ChatKit UI components for chat interface
- 🆕 Multilingual support (English, Roman Urdu, Urdu)
- 🆕 Rate limiting for chat (10 messages/minute per user)

## Technology Stack Research

### 1. OpenRouter API Integration

**Decision**: Use OpenRouter Python SDK with gpt-4o-mini model for cost-efficient LLM inference

**Rationale**:
- OpenRouter provides unified access to 300+ models through single API
- gpt-4o-mini offers good performance at lower cost compared to larger models
- Python SDK provides type-safe, async-compatible interface
- Supports conversation history through messages array

**Implementation Pattern**:
```python
from openrouter import OpenRouter
import os

with OpenRouter(api_key=os.getenv("OPENROUTER_API_KEY")) as client:
    response = client.chat.send(
        model="openai/gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a task management assistant."},
            {"role": "user", "content": "Add task: buy groceries"}
        ],
        temperature=0.7,
        max_tokens=1000
    )
    print(response.choices[0].message.content)
```

**Key Features**:
- Conversation history via messages array (system, user, assistant roles)
- Streaming support for real-time responses
- Provider preferences and zero data retention options
- Error handling with retry logic

**Alternatives Considered**:
- Direct OpenAI API: More expensive, no unified access to multiple models
- Anthropic Claude API: Good quality but higher cost, less flexibility
- Local LLM: Deployment complexity, resource requirements

### 2. OpenAI Agents SDK Integration

**Decision**: Use OpenAI Agents SDK for intent recognition and tool orchestration, with custom OpenRouter backend

**Rationale**:
- Provides robust agent framework with tool integration
- Supports function tools via @function_tool decorator
- Built-in conversation history management
- Can be adapted to use OpenRouter instead of OpenAI API

**Implementation Pattern**:
```python
from agents import Agent, Runner, function_tool

@function_tool
def add_task(user_id: str, title: str, description: str = None) -> dict:
    """Add a new task for the user."""
    # MCP tool invocation logic
    return {"task_id": "...", "status": "created", "title": title}

agent = Agent(
    name="TaskAssistant",
    instructions="You help users manage tasks via natural language. Detect language and respond accordingly.",
    tools=[add_task, list_tasks, complete_task, delete_task, update_task],
)

# Stateless execution - load history from DB
result = await Runner.run(
    agent,
    user_message,
    session=None  # We'll manage session externally via DB
)
```

**Stateless Architecture Approach**:
- Do NOT use SQLiteSession (built-in persistence)
- Load last 20 messages from database on each request
- Reconstruct conversation context manually
- Pass messages array to agent on each invocation
- Store agent response back to database after processing

**Key Features**:
- Function tool integration with type hints
- Automatic intent recognition and tool selection
- Confirmation prompts for destructive actions
- Error handling and graceful degradation

**Alternatives Considered**:
- LangChain: More complex, heavier dependencies, overkill for basic task management
- Custom intent recognition: Requires training data, less robust than LLM-based approach
- Direct LLM prompting: Less structured, harder to maintain tool integration

### 3. MCP SDK for Tool Exposure

**Decision**: Build MCP server using Official MCP SDK (Python) to expose 5 task management tools

**Rationale**:
- Standardized protocol for AI agent tool integration
- Clean separation between agent logic and tool implementation
- Supports async operations natively
- Parameter validation and error handling built-in

**Implementation Pattern**:
```python
from mcp.server import Server
from mcp.types import Tool, CallToolResult, TextContent

server = Server("task-mcp-server")

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="add_task",
            description="Add a new task for the user",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "format": "uuid"},
                    "title": {"type": "string"},
                    "description": {"type": "string"}
                },
                "required": ["user_id", "title"]
            }
        ),
        # ... other tools
    ]

@server.call_tool()
async def handle_tool(name: str, arguments: dict) -> CallToolResult:
    if name == "add_task":
        return await handle_add_task(arguments)
    # ... other tool handlers

async def handle_add_task(arguments: dict) -> CallToolResult:
    user_id = arguments["user_id"]
    title = arguments["title"]
    description = arguments.get("description")

    # Async database operation via SQLModel
    async with get_async_session() as session:
        task = Task(user_id=user_id, title=title, description=description)
        session.add(task)
        await session.commit()
        await session.refresh(task)

    return CallToolResult(
        content=[TextContent(
            type="text",
            text=f"Task created: {task.id}"
        )]
    )
```

**Key Features**:
- All tools require user_id parameter for multi-user isolation
- Async database operations via SQLModel/asyncpg
- Structured responses with success/error status
- Parameter validation via JSON schema

**Integration with FastAPI Backend**:
- MCP server runs as Python package inside backend/ directory (backend/mcp_server/)
- FastAPI chat endpoint invokes MCP tools via agent
- Agent SDK handles tool orchestration automatically
- No separate deployment needed - embedded in backend process
- Shares database connection pool with FastAPI
- **CRITICAL**: Must be inside backend/ because only backend/ is deployed to Hugging Face Spaces via git subtree push

**Alternatives Considered**:
- Direct function calls: Less standardized, harder to maintain
- REST API for tools: Additional HTTP overhead, more complex
- GraphQL: Overkill for simple tool invocations

### 4. SQLModel with asyncpg for Database Operations

**Decision**: Use SQLModel ORM with asyncpg driver for async PostgreSQL operations

**Rationale**:
- SQLModel combines SQLAlchemy and Pydantic for type-safe models
- asyncpg is the fastest PostgreSQL driver for Python
- Native async/await support for non-blocking operations
- Compatible with Neon Serverless PostgreSQL

**Implementation Pattern**:
```python
from sqlmodel import SQLModel, Field, create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import uuid

# Async engine with asyncpg
DATABASE_URL = "postgresql+asyncpg://user:pass@host/db"
async_engine = create_async_engine(DATABASE_URL, echo=True)

async_session_maker = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

# Models with UUID primary keys
class Conversation(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Message(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    conversation_id: uuid.UUID = Field(foreign_key="conversation.id", index=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", index=True)
    role: str = Field(max_length=20)  # user, assistant, tool
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Async CRUD operations
async def get_conversation_history(conversation_id: uuid.UUID, limit: int = 20):
    async with async_session_maker() as session:
        statement = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.desc()).limit(limit)

        result = await session.execute(statement)
        messages = result.scalars().all()
        return list(reversed(messages))  # Oldest first

async def create_message(conversation_id: uuid.UUID, user_id: uuid.UUID, role: str, content: str):
    async with async_session_maker() as session:
        message = Message(
            conversation_id=conversation_id,
            user_id=user_id,
            role=role,
            content=content
        )
        session.add(message)
        await session.commit()
        await session.refresh(message)
        return message
```

**Key Features**:
- UUID primary keys for all models (consistency with Phase 2)
- Async session management with context managers
- Proper indexing on foreign keys and query fields
- Connection pooling via asyncpg

**Alternatives Considered**:
- psycopg3: Good async support but slower than asyncpg
- SQLAlchemy Core: More verbose, less type-safe than SQLModel
- Raw asyncpg: No ORM benefits, more boilerplate code

### 5. OpenAI ChatKit for Frontend Chat UI

**Decision**: Use OpenAI ChatKit React components for chat interface

**Rationale**:
- Production-ready chat UI components
- Built-in message display, user input, and streaming support
- Customizable theme and styling
- Integrates with existing Next.js/React stack

**Implementation Pattern**:
```typescript
import { ChatKit, useChatKit } from '@openai/chatkit-react';

export function ChatInterface() {
  const { control, sendUserMessage } = useChatKit({
    api: {
      url: '/api/chat',  // Our FastAPI backend endpoint
      domainKey: 'todolist-chat',
    },
    theme: {
      colorScheme: 'dark',  // Match existing UI
      radius: 'round',
    },
    composer: {
      placeholder: 'Ask me to manage your tasks...',
    },
    onResponseStart: () => console.log('Agent processing...'),
    onResponseEnd: () => console.log('Agent response complete'),
    onError: (error) => console.error('Chat error:', error),
  });

  return (
    <div className="h-[600px] w-full">
      <ChatKit control={control} />
    </div>
  );
}
```

**Key Features**:
- Message history display with user/assistant roles
- Real-time streaming responses
- Dark mode support (matches existing UI)
- Error handling and loading states
- Customizable prompts and suggestions

**Integration with Backend**:
- ChatKit sends POST requests to configured API URL
- Backend returns responses in ChatKit-compatible format
- JWT token attached via Authorization header
- Email verification checked before allowing chat access

**Alternatives Considered**:
- Custom React chat UI: More development time, less polished
- react-chatbot-kit: Less feature-rich, no streaming support
- Vercel AI SDK UI: Good but less specialized for chat interfaces

### 6. Multilingual Support Strategy

**Decision**: Use LLM-based language detection with prompt engineering for multilingual responses

**Rationale**:
- gpt-4o-mini can detect and respond in multiple languages natively
- No need for separate translation service
- Maintains context and intent across languages
- Simpler architecture than dedicated language detection

**Implementation Pattern**:
```python
SYSTEM_PROMPT = """You are a task management assistant that helps users manage their todo tasks.

IMPORTANT LANGUAGE RULES:
- Detect the user's language from their message (English, Roman Urdu, or Urdu)
- Respond in the SAME language the user used
- Keep tool parameters in English (task titles can be in any language)
- If user switches languages, switch your responses accordingly

SUPPORTED LANGUAGES:
- English: Standard English
- Roman Urdu: Urdu written in Latin script (e.g., "task add karo")
- Urdu: Urdu in Arabic script (اردو)

TASK MANAGEMENT CAPABILITIES:
- Add tasks: "Add task: buy groceries" / "task add karo buy milk"
- List tasks: "Show my tasks" / "mere tasks dikhao"
- Complete tasks: "Mark task 1 as done" / "task 1 complete karo"
- Delete tasks: "Delete task 2" / "task 2 delete karo"
- Update tasks: "Change task 3 to 'New title'" / "task 3 ka title change karo"

Always confirm actions and ask for clarification if intent is ambiguous.
"""

# Language detection happens automatically via LLM
# No separate detection step needed
```

**Key Features**:
- Automatic language detection per message
- Users can switch languages mid-conversation
- Task data stored in original language (no translation)
- Tool parameters remain in English for consistency

**Alternatives Considered**:
- langdetect library: Less accurate for Roman Urdu, additional dependency
- Google Translate API: Additional cost, latency, complexity
- Separate language models: Deployment complexity, resource overhead

### 7. Rate Limiting Implementation

**Decision**: Use FastAPI middleware with in-memory rate limiting (10 messages/minute per user)

**Rationale**:
- Simple implementation for initial version
- No additional infrastructure required
- Sufficient for 50 concurrent users
- Can be upgraded to Redis-based limiting later

**Implementation Pattern**:
```python
from fastapi import Request, HTTPException
from collections import defaultdict
from datetime import datetime, timedelta
import asyncio

# In-memory rate limit tracker
rate_limit_tracker = defaultdict(list)
RATE_LIMIT = 10  # messages per minute
RATE_WINDOW = 60  # seconds

async def check_rate_limit(user_id: str):
    now = datetime.utcnow()
    cutoff = now - timedelta(seconds=RATE_WINDOW)

    # Clean old entries
    rate_limit_tracker[user_id] = [
        timestamp for timestamp in rate_limit_tracker[user_id]
        if timestamp > cutoff
    ]

    # Check limit
    if len(rate_limit_tracker[user_id]) >= RATE_LIMIT:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. Maximum {RATE_LIMIT} messages per minute."
        )

    # Record this request
    rate_limit_tracker[user_id].append(now)

@app.post("/api/{user_id}/chat")
async def chat_endpoint(user_id: str, request: ChatRequest):
    await check_rate_limit(user_id)
    # ... rest of chat logic
```

**Alternatives Considered**:
- Redis-based rate limiting: Better for distributed systems, but overkill for initial version
- slowapi library: Good but adds dependency, in-memory approach is simpler
- No rate limiting: Risk of abuse and high API costs

### 8. Email Verification Enforcement

**Decision**: Check email_verified field from JWT token before allowing chat access

**Rationale**:
- Leverages existing Better Auth JWT infrastructure
- No additional database queries needed
- Stateless verification (no session lookup)
- Clear error messages guide users to verify email

**Implementation Pattern**:
```python
from fastapi import Depends, HTTPException
from jose import jwt

async def verify_email_required(token: str = Depends(get_jwt_token)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("sub")
        email_verified = payload.get("email_verified", False)

        if not email_verified:
            raise HTTPException(
                status_code=403,
                detail="Please verify your email to use the chatbot. Check your inbox for the verification link."
            )

        return user_id
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/api/{user_id}/chat")
async def chat_endpoint(
    user_id: str,
    request: ChatRequest,
    verified_user_id: str = Depends(verify_email_required)
):
    # Verify user_id in path matches token
    if user_id != verified_user_id:
        raise HTTPException(status_code=403, detail="User ID mismatch")

    # ... rest of chat logic
```

**Frontend Integration**:
```typescript
// Check email verification status before showing chat
if (!user.emailVerified) {
  return (
    <EmailVerificationPrompt
      onResendEmail={handleResendVerification}
    />
  );
}

return <ChatInterface />;
```

**Alternatives Considered**:
- Database lookup on each request: Slower, unnecessary with JWT claims
- Separate verification endpoint: Additional HTTP request, more latency
- No email verification: Risk of spam and abuse

## Architecture Decisions

### Stateless Agent Architecture

**Decision**: Agent reconstructs conversation history from database on each request

**Flow**:
1. User sends message to POST /api/{user_id}/chat
2. Backend validates JWT and email verification
3. Backend loads last 20 messages from database
4. Backend constructs messages array for agent
5. Agent processes message with OpenRouter API
6. Agent invokes MCP tools as needed
7. Backend stores user message and agent response in database
8. Backend returns agent response to frontend

**Benefits**:
- Scalable (no server-side state)
- Survives server restarts
- Simple deployment (no session management)
- Easy to debug (all state in database)

**Trade-offs**:
- Database query overhead on each request (~100ms)
- Limited conversation history (20 messages)
- No in-memory caching of conversation context

### MCP Tools Integration

**Decision**: MCP server runs as Python package inside backend/ directory (backend/mcp_server/), not as separate service

**Rationale**:
- **CRITICAL DEPLOYMENT CONSTRAINT**: Only backend/ directory is deployed to Hugging Face Spaces via git subtree push
- Simpler deployment (single process, no separate deployment)
- Lower latency (no HTTP overhead, in-process communication)
- Easier debugging and testing
- Shares database connection pool with FastAPI
- Sufficient for initial version and production use

**Architecture**:
```
Hugging Face Spaces Deployment (backend/)
├── FastAPI Backend (main.py)
│   ├── Chat Endpoint (/api/{user_id}/chat)
│   ├── Agent Logic (OpenAI Agents SDK)
│   ├── Database (SQLModel + asyncpg)
│   └── mcp_server/ (Python package)
│       ├── __init__.py
│       ├── server.py (MCP server entry point)
│       ├── tools/
│       │   ├── __init__.py
│       │   ├── add_task.py
│       │   ├── list_tasks.py
│       │   ├── complete_task.py
│       │   ├── delete_task.py
│       │   └── update_task.py
│       └── tests/
│           ├── test_add_task.py
│           ├── test_list_tasks.py
│           ├── test_complete_task.py
│           ├── test_delete_task.py
│           └── test_update_task.py
```

**Deployment Flow**:
```bash
# Only backend/ is pushed to Hugging Face Spaces
git subtree push --prefix backend origin main

# Everything inside backend/ (including mcp_server/) is deployed together
```

**Future Scaling**:
- Current architecture is production-ready for expected load (50 concurrent users)
- If needed later, can be separated into microservice with HTTP transport
- MCP protocol supports both in-process and HTTP communication
- For MVP and Phase 3, in-process approach is optimal

## Open Questions Resolved

All technical unknowns from the Technical Context section have been resolved:

1. ✅ **OpenRouter Integration**: Use OpenRouter Python SDK with gpt-4o-mini model
2. ✅ **Agent Statefulness**: Stateless architecture with DB-backed conversation history
3. ✅ **MCP Tools**: In-process MCP server with 5 async tools
4. ✅ **SQLModel + asyncpg**: Use SQLAlchemy async engine with asyncpg driver
5. ✅ **Language Detection**: LLM-based detection via prompt engineering
6. ✅ **Rate Limiting**: In-memory rate limiting with FastAPI middleware
7. ✅ **Email Verification**: JWT claim-based verification with frontend prompts

## Next Steps

Proceed to Phase 1: Design & Contracts
- Generate data-model.md with Conversation and Message schemas
- Create API contracts for chat endpoint
- Define MCP tool contracts
- Create quickstart.md for development setup
- Update agent context files (backend/CLAUDE.md, mcp-server/CLAUDE.md, frontend/CLAUDE.md)
