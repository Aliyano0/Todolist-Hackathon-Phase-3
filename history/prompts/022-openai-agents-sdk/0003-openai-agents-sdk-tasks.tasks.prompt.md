---
id: 0003
title: openai-agents-sdk-tasks
stage: tasks
date: 2026-02-12
surface: agent
model: claude-sonnet-4-5
feature: 022-openai-agents-sdk
branch: 022-openai-agents-sdk
user: aliyan
command: /sp.tasks
labels: ["tasks", "implementation", "openai-agents-sdk", "agent-service", "backward-compatibility", "mcp-tools"]
links:
  spec: specs/022-openai-agents-sdk/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/022-openai-agents-sdk/tasks.md
tests:
  - No tests at tasks phase (backward compatibility validated by existing test suite per tasks.md)
---

## Prompt

User invoked `/sp.tasks` command to generate implementation tasks for feature 022-openai-agents-sdk.

Context: The specification and planning phases are complete. Need to generate actionable, dependency-ordered tasks organized by user story for implementing the OpenAI Agents SDK integration.

## Response snapshot

**Task Generation Complete**

Generated 39 implementation tasks organized into 5 phases:

**Phase 1: Setup (5 tasks)**
- Analyze current implementation
- Verify prerequisites (SDK installed, environment variables, existing tests)

**Phase 2: Core SDK Integration - MVP (15 tasks) 🎯**
- Combined US1 (Agent SDK Tool Orchestration) + US2 (OpenRouter Configuration) + US5 (MCP Tools Integration)
- Configure OpenRouter client with set_default_openai_client()
- Add @function_tool decorators to all 5 MCP tools (parallel tasks)
- Create Agent instance with tools and multilingual instructions
- Implement conversation history conversion to SDK input list format
- Replace manual function calling with Runner.run()
- Remove old manual orchestration code

**Phase 3: Multi-Turn State Management (4 tasks)**
- US3: Verify and enhance multi-turn conversation handling
- Test clarifying questions, confirmation flows, context preservation

**Phase 4: Backward Compatibility Validation (8 tasks)**
- US4: Run existing test suite (must pass 100%)
- Verify email verification, rate limiting, multilingual support, user isolation
- Performance validation (<5s simple, <10s complex queries)

**Phase 5: Polish & Cross-Cutting Concerns (7 tasks)**
- Documentation updates (backend/CLAUDE.md)
- Logging enhancements
- OpenRouter API usage verification
- Quickstart validation

**Key Organizational Decisions**:
1. Combined US1+US2+US5 into single MVP phase (interdependent - agent needs tools and OpenRouter config)
2. Marked parallel opportunities: tool decorators (5 files), validation tasks (8 independent checks)
3. Clear constraints documented: MUST NOT modify endpoints, schemas, models, frontend
4. Backward compatibility as critical gate: existing tests must pass 100%

**Dependencies Mapped**:
- Setup → Core SDK Integration (MVP) → Multi-Turn + Backward Compatibility (parallel) → Polish
- Estimated time: 9-15 hours for single developer

## Outcome

- ✅ Impact: Tasks complete and ready for implementation, clear MVP path defined
- 🧪 Tests: Backward compatibility validated by existing test suite (Phase 4, T025-T032)
- 📁 Files: Created tasks.md (39 tasks across 5 phases)
- 🔁 Next prompts: /sp.implement (execute tasks) or begin manual implementation starting with Phase 1
- 🧠 Reflection: Successfully organized tasks by user story with US1+US2+US5 combined as MVP (interdependent core). Clear separation between MVP (Phase 2) and enhancements (Phase 3). Backward compatibility validation (Phase 4) is critical gate before deployment. Single file modification (agent_service.py) plus tool decorators keeps scope minimal. Parallel opportunities identified for tool decorators and validation tasks.

## Evaluation notes (flywheel)

- Failure modes observed: None - tasks generated successfully with clear organization
- Graders run and results (PASS/FAIL): Task Organization ✅ PASS (organized by user story), Format Validation ✅ PASS (all tasks follow [ID] [P?] [Story] format), Dependencies ✅ PASS (clear execution order documented), MVP Definition ✅ PASS (Phase 2 identified as MVP)
- Prompt variant (if applicable): Standard /sp.tasks workflow with user story organization
- Next experiment (smallest change to try): Begin implementation with Phase 1 (Setup) to analyze current code, then proceed to Phase 2 (Core SDK Integration MVP)
