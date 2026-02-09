---
id: 0002
title: Phase 3 AI Chatbot Constitution
stage: constitution
date: 2026-02-09
surface: agent
model: claude-sonnet-4-5
feature: none
branch: main
user: Aliyan Aqeel
command: /sp.constitution
labels: ["constitution", "phase-3", "ai-chatbot", "openai-agents-sdk", "mcp-server", "stateless-architecture"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - None (constitution document)
---

## Prompt

Extend the Phase 2 web app with Phase 3 Todo AI Chatbot: Integrate conversational interface for Basic Level task management (add/list/complete/delete/update) via natural language. Use OpenAI Agents SDK for AI agent logic (intent-based tool triggers, confirmations, error handling). Build MCP server with Official MCP SDK exposing stateless tools (add_task, list_tasks, complete_task, delete_task, update_task—all with user_id UUID param, async DB ops via SQLModel/asyncpg to Neon PostgreSQL). Add stateless FastAPI chat endpoint POST /api/{user_id}/chat (persist conversation/message state in DB models: Conversation/Message with UUIDs). Frontend: Add OpenAI ChatKit UI in Next.js for chat interface (send msgs with JWT, display responses/tools). Ensure auth integration (Better Auth/JWT), multi-user isolation (filter by user_id), stateless architecture. Use 'uv add' for installs (openai-agents-sdk, mcp-sdk). Test e2e NL flows, resume after restart.

## Response snapshot

Updated constitution from v2.4.0 to v2.5.0 (MINOR version bump) to incorporate Phase 3 AI Chatbot requirements.

**Key Changes:**

1. **Added Principle XI: AI Conversational Interface (Stateless Architecture)**
   - OpenAI Agents SDK for intent recognition and tool orchestration
   - MCP server with Official MCP SDK exposing stateless tools
   - All tools accept user_id UUID parameter for multi-user isolation
   - Stateless architecture: conversation state loaded from database on each request
   - Conversation and Message models for persistent chat history
   - Support for resuming conversations after restart

2. **Updated Existing Principles:**
   - Title: "Phase III: AI Chatbot Integration Constitution"
   - Principle IV: Five core features accessible via both web UI and natural language
   - Principle V: Persistent storage for both tasks and conversations
   - Principle VI: Tech stack includes OpenAI Agents SDK, MCP SDK, ChatKit
   - Principle VIII: MCP server component requires CLAUDE.md
   - Principle IX: Chat endpoint requires JWT authentication and user_id validation
   - Principle X: E2E tests required for natural language flows

3. **Updated Project Structure:**
   - Added mcp-server/ directory with tools/ subdirectory
   - Added backend/models/conversation.py and message.py
   - Added backend/api/chat.py for chat endpoint
   - Added backend/core/services/chat_service.py
   - Added backend/schemas/chat.py
   - Added frontend/app/chat/page.tsx
   - Added frontend/components/ChatInterface.tsx

4. **Updated Goals and Success Criteria:**
   - Primary goal includes conversational interface
   - Secondary goals include AI agent patterns and e2e NL tests
   - Success criteria include intent recognition and conversation persistence

5. **Updated Constraints:**
   - Technical: OpenAI Agents SDK, MCP SDK, ChatKit, 'uv add' for installs
   - Process: E2E tests required for natural language flows
   - Quality: Stateless architecture for AI agent and MCP server
   - Forbidden: Stateful AI agent logic, MCP tools without user_id parameter
   - Required: Stateless architecture, user_id parameter in all MCP tools

**Sync Impact Report:**
- Templates requiring updates: spec-template.md, plan-template.md, tasks-template.md
- All placeholders filled (no TODOs)
- Constitution committed to git with detailed commit message

## Outcome

- ✅ Impact: Constitution successfully updated to v2.5.0 with comprehensive Phase 3 AI Chatbot requirements. All architectural decisions documented with clear rationale. Stateless architecture mandate ensures scalability and multi-user isolation.
- 🧪 Tests: None (constitution is a governance document, not code)
- 📁 Files: 1 file modified (.specify/memory/constitution.md)
- 🔁 Next prompts: /sp.specify (create Phase 3 chatbot feature spec), /sp.plan (design MCP server and AI agent architecture), /sp.tasks (generate implementation tasks)
- 🧠 Reflection: The stateless architecture requirement is critical for Phase 3. By mandating that conversation state be loaded from the database on each request, we ensure scalability and enable conversation resumption after restart. The user_id parameter in all MCP tools enforces multi-user isolation at the tool level, preventing cross-user data access. This constitutional amendment provides clear guidance for implementing AI features while maintaining security and clean architecture principles.

## Evaluation notes (flywheel)

- Failure modes observed: None. Constitution update followed semantic versioning correctly (MINOR bump for new principle addition). All placeholders filled with concrete values.
- Graders run and results (PASS/FAIL): PASS - Constitution validates against all requirements: no unexplained bracket tokens, version matches report, dates in ISO format, principles are declarative and testable.
- Prompt variant (if applicable): N/A (standard /sp.constitution command)
- Next experiment (smallest change to try): Validate that spec-template.md, plan-template.md, and tasks-template.md align with new AI chatbot requirements. Consider adding AI-specific sections to templates if needed.
