# Phase 4: Backward Compatibility Validation - Testing Guide

## Overview
This phase validates that the OpenAI Agents SDK integration maintains 100% backward compatibility with the existing chat functionality.

## Prerequisites
- Backend server running at port 8000
- OpenAI Agents SDK installed (openai-agents==0.8.3)
- OPENROUTER_API_KEY configured in .env
- Valid user account with verified email
- JWT token for authentication

## Test Execution

### T025: Run Existing Test Suite

**Command**:
```bash
cd backend
pytest tests/ -v --tb=short
```

**Expected Result**: All tests pass without modification

**Success Criteria**: 100% pass rate (no test failures)

### T026: Email Verification Requirement

**Test**: Attempt to use chat with unverified email

**Steps**:
1. Create user account without verifying email
2. Get JWT token
3. Send POST request to `/api/{user_id}/chat`

**Expected Result**: 403 Forbidden error with message "Email not verified"

### T027: Rate Limiting

**Test**: Send more than 10 messages in one minute

**Steps**:
1. Send 10 messages to `/api/{user_id}/chat` within 60 seconds
2. Send 11th message

**Expected Result**: 11th message returns 429 Too Many Requests error

### T028: Multilingual Support

**Test Cases**:

1. **English**:
   - Input: "add task: buy groceries"
   - Expected: Response in English confirming task creation

2. **Roman Urdu**:
   - Input: "Mujhe apne tasks dikhao"
   - Expected: Response in Roman Urdu listing tasks

3. **Urdu Script**:
   - Input: "مجھے اپنے ٹاسک دکھاؤ"
   - Expected: Response in Urdu script listing tasks

**Success Criteria**: Agent responds in the same language as input

### T029: Conversation Persistence

**Test**: Verify conversation history is loaded correctly

**Steps**:
1. Send message: "add task: test task"
2. Close chat
3. Reopen chat with same conversation_id
4. Send message: "show my tasks"

**Expected Result**: Agent has access to previous conversation context

### T030: User Isolation

**Test**: Verify users can only access their own tasks

**Steps**:
1. User A creates task: "User A's task"
2. User B creates task: "User B's task"
3. User A requests: "show my tasks"

**Expected Result**: User A only sees "User A's task" (not User B's task)

### T031: Chat Endpoint Response Format

**Test**: Verify response schema matches existing format

**Request**:
```json
POST /api/{user_id}/chat
{
  "message": "add task: test",
  "conversation_id": null
}
```

**Expected Response**:
```json
{
  "conversation_id": "uuid",
  "message": "string",
  "timestamp": "ISO 8601 timestamp"
}
```

### T032: Performance Validation

**Test**: Measure response times

**Simple Query** (e.g., "add task: test"):
- Expected: < 5 seconds

**Complex Query** (e.g., "list all my pending tasks, then mark task 1 as complete"):
- Expected: < 10 seconds

**Success Criteria**: No performance regression from previous implementation

## Manual Testing Checklist

- [ ] T025: Run pytest suite (all tests pass)
- [ ] T026: Email verification enforced (403 error)
- [ ] T027: Rate limiting works (429 error on 11th message)
- [ ] T028: English responses work correctly
- [ ] T028: Roman Urdu responses work correctly
- [ ] T028: Urdu script responses work correctly
- [ ] T029: Conversation history loads correctly
- [ ] T030: User isolation verified (no cross-user access)
- [ ] T031: Response format matches schema
- [ ] T032: Simple queries < 5s
- [ ] T032: Complex queries < 10s

## Verification Commands

### Check Server Logs
```bash
# Monitor logs for OpenRouter API calls
tail -f backend/logs/app.log | grep "OpenRouter"

# Monitor agent execution
tail -f backend/logs/app.log | grep "🤖"
```

### Test with curl
```bash
# Get JWT token first (replace with your credentials)
TOKEN="your_jwt_token"
USER_ID="your_user_id"

# Send test message
curl -X POST "http://localhost:8000/api/${USER_ID}/chat" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"message": "add task: test task", "conversation_id": null}'
```

## Success Criteria Summary

✅ **All tests pass**: Existing test suite runs without modification
✅ **Auth preserved**: Email verification and JWT validation work
✅ **Rate limiting**: 10 messages/minute enforced
✅ **Multilingual**: Responses match input language
✅ **Persistence**: Conversation history loads correctly
✅ **Isolation**: User data properly isolated
✅ **Schema**: Response format unchanged
✅ **Performance**: No regression (<5s simple, <10s complex)

## Notes

- All tests should pass without modifying test code
- Any test failures indicate backward compatibility issues
- Performance should be measured under normal load conditions
- Multilingual support should be tested with native speakers if possible
