---
id: 0001
title: openai-agents-sdk-specification
stage: spec
date: 2026-02-12
surface: agent
model: claude-sonnet-4-5
feature: 022-openai-agents-sdk
branch: 022-openai-agents-sdk
user: aliyan
command: /sp.specify
labels: ["specification", "openai-agents-sdk", "agent-system", "llm-integration", "openrouter"]
links:
  spec: specs/022-openai-agents-sdk/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/022-openai-agents-sdk/spec.md
  - specs/022-openai-agents-sdk/checklists/requirements.md
tests:
  - None (specification phase)
---

## Prompt

Reimplement AI agent system using OpenAI Agents SDK for proper agentic workflow instead of basic function calling. Current implementation (021-ai-chatbot) uses direct OpenRouter API calls with manual tool orchestration in agent_service.py, which does not leverage the OpenAI Agents SDK's capabilities for agent state management, multi-turn reasoning, and tool orchestration.

Requirements:
1. Use OpenAI Agents SDK (openai-agents==0.8.3 already installed) for agent creation and orchestration
2. Configure OpenAI Agents SDK to use OpenRouter API as the LLM provider (use OPENROUTER_API_KEY environment variable, NOT OpenAI API key)
3. Register existing MCP tools (add_task, list_tasks, complete_task, delete_task, update_task) with the Agents SDK
4. Maintain all existing functionality: conversation persistence, rate limiting, email verification, multilingual support, user isolation
5. Keep existing MCP server package (backend/mcp_server/) unchanged - only modify agent_service.py
6. Preserve existing chat endpoint (POST /api/{user_id}/chat) and schemas
7. Agent should handle multi-turn conversations with proper state management
8. Agent should orchestrate tool calls automatically based on user intent
9. Support same languages: English, Roman Urdu, Urdu

Technical context:
- Backend: FastAPI with SQLModel ORM, Neon PostgreSQL
- Current file to replace: backend/core/services/agent_service.py
- MCP tools location: backend/mcp_server/tools/
- OpenRouter model: gpt-4o-mini
- Conversation history: Last 20 messages loaded from database (stateless agent)

Success criteria:
- Agent uses OpenAI Agents SDK Agent class instead of manual function calling
- OpenRouter API is used for all LLM inference (not OpenAI API)
- All existing chat functionality works identically from user perspective
- Agent properly orchestrates tool calls with state management
- Multi-turn reasoning works correctly (agent can ask clarifying questions, confirm actions, etc.)

## Response snapshot

Created comprehensive specification for OpenAI Agents SDK integration with the following structure:

**User Stories (5 prioritized)**:
- P1: Agent SDK Tool Orchestration (MVP) - Replace manual function calling with SDK-based orchestration
- P1: OpenRouter LLM Provider Configuration (MVP) - Configure SDK to use OpenRouter instead of OpenAI API
- P2: Multi-Turn Conversation State Management - Enable natural conversational flows
- P2: Existing Functionality Preservation - Ensure backward compatibility
- P3: MCP Tools Integration - Register all 5 tools with SDK

**Functional Requirements**: 40 requirements covering:
- OpenAI Agents SDK integration (FR-001 to FR-004)
- OpenRouter LLM provider configuration (FR-005 to FR-010)
- MCP tools registration (FR-011 to FR-017)
- Conversation state management (FR-018 to FR-022)
- Existing functionality preservation (FR-023 to FR-030)
- Implementation constraints (FR-031 to FR-035)
- Error handling (FR-036 to FR-040)

**Success Criteria**: 10 measurable outcomes including:
- 100% SDK-based tool orchestration
- 100% OpenRouter API usage (verified via network monitoring)
- 100% backward compatibility with existing tests
- 95%+ multi-turn conversation handling
- No performance regression (< 5s for simple queries)

**Validation**: All quality checks passed
- No implementation details in spec
- All requirements testable and unambiguous
- Success criteria measurable and technology-agnostic
- 30+ acceptance scenarios across 5 user stories
- 8 edge cases identified
- Scope clearly bounded (only modify agent_service.py)

## Outcome

- ✅ Impact: Specification complete and validated, ready for planning phase
- 🧪 Tests: No tests at specification phase (will be defined in tasks phase)
- 📁 Files: Created spec.md (293 lines) and requirements.md checklist
- 🔁 Next prompts: /sp.plan (create implementation plan) or /sp.clarify (ask questions if needed)
- 🧠 Reflection: Specification successfully addresses the core issue - current implementation uses manual function calling instead of proper agentic framework. Clear requirements for SDK integration with OpenRouter as LLM provider while maintaining all existing functionality.

## Evaluation notes (flywheel)

- Failure modes observed: None - specification completed successfully on first attempt
- Graders run and results (PASS/FAIL): All quality checklist items PASS (Content Quality ✅, Requirement Completeness ✅, Feature Readiness ✅)
- Prompt variant (if applicable): Standard /sp.specify workflow
- Next experiment (smallest change to try): Proceed to /sp.plan to create implementation plan for agent_service.py rewrite
