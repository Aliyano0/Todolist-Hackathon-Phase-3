---
id: 0002
title: openai-agents-sdk-planning
stage: plan
date: 2026-02-12
surface: agent
model: claude-sonnet-4-5
feature: 022-openai-agents-sdk
branch: 022-openai-agents-sdk
user: aliyan
command: /sp.plan
labels: ["planning", "openai-agents-sdk", "agent-system", "research", "design", "context7"]
links:
  spec: specs/022-openai-agents-sdk/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/022-openai-agents-sdk/plan.md
  - specs/022-openai-agents-sdk/research.md
  - specs/022-openai-agents-sdk/data-model.md
  - specs/022-openai-agents-sdk/quickstart.md
  - specs/022-openai-agents-sdk/contracts/api-contracts.md
  - CLAUDE.md (updated)
tests:
  - None (planning phase - no code implementation yet)
---

## Prompt

User invoked `/sp.plan` command to create implementation plan for feature 022-openai-agents-sdk.

Context: The specification (created in previous session via /sp.specify) identified that the current AI chatbot implementation uses manual function calling instead of proper OpenAI Agents SDK integration. The planning phase must resolve technical unknowns and create design artifacts.

## Response snapshot

**Phase 0: Research (Completed)**

Used Context7 to research OpenAI Agents SDK documentation and resolved all 3 technical unknowns:

1. **OpenRouter Configuration**: Use `set_default_openai_client()` with custom `AsyncOpenAI(base_url="https://openrouter.ai/api/v1", api_key=OPENROUTER_API_KEY)`
2. **Tool Registration**: Use `@function_tool` decorator on existing MCP tool functions for automatic schema extraction
3. **Conversation History**: Use manual input list approach by converting database messages to `[{"role": "...", "content": "..."}]` format

Created `research.md` with comprehensive findings, rationale, and alternatives considered.

**Phase 1: Design & Contracts (Completed)**

Generated all required design artifacts:

- `data-model.md`: Confirmed no database schema changes required (service layer refactoring only)
- `contracts/api-contracts.md`: Confirmed 100% backward compatibility, no API changes
- `quickstart.md`: Comprehensive developer guide with architecture overview, code examples, testing strategy, and troubleshooting
- Updated `CLAUDE.md`: Added OpenAI Agents SDK integration details to agent context

**Architecture Decisions**:
- Single file modification: `backend/core/services/agent_service.py`
- No changes to MCP server, API endpoints, database models, or frontend
- Stateless architecture maintained (load last 20 messages from PostgreSQL on each request)
- All existing functionality preserved (auth, rate limiting, multilingual support, user isolation)

**Constitution Check**: ✅ All checks passed (pre-Phase 0 and post-Phase 1)

## Outcome

- ✅ Impact: Planning complete and validated, ready for task generation phase
- 🧪 Tests: No tests at planning phase (test strategy documented in quickstart.md)
- 📁 Files: Created plan.md, research.md, data-model.md, quickstart.md, contracts/api-contracts.md; updated CLAUDE.md
- 🔁 Next prompts: /sp.tasks (generate implementation tasks) or /sp.adr (document architectural decisions if needed)
- 🧠 Reflection: Planning successfully resolved all technical unknowns through Context7 research. Clear implementation path established: configure SDK with OpenRouter client, register tools with @function_tool decorator, convert DB messages to input list format, use Runner.run() for execution. Single file modification (agent_service.py) maintains clean architecture and 100% backward compatibility.

## Evaluation notes (flywheel)

- Failure modes observed: None - planning completed successfully with all artifacts generated
- Graders run and results (PASS/FAIL): Constitution Check ✅ PASS (all 6 items), Research ✅ COMPLETE (3/3 unknowns resolved), Design ✅ COMPLETE (all Phase 1 artifacts generated)
- Prompt variant (if applicable): Standard /sp.plan workflow with Context7 research integration
- Next experiment (smallest change to try): Proceed to /sp.tasks to generate implementation tasks with test cases for agent_service.py rewrite
