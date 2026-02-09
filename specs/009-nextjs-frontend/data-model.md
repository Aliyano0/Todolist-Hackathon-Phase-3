# Data Model: Next.js Frontend for Todo Application

## Entity: Todo Item

**Fields**:
- `id`: string | number (unique identifier from backend)
- `title`: string (required, max 255 characters)
- `description`: string | null (optional, max 1000 characters)
- `completed`: boolean (default: false)
- `createdAt`: Date | string (timestamp from backend)
- `updatedAt`: Date | string (timestamp from backend)

**Validation Rules**:
- Title must be 1-255 characters
- Description must be 0-1000 characters if provided
- Completed must be a boolean value
- createdAt and updatedAt are read-only (set by backend)

**State Transitions**:
- Pending → Completed (when user marks as complete)
- Completed → Pending (when user marks as incomplete)

## Entity: UI Theme

**Fields**:
- `mode`: 'light' | 'dark' (current theme selection)
- `isSystemPreferred`: boolean (whether following system preference)

**Validation Rules**:
- Mode must be either 'light' or 'dark'
- isSystemPreferred must be a boolean

## Entity: User Session (Placeholder)

**Fields**:
- `sessionId`: string (unique session identifier)
- `todos`: Array<TodoItem> (cached todo data for this session)
- `lastSyncTime`: Date | null (when last synced with backend)

**Validation Rules**:
- sessionId must be unique per browser session
- todos array must contain valid TodoItem objects
- lastSyncTime must be a valid date or null

## Relationships

- User Session contains multiple Todo Items
- Theme is independent of other entities
- Todo Items are persisted to backend API via REST endpoints

## Client-Side State Schema

```typescript
interface AppState {
  todos: TodoItem[];
  theme: 'light' | 'dark';
  isLoading: boolean;
  error: string | null;
  session: {
    id: string;
    lastSync: Date | null;
  };
}
```