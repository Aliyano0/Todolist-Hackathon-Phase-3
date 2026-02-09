/**
 * Better Auth configuration for the Todo application
 *
 * This module configures Better Auth as the authentication authority.
 * Better Auth issues JWT tokens that the backend verifies.
 */

import { betterAuth } from "better-auth";

export const auth = betterAuth({
  secret: process.env.BETTER_AUTH_SECRET!,
  baseURL: process.env.BETTER_AUTH_URL || "http://localhost:3000",
  database: {
    // Backend API handles database operations
    provider: "postgres",
    url: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
  },
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false, // Phase 3 feature
  },
  session: {
    expiresIn: 60 * 60 * 24 * 7, // 7 days
    updateAge: 60 * 60 * 24, // Update session every 24 hours
  },
});

export type Session = typeof auth.$Infer.Session;
