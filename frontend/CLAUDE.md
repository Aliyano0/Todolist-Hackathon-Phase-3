# Claude Code Rules for Frontend Development

You are an expert AI assistant specializing in frontend development for the Todo application.

## Task Context

**Surface**: Frontend development for Next.js Todo application
**Success Metric**: Features match spec, pass tests, follow architecture

## Core Guarantees

### 1. Frontend Development Standards:
- Use Next.js 16.1+ with App Router
- Implement responsive UI with Tailwind CSS
- Follow accessibility standards (WCAG 2.1 AA)
- Use TypeScript for type safety
- Implement proper error handling

### 2. Component Architecture:
- Organize components by feature (todo, theme, navigation)
- Use Shadcn/UI components where appropriate
- Follow Next.js best practices for Client vs Server components
- Implement proper state management with React hooks

### 3. API Integration:
- Integrate with backend API using REST endpoints
- Implement optimistic updates for better UX
- Handle loading and error states properly
- Follow the API contracts defined in specs/011-frontend-rebuild/contracts/

### 4. Theming & UI:
- Implement light/dark theme support
- Use ThemeProvider for context-based theming
- Ensure responsive design across mobile/tablet/desktop
- Add subtle animations for improved UX

## Better Auth Integration (018-better-auth-jwt)

### Authentication Configuration Pattern
```typescript
// lib/auth.ts
import { betterAuth } from "better-auth";
import { nextCookies } from "better-auth/next-js";

export const auth = betterAuth({
  secret: process.env.BETTER_AUTH_SECRET!,
  baseURL: process.env.BETTER_AUTH_URL!,
  database: {
    // Better Auth connects to backend API
    provider: "custom",
  },
  plugins: [nextCookies()],
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false, // Phase 3 feature
  },
});
```

### AuthProvider Pattern
```typescript
// providers/AuthProvider.tsx
"use client";
import { SessionProvider } from "better-auth/react";

export function AuthProvider({ children }: { children: React.ReactNode }) {
  return <SessionProvider>{children}</SessionProvider>;
}
```

### Protected Routes Pattern
```typescript
// app/middleware.ts
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  const token = request.cookies.get("better-auth.session_token");

  if (!token && request.nextUrl.pathname.startsWith("/dashboard")) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/dashboard/:path*"],
};
```

### useAuth Hook Pattern
```typescript
// hooks/useAuth.ts
"use client";
import { useSession, signIn, signOut } from "better-auth/react";

export function useAuth() {
  const { data: session, isPending } = useSession();

  return {
    user: session?.user,
    isAuthenticated: !!session,
    isLoading: isPending,
    signIn,
    signOut,
  };
}
```

### API Client with Credentials Pattern
```typescript
// lib/api.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function apiRequest<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    credentials: "include", // Send cookies with request
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
  });

  if (response.status === 401) {
    // Redirect to login on unauthorized
    window.location.href = "/login";
    throw new Error("Unauthorized");
  }

  if (response.status === 403) {
    throw new Error("Access denied");
  }

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Request failed");
  }

  return response.json();
}
```

### Password Validation Pattern
```typescript
// lib/validation.ts
export function validatePassword(password: string): {
  isValid: boolean;
  errors: string[];
} {
  const errors: string[] = [];

  if (password.length < 8) {
    errors.push("Password must be at least 8 characters");
  }
  if (!/[A-Z]/.test(password)) {
    errors.push("Password must contain at least one uppercase letter");
  }
  if (!/[a-z]/.test(password)) {
    errors.push("Password must contain at least one lowercase letter");
  }
  if (!/[0-9]/.test(password)) {
    errors.push("Password must contain at least one number");
  }
  if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
    errors.push("Password must contain at least one special character");
  }

  return {
    isValid: errors.length === 0,
    errors,
  };
}
```

## Active Technologies
- Next.js 16.1 with App Router
- React 19.2.3
- TypeScript 5.x
- Tailwind CSS with Shadcn/UI
- Radix UI primitives
- Better Auth for authentication
- REST API integration with credentials support
- Priority and category fields support in frontend types (016-backend-db-fix)
- **Framer Motion 11.18+ for animations (020-frontend-ui-upgrade)**

## UI Upgrade Patterns (020-frontend-ui-upgrade)

### Framer Motion Animation Patterns

**Basic Animation Component**:
```typescript
'use client'
import { motion } from 'framer-motion'
import { useReducedMotion } from '@/hooks/useReducedMotion'

export function AnimatedComponent() {
  const shouldReduceMotion = useReducedMotion()

  const variants = {
    hidden: { opacity: 0, y: shouldReduceMotion ? 0 : 20 },
    visible: { opacity: 1, y: 0 }
  }

  return (
    <motion.div
      initial="hidden"
      animate="visible"
      variants={variants}
      transition={{ duration: 0.3 }}
    >
      Content
    </motion.div>
  )
}
```

**Page Transition Pattern**:
```typescript
'use client'
import { motion, AnimatePresence } from 'framer-motion'

export function PageTransition({ children }: { children: React.ReactNode }) {
  return (
    <AnimatePresence mode="wait">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -20 }}
        transition={{ duration: 0.3 }}
      >
        {children}
      </motion.div>
    </AnimatePresence>
  )
}
```

**Staggered List Animation**:
```typescript
const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.05
    }
  }
}

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 }
}

<motion.ul variants={containerVariants} initial="hidden" animate="visible">
  {items.map(item => (
    <motion.li key={item.id} variants={itemVariants}>
      {item.content}
    </motion.li>
  ))}
</motion.ul>
```

**Hover Animation Pattern**:
```typescript
<motion.button
  whileHover={{ scale: 1.02 }}
  whileTap={{ scale: 0.98 }}
  transition={{ duration: 0.15 }}
>
  Click me
</motion.button>
```

### Design System Tokens

**Using Design Tokens**:
```typescript
import { colors, spacing, animations } from '@/lib/design-tokens'

// In Tailwind classes
<div className="bg-priority-high text-white px-md py-sm rounded-lg">

// In Framer Motion
<motion.div
  animate={{ opacity: 1 }}
  transition={{ duration: animations.duration.normal / 1000 }}
>
```

**Priority Color Mapping**:
- High: `#EF4444` (red) - `bg-priority-high`, `border-priority-high`
- Medium: `#F59E0B` (yellow) - `bg-priority-medium`, `border-priority-medium`
- Low: `#10B981` (green) - `bg-priority-low`, `border-priority-low`
- None: `#6B7280` (gray) - `bg-priority-none`, `border-priority-none`

### Accessibility Requirements

**Reduced Motion Support**:
```typescript
// hooks/useReducedMotion.ts
import { useEffect, useState } from 'react'

export function useReducedMotion() {
  const [shouldReduceMotion, setShouldReduceMotion] = useState(false)

  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)')
    setShouldReduceMotion(mediaQuery.matches)

    const listener = (e: MediaQueryListEvent) => setShouldReduceMotion(e.matches)
    mediaQuery.addEventListener('change', listener)
    return () => mediaQuery.removeEventListener('change', listener)
  }, [])

  return shouldReduceMotion
}
```

**ARIA Labels for Interactive Elements**:
- All buttons must have clear `aria-label` attributes
- Priority badges: `aria-label="Priority: high"`
- Category tags: `aria-label="Category: work"`
- Task cards: `role="article"` with descriptive labels

### Component Organization (Atomic Design)

**Atoms**: Basic UI elements
- `PriorityBadge.tsx` - Color-coded priority indicators
- `CategoryTag.tsx` - Category labels with icons

**Molecules**: Simple combinations
- `TaskCard.tsx` - Task display with priority/category
- `TaskForm.tsx` - Task creation/edit form

**Organisms**: Complex sections
- `HeroSection.tsx` - Homepage hero with CTAs
- `FeaturesSection.tsx` - Feature showcase grid
- `TaskList.tsx` - Task list with animations

**Templates**: Page layouts
- `app/page.tsx` - Homepage composition
- `app/todos/page.tsx` - Dashboard layout

## Production Deployment (019-production-deployment)

### Vercel Deployment Configuration
- **Platform**: Vercel serverless edge deployment
- **Framework**: Next.js 16.1+ with automatic optimization
- **Build command**: `npm run build` (default)
- **Output directory**: `.next` (default)
- **Node version**: 18.x or higher

### Environment Variables
```bash
# Required for production
NEXT_PUBLIC_API_URL=https://your-backend.hf.space

# Format requirements:
# - Must use NEXT_PUBLIC_ prefix for client-side variables
# - Must NOT include trailing slash
# - Must use HTTPS in production
# - Must match backend CORS configuration
```

### Security Headers Configuration
```typescript
// next.config.ts
async headers() {
  return [
    {
      source: '/:path*',
      headers: [
        {
          key: 'X-Content-Type-Options',
          value: 'nosniff',
        },
        {
          key: 'X-Frame-Options',
          value: 'DENY',
        },
        {
          key: 'X-XSS-Protection',
          value: '1; mode=block',
        },
        {
          key: 'Referrer-Policy',
          value: 'strict-origin-when-cross-origin',
        },
      ],
    },
  ];
}
```

### Production Build Settings
```typescript
// next.config.ts
const nextConfig: NextConfig = {
  reactStrictMode: true,
  poweredByHeader: false, // Remove X-Powered-By header

  // Environment variables validation
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
  },
};
```

### Deployment Process
1. Push code to GitHub repository
2. Import project in Vercel dashboard
3. Configure environment variables (NEXT_PUBLIC_API_URL)
4. Deploy (automatic on push to main branch)
5. Verify deployment at provided URL

### Best Practices
- Use `.env.example` for documenting required variables
- Never commit `.env.local` or actual secrets
- Test production build locally: `npm run build && npm run start`
- Verify API connectivity with production backend
- Monitor build logs for errors

## Lessons Learned (019-production-deployment)

### Next.js 16 Suspense Boundaries
**Challenge**: Build errors with `useSearchParams()` - "should be wrapped in a suspense boundary"
**Solution**: Wrap components using `useSearchParams()` in `<Suspense>` boundary
**Pattern**:
```typescript
function ContentComponent() {
  const searchParams = useSearchParams(); // Uses search params
  // ... component logic
}

export default function Page() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <ContentComponent />
    </Suspense>
  );
}
```
**Affected Pages**: `/login`, `/reset-password`

### TypeScript Strict Mode Compilation
**Challenge**: Production build enforces stricter TypeScript checks than dev server
**Common Issues**:
1. Promise return types: Functions returning promises must be typed as `Promise<T>`
2. Header types: Use `Record<string, string>` instead of `HeadersInit` for dynamic headers
3. React imports: Import `React` explicitly when using `React.createContext()` or similar

**Best Practice**: Run `npm run build` frequently during development to catch type errors early

### Shadcn UI Component Issues
**Challenge**: Card component import errors during build despite working in dev
**Workaround**: Replaced Card components with plain divs using Tailwind classes
**Note**: Turbopack cache issues may cause component resolution problems

### Security Headers Configuration
**Implementation**: Added 4 security headers in `next.config.ts` via `headers()` function
**Headers**: X-Content-Type-Options, X-Frame-Options, X-XSS-Protection, Referrer-Policy
**Note**: These headers apply to all routes via `source: '/:path*'`

### Production Build Validation
**Process**:
1. Fix all TypeScript errors (build fails on type errors)
2. Add Suspense boundaries where needed
3. Verify all 9 routes compile successfully
4. Check build output for warnings

**Build Time**: ~18-20 seconds for production build with Turbopack

## UI Upgrade Implementation (020-frontend-ui-upgrade)

### Complete Design System

**Design Tokens Location**: `frontend/lib/design-tokens.ts`

All colors, spacing, typography, and animation values are centralized in design tokens. Always import and use these tokens instead of hardcoding values.

**Animation Utilities Location**: `frontend/lib/animations.ts`

Pre-configured animation variants for consistent motion throughout the app.

### Component Library

**Animation Components** (`frontend/components/animations/`):
- `PageTransitionWrapper.tsx` - Wraps app for route transitions (already in layout.tsx)
- `PageTransition.tsx` - Standalone page transition wrapper
- `FadeIn.tsx` - Fade-in animation with configurable delay/duration
- `SlideIn.tsx` - Slide-in from any direction (up/down/left/right)
- `ScaleIn.tsx` - Scale-in animation with configurable initial scale
- `AnimatedButton.tsx` - Button with hover/tap animations

**Homepage Components** (`frontend/components/homepage/`):
- `HeroSection.tsx` - Full-screen hero with gradient, CTAs, conditional auth display
- `FeaturesSection.tsx` - 2x2 grid of features with icons and staggered animations
- `HowItWorksSection.tsx` - 3-step user journey with numbered circles and arrows
- `CTASection.tsx` - Final conversion section with scale-in animation
- `Footer.tsx` - Footer with links and copyright

**Dashboard Components** (`frontend/components/dashboard/`):
- `PriorityBadge.tsx` - Color-coded priority indicators (high/medium/low/none)
- `CategoryTag.tsx` - Category labels with icons and background tints
- `TaskCard.tsx` - Task display with 4px priority border, hover lift effect
- `TaskList.tsx` - Task list with loading/error/empty states, staggered animations
- `TaskForm.tsx` - Task creation/edit form with validation

### Usage Examples

**Creating a New Animated Page**:
```tsx
'use client'

import { FadeIn } from '@/components/animations/FadeIn'
import { SlideIn } from '@/components/animations/SlideIn'

export default function MyPage() {
  return (
    <div className="min-h-screen bg-background">
      <FadeIn delay={0.1}>
        <h1 className="text-4xl font-bold text-foreground">Page Title</h1>
      </FadeIn>

      <SlideIn direction="up" delay={0.2}>
        <p className="text-muted-foreground">Content here</p>
      </SlideIn>
    </div>
  )
}
```

**Using Priority Colors**:
```tsx
// In component
import { colors } from '@/lib/design-tokens'

// In Tailwind classes
<div className="border-priority-high bg-priority-high/10">
  High priority task
</div>

// In inline styles (avoid if possible)
<div style={{ borderColor: colors.priority.high }}>
```

**Using Category Colors**:
```tsx
// Tailwind classes with background tints
<div className="bg-category-work-tint border-category-work">
  Work task
</div>
```

**Creating Animated Buttons**:
```tsx
import { motion } from 'framer-motion'
import { useReducedMotion } from '@/hooks/useReducedMotion'

function MyButton() {
  const shouldReduceMotion = useReducedMotion()

  return (
    <motion.button
      whileHover={{ scale: shouldReduceMotion ? 1 : 1.05 }}
      whileTap={{ scale: shouldReduceMotion ? 1 : 0.95 }}
      transition={{ duration: 0.15 }}
      className="glowing-button px-6 py-3 bg-primary text-primary-foreground rounded-lg"
    >
      Click Me
    </motion.button>
  )
}
```

**Scroll-Triggered Animations**:
```tsx
import { motion } from 'framer-motion'

<motion.section
  initial="hidden"
  whileInView="visible"
  viewport={{ once: true, margin: "-100px" }}
  variants={{
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0 }
  }}
>
  Content animates when scrolled into view
</motion.section>
```

### CSS Utility Classes

**Animation Classes** (defined in `globals.css`):
- `.glowing-button` - Gradient background with glow effect on hover
- `.button-glow` - Radial gradient overlay that expands on hover
- `.card-hover` - Lift effect with enhanced shadow on hover
- `.hero-gradient` - Blue to purple gradient for hero sections
- `.animate-fade-in` - Keyframe fade-in animation

**Priority Border Classes**:
- `.border-priority-high` - 4px left border, red
- `.border-priority-medium` - 4px left border, yellow
- `.border-priority-low` - 4px left border, green
- `.border-priority-none` - 4px left border, gray

**Category Background Tints**:
- `.bg-category-work-tint` - Blue tint (5% opacity, 10% in dark mode)
- `.bg-category-personal-tint` - Purple tint
- `.bg-category-shopping-tint` - Pink tint
- `.bg-category-health-tint` - Green tint
- `.bg-category-other-tint` - Gray tint

### Accessibility Requirements

**Always Include**:
1. **ARIA Labels**: All icon buttons must have `aria-label`
2. **Focus States**: Use design system focus ring (automatic via globals.css)
3. **Reduced Motion**: Always use `useReducedMotion` hook for animations
4. **Semantic HTML**: Use proper heading hierarchy (h1 → h2 → h3)
5. **Form Labels**: Associate labels with inputs using `htmlFor` and `id`
6. **Error Messages**: Use `aria-describedby` and `aria-invalid` for form errors
7. **Loading States**: Use `aria-live="polite"` and `aria-busy="true"`
8. **Error States**: Use `role="alert"` for error messages

**Example Accessible Form**:
```tsx
<div>
  <label htmlFor="email" className="block text-sm font-medium text-foreground">
    Email <span className="text-destructive">*</span>
  </label>
  <input
    id="email"
    type="email"
    aria-required="true"
    aria-invalid={!!errors.email}
    aria-describedby={errors.email ? 'email-error' : undefined}
    className="w-full px-3 py-2 border border-input rounded-lg"
  />
  {errors.email && (
    <p id="email-error" className="text-sm text-destructive" role="alert">
      {errors.email}
    </p>
  )}
</div>
```

### Performance Best Practices

**Animation Performance**:
- ✅ Use `transform` and `opacity` (GPU-accelerated)
- ❌ Avoid animating `width`, `height`, `top`, `left` (layout-triggering)
- ✅ Keep animations simple (< 0.5s duration)
- ✅ Use `useReducedMotion` hook for accessibility

**Component Performance**:
- ✅ Use proper `key` props in lists
- ✅ Avoid inline function definitions in render (where it matters)
- ✅ Use React.memo only when needed (measure first)
- ✅ Keep component trees shallow

**Bundle Size**:
- ✅ Import only needed components from libraries
- ✅ Use dynamic imports for heavy components (if needed)
- ✅ Avoid importing entire icon libraries

### Responsive Design Patterns

**Breakpoints** (Tailwind defaults):
- `sm`: 640px (small devices)
- `md`: 768px (tablets)
- `lg`: 1024px (desktops)
- `xl`: 1280px (large desktops)
- `2xl`: 1536px (extra large)

**Common Patterns**:
```tsx
// Container with responsive padding
<div className="container mx-auto px-4 sm:px-6 lg:px-8">

// Responsive grid
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">

// Responsive text sizing
<h1 className="text-3xl sm:text-4xl lg:text-5xl font-bold">

// Responsive flex direction
<div className="flex flex-col md:flex-row gap-4">

// Responsive visibility
<div className="hidden md:block">Desktop only</div>
<div className="block md:hidden">Mobile only</div>
```

### Testing Checklist

Before deploying UI changes, verify:
- [ ] All pages work in light and dark mode
- [ ] Responsive design works on mobile (375px), tablet (768px), desktop (1024px+)
- [ ] Keyboard navigation works (Tab, Enter, Space)
- [ ] Focus indicators visible on all interactive elements
- [ ] Animations respect reduced motion preference
- [ ] Forms validate correctly with clear error messages
- [ ] Loading and error states display correctly
- [ ] No console errors or warnings
- [ ] Accessibility audit passes (WCAG 2.1 AA)
- [ ] Performance audit passes (Lighthouse 90+)

## Recent Changes
- 020-frontend-ui-upgrade: Complete professional UI upgrade with design system, animations, responsive design, and accessibility compliance
- 019-production-deployment: Added Vercel deployment configuration, security headers, environment variable patterns, fixed TypeScript strict mode issues, added Suspense boundaries
- 018-better-auth-jwt: Implementing Better Auth integration with JWT tokens, protected routes, and password validation
- 016-backend-db-fix: Priority and category fields support in frontend types