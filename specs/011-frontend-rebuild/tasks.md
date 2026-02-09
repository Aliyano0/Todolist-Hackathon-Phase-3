# Tasks: Frontend Rebuild

## Feature Overview
Remove the entire existing /frontend directory and create a clean Next.js 16.1 App Router frontend structure. This involves installing required dependencies (next, tailwindcss, shadcn-ui), implementing responsive UI with light/dark mode support, and integrating with the Phase 2a backend API to perform 5 basic Todo operations.

## Implementation Strategy
MVP approach: Start with User Story 1 (Access Clean Frontend Application) to establish the foundational structure, then incrementally add features for other user stories. Each user story is designed to be independently testable and deliverable.

## Dependencies
- User Story 1 (Access Clean Frontend Application) must be completed before other stories
- User Story 2 (Responsive Interface) and User Story 3 (Basic Todo Operations) can be developed in parallel after User Story 1
- User Story 4 (Navigate Application Pages) depends on User Story 1 and User Story 3

## Parallel Execution Opportunities
- [US2] and [US3] can be developed in parallel after [US1] completion
- Components within each user story can be developed in parallel where they don't share dependencies

---

## Phase 1: Setup

- [x] T001 Remove existing /frontend directory completely
- [x] T002 Create new /frontend directory structure per implementation plan
- [ ] T003 [P] Initialize Next.js 16.1 project with App Router
- [ ] T004 [P] Install required dependencies (next, react, react-dom)
- [ ] T005 [P] Install styling dependencies (tailwindcss, postcss, autoprefixer)
- [ ] T006 [P] Install UI dependencies (shadcn-ui, @radix-ui/react-slot, lucide-react)
- [ ] T007 [P] Install utility dependencies (clsx, tailwind-merge)
- [ ] T008 Set up basic project configuration files (package.json, tsconfig.json, next.config.ts, tailwind.config.ts)

## Phase 2: Foundational Structure

- [x] T009 [P] Create app directory structure (app/, components/, lib/, hooks/, public/)
- [x] T010 [P] Create root layout.tsx with basic HTML structure
- [x] T011 [P] Create globals.css with Tailwind imports and base styles
- [x] T012 [P] Create providers directory with theme-provider.tsx
- [x] T013 [P] Set up basic API client in lib/api.ts
- [x] T014 [P] Create initial environment configuration (.env.local)
- [x] T015 [P] Create basic CLAUDE.md file in frontend directory
- [x] T016 Update root CLAUDE.md to reference frontend CLAUDE.md

## Phase 3: User Story 1 - Access Clean Frontend Application [P1]

**Goal**: As a user, I want to access a clean, rebuilt frontend application without structural conflicts so that I can interact with the Todo application seamlessly.

**Independent Test**: The application can be accessed at the designated URL and displays a functional Todo interface without structural errors or broken components.

- [x] T017 [US1] Create main page.tsx in /app directory with basic Todo dashboard structure
- [x] T018 [P] [US1] Create Navbar component for navigation
- [x] T019 [P] [US1] Create basic TodoList component skeleton
- [x] T020 [P] [US1] Create TodoForm component skeleton
- [x] T021 [P] [US1] Create TodoItem component skeleton
- [x] T022 [US1] Implement basic routing structure with Next.js App Router
- [x] T023 [US1] Test that application loads without structural errors

## Phase 4: User Story 2 - Use Responsive Todo Interface [P1]

**Goal**: As a user, I want to use a responsive Todo application interface with light and dark modes so that I can comfortably manage my tasks on any device.

**Independent Test**: The application renders properly on different screen sizes and supports theme switching functionality.

- [x] T024 [US2] Implement theme context provider in providers/theme-provider.tsx
- [x] T025 [P] [US2] Create ThemeToggle component for switching themes
- [x] T026 [P] [US2] Implement localStorage persistence for theme preference
- [x] T027 [P] [US2] Create responsive layout for mobile, tablet, desktop
- [x] T028 [P] [US2] Add Tailwind CSS classes for responsive design
- [x] T029 [P] [US2] Implement CSS variables for theme colors
- [x] T030 [US2] Test theme switching functionality across all pages
- [x] T031 [US2] Test responsive design on different screen sizes

## Phase 5: User Story 3 - Perform Basic Todo Operations [P1]

**Goal**: As a user, I want to perform the 5 basic Todo operations (create, read, update, delete, mark complete/incomplete) so that I can effectively manage my tasks.

**Independent Test**: All five basic Todo operations can be performed through the frontend interface and successfully communicate with the backend API.

- [x] T032 [US3] Create complete API client service in lib/api.ts for backend integration
- [x] T033 [P] [US3] Create useTodos custom hook in hooks/useTodos.ts
- [x] T034 [P] [US3] Implement GET /todos API call in TodoList component
- [x] T035 [P] [US3] Implement POST /todos API call in TodoForm component
- [x] T036 [P] [US3] Implement PUT /todos/{id} API call in TodoItem component
- [x] T037 [P] [US3] Implement DELETE /todos/{id} API call in TodoItem component
- [x] T038 [P] [US3] Implement PATCH /todos/{id}/toggle API call in TodoItem component
- [x] T039 [P] [US3] Add loading states to all API calls
- [x] T040 [P] [US3] Add error handling for API calls
- [x] T041 [US3] Test all 5 basic Todo operations (CRUD + toggle completion)

## Phase 6: User Story 4 - Navigate Application Pages [P2]

**Goal**: As a user, I want to navigate between different application pages including the Todo list and profile page so that I can access all application features.

**Independent Test**: Navigation between pages works consistently and maintains application state appropriately.

- [x] T042 [US4] Create profile page structure in /app/profile/page.tsx
- [x] T043 [P] [US4] Implement profile page with theme settings
- [x] T044 [P] [US4] Add navigation links to profile page in Navbar
- [x] T045 [P] [US4] Implement navigation between Todo list and profile page
- [x] T046 [P] [US4] Add route protection if needed
- [x] T047 [US4] Test navigation between pages with state preservation
- [x] T048 [US4] Test that theme settings persist across page navigation

## Phase 7: Polish & Cross-Cutting Concerns

- [x] T049 [P] Implement toast notifications for error handling and user feedback
- [x] T050 [P] Add subtle animations for UI interactions (hover, fade, loading)
- [x] T051 [P] Implement proper error boundaries for error handling
- [x] T052 [P] Add loading skeletons for better UX
- [x] T053 [P] Optimize performance and ensure page load times under 3 seconds
- [x] T054 [P] Add proper TypeScript types for all components and API calls
- [x] T055 [P] Implement proper error handling for API connection failures
- [x] T056 [P] Add proper meta tags and SEO considerations
- [x] T057 [P] Test integration with Phase 2a backend API
- [x] T058 [P] Conduct end-to-end testing of all user stories
- [x] T059 [P] Update documentation and create README updates
- [x] T060 Final testing and validation of all requirements