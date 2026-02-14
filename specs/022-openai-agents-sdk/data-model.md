# Data Model: OpenAI Agents SDK Integration

**Feature**: 022-openai-agents-sdk
**Date**: 2026-02-12
**Status**: No changes required

## Overview

This feature does not introduce any new database entities or modify existing ones. The OpenAI Agents SDK integration is purely a service layer refactoring that replaces the manual function calling implementation in `agent_service.py` with proper SDK-based orchestration.

## Existing Entities (Unchanged)

### User
- **Purpose**: Store user account information
- **Fields**: id (UUID), email, password_hash, email_verified, verification_token, created_at, updated_at
- **No changes**: User model remains unchanged

### TodoTask
- **Purpose**: Store user tasks
- **Fields**: id (UUID), user_id (UUID FK), title, description, completed, priority, category, created_at, updated_at
- **No changes**: TodoTask model remains unchanged

### Conversation
- **Purpose**: Store chat conversation metadata
- **Fields**: id (UUID), user_id (UUID FK), created_at, updated_at
- **No changes**: Conversation model remains unchanged

### Message
- **Purpose**: Store individual chat messages
- **Fields**: id (UUID), conversation_id (UUID FK), role (user/assistant), content, created_at
- **No changes**: Message model remains unchanged

## Rationale

The OpenAI Agents SDK operates at the application service layer and does not require any database schema changes. The SDK:
- Uses existing conversation history loaded from the Message table
- Orchestrates tool calls that operate on existing TodoTask entities
- Returns responses that are stored in the existing Message table

All data persistence logic remains unchanged. The only modification is how the agent processes messages and orchestrates tool calls internally within `agent_service.py`.

## Migration

**No database migration required** - This feature involves zero schema changes.
