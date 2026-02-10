---
name: nextjs-app-router
description: Guide for using the App Router in Next.js 16, including route definitions, dynamic routes, layouts, and navigation. Use this when the user asks about routing, pages, or navigation in Next.js projects.
---

## Instructions for Next.js 16 App Router

When assisting with Next.js 16 App Router tasks:

1. **Understand the Structure**: The App Router uses a file-system-based routing in the `app/` directory. Folders represent route segments, and files like `page.tsx` define the UI for that route.

2. **Basic Route Setup**:
   - Create a folder in `app/` for each route segment (e.g., `app/about/` for `/about`).
   - Add a `page.tsx` file exporting a default React component.

3. **Dynamic Routes**:
   - Use brackets for dynamic segments: `app/posts/[id]/page.tsx`.
   - Access params in the component: `export default function Post({ params }: { params: { id: string } }) { ... }`.

4. **Layouts**:
   - Use `layout.tsx` in route groups or root to wrap child routes.
   - Root layout at `app/layout.tsx` must include `<html>` and `<body>`.

5. **Navigation**:
   - Use `Link` from `next/link` for client-side navigation.
   - For programmatic navigation, use `useRouter` from `next/navigation`.

6. **Loading and Error States**:
   - Add `loading.tsx` for suspense boundaries.
   - Add `error.tsx` for error handling.

7. **Route Groups**:
   - Use parentheses for grouping without affecting URL: `app/(auth)/login/page.tsx`.

8. **Parallel Routes**:
   - Use slots with `@` prefix: `app/@analytics/page.tsx`.

9. **Best Practices**:
   - Prefer Server Components where possible.
   - Handle data fetching with `fetch` or third-party libraries.
   - Ensure TypeScript types for params and search params.

## References

Use the shared references located at:
../_shared/reference.md
