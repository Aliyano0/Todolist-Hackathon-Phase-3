# API Contracts: Todo Application

## Base URL
`http://localhost:8000/api` (backend server)

## Authentication
Currently none (temporary single-user implementation). Will implement JWT authentication in future phase.

## Todo Operations

### GET /api/todos
**Description:** Retrieve all todos

**Request:**
- Method: GET
- Headers: None required
- Parameters: None

**Response:**
- Success: 200 OK
- Content-Type: application/json
- Body: `{ "data": [TodoItem] }`

**Example Response:**
```json
{
  "data": [
    {
      "id": "1",
      "title": "Sample task",
      "description": "Sample description",
      "completed": false,
      "createdAt": "2026-02-02T10:00:00",
      "updatedAt": "2026-02-02T10:00:00",
      "userId": "1"
    }
  ]
}
```

### POST /api/todos
**Description:** Create a new todo

**Request:**
- Method: POST
- Headers: Content-Type: application/json
- Body: `{ "title": string, "description": string, "completed": boolean }`

**Response:**
- Success: 201 Created
- Content-Type: application/json
- Body: `{ "data": TodoItem }`

### GET /api/todos/{id}
**Description:** Get a specific todo by ID

**Request:**
- Method: GET
- Headers: None required
- Parameters: id (path parameter)

**Response:**
- Success: 200 OK
- Content-Type: application/json
- Body: `{ "data": TodoItem }`

### PUT /api/todos/{id}
**Description:** Update a todo

**Request:**
- Method: PUT
- Headers: Content-Type: application/json
- Parameters: id (path parameter)
- Body: `{ "title": string, "description": string, "completed": boolean }`

**Response:**
- Success: 200 OK
- Content-Type: application/json
- Body: `{ "data": TodoItem }`

### DELETE /api/todos/{id}
**Description:** Delete a todo

**Request:**
- Method: DELETE
- Headers: Content-Type: application/json
- Parameters: id (path parameter)

**Response:**
- Success: 200 OK
- Content-Type: application/json
- Body: `{ "data": TodoItem }`

### PATCH /api/todos/{id}/toggle
**Description:** Toggle completion status of a todo

**Request:**
- Method: PATCH
- Headers: Content-Type: application/json
- Parameters: id (path parameter)

**Response:**
- Success: 200 OK
- Content-Type: application/json
- Body: `{ "data": TodoItem }`

## Data Format
- ID: String format (converted from integer backend IDs)
- Timestamps: ISO 8601 format in camelCase (createdAt, updatedAt)
- All responses wrapped in `data` property for consistency