---
name: nextjs-server-components
description: Guidance on using Server Components in Next.js 16, including async components, data fetching, and integration with Client Components. Activate for questions about server-side rendering, static generation, or non-interactive components.
---

## Instructions for Next.js 16 Server Components

When working with Server Components in Next.js 16:

1. **Default Behavior**: All components in `app/` are Server Components unless marked with `'use client'`.

2. **Async Components**:
   - Make components async to fetch data: `export default async function Page() { const data = await fetch(...); return <div>{data}</div>; }`.

3. **Data Fetching**:
   - Use `fetch` with caching options: `{ cache: 'force-cache' }` for static, `{ next: { revalidate: 3600 } }` for ISR.
   - Handle errors with try-catch.

4. **Props and Serialization**:
   - Pass serializable props to Client Components (no functions or Dates).
   - Use `Suspense` for streaming: `<Suspense fallback={<Loading/>}><AsyncComponent/></Suspense>`.

5. **Integration with Client Components**:
   - Server Components can import and render Client Components.
   - Avoid importing Client Components that use hooks into Server Components.

6. **Rendering Modes**:
   - Static: Default for routes without dynamic data.
   - Dynamic: Triggered by `cookies()`, `headers()`, or dynamic functions.
   - Use `export const dynamic = 'force-static';` to override.

7. **Best Practices**:
   - Keep logic server-side for security (e.g., API keys).
   - Optimize fetches with deduping and caching.
   - Use React Server Components for better performance.

## References

Use the shared references located at:
../_shared/reference.md
