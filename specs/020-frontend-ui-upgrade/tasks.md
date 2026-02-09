# Tasks: Professional Frontend UI Upgrade

**Input**: Design documents from `/specs/020-frontend-ui-upgrade/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/components.md

**Tests**: Constitution requires TDD workflow. Tests should be written first (Red-Green-Refactor) during implementation, but are not listed as separate tasks here. Each implementation task implicitly includes writing tests first.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- Frontend project: `frontend/` at repository root
- Components: `frontend/components/`
- Pages: `frontend/app/`
- Utilities: `frontend/lib/`, `frontend/hooks/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and dependency installation

- [x] T001 Install Framer Motion dependency in frontend/package.json using npm install framer-motion
- [x] T002 [P] Verify Next.js 16.1+ and React 19 versions in frontend/package.json
- [x] T003 [P] Verify Shadcn UI and Tailwind CSS are properly configured in frontend/
- [x] T004 [P] Update frontend/CLAUDE.md with UI upgrade context and Framer Motion patterns

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core design system and utilities that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 Create design tokens file in frontend/lib/design-tokens.ts with colors, spacing, typography, and animation constants
- [x] T006 Extend Tailwind configuration in frontend/tailwind.config.js with custom design tokens (priority colors, category colors, spacing scale)
- [x] T007 [P] Create animation utilities file in frontend/lib/animations.ts with animation variants (fadeIn, slideUp, scaleIn) and spring configurations
- [x] T008 [P] Create useReducedMotion hook in frontend/hooks/useReducedMotion.ts to respect user's motion preferences
- [x] T009 Update global styles in frontend/app/globals.css with design system variables and base styles

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - First-Time Visitor Landing Experience (Priority: P1) 🎯 MVP

**Goal**: Create a professional homepage at root URL with hero section, features, how-it-works, CTA, and footer that provides clear value proposition and conversion paths for new visitors

**Independent Test**: Visit http://localhost:3000/ without authentication and verify: (1) Hero section with branding and CTAs appears, (2) Features section shows 4 key capabilities, (3) How It Works section shows 3-step journey, (4) CTA section with Sign Up button, (5) Footer with links. Visit as authenticated user and verify Dashboard/Profile buttons appear instead of Login/Signup.

### Implementation for User Story 1

- [x] T010 [P] [US1] Create HeroSection component in frontend/components/homepage/HeroSection.tsx with title, subtitle, primary/secondary CTAs, conditional rendering based on auth status, and fade-in animation
- [x] T011 [P] [US1] Create FeaturesSection component in frontend/components/homepage/FeaturesSection.tsx with 4 features (AI suggestions, categorization, sync, analytics) in 2x2 grid with icons and staggered animations
- [x] T012 [P] [US1] Create HowItWorksSection component in frontend/components/homepage/HowItWorksSection.tsx with 3-step user journey (sign up, organize, insights) with step numbers and flow indicators
- [x] T013 [P] [US1] Create CTASection component in frontend/components/homepage/CTASection.tsx with conversion prompt, Sign Up button, and scale-in animation
- [x] T014 [P] [US1] Create Footer component in frontend/components/layout/Footer.tsx with links (About, Privacy, Terms, Contact) and copyright text
- [x] T015 [US1] Create homepage page in frontend/app/page.tsx composing HeroSection, FeaturesSection, HowItWorksSection, CTASection, and Footer components
- [x] T016 [US1] Update Navbar component in frontend/components/layout/Navbar.tsx to show conditional navigation (Login/Signup for unauthenticated, Dashboard/Profile for authenticated)
- [x] T017 [US1] Add scroll-triggered animations for homepage sections using Intersection Observer in frontend/components/homepage/

**Checkpoint**: At this point, User Story 1 should be fully functional - homepage displays correctly for both authenticated and unauthenticated users with smooth animations

---

## Phase 4: User Story 2 - Enhanced Dashboard Experience (Priority: P2)

**Goal**: Upgrade dashboard UI with modern card-based layout, clear visual hierarchy for priorities and categories, and intuitive task management interactions

**Independent Test**: Log in and navigate to /todos. Verify: (1) Tasks display in modern card layout with 4px left border for priority, (2) Priority badges visible in top-right corner, (3) Category tags below task title with background tint, (4) Hover effects work (lift + shadow), (5) Task actions (complete, edit, delete) provide visual feedback, (6) Light/dark theme switching maintains consistency.

### Implementation for User Story 2

- [x] T018 [P] [US2] Create PriorityBadge component in frontend/components/dashboard/PriorityBadge.tsx with color-coded pill badges (high=red, medium=yellow, low=green, none=gray) and optional icon
- [x] T019 [P] [US2] Create CategoryTag component in frontend/components/dashboard/CategoryTag.tsx with rounded tags, category colors, and optional icon
- [x] T020 [US2] Create TaskCard component in frontend/components/dashboard/TaskCard.tsx with 4px left border, priority badge, category tag, background tint, hover effects (lift + shadow), and action buttons
- [x] T021 [US2] Create TaskList component in frontend/components/dashboard/TaskList.tsx with task rendering, loading state, error state, empty state, and staggered animations for task additions
- [x] T022 [US2] Create TaskForm component in frontend/components/dashboard/TaskForm.tsx with title, description, priority, and category inputs with validation and visual feedback
- [x] T023 [US2] Upgrade dashboard page in frontend/app/todos/page.tsx to use new TaskList, TaskCard, and TaskForm components with modern layout
- [x] T024 [US2] Add task interaction animations (add, complete, delete) with fade/scale/slide effects in frontend/components/dashboard/TaskList.tsx
- [x] T025 [US2] Test theme consistency for dashboard components in both light and dark modes

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - homepage and dashboard are fully functional with modern UI

---

## Phase 5: User Story 4 - Consistent Visual Theme (Priority: P2)

**Goal**: Ensure cohesive visual language with consistent colors, typography, spacing, and design patterns across all pages

**Independent Test**: Navigate through homepage, dashboard, login, register, and profile pages. Verify: (1) Consistent button styles and hover effects across all pages, (2) Consistent form input styling, (3) Consistent spacing and typography, (4) Theme switching works consistently on all pages, (5) Responsive design maintains consistency across mobile/tablet/desktop.

### Implementation for User Story 4

- [ ] T026 [P] [US4] Audit all existing pages (login, register, profile, forgot-password, reset-password) for design token usage in frontend/app/
- [ ] T027 [P] [US4] Update login page in frontend/app/login/page.tsx to use design tokens and match new design system
- [ ] T028 [P] [US4] Update register page in frontend/app/register/page.tsx to use design tokens and match new design system
- [ ] T029 [P] [US4] Update profile page in frontend/app/profile/page.tsx to use design tokens and match new design system
- [ ] T030 [US4] Update root layout in frontend/app/layout.tsx to apply design system globally and ensure theme provider wraps all pages
- [ ] T031 [US4] Create visual consistency validation checklist and verify all pages pass (colors, fonts, spacing, button styles, form styles)
- [ ] T032 [US4] Test responsive design across mobile (< 768px), tablet (768-1023px), and desktop (≥ 1024px) breakpoints for all pages

**Checkpoint**: All pages now have consistent visual theme and responsive design

---

## Phase 6: User Story 3 - Smooth Animations and Transitions (Priority: P3)

**Goal**: Implement smooth, purposeful animations throughout the application that guide attention, provide feedback, and create polished professional feel

**Independent Test**: Navigate through the application and verify: (1) Page transitions are smooth (fade + slide), (2) Hover effects on interactive elements are subtle and responsive, (3) Task additions/removals animate smoothly, (4) Modals and dropdowns animate in/out, (5) Animations respect reduced motion preferences, (6) Animations run at 60 FPS on modern devices.

### Implementation for User Story 3

- [ ] T033 [P] [US3] Create PageTransition component in frontend/components/animations/PageTransition.tsx with fade + slide animations for route changes
- [ ] T034 [P] [US3] Create FadeIn component in frontend/components/animations/FadeIn.tsx with configurable delay and duration
- [ ] T035 [P] [US3] Create SlideIn component in frontend/components/animations/SlideIn.tsx with directional slide (up, down, left, right) and configurable distance
- [ ] T036 [P] [US3] Create ScaleIn component in frontend/components/animations/ScaleIn.tsx with scale from 0.95 to 1.0 and configurable initial scale
- [ ] T037 [US3] Wrap all pages with PageTransition component in frontend/app/layout.tsx for smooth route transitions
- [ ] T038 [US3] Add button hover animations (scale + glow effect) to all buttons across homepage and dashboard using Framer Motion
- [ ] T039 [US3] Add modal/dropdown animations (backdrop fade + content scale) to any modals or dropdowns in the application
- [ ] T040 [US3] Test animation performance using Chrome DevTools Performance tab and ensure 60 FPS on modern devices
- [ ] T041 [US3] Test reduced motion preferences by enabling prefers-reduced-motion and verifying instant transitions

**Checkpoint**: All animations are smooth, performant, and respect accessibility preferences

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements, documentation, and validation

- [ ] T042 [P] Run accessibility audit using axe DevTools or Lighthouse and fix any violations (ARIA labels, keyboard navigation, contrast ratios)
- [ ] T043 [P] Run performance audit using Lighthouse and optimize any issues (image optimization, code splitting, lazy loading)
- [ ] T044 [P] Test all edge cases from spec.md (JavaScript disabled, long task titles, rapid clicks, small screens < 320px, browser compatibility)
- [ ] T045 [P] Update frontend/CLAUDE.md with final patterns, component usage examples, and design system documentation
- [ ] T046 [P] Create visual regression test suite using Playwright for homepage and dashboard screenshots
- [ ] T047 Validate quickstart.md instructions by following setup steps in a clean environment
- [ ] T048 Run full E2E test suite covering all user stories (homepage visit, dashboard usage, theme switching, animations)
- [ ] T049 Code cleanup and refactoring (remove console.logs, unused imports, commented code)
- [ ] T050 Final review of all components for consistency, accessibility, and performance

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User Story 1 (P1): Can start after Foundational - No dependencies on other stories
  - User Story 2 (P2): Can start after Foundational - No dependencies on other stories (can run parallel with US1)
  - User Story 4 (P2): Can start after Foundational - No dependencies on other stories (can run parallel with US1/US2)
  - User Story 3 (P3): Can start after Foundational - Enhances US1/US2 but doesn't block them
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - Independently testable
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Independently testable (can run parallel with US1)
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - Independently testable (can run parallel with US1/US2)
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Enhances US1/US2 but independently testable

### Within Each User Story

- Components marked [P] can be implemented in parallel (different files)
- Components without [P] depend on previous tasks in the same story
- Follow TDD: Write test first, ensure it fails, implement, ensure it passes, refactor

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T002, T003, T004)
- All Foundational tasks marked [P] can run in parallel (T007, T008)
- Once Foundational phase completes, User Stories 1, 2, and 4 can all start in parallel (if team capacity allows)
- Within US1: T010, T011, T012, T013, T014 can all run in parallel (different components)
- Within US2: T018, T019 can run in parallel, then T020-T022 can run in parallel
- Within US4: T026, T027, T028, T029 can all run in parallel (different pages)
- Within US3: T033, T034, T035, T036 can all run in parallel (different animation components)
- All Polish tasks marked [P] can run in parallel (T042, T043, T044, T045, T046)

---

## Parallel Example: User Story 1

```bash
# After Foundational phase completes, launch all homepage components in parallel:
Task T010: "Create HeroSection component in frontend/components/homepage/HeroSection.tsx"
Task T011: "Create FeaturesSection component in frontend/components/homepage/FeaturesSection.tsx"
Task T012: "Create HowItWorksSection component in frontend/components/homepage/HowItWorksSection.tsx"
Task T013: "Create CTASection component in frontend/components/homepage/CTASection.tsx"
Task T014: "Create Footer component in frontend/components/layout/Footer.tsx"

# Then compose them sequentially:
Task T015: "Create homepage page in frontend/app/page.tsx"
Task T016: "Update Navbar component"
Task T017: "Add scroll-triggered animations"
```

---

## Parallel Example: User Story 2

```bash
# After Foundational phase completes, launch atomic components in parallel:
Task T018: "Create PriorityBadge component in frontend/components/dashboard/PriorityBadge.tsx"
Task T019: "Create CategoryTag component in frontend/components/dashboard/CategoryTag.tsx"

# Then launch composite components in parallel:
Task T020: "Create TaskCard component"
Task T021: "Create TaskList component"
Task T022: "Create TaskForm component"

# Then integrate sequentially:
Task T023: "Upgrade dashboard page"
Task T024: "Add task interaction animations"
Task T025: "Test theme consistency"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T004)
2. Complete Phase 2: Foundational (T005-T009) - CRITICAL
3. Complete Phase 3: User Story 1 (T010-T017)
4. **STOP and VALIDATE**: Test homepage independently
   - Visit / without auth → See hero, features, how-it-works, CTA, footer
   - Visit / with auth → See Dashboard/Profile buttons
   - Test animations and responsiveness
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo (Homepage + Dashboard)
4. Add User Story 4 → Test independently → Deploy/Demo (Consistent theme)
5. Add User Story 3 → Test independently → Deploy/Demo (Polished animations)
6. Add Polish → Final validation → Production release

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T009)
2. Once Foundational is done:
   - Developer A: User Story 1 (T010-T017) - Homepage
   - Developer B: User Story 2 (T018-T025) - Dashboard
   - Developer C: User Story 4 (T026-T032) - Theme consistency
3. After US1, US2, US4 complete:
   - Any developer: User Story 3 (T033-T041) - Animations
4. Team completes Polish together (T042-T050)

---

## Task Summary

**Total Tasks**: 50 tasks

**Tasks per Phase**:
- Phase 1 (Setup): 4 tasks
- Phase 2 (Foundational): 5 tasks (BLOCKING)
- Phase 3 (US1 - Homepage): 8 tasks
- Phase 4 (US2 - Dashboard): 8 tasks
- Phase 5 (US4 - Theme): 7 tasks
- Phase 6 (US3 - Animations): 9 tasks
- Phase 7 (Polish): 9 tasks

**Parallel Opportunities**: 28 tasks marked [P] can run in parallel within their phase

**MVP Scope**: Phases 1-3 (17 tasks) deliver a functional homepage

**Full Feature Scope**: All 50 tasks deliver complete professional UI upgrade

---

## Notes

- [P] tasks = different files, no dependencies within phase
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- TDD workflow: Write test first (Red), implement (Green), refactor
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- Constitution requires TDD: Tests are written during implementation, not as separate tasks
