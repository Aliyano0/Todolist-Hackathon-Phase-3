# Research: Professional Frontend UI Upgrade

**Date**: 2026-02-09
**Feature**: 020-frontend-ui-upgrade
**Phase**: Phase 0 - Research & Technical Decisions

## Overview

This document captures technical research, decisions, and best practices for implementing the professional frontend UI upgrade. All decisions are based on official documentation accessed through MCP servers and Context7.

## Technical Decisions

### Decision 1: Animation Library - Framer Motion

**Decision**: Use Framer Motion (motion for web) for all animations

**Rationale**:
- Official React animation library with excellent Next.js 16 App Router support
- Declarative API that integrates seamlessly with React components
- Built-in support for reduced motion preferences via `useReducedMotion` hook
- Performance optimized with GPU acceleration and automatic will-change handling
- Spring physics support for natural-feeling animations
- Comprehensive documentation and active maintenance

**Alternatives Considered**:
- **React Spring**: More complex API, steeper learning curve, less declarative
- **CSS Animations**: Limited control, no JavaScript orchestration, harder to coordinate
- **GSAP**: Requires commercial license for some features, imperative API less React-friendly
- **React Transition Group**: Lower-level, requires more boilerplate, no spring physics

**Implementation Notes**:
- Install: `npm install framer-motion`
- Use `motion` components for animated elements
- Wrap page transitions with `AnimatePresence`
- Use `useReducedMotion()` hook to respect accessibility preferences
- Leverage `variants` for coordinated animations

**References**:
- Framer Motion documentation (via Context7)
- Next.js 16 App Router animation patterns (via nextjs MCP server)

---

### Decision 2: Design System Implementation - Tailwind CSS + Design Tokens

**Decision**: Implement design system using Tailwind CSS with custom design tokens in a centralized configuration

**Rationale**:
- Tailwind CSS already integrated in the project (constitution requirement)
- Design tokens provide single source of truth for colors, spacing, typography
- Tailwind's `extend` configuration allows custom tokens without losing defaults
- Type-safe design tokens via TypeScript module
- Easy to maintain consistency across all components
- Supports light/dark theme variants natively

**Alternatives Considered**:
- **CSS Variables**: Less type-safe, harder to integrate with Tailwind utilities
- **Styled Components**: Adds runtime overhead, conflicts with Tailwind approach
- **CSS Modules**: More boilerplate, less utility-first, harder to maintain consistency

**Implementation Notes**:
- Create `lib/design-tokens.ts` with TypeScript constants
- Extend `tailwind.config.js` with custom colors, spacing, typography
- Use semantic color names (e.g., `priority-high`, `priority-medium`, `priority-low`)
- Define animation durations and easing functions as tokens
- Export tokens for use in Framer Motion animations

**Design Token Structure**:
```typescript
export const colors = {
  priority: {
    high: '#EF4444',
    medium: '#F59E0B',
    low: '#10B981',
    none: '#6B7280'
  },
  // ... other colors
}

export const spacing = {
  xs: '4px',
  sm: '8px',
  md: '16px',
  // ... other spacing
}

export const animations = {
  duration: {
    fast: 150,
    normal: 200,
    slow: 300
  },
  easing: {
    easeInOut: [0.4, 0, 0.2, 1],
    easeOut: [0, 0, 0.2, 1]
  }
}
```

**References**:
- Tailwind CSS configuration documentation (via Context7)
- Design system best practices for React applications

---

### Decision 3: Component Architecture - Atomic Design Pattern

**Decision**: Organize components using Atomic Design principles (atoms, molecules, organisms)

**Rationale**:
- Clear component hierarchy improves maintainability
- Promotes reusability and composition
- Aligns with Shadcn UI component structure (already in use)
- Makes testing easier (test atoms independently, then compositions)
- Scales well as component library grows

**Alternatives Considered**:
- **Flat structure**: Harder to navigate as component count grows
- **Feature-based**: Creates duplication across features
- **Page-based**: Reduces reusability, harder to maintain consistency

**Implementation Notes**:
- **Atoms**: Basic UI elements (PriorityBadge, CategoryTag, Button from Shadcn)
- **Molecules**: Simple component combinations (TaskCard with badge + tag)
- **Organisms**: Complex sections (HeroSection, FeaturesSection, TaskList)
- **Templates**: Page layouts (Homepage, Dashboard)
- Keep existing Shadcn UI components in `components/ui/`
- New components in feature-specific directories (`homepage/`, `dashboard/`, `animations/`)

**Component Hierarchy**:
```
Atoms: PriorityBadge, CategoryTag, Button, Input
↓
Molecules: TaskCard (badge + tag + actions)
↓
Organisms: TaskList (multiple TaskCards + animations)
↓
Templates: Dashboard (TaskList + filters + header)
```

**References**:
- Atomic Design methodology by Brad Frost
- React component composition patterns

---

### Decision 4: Animation Strategy - Progressive Enhancement

**Decision**: Implement animations as progressive enhancement with graceful degradation

**Rationale**:
- Respects user preferences (reduced motion, low-end devices)
- Ensures core functionality works without animations
- Improves accessibility compliance (WCAG 2.1 Level AA)
- Prevents performance issues on older devices
- Aligns with constitution requirement for reduced motion support

**Alternatives Considered**:
- **Animation-first**: Risks accessibility violations and performance issues
- **No animations**: Misses opportunity for improved UX and polish
- **CSS-only fallback**: Harder to coordinate, less control

**Implementation Notes**:
- Use `useReducedMotion()` hook from Framer Motion
- Provide instant transitions when reduced motion is preferred
- Test on low-end devices (throttle CPU in Chrome DevTools)
- Use `will-change` sparingly (only during animation)
- Prefer `transform` and `opacity` for GPU acceleration
- Keep animation durations under 300ms for responsiveness

**Reduced Motion Implementation**:
```typescript
const shouldReduceMotion = useReducedMotion()

const variants = {
  hidden: { opacity: 0, y: shouldReduceMotion ? 0 : 20 },
  visible: { opacity: 1, y: 0 }
}
```

**References**:
- WCAG 2.1 Animation guidelines
- Framer Motion reduced motion documentation

---

### Decision 5: Homepage Layout - Hero-First with Scroll Sections

**Decision**: Implement homepage with full-viewport hero section followed by scrollable content sections

**Rationale**:
- Hero-first design is industry standard for SaaS landing pages
- Full viewport hero creates strong first impression
- Scroll-based sections encourage exploration
- Clear visual hierarchy guides user attention
- Supports both desktop and mobile layouts

**Alternatives Considered**:
- **Multi-column layout**: Less mobile-friendly, harder to prioritize content
- **Carousel hero**: Lower conversion rates, accessibility issues
- **Video background**: Performance concerns, distracting

**Implementation Notes**:
- Hero section: 100vh height on desktop, auto on mobile
- Sections: Features (3-column grid), How It Works (3-step timeline), CTA (centered), Footer
- Use Intersection Observer for scroll-triggered animations
- Implement smooth scroll behavior for anchor links
- Ensure keyboard navigation works for all interactive elements

**Section Structure**:
1. **Hero**: Full viewport, gradient background, centered content, CTA buttons
2. **Features**: 4 features in 2x2 grid (desktop) or stacked (mobile), icons + text
3. **How It Works**: 3 steps with numbers, arrows between steps, visual flow
4. **CTA**: Final conversion prompt, primary button, secondary link
5. **Footer**: Links (About, Privacy, Terms, Contact), copyright

**References**:
- SaaS landing page design patterns
- Next.js 16 App Router page layout best practices

---

### Decision 6: Dashboard Redesign - Card-Based Layout with Visual Hierarchy

**Decision**: Redesign dashboard using card-based layout with clear visual hierarchy for priorities and categories

**Rationale**:
- Card-based design is familiar and scannable
- Visual hierarchy (borders, badges, tints) enables quick task identification
- Supports both list and grid views
- Works well with animations (cards can animate independently)
- Aligns with modern task management UI patterns (Todoist, Asana, Linear)

**Alternatives Considered**:
- **Table layout**: Less visual, harder to show rich metadata
- **Kanban board**: Requires drag-and-drop, more complex for basic use case
- **Timeline view**: Not suitable for task management without due dates

**Implementation Notes**:
- Task cards with 4px left border for priority (color-coded)
- Priority badge in top-right corner (pill shape, matching border color)
- Category tag below title (rounded, subtle background tint)
- Hover effect: lift card (translateY -2px) + shadow increase
- Completed tasks: reduced opacity, strikethrough text
- Empty state: illustration + helpful message

**Visual Hierarchy Rules**:
1. **Priority** (most prominent): Left border + badge
2. **Category** (secondary): Background tint + tag
3. **Status** (tertiary): Checkbox + opacity
4. **Actions** (on-demand): Show on hover/focus

**References**:
- Task management UI patterns
- Material Design card component guidelines

---

### Decision 7: Theme System - Extend Existing Light/Dark Mode

**Decision**: Extend existing theme system with new design tokens while maintaining light/dark mode support

**Rationale**:
- Theme system already implemented (constitution requirement to maintain)
- New design tokens must work in both themes
- Consistency with existing pages (login, register, profile)
- User preference already stored and respected

**Alternatives Considered**:
- **Replace theme system**: Breaks existing functionality, violates constitution
- **Add third theme**: Unnecessary complexity, not in requirements
- **Ignore dark mode**: Violates constitution requirement

**Implementation Notes**:
- Define color tokens with light/dark variants in Tailwind config
- Use CSS variables for theme-aware colors
- Test all new components in both themes
- Ensure contrast ratios meet WCAG AA in both themes
- Priority colors work in both themes (adjust saturation/lightness if needed)

**Theme Token Example**:
```javascript
// tailwind.config.js
colors: {
  'priority-high': {
    light: '#EF4444',
    dark: '#F87171'  // Lighter for dark mode
  }
}
```

**References**:
- Tailwind CSS dark mode documentation
- WCAG contrast ratio guidelines

---

### Decision 8: Testing Strategy - Component Tests + E2E Visual Tests

**Decision**: Implement component tests with React Testing Library and E2E visual tests with Playwright

**Rationale**:
- Component tests verify behavior and accessibility
- E2E tests verify visual appearance and animations
- Playwright supports visual regression testing
- Aligns with TDD workflow (write test first, then implement)
- Constitution requires TDD for all implementation

**Alternatives Considered**:
- **Jest snapshots only**: Brittle, doesn't test behavior
- **Manual testing only**: Not repeatable, violates TDD requirement
- **Cypress**: Playwright has better Next.js 16 support and visual testing

**Implementation Notes**:
- Component tests: Render, user interactions, accessibility (aria labels, keyboard nav)
- E2E tests: Full page flows, animation verification, theme switching
- Visual regression: Screenshot comparison for homepage and dashboard
- Test reduced motion: Mock `matchMedia` to test both modes

**Test Coverage Goals**:
- All new components: 80%+ coverage
- Critical user flows: 100% E2E coverage (homepage visit, dashboard view)
- Accessibility: All interactive elements have proper ARIA labels

**References**:
- React Testing Library best practices
- Playwright visual testing documentation

---

## Best Practices Summary

### Performance
- Use `transform` and `opacity` for animations (GPU accelerated)
- Lazy load images with Next.js Image component
- Code split homepage sections (dynamic imports)
- Minimize layout shifts (reserve space for dynamic content)
- Monitor Core Web Vitals (LCP, FID, CLS)

### Accessibility
- Respect `prefers-reduced-motion` media query
- Ensure keyboard navigation works for all interactions
- Provide ARIA labels for icon-only buttons
- Maintain WCAG AA contrast ratios in both themes
- Test with screen readers (NVDA, VoiceOver)

### Maintainability
- Use design tokens for all visual properties
- Document component APIs with TypeScript types
- Keep components small and focused (single responsibility)
- Write tests before implementation (TDD)
- Update CLAUDE.md with new patterns and conventions

### Security
- No changes to authentication (frontend only)
- Sanitize user input in task titles/descriptions (already handled by backend)
- No new API endpoints (uses existing backend)

---

## Open Questions

None - all technical decisions are clear and documented.

---

## Next Steps

Proceed to Phase 1:
1. Create data-model.md (component data structures)
2. Create contracts/components.md (component API contracts)
3. Create quickstart.md (developer setup guide)
4. Update frontend/CLAUDE.md with new patterns
