---
name: nextjs-data-fetching
description: Step-by-step guide for data fetching in Next.js 16, including fetch API, caching, mutations, and third-party libraries. Trigger for queries about APIs, databases, or data loading.
---

## Instructions for Next.js 16 Data Fetching

Handle data fetching in Next.js 16 as follows:

1. **Built-in Fetch**:
   - Use `fetch(url, { cache: 'no-store' })` for dynamic data.
   - Static: `fetch(url, { cache: 'force-cache' })`.
   - ISR: `fetch(url, { next: { revalidate: 60 } })`.

2. **Server-Side Fetching**:
   - In Server Components or Route Handlers.
   - Automatic deduping for same requests.

3. **Client-Side Fetching**:
   - In Client Components with SWR or React Query.
   - Use `useSWR` for caching and revalidation.

4. **Mutations**:
   - Use `revalidatePath` or `revalidateTag` for on-demand revalidation.
   - In forms: Server Actions with `useFormState`.

5. **Loading States**:
   - Wrap async components in `Suspense`.
   - Use `loading.tsx` for route-level loading.

6. **Error Handling**:
   - `error.tsx` for route errors.
   - Try-catch in fetch calls.

7. **Best Practices**:
   - Colocate data fetching with components.
   - Secure API keys on server.
   - Handle pagination and infinite scrolling on client.

## References

Use the shared references located at:
../_shared/reference.md
