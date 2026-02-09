# Quickstart Guide: Frontend UI Upgrade Development

**Date**: 2026-02-09
**Feature**: 020-frontend-ui-upgrade
**Phase**: Phase 1 - Developer Setup

## Overview

This guide helps developers set up their environment and start implementing the professional frontend UI upgrade. Follow these steps to get started quickly.

---

## Prerequisites

- Node.js 18+ installed
- npm or yarn package manager
- Git configured
- Code editor (VS Code recommended)
- Basic knowledge of Next.js 16, React 19, TypeScript, Tailwind CSS

---

## Initial Setup

### 1. Checkout Feature Branch

```bash
# Ensure you're in the project root
cd /mnt/c/Study/claude-code/todolist-hackathon/todolist-phase-1

# Checkout the feature branch
git checkout 020-frontend-ui-upgrade

# Pull latest changes
git pull origin 020-frontend-ui-upgrade
```

### 2. Install Dependencies

```bash
# Navigate to frontend directory
cd frontend

# Install existing dependencies
npm install

# Install Framer Motion for animations
npm install framer-motion

# Verify installation
npm list framer-motion
```

### 3. Review Documentation

Read these documents in order:
1. `specs/020-frontend-ui-upgrade/spec.md` - Feature requirements
2. `specs/020-frontend-ui-upgrade/research.md` - Technical decisions
3. `specs/020-frontend-ui-upgrade/data-model.md` - Component data structures
4. `specs/020-frontend-ui-upgrade/contracts/components.md` - Component contracts

---

## Project Structure

### Frontend Directory Layout

```
frontend/
├── app/                    # Next.js App Router pages
│   ├── page.tsx           # Homepage (TO BE CREATED)
│   ├── todos/page.tsx     # Dashboard (TO BE UPGRADED)
│   └── ...                # Other pages (maintain)
├── components/
│   ├── ui/                # Shadcn UI components (existing)
│   ├── homepage/          # Homepage components (TO BE CREATED)
│   ├── dashboard/         # Dashboard components (TO BE CREATED)
│   ├── animations/        # Animation wrappers (TO BE CREATED)
│   └── layout/            # Layout components (TO BE UPDATED)
├── lib/
│   ├── design-tokens.ts   # Design system tokens (TO BE CREATED)
│   └── animations.ts      # Animation utilities (TO BE CREATED)
└── hooks/
    └── useReducedMotion.ts # Reduced motion hook (TO BE CREATED)
```

---

## Development Workflow (TDD)

### Red-Green-Refactor Cycle

For each component:

#### 1. RED - Write Failing Test

```bash
# Create test file
touch frontend/components/homepage/__tests__/HeroSection.test.tsx

# Write test that fails
npm test -- HeroSection.test.tsx
```

Example test:
```typescript
import { render, screen } from '@testing-library/react'
import { HeroSection } from '../HeroSection'

describe('HeroSection', () => {
  it('renders hero section with title and CTAs', () => {
    render(
      <HeroSection
        title="AI Powered Todo Web App"
        subtitle="Manage your tasks efficiently"
        primaryCTA="Sign Up"
        secondaryCTA="Login"
        onPrimaryCTAClick={() => {}}
        onSecondaryCTAClick={() => {}}
        isAuthenticated={false}
      />
    )

    expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent('AI Powered Todo Web App')
    expect(screen.getByRole('button', { name: /sign up/i })).toBeInTheDocument()
  })
})
```

#### 2. GREEN - Implement Minimal Code

```bash
# Create component file
touch frontend/components/homepage/HeroSection.tsx

# Implement component to pass test
```

Example implementation:
```typescript
'use client'

import { motion } from 'framer-motion'
import { useReducedMotion } from '@/hooks/useReducedMotion'

export interface HeroSectionProps {
  title: string
  subtitle: string
  primaryCTA: string
  secondaryCTA: string
  onPrimaryCTAClick: () => void
  onSecondaryCTAClick: () => void
  isAuthenticated: boolean
}

export function HeroSection({
  title,
  subtitle,
  primaryCTA,
  secondaryCTA,
  onPrimaryCTAClick,
  onSecondaryCTAClick,
  isAuthenticated
}: HeroSectionProps) {
  const shouldReduceMotion = useReducedMotion()

  const variants = {
    hidden: { opacity: 0, y: shouldReduceMotion ? 0 : 20 },
    visible: { opacity: 1, y: 0 }
  }

  return (
    <motion.section
      className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-500 to-purple-600"
      initial="hidden"
      animate="visible"
      variants={variants}
      transition={{ duration: 0.3 }}
    >
      <div className="text-center text-white px-4">
        <h1 className="text-5xl font-bold mb-4">{title}</h1>
        <p className="text-xl mb-8">{subtitle}</p>
        <div className="flex gap-4 justify-center">
          <button
            onClick={onPrimaryCTAClick}
            className="px-8 py-3 bg-white text-blue-600 rounded-lg font-semibold hover:scale-105 transition-transform"
          >
            {primaryCTA}
          </button>
          <button
            onClick={onSecondaryCTAClick}
            className="px-8 py-3 border-2 border-white text-white rounded-lg font-semibold hover:bg-white hover:text-blue-600 transition-colors"
          >
            {secondaryCTA}
          </button>
        </div>
      </div>
    </motion.section>
  )
}
```

#### 3. REFACTOR - Improve Code

```bash
# Run tests to ensure they still pass
npm test -- HeroSection.test.tsx

# Refactor for better structure, extract utilities, etc.
```

---

## Design System Setup

### 1. Create Design Tokens

```bash
# Create design tokens file
touch frontend/lib/design-tokens.ts
```

Copy token definitions from `data-model.md`:
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

export const animations = {
  duration: {
    fast: 150,
    normal: 200,
    medium: 250,
    slow: 300
  },
  // ... other animation tokens
}
```

### 2. Extend Tailwind Config

```bash
# Edit tailwind.config.js
```

Add custom tokens:
```javascript
import { colors } from './lib/design-tokens'

module.exports = {
  theme: {
    extend: {
      colors: {
        'priority-high': colors.priority.high,
        'priority-medium': colors.priority.medium,
        'priority-low': colors.priority.low,
        'priority-none': colors.priority.none,
      }
    }
  }
}
```

### 3. Create Animation Utilities

```bash
# Create animation utilities file
touch frontend/lib/animations.ts
```

Copy animation variants from `data-model.md`.

---

## Component Development Order

Implement components in this order (dependencies first):

### Phase 1: Foundation (Week 1)
1. **Design System**
   - [ ] `lib/design-tokens.ts` - Design tokens
   - [ ] `lib/animations.ts` - Animation utilities
   - [ ] `hooks/useReducedMotion.ts` - Reduced motion hook
   - [ ] Update `tailwind.config.js` - Extend with tokens

2. **Animation Wrappers**
   - [ ] `components/animations/FadeIn.tsx`
   - [ ] `components/animations/SlideIn.tsx`
   - [ ] `components/animations/ScaleIn.tsx`
   - [ ] `components/animations/PageTransition.tsx`

### Phase 2: Atoms (Week 1-2)
3. **Basic Components**
   - [ ] `components/dashboard/PriorityBadge.tsx`
   - [ ] `components/dashboard/CategoryTag.tsx`

### Phase 3: Molecules (Week 2)
4. **Composite Components**
   - [ ] `components/dashboard/TaskCard.tsx`
   - [ ] `components/dashboard/TaskForm.tsx`

### Phase 4: Organisms (Week 2-3)
5. **Homepage Sections**
   - [ ] `components/homepage/HeroSection.tsx`
   - [ ] `components/homepage/FeaturesSection.tsx`
   - [ ] `components/homepage/HowItWorksSection.tsx`
   - [ ] `components/homepage/CTASection.tsx`
   - [ ] `components/layout/Footer.tsx`

6. **Dashboard Components**
   - [ ] `components/dashboard/TaskList.tsx`

### Phase 5: Templates (Week 3)
7. **Pages**
   - [ ] `app/page.tsx` - Homepage
   - [ ] `app/todos/page.tsx` - Dashboard (upgrade)
   - [ ] `components/layout/Navbar.tsx` - Update with conditional logic

### Phase 6: Polish (Week 4)
8. **Testing & Refinement**
   - [ ] E2E tests with Playwright
   - [ ] Visual regression tests
   - [ ] Accessibility audit
   - [ ] Performance optimization

---

## Running the Application

### Development Server

```bash
# From frontend directory
npm run dev

# Application runs at http://localhost:3000
```

### Running Tests

```bash
# Run all tests
npm test

# Run tests in watch mode
npm test -- --watch

# Run specific test file
npm test -- HeroSection.test.tsx

# Run tests with coverage
npm test -- --coverage
```

### E2E Tests

```bash
# Install Playwright (if not installed)
npx playwright install

# Run E2E tests
npm run test:e2e

# Run E2E tests in UI mode
npm run test:e2e -- --ui
```

---

## Useful Commands

### Component Generation

```bash
# Create new component with test
mkdir -p frontend/components/homepage
touch frontend/components/homepage/HeroSection.tsx
touch frontend/components/homepage/__tests__/HeroSection.test.tsx
```

### Type Checking

```bash
# Check TypeScript types
npm run type-check

# Watch mode
npm run type-check -- --watch
```

### Linting

```bash
# Run ESLint
npm run lint

# Fix auto-fixable issues
npm run lint -- --fix
```

### Build

```bash
# Build for production
npm run build

# Check build output
npm run start
```

---

## Debugging Tips

### Animation Issues

1. **Animations not working**:
   - Check if Framer Motion is installed: `npm list framer-motion`
   - Verify component is client component: `'use client'` directive
   - Check browser console for errors

2. **Animations too slow/fast**:
   - Adjust duration in animation tokens
   - Use Chrome DevTools Performance tab to profile

3. **Reduced motion not working**:
   - Test with browser DevTools: Rendering > Emulate CSS media feature prefers-reduced-motion
   - Verify `useReducedMotion()` hook is used

### Styling Issues

1. **Tailwind classes not applying**:
   - Run `npm run dev` to rebuild Tailwind
   - Check if class names are in `safelist` if dynamic
   - Verify `tailwind.config.js` includes correct paths

2. **Dark mode not working**:
   - Check theme provider is wrapping app
   - Verify dark mode classes are defined
   - Test theme toggle functionality

### Testing Issues

1. **Tests failing**:
   - Check test setup in `jest.config.js`
   - Verify mocks for Framer Motion: `jest.mock('framer-motion')`
   - Check if async operations need `waitFor`

---

## Resources

### Documentation
- [Next.js 16 Documentation](https://nextjs.org/docs) (via nextjs MCP server)
- [Framer Motion Documentation](https://www.framer.com/motion/) (via Context7)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs) (via Context7)
- [Shadcn UI Components](https://ui.shadcn.com/) (via Context7)

### Internal Documentation
- Feature Spec: `specs/020-frontend-ui-upgrade/spec.md`
- Research: `specs/020-frontend-ui-upgrade/research.md`
- Data Model: `specs/020-frontend-ui-upgrade/data-model.md`
- Component Contracts: `specs/020-frontend-ui-upgrade/contracts/components.md`
- Frontend CLAUDE.md: `frontend/CLAUDE.md`

### Design References
- Priority colors: Red (#EF4444), Yellow (#F59E0B), Green (#10B981), Gray (#6B7280)
- Animation durations: Fast (150ms), Normal (200ms), Medium (250ms), Slow (300ms)
- Spacing scale: 4px, 8px, 16px, 24px, 32px, 48px, 64px
- Border radius: 8px for cards and buttons

---

## Getting Help

1. **Check documentation first**: Review spec, research, and contracts
2. **Use MCP servers**: Query Context7 for library documentation
3. **Review existing code**: Look at similar components in the codebase
4. **Ask specific questions**: Include error messages, code snippets, and what you've tried

---

## Next Steps

After setup:
1. Read all documentation in `specs/020-frontend-ui-upgrade/`
2. Start with Phase 1 (Foundation) components
3. Follow TDD workflow (Red-Green-Refactor)
4. Commit frequently with clear messages
5. Create PR when feature is complete

**Ready to start? Begin with creating `lib/design-tokens.ts`!**
