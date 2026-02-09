# ADR-0001: Frontend Technology Stack

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2026-01-30
- **Feature:** 009-nextjs-frontend
- **Context:** Selection of technology stack for the Next.js frontend application that needs to provide responsive UI with light/dark theme support, integrate with existing backend API using REST endpoints, and implement all 5 basic todo operations (view, add, update, delete, mark complete/incomplete). The frontend must use client-side state with optimistic updates and handle API errors gracefully while maintaining session-based data isolation without authentication.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security?
     2) Alternatives: Multiple viable options considered with tradeoffs?
     3) Scope: Cross-cutting concern (not an isolated detail)?
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

Selected a cohesive frontend technology stack consisting of:
- **Framework**: Next.js 16.1 with App Router
- **Styling**: Tailwind CSS with Shadcn/UI components
- **Runtime**: React 18+ with TypeScript 5.0+
- **State Management**: React hooks with SWR/React Query for data fetching and optimistic updates
- **Theming**: Custom theme provider using Tailwind CSS and CSS variables
- **API Integration**: REST API client using fetch with proper error handling

## Consequences

### Positive

- Excellent developer experience with integrated tooling and hot reloading
- Strong TypeScript support for type safety across the application
- Built-in optimizations for performance (code splitting, image optimization)
- Robust routing capabilities with App Router for complex navigation
- Strong ecosystem with extensive community support and resources
- SEO-friendly with server-side rendering capabilities
- Responsive design made easier with Tailwind's utility classes
- Component reusability and maintainability through Shadcn/UI patterns
- Optimistic update patterns supported through SWR/React Query integration

### Negative

- Potential vendor lock-in to Next.js ecosystem and conventions
- Bundle size considerations with framework overhead
- Learning curve for developers unfamiliar with Next.js App Router patterns
- Potential complexity when customizing beyond default behaviors
- Dependency on Next.js release cycles for updates and fixes
- Possible performance overhead for very simple applications

## Alternatives Considered

**Alternative Stack A**: React + Vite + React Router + Styled Components
- Rejected because: Requires more manual setup for routing, SSR, and bundling; lacks the integrated optimization features of Next.js; more boilerplate code needed

**Alternative Stack B**: Remix + Tailwind CSS
- Rejected because: Smaller ecosystem compared to Next.js; less familiar to team members; though it has excellent data loading patterns, Next.js has broader adoption and tooling

**Alternative Stack C**: Astro + Tailwind CSS
- Rejected because: Better suited for content-heavy sites rather than interactive applications; would not provide the component-based interactivity needed for todo operations

**Alternative Stack D**: Vanilla React + TypeScript + Webpack + CSS Modules
- Rejected because: Requires significant manual configuration for build pipeline, routing, and optimization; much more boilerplate and maintenance overhead

## References

- Feature Spec: ../specs/009-nextjs-frontend/spec.md
- Implementation Plan: ../specs/009-nextjs-frontend/plan.md
- Related ADRs: None
- Evaluator Evidence: ../specs/009-nextjs-frontend/research.md <!-- link to eval notes/PHR showing graders and outcomes -->
