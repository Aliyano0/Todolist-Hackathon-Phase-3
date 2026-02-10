---
name: nextjs-client-components
description: Instructions for Client Components in Next.js 16, covering interactivity, hooks, and state management. Use when the query involves client-side logic, events, or hooks like useState.
---

## Instructions for Next.js 16 Client Components

For Client Components in Next.js 16:

1. **Declaration**: Add `'use client';` at the top of the file to mark as Client Component.

2. **Use Cases**:
   - Interactivity: Event handlers (onClick, etc.).
   - State: `useState`, `useReducer`.
   - Effects: `useEffect` for side effects.
   - Browser APIs: Access to `window`, `document`.

3. **Hooks**:
   - Routing: `useRouter`, `usePathname`, `useSearchParams` from `next/navigation`.
   - Context: `useContext` for shared state.

4. **Integration with Server Components**:
   - Client Components can be children of Server Components.
   - Receive props from Server Components (must be serializable).

5. **Optimization**:
   - Minimize client bundle size by keeping non-interactive parts as Server Components.
   - Use `Suspense` boundaries for loading states.

6. **Third-Party Libraries**:
   - Install and use client-side libs like React Query for data fetching.

7. **Best Practices**:
   - Avoid server-only code in Client Components.
   - Handle hydration mismatches carefully.
   - Use TypeScript for better type safety with hooks.

## References

Use the shared references located at:
../_shared/reference.md
