# Data Model: Backend-Frontend API Integration Review

## Backend Data Models

### TodoTask Model
- **id**: int (primary key, auto-generated)
- **title**: str (required, max_length=255)
- **description**: str (optional)
- **completed**: bool (default=False)
- **created_at**: datetime (auto-generated)
- **updated_at**: datetime (auto-generated)

### User Model
- **id**: int (primary key, auto-generated)
- **email**: str (unique, required)
- **username**: str (unique, required)
- **hashed_password**: str (required)
- **created_at**: datetime (auto-generated)
- **updated_at**: datetime (auto-generated)

## Frontend Data Models

### TodoItem Interface
- **id**: string (required)
- **title**: string (required)
- **description**: string (optional)
- **completed**: boolean (required)
- **createdAt**: string (ISO date string)
- **updatedAt**: string (ISO date string)
- **userId**: string (required, though not used in backend)

### API Response Format (Expected by Frontend)
- **data**: Array<TodoItem> (wrapped array response)
- **error**: string (optional, for error responses)

## Inconsistencies Identified

1. **ID Type**: Backend uses integer IDs, frontend expects string IDs
2. **Field Names**: Backend uses snake_case, frontend expects camelCase
3. **User Context**: Backend is currently single-user (no user filtering), frontend expects userId
4. **Response Format**: Backend returns direct arrays, frontend expects wrapped responses
5. **Endpoint Paths**: Backend uses `/api/tasks`, frontend calls `/todos`

## Recommended Data Model Alignment

### Standardized Todo Entity
- **id**: string (to match frontend expectation)
- **title**: string
- **description**: string (nullable)
- **completed**: boolean
- **createdAt**: string (ISO 8601 format)
- **updatedAt**: string (ISO 8601 format)
- **userId**: string (to be implemented when auth is added)

### API Contract Standardization
- Standardize on `/api/todos` endpoints to match frontend expectations
- Return wrapped responses in format `{ data: [...] }` for collections
- Convert snake_case to camelCase for timestamp fields
- Convert integer IDs to string IDs in API responses