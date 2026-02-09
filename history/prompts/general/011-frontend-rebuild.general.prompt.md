---
id: "011"
title: "Frontend Rebuild Specification"
stage: "spec"
date_iso: "2026-01-31"
surface: "agent"
model: "Claude Sonnet 4.5"
feature: "frontend-rebuild"
branch: "011-frontend-rebuild"
user: "user"
command: "/sp.specify Phase 2b (frontend): First, remove the entire existing /frontend directory to resolve problems and start from scratch. Then, recreate /frontend directory with a clean setup. With Phase 2a backend ready (no auth), build Next.js 16.1 App Router frontend in /frontend. Set up structure per root/folder-structure.md, install deps (next, tailwindcss, shadcn-ui). Update root claude.md if needed, confirm /frontend dir, create separate CLAUDE.md in /frontend for frontend context. Create responsive UI with mild animations, Tailwind, Shadcn/UI (Lyra style from up-to-date docs), Dark/White modes. Implement Todo UI for 5 Basic features via backend API integration (no auth). Add placeholder profile. Test full stack locally."
labels: ["frontend", "nextjs", "rebuild", "todo-app"]
links:
  spec: "specs/011-frontend-rebuild/spec.md"
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "specs/011-frontend-rebuild/spec.md"
  - "specs/011-frontend-rebuild/checklists/requirements.md"
  - "history/prompts/general/011-frontend-rebuild.general.prompt.md"
tests_yaml:
  - "None yet"
prompt_text: "Phase 2b (frontend): First, remove the entire existing /frontend directory to resolve problems and start from scratch. Then, recreate /frontend directory with a clean setup. With Phase 2a backend ready (no auth), build Next.js 16.1 App Router frontend in /frontend. Set up structure per root/folder-structure.md, install deps (next, tailwindcss, shadcn-ui). Update root claude.md if needed, confirm /frontend dir, create separate CLAUDE.md in /frontend for frontend context. Create responsive UI with mild animations, Tailwind, Shadcn/UI (Lyra style from up-to-date docs), Dark/White modes. Implement Todo UI for 5 Basic features via backend API integration (no auth). Add placeholder profile. Test full stack locally."
response_text: "Created specification for frontend rebuild task. The spec defines user scenarios for accessing a clean frontend application, using responsive Todo interface with light/dark modes, performing basic Todo operations, and navigating application pages. It includes 14 functional requirements covering directory removal, Next.js structure setup, dependency installation, responsive design, theme support, backend API integration, profile page, styling with Tailwind/Shadcn/UI, animations, error handling, and documentation updates. Success criteria define measurable outcomes for directory removal, Todo operations, responsiveness, theme switching, API integration, performance, and documentation updates."
outcome:
evaluation:
---

# Frontend Rebuild Specification

## Summary

Specification created for rebuilding the frontend application from scratch. The task involves removing the existing /frontend directory, creating a clean setup with Next.js 16.1 App Router, implementing responsive UI with light/dark modes, and integrating with backend API for 5 basic Todo features.

## Details

The feature specification defines requirements for:
- Complete removal of existing /frontend directory
- Clean Next.js 16.1 App Router structure implementation
- Installation of required dependencies (next, tailwindcss, shadcn-ui)
- Responsive UI with light/dark mode support
- Backend API integration for 5 basic Todo operations
- Placeholder profile page
- Proper documentation updates with CLAUDE.md files