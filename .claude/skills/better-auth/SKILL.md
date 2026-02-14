---
name: better-auth
description: Provides the TypeScript setup for Better-Auth (JWT + mandatory email verification) as required by Phase III Todo AI Chatbot plan.
---

# Better-Auth TypeScript Skill

When the user asks for authentication setup, email verification enforcement, or JWT middleware for the chatbot, output this exact implementation.

## Where to place the file
`frontend/src/auth.ts` (or equivalent in your TypeScript backend/frontend layer)

## Code
```typescript
// auth.ts
import { createAuth } from 'better-auth';
import { email } from 'better-auth/plugins';

export const auth = createAuth({
  database: { type: 'your-db-type' },
  secret: process.env.BETTER_AUTH_SECRET!,
  plugins: [
    email({
      requireVerification: true,
      from: 'no-reply@yourapp.com',
      onSignup: async (user) => {
        await updateUser(user.id, { email_verified: false });
      },
    }),
  ],
});

export async function verifyUser(token: string, userId: string) {
  const session = await auth.verifySession(token);
  if (!session || session.userId !== userId) {
    throw new Error('Invalid token or user mismatch');
  }
  if (!session.user.email_verified) {
    throw { error: 'email_not_verified', message: 'Please verify your email to use the chatbot.' };
  }
  return session;
}

export async function resendVerificationEmail(userId: string) {
  const user = await auth.getUser(userId);
  if (!user.email_verified) {
    await auth.plugins.email.sendVerificationEmail(user);
    return { success: true, message: 'Verification email resent.' };
  }
  return { success: false, message: 'Email already verified.' };
}
```

Use this in `/api/{user_id}/chat` middleware and on the frontend for the verification prompt + resend button.
```

