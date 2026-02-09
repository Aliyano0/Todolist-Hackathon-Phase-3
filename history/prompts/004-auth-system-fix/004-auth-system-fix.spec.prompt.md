---
id: 004
title: auth-system-fix
stage: spec
date_iso: 2026-01-26
surface: agent
model: claude-sonnet-4-5-20250929
feature: auth-system-fix
branch: 004-auth-system-fix
user: claude
command: /sp.specify
labels: ["authentication", "backend", "frontend", "integration"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - specs/004-auth-system-fix/spec.md
  - specs/004-auth-system-fix/checklists/requirements.md
tests_yaml: []
---

# PHR: Authentication System Fix Specification

## User Prompt

I have phase-2 of the project which is a full-stack todo web app. Review all the previous specs and /backend and /frontend directories. Review authentication specifically. This is the error it shows after submitting the signup form 127.0.0.1:47862 - "POST /auth/register HTTP/1.1" 400 Bad Request on my fastapi backend. All the backend endpoints are in fastapi server but the authentication system is implemented using better-auth in next.js using jwt tokens. Come up with a solution to it or redefine the system which is causing this error if needed.

## Analysis and Response

Identified an architecture inconsistency in the authentication system where:
1. The frontend has a custom authentication provider implementation that calls backend auth endpoints
2. Better Auth is installed in the frontend but not properly configured
3. The backend has FastAPI auth endpoints that are compatible with the frontend's API calls

The issue is likely caused by:
- Conflicting authentication implementations (custom vs Better Auth)
- Potential configuration mismatch between frontend and backend
- Possible CORS or networking configuration issue

Created a comprehensive specification for fixing the authentication system with:
- Clear user stories for registration, login, and authentication consistency
- Functional requirements addressing the 400 Bad Request error
- Success criteria for measuring resolution
- Proper architecture decision to unify the authentication approach

## Outcome

Successfully created specification file at specs/004-auth-system-fix/spec.md with a complete requirements analysis and identified the core issue as an architectural inconsistency between authentication implementations.