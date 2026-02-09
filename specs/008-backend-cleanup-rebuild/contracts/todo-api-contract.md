# API Contract: Todo Task Management

## Base URL
`/api/tasks`

## Endpoints

### GET /api/tasks
**Description:** Retrieve all todo tasks

**Response:**
- Status: 200 OK
- Body: Array of Task objects
```json
[
  {
    "id": 1,
    "title": "Sample task",
    "description": "Sample description",
    "completed": false,
    "created_at": "2026-01-30T10:00:00Z",
    "updated_at": "2026-01-30T10:00:00Z"
  }
]
```

### POST /api/tasks
**Description:** Create a new todo task

**Request:**
- Body:
```json
{
  "title": "New task",
  "description": "Task description (optional)",
  "completed": false
}
```

**Response:**
- Status: 201 Created
- Body: Created Task object
```json
{
  "id": 2,
  "title": "New task",
  "description": "Task description (optional)",
  "completed": false,
  "created_at": "2026-01-30T10:00:00Z",
  "updated_at": "2026-01-30T10:00:00Z"
}
```

**Validation:**
- Title is required
- Title must be less than 255 characters

### GET /api/tasks/{id}
**Description:** Retrieve a specific todo task by ID

**Path Parameters:**
- id: Task identifier

**Response:**
- Status: 200 OK
- Body: Task object
```json
{
  "id": 1,
  "title": "Sample task",
  "description": "Sample description",
  "completed": false,
  "created_at": "2026-01-30T10:00:00Z",
  "updated_at": "2026-01-30T10:00:00Z"
}
```
- Status: 404 Not Found if task doesn't exist

### PUT /api/tasks/{id}
**Description:** Update an existing todo task

**Path Parameters:**
- id: Task identifier

**Request:**
- Body:
```json
{
  "title": "Updated task",
  "description": "Updated description",
  "completed": true
}
```

**Response:**
- Status: 200 OK
- Body: Updated Task object
- Status: 404 Not Found if task doesn't exist

**Validation:**
- Title is required
- Title must be less than 255 characters

### DELETE /api/tasks/{id}
**Description:** Delete a todo task

**Path Parameters:**
- id: Task identifier

**Response:**
- Status: 204 No Content
- Status: 404 Not Found if task doesn't exist

### PATCH /api/tasks/{id}/complete
**Description:** Toggle the completion status of a task

**Path Parameters:**
- id: Task identifier

**Response:**
- Status: 200 OK
- Body: Updated Task object with toggled completion status
- Status: 404 Not Found if task doesn't exist

## Error Responses
All error responses follow the format:
```json
{
  "detail": "Error message"
}
```

Common error statuses:
- 400 Bad Request: Invalid request format or validation errors
- 404 Not Found: Resource doesn't exist
- 500 Internal Server Error: Server-side error