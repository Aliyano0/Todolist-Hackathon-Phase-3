# Fix: Update Task Priority and Category

**Issue**: Chatbot couldn't update task priority or category - it would write these values in the description instead.

**Root Cause**: The `update_task` tool only supported updating `title` and `description` fields, not `priority` or `category`.

---

## Changes Made

### 1. Updated MCP Tool (`update_task_tool`)

**File**: `backend/mcp_server/tools/update_task.py`

**Changes**:
- Added `priority` parameter (optional, validates "low", "medium", "high")
- Added `category` parameter (optional, any string)
- Updated validation to check at least one field is provided
- Added priority validation logic
- Updated field update logic to include priority and category
- Updated return value to include priority and category

**New Signature**:
```python
async def update_task_tool(
    user_id: str,
    task_id: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
    priority: Optional[str] = None,  # NEW
    category: Optional[str] = None   # NEW
) -> dict
```

### 2. Updated Agent Wrapper Function

**File**: `backend/core/services/agent_service.py`

**Changes**:
- Added `priority` and `category` parameters to `@function_tool` decorated function
- Updated docstring to document new parameters
- Updated tool call to pass priority and category to underlying tool

**New Signature**:
```python
@function_tool
async def update_task(
    ctx: RunContextWrapper[Any],
    task_id: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
    priority: Optional[str] = None,  # NEW
    category: Optional[str] = None   # NEW
) -> dict
```

### 3. Updated Agent Instructions

**File**: `backend/core/services/agent_service.py`

**Changes**:
- Added "Task Properties" section explaining priority and category
- Updated capabilities list to mention priority and category updates
- Added examples for priority and category updates:
  - "Change task 2 priority to high"
  - "Set task 3 category to work"
  - "Add high priority task: finish report"

---

## How It Works Now

### User Request Examples

**Update Priority**:
```
User: "Change task 1 priority to high"
Agent: Calls update_task(task_id="...", priority="high")
Response: "I've updated task 1 priority to high!"
```

**Update Category**:
```
User: "Set task 2 category to work"
Agent: Calls update_task(task_id="...", category="work")
Response: "I've set task 2 category to work!"
```

**Update Multiple Fields**:
```
User: "Update task 3: change title to 'Meeting' and set priority to high"
Agent: Calls update_task(task_id="...", title="Meeting", priority="high")
Response: "I've updated task 3 with the new title and priority!"
```

**Add Task with Priority**:
```
User: "Add high priority task: finish report"
Agent: Calls add_task(title="finish report", priority="high")
Response: "I've added 'finish report' as a high priority task!"
```

---

## Validation

### Priority Validation
- Valid values: "low", "medium", "high" (case-insensitive)
- Invalid values will raise `ValueError` with clear message
- Agent is instructed to use these exact values

### Category Validation
- Any string value is accepted
- Empty strings are converted to `None`
- No predefined categories (user can create custom ones)

---

## Testing Instructions

### 1. Restart Backend Server
```bash
cd backend
# Stop current server (Ctrl+C)
uv run uvicorn main:app --host 0.0.0.0 --port 8000
```

### 2. Test Priority Updates

**Test Case 1: Update priority to high**
```
User message: "Change task 1 priority to high"
Expected: Task 1 priority updated to "high"
```

**Test Case 2: Update priority to medium**
```
User message: "Set task 2 priority to medium"
Expected: Task 2 priority updated to "medium"
```

**Test Case 3: Update priority to low**
```
User message: "Make task 3 low priority"
Expected: Task 3 priority updated to "low"
```

### 3. Test Category Updates

**Test Case 4: Set category to work**
```
User message: "Set task 1 category to work"
Expected: Task 1 category updated to "work"
```

**Test Case 5: Set category to personal**
```
User message: "Change task 2 category to personal"
Expected: Task 2 category updated to "personal"
```

**Test Case 6: Custom category**
```
User message: "Set task 3 category to shopping"
Expected: Task 3 category updated to "shopping"
```

### 4. Test Combined Updates

**Test Case 7: Update title and priority**
```
User message: "Update task 1: change title to 'Important Meeting' and set priority to high"
Expected: Task 1 title and priority both updated
```

**Test Case 8: Update description and category**
```
User message: "Update task 2 description to 'Buy groceries for dinner' and set category to shopping"
Expected: Task 2 description and category both updated
```

### 5. Test Add Task with Priority/Category

**Test Case 9: Add task with priority**
```
User message: "Add high priority task: finish report"
Expected: New task created with priority="high"
```

**Test Case 10: Add task with category**
```
User message: "Add work task: prepare presentation"
Expected: New task created with category="work"
```

---

## Verification

After testing, verify:
- ✅ Priority updates work correctly (not written to description)
- ✅ Category updates work correctly (not written to description)
- ✅ Agent understands natural language requests for priority/category
- ✅ Multiple fields can be updated in one request
- ✅ Invalid priority values are rejected with clear error
- ✅ Tasks can be created with priority/category from the start

---

## Rollback Plan

If issues occur, revert these files:
1. `backend/mcp_server/tools/update_task.py`
2. `backend/core/services/agent_service.py`

Use git to restore previous versions:
```bash
git checkout HEAD~1 backend/mcp_server/tools/update_task.py
git checkout HEAD~1 backend/core/services/agent_service.py
```

---

## Related Files

**Not Modified** (no changes needed):
- `backend/models/todo.py` - Already has priority and category fields
- `backend/api/tasks.py` - CRUD endpoints already support priority/category
- `backend/schemas/todo.py` - Schemas already include priority/category
- Database schema - Already has priority and category columns

---

**Fix Status**: ✅ Complete, ready for testing
**Backward Compatible**: Yes
**Breaking Changes**: None
**Deployment**: Restart backend server required
