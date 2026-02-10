---
name: full-stack-authentication
description: Comprehensive guide for implementing an authentication system using Better Auth (TypeScript) for auth logic, JWT tokens for secure communication, FastAPI backend for API endpoints, Neon Serverless PostgreSQL with SQLModel for database storage, Next.js 16.1 App Router for frontend routing, and Shadcn UI for user interfaces. Use this skill for tasks involving user registration, login, session management, protected routes, and cross-service integration. This skill draws from related skills like better-auth-fastapi-jwt and sqlmodel-neon-postgres.
---

## Instructions for Full-Stack Authentication System

When assisting with authentication in a full-stack app using Better Auth, JWT, FastAPI, Neon Postgres, Next.js 16.1, and Shadcn UI:

1. **Overall Architecture Overview**:
   - **Auth Service**: Better Auth (TypeScript/Node.js) handles user signup, login, and JWT issuance. It uses Neon Postgres as the DB backend.
   - **Backend API**: FastAPI verifies JWT tokens from Better Auth and provides protected endpoints (e.g., user data, CRUD operations) using SQLModel for Neon Postgres interactions.
   - **Frontend**: Next.js 16.1 App Router with Shadcn UI for login/signup forms, protected pages, and API calls with JWT.
   - **Flow**: User authenticates via Better Auth → Receives JWT → Frontend stores JWT (e.g., cookies or localStorage) → Sends JWT in headers to FastAPI for protected resources.
   - **Database**: Shared Neon Postgres instance for user data, accessed via SQLModel in FastAPI and directly in Better Auth (if configured).

2. **Better Auth Setup (TypeScript)**:
   - Install: `npm install better-auth`.
   - Configure with JWT and database (using Prisma or similar for Neon Postgres):
     ```ts
     import { betterAuth } from "better-auth";
     import { jwt } from "better-auth/plugins";
     import { prismaAdapter } from "better-auth/adapters/prisma";
     import { PrismaClient } from "@prisma/client";

     const prisma = new PrismaClient({ datasourceUrl: process.env.DATABASE_URL }); // Neon Postgres URL

     export const auth = betterAuth({
       baseURL: process.env.AUTH_BASE_URL || "http://localhost:3000",
       database: prismaAdapter(prisma, { provider: "postgresql" }),
       plugins: [
         jwt({
           jwt: {
             secret: process.env.JWT_SECRET,
             expirationTime: "1h",
             issuer: process.env.AUTH_BASE_URL,
             audience: process.env.API_AUDIENCE // FastAPI URL
           }
         })
       ] 
     });
     ```
    - Run server: Integrate into Next.js or run as separate Node service.
    - Endpoints: Better Auth provides /signup, /signin, /token for JWT.

3. Neon Postgres with SQLModel Integration:
    - Use SQLModel for FastAPI DB ops; Better Auth uses its own adapter (e.g., Prisma) but shares the same Neon DB schema.
    - Define User model in SQLModel:
    ```py
    from sqlmodel import SQLModel, Field
    from typing import Optional

    class User(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        email: str = Field(index=True, unique=True)
        hashed_password: str
        # Add fields matching Better Auth schema
    ```
    - Engine: engine = create_engine(os.getenv("DATABASE_URL")) with Neon's connection string.
    - Sync schemas: Ensure Better Auth's tables (users, sessions) align with SQLModel queries.

4. FastAPI Backend with JWT Verification:
    - Install: uv add fastapi sqlmodel python-jose[cryptography].
    - JWT Dependency (from better-auth-fastapi-jwt skill):
    ```py
    from fastapi import Depends, HTTPException
    from fastapi.security import OAuth2PasswordBearer
    from jose import JWTError, jwt
    import httpx
    import os

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
    JWKS_URL = f"{os.getenv('AUTH_BASE_URL')}/api/auth/jwks"

    async def get_current_user(token: str = Depends(oauth2_scheme)):
        try:
            jwks = httpx.get(JWKS_URL).json()
            # Verify JWT using jwks (as in better-auth-fastapi-jwt)
            payload = jwt.decode(token, jwks, audience=os.getenv('API_AUDIENCE'))
            return payload
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
    ```
    - Protected Route:
    ```py
    from fastapi import APIRouter, Depends
    from sqlmodel import Session, select

    router = APIRouter()

    @router.get("/users/me")
    def read_current_user(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
        stmt = select(User).where(User.email == user['email'])
        return db.exec(stmt).first()
    ```

5. Next.js 16.1 Frontend with App Router and Shadcn UI:
    - Install Shadcn: npx shadcn-ui@latest init.
    - Auth Components: Use Shadcn for forms (Button, Input, Label).
    - Client-Side Auth (using Better Auth client):
    ```ts
    'use client';
    import { createAuthClient } from "better-auth/client";
    import { jwtClient } from "better-auth/client/plugins";
    import { useState } from "react";
    import { Button, Input } from "@/components/ui"; // Shadcn

    const client = createAuthClient({ baseURL: process.env.NEXT_PUBLIC_AUTH_BASE_URL, plugins: [jwtClient()] });

    function LoginForm() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    async function handleLogin() {
        const { data, error } = await client.signIn.email({ email, password });
        if (data?.token) {
        // Store JWT in cookies or localStorage
        document.cookie = `authToken=${data.token}; path=/`;
        }
    }

    return (
        <div>
        <Input type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
        <Input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        <Button onClick={handleLogin}>Login</Button>
        </div>
        );
    }
    ```
    - Protected Page: Use middleware or hooks to check JWT.
        - In middleware.ts: Verify JWT or redirect.
    - API Calls: Use fetch with JWT header to FastAPI endpoints.

6. Complete Flow Implementation:
    - Signup/Login: Frontend → Better Auth → Store JWT.
    - Protected Access: Frontend sends JWT → FastAPI verifies → Queries Neon DB via SQLModel.
    - Logout: Clear JWT, call Better Auth signout.

7. Best Practices:
    - Security: Use HTTPS, secure cookies (HttpOnly, Secure), validate inputs.
    - Environment: .env for secrets (JWT_SECRET, DATABASE_URL).
    - Error Handling: Custom errors in FastAPI, loading states in Next.js.
    - Testing: Unit tests for auth flows, integration tests across services.
    - Deployment: Vercel for Next.js/Better Auth, Render/Fly.io for FastAPI, Neon for DB.

## References

Use the shared references located at:
../_shared/reference.md
