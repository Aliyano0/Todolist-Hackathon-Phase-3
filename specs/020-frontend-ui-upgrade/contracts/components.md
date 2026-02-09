# Component API Contracts

**Date**: 2026-02-09
**Feature**: 020-frontend-ui-upgrade
**Phase**: Phase 1 - Component Contracts

## Overview

This document defines the API contracts for all components in the frontend UI upgrade. Each contract specifies the component's responsibilities, inputs, outputs, and behavior guarantees.

---

## Homepage Components

### HeroSection

**Responsibility**: Display the main hero section with branding, value proposition, and call-to-action buttons

**Contract**:
```typescript
interface HeroSectionContract {
  // INPUTS
  props: {
    title: string                    // REQUIRED: Main heading
    subtitle: string                 // REQUIRED: Value proposition
    primaryCTA: string               // REQUIRED: Primary button text
    secondaryCTA: string             // REQUIRED: Secondary button text
    onPrimaryCTAClick: () => void    // REQUIRED: Primary button handler
    onSecondaryCTAClick: () => void  // REQUIRED: Secondary button handler
    isAuthenticated: boolean         // REQUIRED: Auth status
  }

  // OUTPUTS
  events: {
    onPrimaryCTAClick: void          // Emitted when primary CTA clicked
    onSecondaryCTAClick: void        // Emitted when secondary CTA clicked
  }

  // BEHAVIOR GUARANTEES
  guarantees: {
    // MUST render full viewport height on desktop
    // MUST render auto height on mobile (<768px)
    // MUST show gradient background
    // MUST animate on mount (fade in + slide up)
    // MUST respect reduced motion preferences
    // MUST show different CTAs based on isAuthenticated
    // MUST be keyboard accessible (tab navigation)
  }
}
```

**Accessibility Requirements**:
- Primary CTA must have `aria-label` describing action
- Secondary CTA must have `aria-label` describing action
- Heading must use semantic `<h1>` tag
- Subtitle must use semantic `<p>` tag

**Animation Behavior**:
- On mount: Fade in (0 → 1 opacity) + Slide up (20px → 0) over 300ms
- Respects `prefers-reduced-motion`: Instant appearance if enabled

---

### FeaturesSection

**Responsibility**: Display 4 key features with icons and descriptions in a grid layout

**Contract**:
```typescript
interface FeaturesSectionContract {
  // INPUTS
  props: {
    features: Feature[]              // REQUIRED: Array of 4 features
    heading: string                  // REQUIRED: Section heading
    subheading?: string              // OPTIONAL: Section subheading
  }

  // OUTPUTS
  events: {} // No events emitted

  // BEHAVIOR GUARANTEES
  guarantees: {
    // MUST render features in 2x2 grid on desktop (≥1024px)
    // MUST render features in 2x1 grid on tablet (768px-1023px)
    // MUST render features stacked on mobile (<768px)
    // MUST animate features with stagger (50ms delay between each)
    // MUST show icons from icon library
    // MUST respect reduced motion preferences
  }
}
```

**Accessibility Requirements**:
- Section must have `aria-labelledby` pointing to heading
- Each feature must be in a `<article>` tag
- Icons must have `aria-hidden="true"` (decorative)

**Animation Behavior**:
- On scroll into view: Each feature fades in + scales (0.95 → 1) with 50ms stagger
- Respects `prefers-reduced-motion`: Instant appearance if enabled

---

### HowItWorksSection

**Responsibility**: Display 3-step user journey with visual flow indicators

**Contract**:
```typescript
interface HowItWorksSectionContract {
  // INPUTS
  props: {
    steps: Step[]                    // REQUIRED: Array of 3 steps
    heading: string                  // REQUIRED: Section heading
  }

  // OUTPUTS
  events: {} // No events emitted

  // BEHAVIOR GUARANTEES
  guarantees: {
    // MUST render steps horizontally on desktop (≥768px)
    // MUST render steps vertically on mobile (<768px)
    // MUST show arrows between steps on desktop
    // MUST show step numbers (1, 2, 3) prominently
    // MUST animate steps with stagger on scroll into view
    // MUST respect reduced motion preferences
  }
}
```

**Accessibility Requirements**:
- Section must use `<ol>` (ordered list) for steps
- Each step must be in `<li>` tag
- Step numbers must be visible to screen readers

**Animation Behavior**:
- On scroll into view: Each step fades in + slides up with 100ms stagger
- Respects `prefers-reduced-motion`: Instant appearance if enabled

---

### CTASection

**Responsibility**: Display final call-to-action with conversion prompt

**Contract**:
```typescript
interface CTASectionContract {
  // INPUTS
  props: {
    heading: string                  // REQUIRED: CTA heading
    description: string              // REQUIRED: CTA description
    buttonText: string               // REQUIRED: Button text
    onButtonClick: () => void        // REQUIRED: Button click handler
  }

  // OUTPUTS
  events: {
    onButtonClick: void              // Emitted when button clicked
  }

  // BEHAVIOR GUARANTEES
  guarantees: {
    // MUST center content horizontally
    // MUST show button with glowing effect on hover
    // MUST animate on scroll into view
    // MUST respect reduced motion preferences
    // MUST be keyboard accessible
  }
}
```

**Accessibility Requirements**:
- Button must have clear `aria-label`
- Heading must use semantic `<h2>` tag
- Focus must be visible on button

**Animation Behavior**:
- On scroll into view: Fade in + scale (0.95 → 1) over 250ms
- Button hover: Scale (1 → 1.02) + glow effect over 150ms
- Respects `prefers-reduced-motion`: Instant appearance if enabled

---

### Footer

**Responsibility**: Display footer with links and copyright information

**Contract**:
```typescript
interface FooterContract {
  // INPUTS
  props: {
    links: FooterLink[]              // REQUIRED: Array of footer links
    copyright: string                // REQUIRED: Copyright text
  }

  // OUTPUTS
  events: {} // No events emitted

  // BEHAVIOR GUARANTEES
  guarantees: {
    // MUST render links horizontally on desktop
    // MUST render links vertically on mobile
    // MUST show copyright text
    // MUST use semantic <footer> tag
    // MUST be keyboard accessible
  }
}
```

**Accessibility Requirements**:
- Must use `<footer>` semantic tag
- Links must have clear text (no "click here")
- Copyright must be in `<small>` tag

---

## Dashboard Components

### TaskCard

**Responsibility**: Display individual task with priority/category indicators and action buttons

**Contract**:
```typescript
interface TaskCardContract {
  // INPUTS
  props: {
    task: Task                       // REQUIRED: Task data
    onComplete: (id: string) => void // REQUIRED: Complete handler
    onEdit: (id: string) => void     // REQUIRED: Edit handler
    onDelete: (id: string) => void   // REQUIRED: Delete handler
    isEditing?: boolean              // OPTIONAL: Edit mode flag
  }

  // OUTPUTS
  events: {
    onComplete: string               // Emitted with task ID
    onEdit: string                   // Emitted with task ID
    onDelete: string                 // Emitted with task ID
  }

  // BEHAVIOR GUARANTEES
  guarantees: {
    // MUST show 4px left border with priority color
    // MUST show priority badge in top-right corner
    // MUST show category tag below title
    // MUST apply category background tint (5-10% opacity)
    // MUST show action buttons on hover/focus
    // MUST animate on mount (fade in + scale)
    // MUST show completed state (opacity + strikethrough)
    // MUST lift on hover (translateY -2px + shadow)
    // MUST respect reduced motion preferences
    // MUST be keyboard accessible
  }
}
```

**Accessibility Requirements**:
- Checkbox must have `aria-label` with task title
- Edit button must have `aria-label="Edit task: {title}"`
- Delete button must have `aria-label="Delete task: {title}"`
- Card must have `role="article"`
- Completed tasks must have `aria-label` indicating completion

**Animation Behavior**:
- On mount: Fade in (0 → 1) + Scale (0.95 → 1) over 250ms with spring physics
- On hover: Lift (translateY 0 → -2px) + Shadow increase over 200ms
- On complete: Fade out + Scale (1 → 0.95) + Slide up over 250ms
- Respects `prefers-reduced-motion`: Instant transitions if enabled

---

### PriorityBadge

**Responsibility**: Display priority indicator with color and optional icon

**Contract**:
```typescript
interface PriorityBadgeContract {
  // INPUTS
  props: {
    priority: Priority               // REQUIRED: Priority level
    size?: 'sm' | 'md' | 'lg'       // OPTIONAL: Badge size (default: md)
    showIcon?: boolean               // OPTIONAL: Show icon (default: false)
  }

  // OUTPUTS
  events: {} // No events emitted

  // BEHAVIOR GUARANTEES
  guarantees: {
    // MUST use priority color from design tokens
    // MUST render as pill shape (rounded)
    // MUST show priority text (High, Medium, Low, None)
    // MUST show icon if showIcon=true
    // MUST scale based on size prop
  }
}
```

**Accessibility Requirements**:
- Badge must have `aria-label="Priority: {priority}"`
- Icon must have `aria-hidden="true"` (decorative)

---

### CategoryTag

**Responsibility**: Display category indicator with color and optional icon

**Contract**:
```typescript
interface CategoryTagContract {
  // INPUTS
  props: {
    category: Category               // REQUIRED: Category name
    size?: 'sm' | 'md' | 'lg'       // OPTIONAL: Tag size (default: md)
    showIcon?: boolean               // OPTIONAL: Show icon (default: false)
  }

  // OUTPUTS
  events: {} // No events emitted

  // BEHAVIOR GUARANTEES
  guarantees: {
    // MUST use category color from design tokens
    // MUST render as rounded tag
    // MUST show category text (Work, Personal, etc.)
    // MUST show icon if showIcon=true
    // MUST scale based on size prop
  }
}
```

**Accessibility Requirements**:
- Tag must have `aria-label="Category: {category}"`
- Icon must have `aria-hidden="true"` (decorative)

---

### TaskList

**Responsibility**: Display list of tasks with loading/error/empty states

**Contract**:
```typescript
interface TaskListContract {
  // INPUTS
  props: {
    tasks: Task[]                    // REQUIRED: Array of tasks
    isLoading: boolean               // REQUIRED: Loading state
    error?: string                   // OPTIONAL: Error message
    onComplete: (id: string) => void // REQUIRED: Complete handler
    onEdit: (id: string) => void     // REQUIRED: Edit handler
    onDelete: (id: string) => void   // REQUIRED: Delete handler
    emptyMessage?: string            // OPTIONAL: Empty state message
  }

  // OUTPUTS
  events: {
    onComplete: string               // Emitted with task ID
    onEdit: string                   // Emitted with task ID
    onDelete: string                 // Emitted with task ID
  }

  // BEHAVIOR GUARANTEES
  guarantees: {
    // MUST show loading spinner when isLoading=true
    // MUST show error message when error is present
    // MUST show empty state when tasks.length=0
    // MUST render TaskCard for each task
    // MUST animate task additions with stagger
    // MUST animate task removals with collapse
    // MUST respect reduced motion preferences
  }
}
```

**Accessibility Requirements**:
- List must use `<ul>` semantic tag
- Each task must be in `<li>` tag
- Loading state must have `aria-live="polite"` and `aria-busy="true"`
- Error message must have `role="alert"`
- Empty state must have clear message

**Animation Behavior**:
- Task addition: Fade in + Scale + Slide down with 50ms stagger
- Task removal: Fade out + Scale + Slide up, then collapse height
- Respects `prefers-reduced-motion`: Instant transitions if enabled

---

### TaskForm

**Responsibility**: Display form for creating/editing tasks with validation

**Contract**:
```typescript
interface TaskFormContract {
  // INPUTS
  props: {
    initialData?: Partial<TaskFormData> // OPTIONAL: Initial values (edit mode)
    onSubmit: (data: TaskFormData) => void // REQUIRED: Submit handler
    onCancel: () => void             // REQUIRED: Cancel handler
    submitText?: string              // OPTIONAL: Submit button text
    isSubmitting?: boolean           // OPTIONAL: Submitting state
  }

  // OUTPUTS
  events: {
    onSubmit: TaskFormData           // Emitted with form data
    onCancel: void                   // Emitted when cancelled
  }

  // BEHAVIOR GUARANTEES
  guarantees: {
    // MUST validate title (required, 1-200 chars)
    // MUST validate description (optional, max 1000 chars)
    // MUST validate priority (required, enum)
    // MUST validate category (required, enum)
    // MUST show validation errors inline
    // MUST disable submit button when invalid
    // MUST disable form when isSubmitting=true
    // MUST show loading state on submit button
    // MUST be keyboard accessible
    // MUST support Enter to submit, Escape to cancel
  }
}
```

**Accessibility Requirements**:
- All inputs must have associated `<label>` tags
- Validation errors must have `role="alert"` and `aria-live="polite"`
- Required fields must have `aria-required="true"`
- Submit button must have `aria-disabled="true"` when invalid
- Form must have `aria-labelledby` pointing to form heading

---

## Animation Components

### PageTransition

**Responsibility**: Wrap page content with transition animations

**Contract**:
```typescript
interface PageTransitionContract {
  // INPUTS
  props: {
    children: React.ReactNode        // REQUIRED: Page content
    direction?: 'up' | 'down' | 'left' | 'right' // OPTIONAL: Direction
    duration?: number                // OPTIONAL: Duration in ms
  }

  // OUTPUTS
  events: {} // No events emitted

  // BEHAVIOR GUARANTEES
  guarantees: {
    // MUST animate page entry (fade + slide)
    // MUST animate page exit (fade + slide)
    // MUST use direction prop for slide direction
    // MUST use duration prop for animation timing
    // MUST respect reduced motion preferences
    // MUST not block page rendering
  }
}
```

**Animation Behavior**:
- Entry: Fade in (0 → 1) + Slide (20px → 0) over 300ms
- Exit: Fade out (1 → 0) + Slide (0 → 20px) over 300ms
- Respects `prefers-reduced-motion`: Instant transitions if enabled

---

### FadeIn

**Responsibility**: Wrap content with fade-in animation

**Contract**:
```typescript
interface FadeInContract {
  // INPUTS
  props: {
    children: React.ReactNode        // REQUIRED: Content to animate
    delay?: number                   // OPTIONAL: Delay in ms
    duration?: number                // OPTIONAL: Duration in ms
    animateOnMount?: boolean         // OPTIONAL: Animate on mount
  }

  // OUTPUTS
  events: {} // No events emitted

  // BEHAVIOR GUARANTEES
  guarantees: {
    // MUST fade in from 0 to 1 opacity
    // MUST apply delay if specified
    // MUST use duration if specified
    // MUST animate on mount if animateOnMount=true
    // MUST respect reduced motion preferences
  }
}
```

---

### SlideIn

**Responsibility**: Wrap content with slide-in animation

**Contract**:
```typescript
interface SlideInContract {
  // INPUTS
  props: {
    children: React.ReactNode        // REQUIRED: Content to animate
    direction: 'up' | 'down' | 'left' | 'right' // REQUIRED: Slide direction
    distance?: number                // OPTIONAL: Slide distance in px
    delay?: number                   // OPTIONAL: Delay in ms
    duration?: number                // OPTIONAL: Duration in ms
  }

  // OUTPUTS
  events: {} // No events emitted

  // BEHAVIOR GUARANTEES
  guarantees: {
    // MUST slide from distance to 0
    // MUST use direction prop for slide axis
    // MUST apply delay if specified
    // MUST use duration if specified
    // MUST respect reduced motion preferences
  }
}
```

---

### ScaleIn

**Responsibility**: Wrap content with scale-in animation

**Contract**:
```typescript
interface ScaleInContract {
  // INPUTS
  props: {
    children: React.ReactNode        // REQUIRED: Content to animate
    initialScale?: number            // OPTIONAL: Initial scale (default: 0.95)
    delay?: number                   // OPTIONAL: Delay in ms
    duration?: number                // OPTIONAL: Duration in ms
  }

  // OUTPUTS
  events: {} // No events emitted

  // BEHAVIOR GUARANTEES
  guarantees: {
    // MUST scale from initialScale to 1
    // MUST apply delay if specified
    // MUST use duration if specified
    // MUST respect reduced motion preferences
  }
}
```

---

## Layout Components

### Navbar

**Responsibility**: Display navigation bar with conditional links based on auth status

**Contract**:
```typescript
interface NavbarContract {
  // INPUTS
  props: {
    isAuthenticated: boolean         // REQUIRED: Auth status
    userEmail?: string               // OPTIONAL: User email (if authenticated)
    links: NavLink[]                 // REQUIRED: Navigation links
    onLogout?: () => void            // OPTIONAL: Logout handler
  }

  // OUTPUTS
  events: {
    onLogout: void                   // Emitted when logout clicked
  }

  // BEHAVIOR GUARANTEES
  guarantees: {
    // MUST show login/signup links when not authenticated
    // MUST show dashboard/profile links when authenticated
    // MUST show user email when authenticated
    // MUST show logout button when authenticated
    // MUST highlight active link
    // MUST be responsive (hamburger menu on mobile)
    // MUST be keyboard accessible
    // MUST show theme toggle
  }
}
```

**Accessibility Requirements**:
- Must use `<nav>` semantic tag
- Links must have clear text
- Active link must have `aria-current="page"`
- Mobile menu button must have `aria-label="Toggle menu"`
- Mobile menu must have `aria-expanded` attribute

---

## Contract Validation

All components MUST:
1. **Type Safety**: Accept only typed props (no `any`)
2. **Error Handling**: Handle all error states gracefully
3. **Accessibility**: Meet WCAG 2.1 Level AA standards
4. **Performance**: Render in <100ms on modern devices
5. **Reduced Motion**: Respect `prefers-reduced-motion` preference
6. **Keyboard Navigation**: Support full keyboard accessibility
7. **Theme Support**: Work in both light and dark themes
8. **Responsive**: Work on mobile, tablet, and desktop
9. **Testing**: Have unit tests covering all behavior guarantees
10. **Documentation**: Include JSDoc comments for all props

---

## Contract Testing

Each component contract MUST be verified with:
- **Unit Tests**: Test all behavior guarantees
- **Accessibility Tests**: Test ARIA labels, keyboard navigation, screen reader support
- **Visual Tests**: Test appearance in both themes
- **Animation Tests**: Test animations with and without reduced motion
- **Responsive Tests**: Test on mobile, tablet, desktop viewports
