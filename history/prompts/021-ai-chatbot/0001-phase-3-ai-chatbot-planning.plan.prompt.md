---
id: 0001
title: phase-3-ai-chatbot-planning
stage: plan
date: 2026-02-10
surface: agent
model: claude-sonnet-4-5
feature: 021-ai-chatbot
branch: 021-ai-chatbot
user: Aliyan Aqeel
command: /sp.plan
labels: ["planning", "ai-chatbot", "phase-3", "openai-agents", "mcp-server", "openrouter", "chatkit", "multilingual", "stateless-architecture", "email-verification"]
links:
  spec: specs/021-ai-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/021-ai-chatbot/plan.md
  - specs/021-ai-chatbot/research.md
  - specs/021-ai-chatbot/data-model.md
  - specs/021-ai-chatbot/contracts/chat-endpoint.yaml
  - specs/021-ai-chatbot/contracts/mcp-tools.md
  - specs/021-ai-chatbot/quickstart.md
  - CLAUDE.md (updated with Phase 3 technologies)
tests:
  - No tests yet (planning phase - tests will be created during implementation)
---

## Prompt

Execute `/sp.plan` command to create implementation plan for Phase III AI Chatbot Integration feature (021-ai-chatbot).

## Response snapshot

Completed comprehensive implementation planning for Phase III AI Chatbot Integration with the following deliverables:

**Phase 0: Research (research.md)**
- Researched 8 key technologies using Context7 MCP server
- OpenRouter API integration with gpt-4o-mini model
- OpenAI Agents SDK for stateless agent architecture
- Official MCP SDK for tool exposure (5 tools)
- SQLModel with asyncpg for async PostgreSQL operations
- OpenAI ChatKit for frontend chat UI
- Multilingual support strategy (LLM-based language detection)
- Rate limiting and email verification enforcement patterns
- All technical unknowns resolved with implementation patterns

**Phase 1: Design & Contracts**
- Created data-model.md with Conversation and Message schemas
- Defined database migration script for new tables
- Created OpenAPI specification for POST /api/{user_id}/chat endpoint
- Documented 5 MCP tools with input/output schemas and examples
- Defined query patterns and data isolation requirements
- Created quickstart.md with setup instructions and TDD workflow

**Architecture Decisions**:
- Stateless agent: Reconstructs conversation from database (last 20 messages)
- In-process MCP server: Runs with FastAPI backend (not separate HTTP service)
- LLM-based language detection: No separate translation service needed
- JWT claim-based email verification: No additional database queries
- In-memory rate limiting: 10 messages/minute per user

**Constitution Compliance**:
- ✅ Documentation-first approach using MCP servers and Context7
- ✅ Clean architecture with stateless agent and MCP tools as ports
- ✅ Tech stack compliance verified through official documentation
- ✅ TDD workflow defined with Red-Green-Refactor cycle
- ✅ Multi-user authentication with JWT and email verification
- ✅ Agent context updated with Phase 3 technologies

## Outcome

- ✅ Impact: Complete implementation plan created for Phase III AI Chatbot, ready for task generation and implementation
- 🧪 Tests: Planning phase complete - no tests yet (tests will be created during TDD implementation)
- 📁 Files: Created 6 planning artifacts (plan.md, research.md, data-model.md, 2 contract files, quickstart.md) and updated CLAUDE.md
- 🔁 Next prompts: `/sp.tasks` to generate actionable, dependency-ordered tasks for implementation
- 🧠 Reflection: Successfully completed planning phase with comprehensive research, design, and contracts. All technical unknowns resolved through Context7 documentation queries. Stateless architecture and multi-user isolation clearly specified. Ready for task generation and TDD implementation.

## Evaluation notes (flywheel)

- Failure modes observed: None - planning completed successfully with all artifacts generated
- Graders run and results (PASS/FAIL): Constitution Check - PASS (all 6 criteria met, no violations)
- Prompt variant (if applicable): Standard /sp.plan workflow for Phase III feature
- Next experiment (smallest change to try): Consider adding more specific performance benchmarks for conversation history reconstruction in future planning sessions
