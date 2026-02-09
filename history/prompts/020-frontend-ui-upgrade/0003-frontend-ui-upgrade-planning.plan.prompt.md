---
id: 0003
title: Frontend UI Upgrade Implementation Planning
stage: plan
date: 2026-02-09
surface: agent
model: claude-sonnet-4-5
feature: 020-frontend-ui-upgrade
branch: 020-frontend-ui-upgrade
user: Aliyan Aqeel
command: /sp.plan
labels: ["frontend", "ui-upgrade", "planning", "architecture", "design-system", "framer-motion", "component-design"]
links:
  spec: specs/020-frontend-ui-upgrade/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/020-frontend-ui-upgrade/plan.md
  - specs/020-frontend-ui-upgrade/research.md
  - specs/020-frontend-ui-upgrade/data-model.md
  - specs/020-frontend-ui-upgrade/contracts/components.md
  - specs/020-frontend-ui-upgrade/quickstart.md
  - CLAUDE.md
tests:
  - None (planning phase - implementation tests will be created during /sp.tasks)
---

## Prompt

/sp.plan

## Response snapshot

Completed comprehensive implementation planning for frontend UI upgrade. Generated complete technical architecture with 8 key decisions, component data models, API contracts, and developer quickstart guide.

**Planning Workflow Executed:**

1. **Setup & Context Loading**: Ran setup-plan.sh, loaded spec.md and constitution.md
2. **Plan Template Filled**: Updated plan.md with summary, technical context, and project structure
3. **Constitution Check (Pre-Design)**: ✅ PASSED - All 6 requirements satisfied
4. **Phase 0 - Research**: Created research.md with 8 technical decisions
5. **Phase 1 - Design**: Created data-model.md, contracts/components.md, quickstart.md
6. **Agent Context Update**: Updated CLAUDE.md with Framer Motion technology
7. **Constitution Check (Post-Design)**: ✅ PASSED - Design maintains all requirements
8. **Implementation Readiness**: Documented scope and next steps

**Phase 0: Research (8 Technical Decisions)**

1. **Animation Library**: Framer Motion (motion for web)
   - Rationale: Official React library, Next.js 16 support, reduced motion support, spring physics
   - Alternatives rejected: React Spring (complex API), CSS Animations (limited control), GSAP (licensing)

2. **Design System**: Tailwind CSS + Design Tokens
   - Rationale: Already integrated, type-safe tokens, native theme support
   - Implementation: `lib/design-tokens.ts` with TypeScript constants, extend tailwind.config.js

3. **Component Architecture**: Atomic Design Pattern
   - Rationale: Clear hierarchy, promotes reusability, aligns with Shadcn UI
   - Structure: Atoms → Molecules → Organisms → Templates

4. **Animation Strategy**: Progressive Enhancement
   - Rationale: Respects user preferences, ensures accessibility, prevents performance issues
   - Implementation: `useReducedMotion()` hook, instant transitions when preferred

5. **Homepage Layout**: Hero-First with Scroll Sections
   - Rationale: Industry standard for SaaS, strong first impression, mobile-friendly
   - Sections: Hero (full viewport) → Features (2x2 grid) → How It Works (3 steps) → CTA → Footer

6. **Dashboard Redesign**: Card-Based Layout with Visual Hierarchy
   - Rationale: Scannable, supports animations, aligns with modern task management UIs
   - Visual hierarchy: Priority (left border + badge) > Category (tint + tag) > Status (checkbox)

7. **Theme System**: Extend Existing Light/Dark Mode
   - Rationale: Maintains constitution requirement, consistency with existing pages
   - Implementation: Define tokens with light/dark variants, test contrast ratios

8. **Testing Strategy**: Component Tests + E2E Visual Tests
   - Rationale: Verify behavior and appearance, aligns with TDD requirement
   - Tools: React Testing Library (components), Playwright (E2E + visual regression)

**Phase 1: Design & Contracts**

**data-model.md** - Component Data Structures:
- Design system tokens (colors, spacing, typography, animations)
- 15+ TypeScript interfaces for component props
- State management types (AuthState, ThemeState)
- API response types (TaskResponse, TaskListResponse)
- Validation schemas (taskFormSchema)
- Utility types (AnimationVariants, type guards)

**contracts/components.md** - Component API Contracts:
- 15+ component contracts with behavior guarantees
- Accessibility requirements for each component
- Animation behavior specifications
- Input/output contracts
- Contract validation rules (10 requirements)
- Contract testing guidelines

**quickstart.md** - Developer Setup Guide:
- Prerequisites and initial setup
- Project structure overview
- TDD workflow (Red-Green-Refactor)
- Design system setup instructions
- Component development order (6 phases over 3-4 weeks)
- Running tests, debugging tips, resources

**Project Structure Defined**:
```
frontend/
├── app/                    # Pages (homepage NEW, dashboard UPGRADE)
├── components/
│   ├── homepage/          # NEW: 4 sections + footer
│   ├── dashboard/         # NEW: TaskCard, TaskList, badges, tags
│   ├── animations/        # NEW: 4 animation wrappers
│   └── layout/            # UPDATE: Navbar with conditional logic
├── lib/
│   ├── design-tokens.ts   # NEW: Design system tokens
│   └── animations.ts      # NEW: Animation utilities
└── hooks/
    └── useReducedMotion.ts # NEW: Accessibility hook
```

**Component Hierarchy**:
- **Atoms** (2): PriorityBadge, CategoryTag
- **Molecules** (2): TaskCard, TaskForm
- **Organisms** (6): HeroSection, FeaturesSection, HowItWorksSection, CTASection, TaskList, Footer
- **Templates** (2): Homepage, Dashboard

**Technical Context**:
- Language: TypeScript 5.0+ (frontend only)
- Dependencies: Next.js 16.1+, React 19, Shadcn UI, Tailwind CSS, Framer Motion
- Testing: React Testing Library, Playwright
- Performance: <2s dashboard load, 60 FPS animations, <300ms transitions
- Constraints: No backend changes, no auth changes, reduced motion support, light/dark themes
- Scope: 7 pages, 20+ components, 4 homepage sections

**Constitution Compliance**:
- ✅ Documentation-first: All decisions reference official docs via MCP/Context7
- ✅ Clean architecture: Component-based with clear separation
- ✅ Tech stack: Next.js 16.1+, Shadcn UI, Tailwind CSS (constitution compliant)
- ✅ TDD workflow: Red-Green-Refactor documented
- ✅ Authentication: No changes to existing Better Auth
- ✅ CLAUDE.md: Updated with Framer Motion

## Outcome

- ✅ Impact: Comprehensive implementation plan created with complete technical architecture. All planning artifacts generated (research, data model, contracts, quickstart). Design decisions are well-documented with rationale and alternatives. Component hierarchy follows Atomic Design principles. Ready for /sp.tasks phase to generate actionable task breakdown.
- 🧪 Tests: None (planning phase - test specifications included in contracts)
- 📁 Files: 6 files created/modified (plan.md, research.md, data-model.md, contracts/components.md, quickstart.md, CLAUDE.md)
- 🔁 Next prompts: /sp.tasks (generate actionable task breakdown with dependencies and test cases)
- 🧠 Reflection: The planning phase successfully translated the specification into concrete technical architecture. The 8 research decisions provide clear direction for implementation, with each decision justified by rationale and alternatives considered. The component hierarchy (Atomic Design) ensures maintainability and reusability. The contracts document provides behavior guarantees that will guide TDD implementation. The quickstart guide gives developers a clear path from setup to implementation. Key insight: Progressive enhancement for animations is critical - the `useReducedMotion()` hook ensures accessibility compliance while still delivering polished UX for users who can experience animations. The 3-4 week timeline is realistic given the scope (20+ components, design system foundation, comprehensive testing).

## Evaluation notes (flywheel)

- Failure modes observed: None. Planning workflow followed template structure correctly. All phases completed (Phase 0 research, Phase 1 design). Constitution checks passed both pre and post-design.
- Graders run and results (PASS/FAIL): PASS - All planning artifacts generated successfully. Technical context filled completely (no NEEDS CLARIFICATION markers). Project structure defined with concrete paths. Component hierarchy clear and justified. Constitution compliance verified twice.
- Prompt variant (if applicable): Standard /sp.plan workflow with Phase 0 (research) and Phase 1 (design + contracts)
- Next experiment (smallest change to try): In /sp.tasks phase, consider grouping tasks by component hierarchy level (Atoms → Molecules → Organisms → Templates) to ensure dependencies are clear and implementation can proceed in parallel where possible. This would allow multiple developers to work on different hierarchy levels simultaneously once foundation (design tokens, animation wrappers) is complete.
