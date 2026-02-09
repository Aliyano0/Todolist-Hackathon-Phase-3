# Data Model: Component Data Structures

**Date**: 2026-02-09
**Feature**: 020-frontend-ui-upgrade
**Phase**: Phase 1 - Component Data Structures

## Overview

This document defines the data structures, TypeScript interfaces, and props contracts for all components in the frontend UI upgrade. These structures ensure type safety and clear component APIs.

## Design System Tokens

### Color Tokens

```typescript
// lib/design-tokens.ts

export const colors = {
  priority: {
    high: '#EF4444',
    medium: '#F59E0B',
    low: '#10B981',
    none: '#6B7280'
  },
  category: {
    work: '#3B82F6',
    personal: '#8B5CF6',
    shopping: '#EC4899',
    health: '#10B981',
    other: '#6B7280'
  }
} as const

export type PriorityColor = keyof typeof colors.priority
export type CategoryColor = keyof typeof colors.category
```

### Spacing Tokens

```typescript
export const spacing = {
  xs: '4px',
  sm: '8px',
  md: '16px',
  lg: '24px',
  xl: '32px',
  '2xl': '48px',
  '3xl': '64px'
} as const

export type SpacingToken = keyof typeof spacing
```

### Typography Tokens

```typescript
export const typography = {
  fontSize: {
    xs: '12px',
    sm: '14px',
    base: '16px',
    lg: '18px',
    xl: '20px',
    '2xl': '24px',
    '3xl': '32px'
  },
  lineHeight: {
    tight: 1.2,
    normal: 1.5,
    relaxed: 1.75
  },
  fontWeight: {
    normal: 400,
    medium: 500,
    semibold: 600,
    bold: 700
  }
} as const
```

### Animation Tokens

```typescript
export const animations = {
  duration: {
    fast: 150,
    normal: 200,
    medium: 250,
    slow: 300
  },
  easing: {
    easeInOut: [0.4, 0, 0.2, 1] as const,
    easeOut: [0, 0, 0.2, 1] as const,
    easeIn: [0.4, 0, 1, 1] as const
  },
  spring: {
    default: { stiffness: 300, damping: 30 },
    gentle: { stiffness: 200, damping: 25 },
    stiff: { stiffness: 400, damping: 35 }
  }
} as const
```

---

## Component Data Structures

### Homepage Components

#### HeroSection

```typescript
// components/homepage/HeroSection.tsx

export interface HeroSectionProps {
  /** Main heading text */
  title: string
  /** Subheading/value proposition */
  subtitle: string
  /** Primary CTA button text */
  primaryCTA: string
  /** Secondary CTA button text */
  secondaryCTA: string
  /** Primary CTA click handler */
  onPrimaryCTAClick: () => void
  /** Secondary CTA click handler */
  onSecondaryCTAClick: () => void
  /** Whether user is authenticated */
  isAuthenticated: boolean
}
```

#### FeaturesSection

```typescript
// components/homepage/FeaturesSection.tsx

export interface Feature {
  /** Unique identifier */
  id: string
  /** Feature title */
  title: string
  /** Feature description */
  description: string
  /** Icon name (from icon library) */
  icon: string
}

export interface FeaturesSectionProps {
  /** Array of features to display */
  features: Feature[]
  /** Section heading */
  heading: string
  /** Section subheading (optional) */
  subheading?: string
}
```

#### HowItWorksSection

```typescript
// components/homepage/HowItWorksSection.tsx

export interface Step {
  /** Step number (1, 2, 3) */
  number: number
  /** Step title */
  title: string
  /** Step description */
  description: string
}

export interface HowItWorksSectionProps {
  /** Array of steps (3 steps) */
  steps: Step[]
  /** Section heading */
  heading: string
}
```

#### CTASection

```typescript
// components/homepage/CTASection.tsx

export interface CTASectionProps {
  /** CTA heading */
  heading: string
  /** CTA description */
  description: string
  /** Button text */
  buttonText: string
  /** Button click handler */
  onButtonClick: () => void
}
```

#### Footer

```typescript
// components/layout/Footer.tsx

export interface FooterLink {
  /** Link label */
  label: string
  /** Link URL */
  href: string
}

export interface FooterProps {
  /** Array of footer links */
  links: FooterLink[]
  /** Copyright text */
  copyright: string
}
```

---

### Dashboard Components

#### TaskCard

```typescript
// components/dashboard/TaskCard.tsx

export type Priority = 'high' | 'medium' | 'low' | 'none'
export type Category = 'work' | 'personal' | 'shopping' | 'health' | 'other'

export interface Task {
  /** Unique task ID */
  id: string
  /** Task title */
  title: string
  /** Task description (optional) */
  description?: string
  /** Task priority */
  priority: Priority
  /** Task category */
  category: Category
  /** Completion status */
  completed: boolean
  /** Creation timestamp */
  createdAt: string
  /** Last update timestamp */
  updatedAt: string
}

export interface TaskCardProps {
  /** Task data */
  task: Task
  /** Complete task handler */
  onComplete: (taskId: string) => void
  /** Edit task handler */
  onEdit: (taskId: string) => void
  /** Delete task handler */
  onDelete: (taskId: string) => void
  /** Whether card is in edit mode */
  isEditing?: boolean
}
```

#### PriorityBadge

```typescript
// components/dashboard/PriorityBadge.tsx

export interface PriorityBadgeProps {
  /** Priority level */
  priority: Priority
  /** Badge size */
  size?: 'sm' | 'md' | 'lg'
  /** Show icon */
  showIcon?: boolean
}
```

#### CategoryTag

```typescript
// components/dashboard/CategoryTag.tsx

export interface CategoryTagProps {
  /** Category name */
  category: Category
  /** Tag size */
  size?: 'sm' | 'md' | 'lg'
  /** Show icon */
  showIcon?: boolean
}
```

#### TaskList

```typescript
// components/dashboard/TaskList.tsx

export interface TaskListProps {
  /** Array of tasks */
  tasks: Task[]
  /** Loading state */
  isLoading: boolean
  /** Error message (if any) */
  error?: string
  /** Complete task handler */
  onComplete: (taskId: string) => void
  /** Edit task handler */
  onEdit: (taskId: string) => void
  /** Delete task handler */
  onDelete: (taskId: string) => void
  /** Empty state message */
  emptyMessage?: string
}
```

#### TaskForm

```typescript
// components/dashboard/TaskForm.tsx

export interface TaskFormData {
  /** Task title */
  title: string
  /** Task description */
  description: string
  /** Task priority */
  priority: Priority
  /** Task category */
  category: Category
}

export interface TaskFormProps {
  /** Initial form data (for edit mode) */
  initialData?: Partial<TaskFormData>
  /** Form submit handler */
  onSubmit: (data: TaskFormData) => void
  /** Form cancel handler */
  onCancel: () => void
  /** Submit button text */
  submitText?: string
  /** Whether form is submitting */
  isSubmitting?: boolean
}
```

---

### Animation Components

#### PageTransition

```typescript
// components/animations/PageTransition.tsx

export interface PageTransitionProps {
  /** Child elements to animate */
  children: React.ReactNode
  /** Transition direction */
  direction?: 'up' | 'down' | 'left' | 'right'
  /** Animation duration (ms) */
  duration?: number
}
```

#### FadeIn

```typescript
// components/animations/FadeIn.tsx

export interface FadeInProps {
  /** Child elements to animate */
  children: React.ReactNode
  /** Animation delay (ms) */
  delay?: number
  /** Animation duration (ms) */
  duration?: number
  /** Whether to animate on mount */
  animateOnMount?: boolean
}
```

#### SlideIn

```typescript
// components/animations/SlideIn.tsx

export interface SlideInProps {
  /** Child elements to animate */
  children: React.ReactNode
  /** Slide direction */
  direction: 'up' | 'down' | 'left' | 'right'
  /** Slide distance (px) */
  distance?: number
  /** Animation delay (ms) */
  delay?: number
  /** Animation duration (ms) */
  duration?: number
}
```

#### ScaleIn

```typescript
// components/animations/ScaleIn.tsx

export interface ScaleInProps {
  /** Child elements to animate */
  children: React.ReactNode
  /** Initial scale (0-1) */
  initialScale?: number
  /** Animation delay (ms) */
  delay?: number
  /** Animation duration (ms) */
  duration?: number
}
```

---

### Layout Components

#### Navbar

```typescript
// components/layout/Navbar.tsx

export interface NavLink {
  /** Link label */
  label: string
  /** Link URL */
  href: string
  /** Whether link is active */
  isActive?: boolean
}

export interface NavbarProps {
  /** Whether user is authenticated */
  isAuthenticated: boolean
  /** User email (if authenticated) */
  userEmail?: string
  /** Navigation links */
  links: NavLink[]
  /** Logout handler */
  onLogout?: () => void
}
```

---

## State Management

### Authentication State

```typescript
// providers/AuthProvider.tsx

export interface User {
  /** User ID */
  id: string
  /** User email */
  email: string
  /** Email verification status */
  emailVerified: boolean
}

export interface AuthState {
  /** Current user (null if not authenticated) */
  user: User | null
  /** Whether auth is loading */
  isLoading: boolean
  /** Authentication error */
  error: string | null
}

export interface AuthContextValue extends AuthState {
  /** Login function */
  login: (email: string, password: string) => Promise<void>
  /** Logout function */
  logout: () => Promise<void>
  /** Register function */
  register: (email: string, password: string) => Promise<void>
}
```

### Theme State

```typescript
// providers/ThemeProvider.tsx (existing)

export type Theme = 'light' | 'dark'

export interface ThemeContextValue {
  /** Current theme */
  theme: Theme
  /** Toggle theme function */
  toggleTheme: () => void
}
```

---

## API Response Types

### Task API Responses

```typescript
// lib/api.ts

export interface TaskResponse {
  id: string
  title: string
  description: string
  priority: Priority
  category: Category
  completed: boolean
  created_at: string
  updated_at: string
  user_id: string
}

export interface TaskListResponse {
  tasks: TaskResponse[]
  total: number
}

export interface TaskCreateRequest {
  title: string
  description: string
  priority: Priority
  category: Category
}

export interface TaskUpdateRequest {
  title?: string
  description?: string
  priority?: Priority
  category?: Category
  completed?: boolean
}
```

---

## Validation Schemas

### Task Form Validation

```typescript
// lib/validation.ts

export const taskFormSchema = {
  title: {
    required: true,
    minLength: 1,
    maxLength: 200,
    errorMessages: {
      required: 'Task title is required',
      minLength: 'Task title cannot be empty',
      maxLength: 'Task title must be less than 200 characters'
    }
  },
  description: {
    required: false,
    maxLength: 1000,
    errorMessages: {
      maxLength: 'Description must be less than 1000 characters'
    }
  },
  priority: {
    required: true,
    enum: ['high', 'medium', 'low', 'none'],
    errorMessages: {
      required: 'Priority is required',
      enum: 'Invalid priority value'
    }
  },
  category: {
    required: true,
    enum: ['work', 'personal', 'shopping', 'health', 'other'],
    errorMessages: {
      required: 'Category is required',
      enum: 'Invalid category value'
    }
  }
}
```

---

## Utility Types

### Animation Variants

```typescript
// lib/animations.ts

export interface AnimationVariants {
  hidden: {
    opacity: number
    y?: number
    x?: number
    scale?: number
  }
  visible: {
    opacity: number
    y?: number
    x?: number
    scale?: number
    transition?: {
      duration: number
      ease: number[]
      delay?: number
    }
  }
}

export const fadeInVariants: AnimationVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { duration: 0.2, ease: [0.4, 0, 0.2, 1] }
  }
}

export const slideUpVariants: AnimationVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.3, ease: [0.4, 0, 0.2, 1] }
  }
}

export const scaleInVariants: AnimationVariants = {
  hidden: { opacity: 0, scale: 0.95 },
  visible: {
    opacity: 1,
    scale: 1,
    transition: { duration: 0.25, ease: [0.4, 0, 0.2, 1] }
  }
}
```

---

## Type Guards

```typescript
// lib/type-guards.ts

export function isPriority(value: unknown): value is Priority {
  return typeof value === 'string' &&
    ['high', 'medium', 'low', 'none'].includes(value)
}

export function isCategory(value: unknown): value is Category {
  return typeof value === 'string' &&
    ['work', 'personal', 'shopping', 'health', 'other'].includes(value)
}

export function isTask(value: unknown): value is Task {
  return (
    typeof value === 'object' &&
    value !== null &&
    'id' in value &&
    'title' in value &&
    'priority' in value &&
    'category' in value &&
    'completed' in value
  )
}
```

---

## Summary

This data model provides:
- **Type Safety**: All component props and data structures are strongly typed
- **Consistency**: Shared types ensure consistent data flow across components
- **Validation**: Schemas define validation rules for user input
- **Reusability**: Common types (Priority, Category, Task) used throughout
- **Documentation**: Each interface includes JSDoc comments for clarity

All types align with the design guidelines from the specification and research phase.
