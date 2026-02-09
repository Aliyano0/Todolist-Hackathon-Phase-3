# Implementation Plan: Frontend Structure Resolution

**Branch**: `010-frontend-structure-resolution` | **Date**: 2026-01-31 | **Spec**: [link]
**Input**: Feature specification from `/specs/010-frontend-structure-resolution/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Resolve the conflict between two app directories (/src/app and /app) in the frontend by consolidating to a single Next.js 16+ App Router compliant structure. This involves migrating necessary files from /src/app to /app, adding missing files (layout.tsx, page.tsx, components for Todo UI, profile page), implementing responsive UI with light/dark mode support, and integrating with backend API to perform 5 basic Todo operations.

## Technical Context

**Language/Version**: TypeScript 5.0+ for frontend, Next.js 16+
**Primary Dependencies**: Next.js 16+ with App Router, Shadcn UI, Tailwind CSS, Better Auth, React 19
**Storage**: N/A (frontend only)
**Testing**: Jest, React Testing Library, Playwright for E2E testing
**Target Platform**: Web browser (Chrome, Firefox, Safari, Edge)
**Project Type**: Web application (frontend component)
**Performance Goals**: Page load times under 3 seconds, responsive UI with smooth animations
**Constraints**: Must follow Next.js 16+ App Router standards, integrate with existing backend API, support light/dark themes
**Scale/Scope**: Single user interface with responsive design for mobile/tablet/desktop

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] Verify documentation-first approach using MCP servers and Context7
- [x] Confirm adherence to clean architecture principles
- [x] Validate tech stack compliance with specified technologies
- [x] Ensure TDD workflow will be followed
- [x] Confirm multi-user authentication & authorization requirements
- [x] Ensure `CLAUDE.md` files exist for each major component (`backend/`, `frontend/`) and adhere to context-specific guidelines

## Project Structure

### Documentation (this feature)

```text
specs/010-frontend-structure-resolution/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

frontend/
├── app/                 # Next.js 16+ App Router pages
│   ├── layout.tsx       # Root layout with theme provider
│   ├── page.tsx         # Main Todo dashboard page
│   ├── profile/         # Profile page with theme settings
│   │   └── page.tsx
│   ├── globals.css      # Global styles and Tailwind imports
│   └── providers/       # React context providers
│       └── theme-provider.tsx
├── components/          # Reusable UI components
│   ├── todo/            # Todo-specific components
│   │   ├── TodoForm.tsx
│   │   ├── TodoItem.tsx
│   │   ├── TodoList.tsx
│   │   └── TodoActions.tsx
│   ├── ui/              # Shadcn UI components
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   └── ...
│   ├── theme/           # Theme toggle components
│   │   └── ThemeToggle.tsx
│   └── navigation/      # Navigation components
│       └── Navbar.tsx
├── lib/                 # Utility functions
│   ├── api.ts           # API client for backend integration
│   ├── utils.ts         # General utility functions
│   └── theme.ts         # Theme-related utilities
├── hooks/               # Custom React hooks
│   └── useTodos.ts      # Todo management hooks
├── public/              # Static assets
│   └── favicon.ico
├── package.json
├── next.config.ts
├── tailwind.config.ts
├── tsconfig.json
└── CLAUDE.md            # Frontend-specific Claude instructions

**Structure Decision**: Selected the web application structure with Next.js 16+ App Router approach. The frontend will be located in the /frontend directory with the Next.js 16+ App Router structure under /frontend/app. This follows the requirements to consolidate to the /app directory as the primary Next.js App Router structure, removing the conflicting /src/app directory.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
