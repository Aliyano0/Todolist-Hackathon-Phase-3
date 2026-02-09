# Implementation Plan: Professional Frontend UI Upgrade

**Branch**: `020-frontend-ui-upgrade` | **Date**: 2026-02-09 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/020-frontend-ui-upgrade/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Transform the existing Next.js frontend from functional to professional-grade by creating a dedicated homepage at the root URL with hero section and conditional navigation, upgrading the dashboard UI with modern visual design and clear task organization, implementing smooth animations using Framer Motion throughout the application, and establishing a consistent design system with concrete visual guidelines. This frontend-only upgrade maintains all existing authentication and backend functionality while significantly improving first-time user experience, daily user satisfaction, and overall application polish.

## Technical Context

**Language/Version**: TypeScript 5.0+ (frontend only)
**Primary Dependencies**: Next.js 16.1+ (App Router), React 19, Shadcn UI, Tailwind CSS, Framer Motion (motion for web)
**Storage**: N/A (frontend only - uses existing backend API)
**Testing**: React Testing Library (component tests), Playwright (e2e tests for user flows)
**Target Platform**: Modern web browsers (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+)
**Project Type**: Web application (frontend only)
**Performance Goals**: <2s dashboard load time, 60 FPS animations, <300ms page transitions
**Constraints**: No backend API changes, no authentication changes, must maintain existing functionality, must respect reduced motion preferences, must support light/dark themes
**Scale/Scope**: 7 pages (homepage, login, register, dashboard, profile, forgot-password, reset-password), 20+ components, 4 new homepage sections, dashboard redesign with priority/category visual treatments

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] Verify documentation-first approach using MCP servers and Context7 - Will use nextjs MCP server and Context7 for Next.js 16, Framer Motion, and Shadcn UI documentation
- [x] Confirm adherence to clean architecture principles - Frontend follows component-based architecture with clear separation of concerns (UI components, API client, providers)
- [x] Validate tech stack compliance with specified technologies - Uses Next.js 16.1+, Shadcn UI, Tailwind CSS as specified in constitution
- [x] Ensure TDD workflow will be followed - Will write component tests first, then implement components (Red-Green-Refactor)
- [x] Confirm multi-user authentication & authorization requirements - No changes to authentication; maintains existing Better Auth JWT implementation
- [x] Ensure `CLAUDE.md` files exist for each major component - frontend/CLAUDE.md already exists and will be updated with UI upgrade context

**Gate Status**: ✅ PASSED - All constitution requirements satisfied. This is a frontend-only UI upgrade that maintains existing architecture and authentication.

## Project Structure

### Documentation (this feature)

```text
specs/020-frontend-ui-upgrade/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (to be created)
├── data-model.md        # Phase 1 output (to be created)
├── quickstart.md        # Phase 1 output (to be created)
├── contracts/           # Phase 1 output (to be created)
│   └── components.md    # Component API contracts
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
frontend/
├── CLAUDE.md                    # Frontend-specific Claude Code instructions (to be updated)
├── package.json                 # Dependencies (add framer-motion)
├── next.config.js
├── tsconfig.json
├── app/                         # Next.js App Router pages
│   ├── layout.tsx               # Root layout (update with design system)
│   ├── page.tsx                 # NEW: Homepage with hero section (currently redirects)
│   ├── login/page.tsx           # Existing (maintain)
│   ├── register/page.tsx        # Existing (maintain)
│   ├── todos/page.tsx           # Dashboard page (upgrade UI)
│   ├── profile/page.tsx         # Existing (maintain)
│   ├── forgot-password/page.tsx # Existing (maintain)
│   ├── reset-password/page.tsx  # Existing (maintain)
│   └── globals.css              # Global styles (update with design tokens)
├── components/                  # React components
│   ├── ui/                      # Shadcn UI components (existing)
│   ├── layout/                  # NEW: Layout components
│   │   ├── Navbar.tsx           # Navigation (update with conditional logic)
│   │   └── Footer.tsx           # NEW: Footer component
│   ├── homepage/                # NEW: Homepage components
│   │   ├── HeroSection.tsx      # Hero with branding and CTA
│   │   ├── FeaturesSection.tsx  # 4 key features with icons
│   │   ├── HowItWorksSection.tsx # 3-step user journey
│   │   └── CTASection.tsx       # Final conversion prompt
│   ├── dashboard/               # NEW: Dashboard components (refactored from existing)
│   │   ├── TaskCard.tsx         # Task card with priority/category visuals
│   │   ├── TaskList.tsx         # Task list with animations
│   │   ├── TaskForm.tsx         # Task creation/edit form
│   │   ├── PriorityBadge.tsx    # Priority indicator component
│   │   └── CategoryTag.tsx      # Category tag component
│   ├── animations/              # NEW: Animation wrappers
│   │   ├── PageTransition.tsx   # Page transition wrapper
│   │   ├── FadeIn.tsx           # Fade in animation
│   │   ├── SlideIn.tsx          # Slide in animation
│   │   └── ScaleIn.tsx          # Scale in animation
│   └── theme/                   # Existing theme components
│       └── ThemeToggle.tsx      # Theme switcher (maintain)
├── lib/                         # Utility functions
│   ├── api.ts                   # API client (existing, maintain)
│   ├── design-tokens.ts         # NEW: Design system tokens (colors, spacing, typography)
│   └── animations.ts            # NEW: Animation constants and utilities
├── providers/                   # Context providers
│   └── AuthProvider.tsx         # Authentication context (existing, maintain)
├── hooks/                       # NEW: Custom hooks
│   └── useReducedMotion.ts      # Hook for reduced motion preference
└── tests/                       # Frontend tests
    ├── components/              # Component tests
    ├── pages/                   # Page tests
    └── e2e/                     # End-to-end tests
```

**Structure Decision**: This is a frontend-only upgrade using the existing Next.js 16.1 App Router structure. The implementation adds new homepage components, refactors dashboard components for better visual organization, introduces animation wrappers for Framer Motion, and establishes a design system with tokens. All new components follow the existing Shadcn UI + Tailwind CSS pattern. No backend or mobile components are involved.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations detected. All constitution requirements are satisfied for this frontend-only UI upgrade.

---

## Phase 0: Research Complete ✅

**Output**: `research.md` - 8 technical decisions documented with rationale and alternatives

**Key Decisions**:
1. Animation Library: Framer Motion (motion for web)
2. Design System: Tailwind CSS + Design Tokens
3. Component Architecture: Atomic Design Pattern
4. Animation Strategy: Progressive Enhancement
5. Homepage Layout: Hero-First with Scroll Sections
6. Dashboard Redesign: Card-Based Layout with Visual Hierarchy
7. Theme System: Extend Existing Light/Dark Mode
8. Testing Strategy: Component Tests + E2E Visual Tests

---

## Phase 1: Design & Contracts Complete ✅

**Outputs**:
- `data-model.md` - Component data structures and TypeScript interfaces
- `contracts/components.md` - Component API contracts with behavior guarantees
- `quickstart.md` - Developer setup guide and workflow
- `CLAUDE.md` - Updated with new technologies (Framer Motion)

**Component Hierarchy Defined**:
- **Atoms**: PriorityBadge, CategoryTag
- **Molecules**: TaskCard, TaskForm
- **Organisms**: HeroSection, FeaturesSection, HowItWorksSection, CTASection, TaskList
- **Templates**: Homepage, Dashboard

---

## Constitution Check (Post-Design) ✅

*Re-evaluation after Phase 1 design completion*

- [x] Documentation-first approach maintained - All decisions reference official docs via MCP/Context7
- [x] Clean architecture preserved - Component-based architecture with clear separation
- [x] Tech stack compliance verified - Next.js 16.1+, Shadcn UI, Tailwind CSS, Framer Motion
- [x] TDD workflow planned - Red-Green-Refactor cycle documented in quickstart
- [x] Authentication unchanged - No modifications to existing Better Auth implementation
- [x] CLAUDE.md updated - Frontend context file updated with new patterns

**Final Gate Status**: ✅ PASSED - Design maintains all constitution requirements. Ready for /sp.tasks phase.

---

## Implementation Readiness

**Ready to Proceed**: ✅ Yes

**Artifacts Generated**:
1. ✅ `plan.md` - Implementation plan (this file)
2. ✅ `research.md` - Technical decisions and best practices
3. ✅ `data-model.md` - Component data structures
4. ✅ `contracts/components.md` - Component API contracts
5. ✅ `quickstart.md` - Developer setup guide
6. ✅ `CLAUDE.md` - Updated agent context

**Next Command**: `/sp.tasks` - Generate actionable task breakdown

**Estimated Scope**:
- 20+ components to implement
- 7 pages to create/upgrade
- 4 homepage sections
- Design system foundation
- Animation wrappers
- Comprehensive test coverage

**Timeline Estimate**: 3-4 weeks (based on component development order in quickstart.md)
