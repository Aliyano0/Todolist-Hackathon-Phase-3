# API Contracts: OpenAI Agents SDK Integration

**Feature**: 022-openai-agents-sdk
**Date**: 2026-02-12
**Status**: No changes required

## Overview

This feature does not modify any API contracts. The OpenAI Agents SDK integration is an internal service layer refactoring that maintains 100% backward compatibility with existing endpoints.

## Existing Endpoints (Unchanged)

### POST /api/{user_id}/chat

**Purpose**: Send a message to the AI chatbot and receive a response

**Request**:
```json
{
  "message": "string",
  "conversation_id": "uuid | null"
}
```

**Response** (200 OK):
```json
{
  "response": "string",
  "conversation_id": "uuid"
}
```

**Error Responses**:
- 401 Unauthorized: Invalid or missing JWT token
- 403 Forbidden: Email not verified
- 429 Too Many Requests: Rate limit exceeded (10 messages per minute)
- 500 Internal Server Error: Agent processing error

**No changes**: Request/response schemas remain identical. The only difference is internal - the agent now uses OpenAI Agents SDK for tool orchestration instead of manual function calling.

## Internal Changes (Not Visible to API Consumers)

The following changes occur internally within `agent_service.py` but do not affect the API contract:

1. **Agent Initialization**: Uses `Agent` class from OpenAI Agents SDK instead of manual OpenAI client setup
2. **Tool Orchestration**: SDK automatically selects and executes tools instead of manual function calling
3. **Conversation Processing**: Uses `Runner.run()` with input list instead of manual message processing
4. **State Management**: SDK handles multi-turn conversation state automatically

## Backward Compatibility Guarantee

All existing API consumers (frontend chat widget, full chat page) will continue to work without any modifications. The chat endpoint behavior remains identical:
- Same authentication requirements (JWT + email verification)
- Same rate limiting (10 messages/minute)
- Same request/response format
- Same error handling
- Same multilingual support (English, Roman Urdu, Urdu)
- Same user isolation (user_id in path)

## Testing Strategy

Backward compatibility will be validated by:
1. Running existing test suite without modifications - all tests must pass
2. Manual testing of chat functionality from frontend
3. Verifying response format matches existing schemas
4. Confirming error handling behavior is unchanged
