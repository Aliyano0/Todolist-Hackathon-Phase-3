---
id: 001
title: analyze-cli-data-persistence-issue
stage: misc
date: 2026-01-02
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 001-todo-console-app
user: aliyan
command: /sp.analyze
labels: ["analysis","bug","cli","data-persistence"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - adapters/cli/__main__.py
  - adapters/repository/memory_repository.py
  - specs/001-todo-console-app/tasks.md
tests: []
---

## Prompt

it says add tasks first when i run uv run todolist list even though i have added a task with description before

## Response snapshot

ANALYSIS COMPLETE

Root Cause: Each CLI command creates an isolated MemoryRepository instance, so tasks added in one command are lost before the next command runs.

CRITICAL Finding:
- Location: adapters/cli/__main__.py:83,95,111,127,138,149
- Issue: `repository = MemoryRepository()` called in every command handler
- Impact: User Story 1 acceptance criterion fails (task should persist across commands)

Recommendation: Add shared repository instance at module level to maintain session state.

## Outcome

- ✅ Impact: Critical bug identified - breaks core functionality (task persistence)
- 🧪 Tests: No tests affected (all unit tests pass with fresh repository)
- 📁 Files: 3 files analyzed
- 🔁 Next prompts: Fix shared repository state in CLI
- 🧠 Reflection: Spec FR-012 "store all data in memory for the duration of the session" was implemented but not integrated correctly across command boundaries

## Evaluation notes (flywheel)

- Failure modes observed: Each command handler creates isolated MemoryRepository
- Graders run and results (PASS/FAIL): N/A - analysis only
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Add module-level _shared_repository in __main__.py
