# Tasks: Frontend Structure Resolution

## Feature Overview
Resolve the conflict between two app directories (/src/app and /app) in the frontend by consolidating to a single Next.js 16+ App Router compliant structure. This involves migrating necessary files from /src/app to /app, adding missing files (layout.tsx, page.tsx, components for Todo UI, profile page), implementing responsive UI with light/dark mode support, and integrating with backend API to perform 5 basic Todo operations.

## Implementation Strategy
MVP approach: Start with User Story 1 (Access Unified Frontend Application) to establish the foundational structure, then incrementally add features for other user stories. Each user story is designed to be independently testable and deliverable.

## Dependencies
- User Story 1 (Access Unified Frontend Application) must be completed before other stories
- User Story 2 (Responsive Interface) and User Story 3 (Basic Todo Operations) can be developed in parallel after User Story 1
- User Story 4 (Navigate Application Pages) depends on User Story 1 and User Story 3

## Parallel Execution Opportunities
- [US2] and [US3] can be developed in parallel after [US1] completion
- Components within each user story can be developed in parallel where they don't share dependencies

---

## Phase 1: Setup

- [ ] T001 Create frontend project structure per implementation plan
- [ ] T002 [P] Install Next.js 16+ dependencies in frontend directory
- [ ] T003 [P] Configure Tailwind CSS for the project
- [ ] T004 [P] Configure Shadcn UI components for the project
- [ ] T005 [P] Set up TypeScript configuration
- [ ] T006 [P] Set up ESLint and Prettier configurations
- [ ] T007 Create initial package.json with required dependencies

## Phase 2: Foundational Structure

- [x] T008 [P] Consolidate app directories: move files from /src/app to /app
- [x] T009 [P] Remove /src/app directory after consolidation
- [x] T010 [P] Create root layout.tsx in /app directory with theme provider
- [x] T011 [P] Create global CSS file with Tailwind imports
- [x] T012 [P] Create providers directory with theme provider component
- [x] T013 [P] Set up Next.js configuration for App Router
- [x] T014 [P] Create lib directory with utility functions
- [x] T015 [P] Create hooks directory with custom React hooks

## Phase 3: User Story 1 - Access Unified Frontend Application [P1]

**Goal**: As a user, I want to access a unified frontend application without encountering structural conflicts so that I can interact with the Todo application seamlessly.

**Independent Test**: The application can be accessed at the designated URL and displays a functional Todo interface without structural errors or broken components.

- [x] T016 [US1] Create main page.tsx in /app directory with basic Todo dashboard
- [x] T017 [P] [US1] Create Navbar component for navigation
- [x] T018 [P] [US1] Create basic TodoList component placeholder
- [x] T019 [P] [US1] Create TodoForm component placeholder
- [x] T020 [P] [US1] Create TodoItem component placeholder
- [x] T021 [US1] Implement basic routing structure
- [x] T022 [US1] Test that application loads without structural errors

## Phase 4: User Story 2 - Use Responsive Todo Interface [P1]

**Goal**: As a user, I want to use a responsive Todo application interface with light and dark modes so that I can comfortably manage my tasks on any device.

**Independent Test**: The application renders properly on different screen sizes and supports theme switching functionality.

- [x] T023 [US2] Implement theme context provider in providers/theme-provider.tsx
- [x] T024 [P] [US2] Create ThemeToggle component for switching themes
- [x] T025 [P] [US2] Implement localStorage persistence for theme preference
- [x] T026 [P] [US2] Create responsive layout for mobile, tablet, desktop
- [x] T027 [P] [US2] Add Tailwind CSS classes for responsive design
- [x] T028 [P] [US2] Implement CSS variables for theme colors
- [x] T029 [US2] Test theme switching functionality across all pages
- [x] T030 [US2] Test responsive design on different screen sizes

## Phase 5: User Story 3 - Perform Basic Todo Operations [P1]

**Goal**: As a user, I want to perform the 5 basic Todo operations (create, read, update, delete, mark complete/incomplete) so that I can effectively manage my tasks.

**Independent Test**: All five basic Todo operations can be performed through the frontend interface and successfully communicate with the backend API.

- [x] T031 [US3] Create API client service in lib/api.ts for backend integration
- [x] T032 [P] [US3] Create useTodos custom hook in hooks/useTodos.ts
- [x] T033 [P] [US3] Implement GET /todos API call in TodoList component
- [x] T034 [P] [US3] Implement POST /todos API call in TodoForm component
- [x] T035 [P] [US3] Implement PUT /todos/{id} API call in TodoItem component
- [x] T036 [P] [US3] Implement DELETE /todos/{id} API call in TodoItem component
- [x] T037 [P] [US3] Implement PATCH /todos/{id}/toggle API call in TodoItem component
- [x] T038 [P] [US3] Add loading states to all API calls
- [x] T039 [P] [US3] Add error handling for API calls
- [x] T040 [US3] Test all 5 basic Todo operations (CRUD + toggle completion)

## Phase 6: User Story 4 - Navigate Application Pages [P2]

**Goal**: As a user, I want to navigate between different application pages including the Todo list and profile page so that I can access all application features.

**Independent Test**: Navigation between pages works consistently and maintains application state appropriately.

- [x] T041 [US4] Create profile page structure in /app/profile/page.tsx
- [x] T042 [P] [US4] Implement profile page with theme settings
- [x] T043 [P] [US4] Add navigation links to profile page in Navbar
- [x] T044 [P] [US4] Implement navigation between Todo list and profile page
- [x] T045 [P] [US4] Add route protection if needed
- [x] T046 [US4] Test navigation between pages with state preservation
- [x] T047 [US4] Test that theme settings persist across page navigation

## Phase 7: Polish & Cross-Cutting Concerns

- [x] T048 [P] Implement toast notifications for error handling and user feedback
- [x] T049 [P] Add subtle animations for UI interactions (hover, fade, loading)
- [x] T050 [P] Implement proper error boundaries for error handling
- [x] T051 [P] Add loading skeletons for better UX
- [x] T052 [P] Optimize performance and ensure page load times under 3 seconds
- [x] T053 [P] Add proper TypeScript types for all components and API calls
- [x] T054 [P] Create CLAUDE.md file in frontend directory with frontend-specific instructions
- [x] T055 [P] Update root CLAUDE.md to reference frontend CLAUDE.md
- [x] T056 [P] Add proper meta tags and SEO considerations
- [x] T057 [P] Test integration with Phase 2a backend API
- [x] T058 [P] Conduct end-to-end testing of all user stories
- [x] T059 [P] Update documentation and create README updates
- [x] T060 Final testing and validation of all requirements