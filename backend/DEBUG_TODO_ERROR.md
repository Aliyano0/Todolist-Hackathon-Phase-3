# Debugging Todo Creation Error

## Error Message
```
Error adding todo: Error: [object Object]
```

## Improved Error Handling

I've updated the API client to show the actual error message instead of "[object Object]".

## Next Steps to Debug

### 1. Check Browser Console
After restarting the frontend, try creating a todo again and check the browser console for:
- The actual error message (should now be readable)
- The API request details
- The response from the backend

### 2. Check Backend Logs
Look at the backend terminal for:
- The incoming request
- Any error messages
- Stack traces

### 3. Common Issues to Check

**Issue 1: User ID Not Found**
- Error: "User not found" or 401
- Solution: Make sure you're logged in and the token is valid

**Issue 2: Missing Required Fields**
- Error: "Title is required" or validation error
- Solution: Check that the todo form is sending all required fields

**Issue 3: Database Connection**
- Error: Database-related errors
- Solution: Verify DATABASE_URL is set and database is accessible

**Issue 4: Async/Await Issues**
- Error: "Cannot read property" or similar
- Solution: Already fixed by converting to async

### 4. Test with curl

```bash
# Get your token from localStorage in browser console:
# localStorage.getItem('access_token')

# Get your user ID:
# JSON.parse(localStorage.getItem('user')).id

# Test create todo:
curl -X POST http://localhost:8000/api/{USER_ID}/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {YOUR_TOKEN}" \
  -d '{
    "title": "Test Task",
    "description": "Test Description",
    "completed": false,
    "priority": "medium",
    "category": "personal"
  }'
```

### 5. Restart Frontend

```bash
cd frontend
npm run dev
```

Then try creating a todo again and check the console for the actual error message.
