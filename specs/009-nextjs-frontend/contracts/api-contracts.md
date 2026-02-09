# API Contracts: Todo Operations

## Base URL
`http://localhost:8000/api` (or as configured)

## Endpoints

### GET /todos
**Description**: Retrieve all todos for the current session

**Request**:
- Method: GET
- Headers: None required
- Parameters: None

**Response**:
- Success (200): `Array<TodoItem>`
```json
[
  {
    "id": "1",
    "title": "Sample todo",
    "description": "Sample description",
    "completed": false,
    "createdAt": "2026-01-30T10:00:00Z",
    "updatedAt": "2026-01-30T10:00:00Z"
  }
]
```

**Error Responses**:
- 500: Internal server error

### POST /todos
**Description**: Create a new todo

**Request**:
- Method: POST
- Headers: `Content-Type: application/json`
- Body:
```json
{
  "title": "New todo title",
  "description": "Optional description",
  "completed": false
}
```

**Response**:
- Success (201): `TodoItem`
```json
{
  "id": "2",
  "title": "New todo title",
  "description": "Optional description",
  "completed": false,
  "createdAt": "2026-01-30T10:05:00Z",
  "updatedAt": "2026-01-30T10:05:00Z"
}
```

**Error Responses**:
- 400: Validation error
- 500: Internal server error

### PUT /todos/{id}
**Description**: Update an existing todo

**Request**:
- Method: PUT
- Headers: `Content-Type: application/json`
- Path Parameter: `id` (todo ID)
- Body:
```json
{
  "title": "Updated title",
  "description": "Updated description",
  "completed": true
}
```

**Response**:
- Success (200): `TodoItem`
```json
{
  "id": "2",
  "title": "Updated title",
  "description": "Updated description",
  "completed": true,
  "createdAt": "2026-01-30T10:05:00Z",
  "updatedAt": "2026-01-30T10:10:00Z"
}
```

**Error Responses**:
- 400: Validation error
- 404: Todo not found
- 500: Internal server error

### DELETE /todos/{id}
**Description**: Delete a todo

**Request**:
- Method: DELETE
- Path Parameter: `id` (todo ID)

**Response**:
- Success (204): No content

**Error Responses**:
- 404: Todo not found
- 500: Internal server error

### PATCH /todos/{id}/toggle-complete
**Alternative**: Toggle completion status via PUT to /todos/{id} with updated `completed` field

**Description**: Toggle the completion status of a todo

**Request**:
- Method: PATCH
- Path Parameter: `id` (todo ID)

**Response**:
- Success (200): `TodoItem`
```json
{
  "id": "2",
  "title": "Updated title",
  "description": "Updated description",
  "completed": false,
  "createdAt": "2026-01-30T10:05:00Z",
  "updatedAt": "2026-01-30T10:15:00Z"
}
```

**Error Responses**:
- 404: Todo not found
- 500: Internal server error