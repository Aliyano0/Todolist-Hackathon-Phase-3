# Quickstart Guide: Phase III - AI Chatbot Integration

**Date**: 2026-02-10
**Feature**: [spec.md](./spec.md)
**Status**: Complete

## Overview

This guide provides step-by-step instructions for setting up the development environment and implementing the AI chatbot feature for the Todo application.

**Important Context**: This is Phase 3 building on top of existing implementations:
- ✅ **Already Implemented (018-better-auth-jwt)**: User registration, login, JWT tokens, password reset with email
- ✅ **Already Implemented (019-production-deployment)**: SMTP email service (aiosmtplib), Docker containerization, production configuration
- ✅ **Already Implemented (020-frontend-ui-upgrade)**: Modern UI with animations, homepage, dashboard

**Phase 3 Adds**:
- 🆕 Email verification flow (send verification email, verify endpoint, resend endpoint, JWT claim)
- 🆕 Chat infrastructure (Conversation/Message models, MCP server, OpenAI Agents SDK, OpenRouter API)
- 🆕 Chat UI (ChatKit components, email verification prompt)
- 🆕 Multilingual support (English, Roman Urdu, Urdu)
- 🆕 Rate limiting for chat (10 messages/minute per user)

## Prerequisites

- Python 3.13+ installed
- Node.js 18+ and npm installed
- UV package manager installed (`pip install uv`)
- PostgreSQL database (Neon Serverless recommended)
- OpenRouter API account and API key
- Git repository cloned

## Environment Setup

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create UV virtual environment (if not exists)
uv venv

# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate  # Windows

# Install dependencies
uv add fastapi
uv add sqlmodel
uv add asyncpg==0.30.0
uv add python-jose[cryptography]
uv add uvicorn
uv add openrouter  # OpenRouter Python SDK
uv add openai-agents  # OpenAI Agents SDK
uv add mcp  # Official MCP SDK
uv add aiohttp  # Required for async HTTP requests

# Create MCP server package structure
mkdir -p mcp_server/tools mcp_server/tests
touch mcp_server/__init__.py
touch mcp_server/tools/__init__.py
```

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Install ChatKit
npm install @openai/chatkit-react

# Install additional dependencies if needed
npm install
```

### 3. Environment Variables

Create `.env` file in backend directory:

```bash
# Database
DATABASE_URL=postgresql+asyncpg://user:password@host:5432/database

# Authentication
JWT_SECRET_KEY=your-secret-key-minimum-32-characters-long
JWT_ALGORITHM=HS256

# OpenRouter API
OPENROUTER_API_KEY=sk-or-v1-your-openrouter-api-key-here

# Email Service (choose one: sendgrid or smtp)
EMAIL_PROVIDER=sendgrid
SENDGRID_API_KEY=SG.your-sendgrid-api-key-here
SENDGRID_FROM_EMAIL=your-verified-email@example.com
SENDGRID_FROM_NAME=Todo App

# Frontend Configuration
FRONTEND_URL=http://localhost:3000

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

Create `.env.local` file in frontend directory:

```bash
# API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Better Auth
BETTER_AUTH_SECRET=your-secret-key-here
BETTER_AUTH_URL=http://localhost:3000
```

## Database Migration

### Run Migration for Conversation Tables

```bash
# Navigate to backend directory
cd backend

# Activate virtual environment
source .venv/bin/activate

# Run Alembic migration
alembic upgrade head

# Or manually create tables using async SQLModel
python -c "
import asyncio
from database.session import engine, create_db_and_tables

async def main():
    await create_db_and_tables()
    print('Tables created successfully')

asyncio.run(main())
"
```

### Verify Tables Created

```sql
-- Connect to PostgreSQL database
psql $DATABASE_URL

-- Check tables exist
\dt

-- Expected output should include:
-- conversation
-- message
-- user (from Phase 2)
-- task (from Phase 2)

-- Verify conversation table structure
\d conversation

-- Verify message table structure
\d message
```

## Development Workflow

### 1. Start Backend Server

```bash
# Navigate to backend directory
cd backend

# Activate virtual environment
source .venv/bin/activate

# Start FastAPI server with hot reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Server should start at http://localhost:8000
# API docs available at http://localhost:8000/docs
```

### 2. Start Frontend Development Server

```bash
# Navigate to frontend directory
cd frontend

# Start Next.js development server
npm run dev

# Frontend should start at http://localhost:3000
```

### 3. Test Chat Endpoint

```bash
# Register a new user (if not exists)
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123!"
  }'

# Login to get JWT token
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123!"
  }'

# Copy the access_token from response

# Verify email (for testing, you may need to manually update database)
# UPDATE "user" SET email_verified = true WHERE email = 'test@example.com';

# Send chat message
curl -X POST http://localhost:8000/api/{user_id}/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "message": "Add task: buy groceries"
  }'
```

## Implementation Order

Follow this order for TDD implementation (see [tasks.md](./tasks.md) for detailed 92-task breakdown):

### Phase 1: Setup (T001-T006)
- Create backend/mcp_server directory structure
- Install dependencies (openrouter, agents, mcp SDKs)
- Configure environment variables
- Update CLAUDE.md files

### Phase 2: Foundational - BLOCKS all user stories (T013-T033)

**Email Verification Extension (T013-T016)** - Extends existing 018-better-auth-jwt:
1. Add send verification email to registration endpoint (uses existing SMTP service from 019)
2. Create verify email endpoint POST /api/auth/verify-email
3. Create resend verification email endpoint
4. Update JWT creation to include email_verified claim

**Database Schema (T017-T020)** - NEW for Phase 3:
1. Create Conversation and Message models
2. Run Alembic migration

**MCP Server Infrastructure (T021-T026)** - NEW for Phase 3:
1. Create MCP server entry point in backend/mcp_server/server.py
2. Implement 5 MCP tools (add_task, list_tasks, complete_task, delete_task, update_task)

**Chat Service Infrastructure (T027-T030)** - NEW for Phase 3:
1. Create chat service with conversation history loading
2. Implement OpenRouter API client wrapper
3. Implement OpenAI Agents SDK integration
4. Create chat request/response schemas

**Chat Endpoint & Rate Limiting (T031-T033)** - NEW for Phase 3:
1. Create email verification dependency (check JWT claim)
2. Implement rate limiting middleware (10 messages/minute)
3. Create chat endpoint POST /api/{user_id}/chat

### Phase 3-9: User Stories (T034-T086)
Each user story follows TDD: Write tests FIRST → Implement → Refactor

- **Phase 3 (T034-T044)**: User Story 1 - Natural Language Task Creation (MVP)
- **Phase 4 (T045-T051)**: User Story 2 - Task Listing and Querying
- **Phase 5 (T052-T057)**: User Story 3 - Task Completion
- **Phase 6 (T058-T064)**: User Story 4 - Task Deletion with Confirmation
- **Phase 7 (T065-T070)**: User Story 5 - Task Update and Modification
- **Phase 8 (T071-T078)**: User Story 6 - Conversation Persistence
- **Phase 9 (T079-T086)**: User Story 7 - Multilingual Support

### Phase 10: Polish & Cross-Cutting Concerns (T087-T098)
- Error handling, retry logic, logging
- Frontend loading states, dark mode consistency
- Documentation updates

## Testing Strategy

### Unit Tests

```bash
# Backend unit tests
cd backend
pytest tests/test_chat_service.py -v
pytest tests/test_chat_endpoint.py -v

# MCP server unit tests (inside backend)
cd backend
pytest mcp_server/tests/test_add_task.py -v
pytest mcp_server/tests/test_list_tasks.py -v
pytest mcp_server/tests/test_complete_task.py -v
pytest mcp_server/tests/test_delete_task.py -v
pytest mcp_server/tests/test_update_task.py -v

# Frontend unit tests
cd frontend
npm test -- ChatInterface.test.tsx
```

### Integration Tests

```bash
# Backend integration tests
cd backend
pytest tests/integration/ -v

# End-to-end tests
cd frontend
npm run test:e2e
```

### Manual Testing Checklist

- [ ] User can register and verify email
- [ ] Unverified user sees email verification prompt
- [ ] Verified user can access chat interface
- [ ] User can send message and receive response
- [ ] Agent correctly detects English language
- [ ] Agent correctly detects Roman Urdu language
- [ ] Agent correctly detects Urdu language
- [ ] User can add task via natural language
- [ ] User can list tasks via natural language
- [ ] User can complete task via natural language
- [ ] User can delete task with confirmation
- [ ] User can update task via natural language
- [ ] Conversation persists after page refresh
- [ ] Rate limiting blocks excessive messages
- [ ] Multi-user isolation prevents cross-user access

## Common Issues and Solutions

### Issue: OpenRouter API Key Not Working

**Solution**: Verify API key is correct and has sufficient credits
```bash
# Test API key
curl https://openrouter.ai/api/v1/models \
  -H "Authorization: Bearer $OPENROUTER_API_KEY"
```

### Issue: Database Connection Failed

**Solution**: Check DATABASE_URL format and credentials
```bash
# Test connection
python -c "
import asyncpg
import asyncio

async def test():
    conn = await asyncpg.connect('postgresql://user:pass@host/db')
    print('Connection successful')
    await conn.close()

asyncio.run(test())
"
```

### Issue: Email Verification Not Working

**Solution**: For development, manually verify email in database
```sql
UPDATE "user" SET email_verified = true WHERE email = 'test@example.com';
```

### Issue: ChatKit Not Rendering

**Solution**: Check API URL configuration and CORS settings
```typescript
// Verify API URL in frontend/.env.local
NEXT_PUBLIC_API_URL=http://localhost:8000

// Check CORS in backend/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue: Rate Limiting Too Aggressive

**Solution**: Adjust rate limit constants in backend
```python
# backend/api/chat.py
RATE_LIMIT = 10  # Increase if needed for development
RATE_WINDOW = 60  # seconds
```

## Next Steps

After completing the quickstart setup:

1. Review [data-model.md](./data-model.md) for database schema details
2. Review [contracts/chat-endpoint.yaml](./contracts/chat-endpoint.yaml) for API contract
3. Review [contracts/mcp-tools.md](./contracts/mcp-tools.md) for MCP tool specifications
4. Follow TDD workflow: Red → Green → Refactor
5. Run `/sp.tasks` to generate detailed task breakdown
6. Implement features following the task order
7. Write tests before implementation (TDD)
8. Commit frequently with descriptive messages

## Resources

- [OpenRouter API Documentation](https://openrouter.ai/docs)
- [OpenAI Agents SDK Documentation](https://github.com/openai/openai-agents-python)
- [MCP SDK Documentation](https://github.com/modelcontextprotocol/python-sdk)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [ChatKit Documentation](https://openai.github.io/chatkit-js/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)

## Support

For issues or questions:
- Check existing GitHub issues
- Review constitution.md for project principles
- Consult component-specific CLAUDE.md files
- Ask in team chat or create new issue
