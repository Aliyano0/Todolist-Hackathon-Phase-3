# Data Model: Backend Cleanup and Frontend Consistency

## Backend Data Models (Post-Cleanup)

### TodoTask Model
- **id**: int (primary key, auto-generated) → string (for frontend compatibility)
- **title**: str (required, max_length=255)
- **description**: str (optional)
- **completed**: bool (default=False)
- **created_at**: datetime (auto-generated)
- **updated_at**: datetime (auto-generated)

## Frontend Data Models

### TodoItem Interface
- **id**: string (required) - matches backend ID after conversion
- **title**: string (required)
- **description**: string (optional)
- **completed**: boolean (required)
- **createdAt**: string (ISO date string) - converted from created_at
- **updatedAt**: string (ISO date string) - converted from updated_at
- **userId**: string (not used in single-user implementation)

## Data Flow and Transformation

### Backend → Frontend Transformation
1. Integer IDs converted to string IDs
2. Snake_case fields (created_at, updated_at) converted to camelCase (createdAt, updatedAt)
3. Response wrapped in { data: [...] } format for frontend compatibility

### Frontend → Backend Transformation
1. Frontend sends data in expected format
2. Backend receives and stores in SQLModel format
3. Backend handles validation and persistence

## API Contract Consistency

### Standardized Todo Entity
- **id**: string (to match frontend expectation)
- **title**: string
- **description**: string (nullable)
- **completed**: boolean
- **createdAt**: string (ISO 8601 format)
- **updatedAt**: string (ISO 8601 format)
- **userId**: string (reserved for future multi-user implementation)

### API Endpoint Consistency
- All endpoints return consistent data format
- Proper error handling and response wrapping
- Field naming consistency (camelCase for frontend)
- ID type consistency (string IDs for frontend compatibility)

## Database Schema (Preserved)
- SQLModel TodoTask model remains unchanged in database
- Backend handles transformation from int IDs to string IDs for frontend
- Timestamps preserved as datetime in database, converted to ISO string for frontend