# Reference Guide for Full-Stack Technologies

This reference.md provides an overview, official documentation links, installation instructions, key features, and examples for the technologies used in the full-stack authentication system: Next.js 16.1 (with App Router and local MCP), FastAPI, SQLModel for Neon Serverless PostgreSQL, Better Auth (TypeScript) with JWT tokens, Shadcn UI, Context7 MCP Server, and Next.js Local MCP. This serves as a supporting reference file for related Claude Code skills. Code examples have been expanded for clarity and practicality.

## Next.js 16.1 (App Router)

### Overview
Next.js is a React framework for building server-side rendered and static web applications. Version 16.1 introduces improvements in Turbopack, bundle analysis, and MCP (Model Context Protocol) support for AI coding assistants.

### Official Documentation
- [Next.js Docs](https://nextjs.org/docs)
- [What's New in Next.js 16.1](https://nextjs.org/blog/next-16-1)
- [App Router Guide](https://nextjs.org/docs/app)

### Installation
```bash
npx create-next-app@16.1.1 my-app --typescript --eslint
cd my-app
npm run dev
```

### Key Features
- App Router for file-system-based routing.
- Server Components for server-side rendering.
- Built-in optimizations like image handling and API routes.
- Integration with MCP for local dev tools.

### Example
Basic page with Server Component data fetching in `app/page.tsx`:
```tsx
import { Suspense } from 'react';

async function fetchData() {
  const res = await fetch('https://api.example.com/data', { cache: 'force-cache' });
  return res.json();
}

export default async function Home() {
  const data = await fetchData();
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <h1>Hello, Next.js 16.1!</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </Suspense>
  );
}
```

## FastAPI

### Overview
FastAPI is a modern Python web framework for building APIs with automatic interactive documentation (Swagger/ReDoc).

### Official Documentation
- [FastAPI Docs](https://fastapi.tiangolo.com/)

### Installation
```bash
uv add fastapi uvicorn
```

### Key Features
- Automatic data validation with Pydantic.
- Async support.
- Dependency injection.
- Built-in OAuth2 and JWT support.

### Example
Basic app with a POST endpoint and Pydantic model in `main.py`:
```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

@app.get("/")
async def root():
    return {"message": "Hello FastAPI"}

@app.post("/items/")
async def create_item(item: Item):
    return {"item_name": item.name, "item_price": item.price}
```

Run with: `uvicorn main:app --reload`

## SQLModel for Neon Serverless PostgreSQL

### Overview
SQLModel combines SQLAlchemy and Pydantic for type-safe database modeling. Neon is a serverless PostgreSQL database with auto-scaling.

### Official Documentation
- [SQLModel Docs](https://sqlmodel.tiangolo.com/)
- [Neon Docs](https://neon.tech/docs)

### Installation
```bash
pip install sqlmodel psycopg2-binary
```

### Key Features
- ORM with Pydantic validation.
- Async support.
- Easy migrations with Alembic.
- Neon's branching for dev environments.

### Example
Model definition and CRUD operations:
```python
from sqlmodel import SQLModel, Field, Session, create_engine, select
import os
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str

engine = create_engine(os.getenv("DATABASE_URL"))  # Neon connection string
SQLModel.metadata.create_all(engine)

# Create a user
with Session(engine) as session:
    user = User(email="user@example.com", hashed_password="hashedpass")
    session.add(user)
    session.commit()
    session.refresh(user)

# Read a user
with Session(engine) as session:
    statement = select(User).where(User.email == "user@example.com")
    result = session.exec(statement).first()
    print(result)
```

## Better Auth (TypeScript) with JWT Tokens

### Overview
Better Auth is a TypeScript authentication library for Node.js, configurable to issue JWT tokens for secure user sessions.

### Official Documentation
- [Better Auth Docs](https://better-auth.com/docs) (assuming based on context; check for updates)

### Installation
```bash
npm install better-auth
```

### Key Features
- Plugins for JWT, email/password, OAuth.
- Database adapters (e.g., Prisma for Postgres).
- Self-contained JWT with user info.

### Example
Configuration and basic usage:
```ts
import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";
import { prismaAdapter } from "better-auth/adapters/prisma";
import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient({ datasourceUrl: process.env.DATABASE_URL });

export const auth = betterAuth({
  baseURL: process.env.AUTH_BASE_URL || "http://localhost:3000",
  database: prismaAdapter(prisma, { provider: "postgresql" }),
  plugins: [
    jwt({
      jwt: {
        secret: process.env.JWT_SECRET,
        expirationTime: "1h",
      }
    })
  ]
});

// Example: Sign up (in a handler)
async function signUp(email: string, password: string) {
  const { user } = await auth.handlers.signUp.email({ email, password });
  return user;
}
```

## Shadcn UI

### Overview
Shadcn UI is a collection of reusable React components built with Radix UI and Tailwind CSS, copy-pasteable into projects.

### Official Documentation
- [Shadcn UI Docs](https://ui.shadcn.com/)

### Installation
```bash
npx shadcn-ui@latest init
npx shadcn-ui@latest add button input
```

### Key Features
- Customizable components.
- Accessible and themeable.
- Integration with Next.js.

### Example
Login form using Shadcn components:
```tsx
'use client';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useState } from "react";

export default function LoginForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Handle login logic
  };

  return (
    <form onSubmit={handleSubmit}>
      <Input 
        type="email" 
        placeholder="Email" 
        value={email} 
        onChange={(e) => setEmail(e.target.value)} 
      />
      <Input 
        type="password" 
        placeholder="Password" 
        value={password} 
        onChange={(e) => setPassword(e.target.value)} 
      />
      <Button type="submit">Login</Button>
    </form>
  );
}
```


## Next.js Local MCP for Next.js 16.1

### Overview
Next.js 16.1 includes built-in MCP (Model Context Protocol) support via Next.js DevTools, allowing AI coding agents (e.g., Claude Code) to access app state, routes, and internals in real-time for automated tasks like upgrades and migrations.

### Official Documentation
- [Next.js MCP Guide](https://nextjs.org/docs/app/guides/mcp)
- [Next.js 16.1 Blog](https://nextjs.org/blog/next-16-1)
- [GitHub: next-devtools-mcp](https://github.com/vercel/next-devtools-mcp)

### Installation/Setup
Enabled by default in Next.js 16.1 dev server.
- Run: `npm run dev`
- MCP endpoint: `http://localhost:3000/_next/mcp`
- For advanced: `npx next-devtools-mcp@latest`

### Key Features
- Tools like `get_routes` for route inspection.
- Automates migrations (e.g., to Cache Components).
- Integrates with coding agents for real-time assistance.

### Example
In your AI agent prompt: "Next Devtools, help me upgrade my Next.js app to version 16.1"  
Or configure in `.mcp.json`:
```json
{
  "mcpServers": {
    "next-devtools": {
      "command": "npx",
      "args": ["-y", "next-devtools-mcp@latest"]
    }
  }
}
```

Using MCP programmatically (example Node.js script to query routes):
```ts
import fetch from 'node-fetch';

async function getNextRoutes() {
  const response = await fetch('http://localhost:3000/_next/mcp/get_routes');
  const data = await response.json();
  return data;
}

// Usage
getNextRoutes().then(console.log);
```


# shared-reference.md

## Official Documentation


- OpenAI Agents SDK  
  https://openai.github.io/openai-agents-python/

- Model Context Protocol (MCP)  
  https://modelcontextprotocol.io/

- OpenAI ChatKit  
  https://openai.github.io/chatkit-js/

## Architectural References
- Stateless server design
- Tool-first agent patterns
- Database-backed conversation memory
