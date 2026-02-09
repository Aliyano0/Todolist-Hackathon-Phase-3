# Data Model: Frontend Rebuild

## Overview
This document outlines the frontend data structures and entities for the Todo application rebuild.

## Entities

### Todo Item
**Description**: Represents a task with properties such as title, description, completion status, and timestamps

**Fields**:
- `id`: string | Unique identifier for the todo item
- `title`: string | Title of the todo item (required, max 255 characters)
- `description`: string | Optional description of the todo item (nullable, max 1000 characters)
- `completed`: boolean | Completion status of the todo item (default: false)
- `createdAt`: Date | Timestamp when the todo was created
- `updatedAt`: Date | Timestamp when the todo was last updated
- `userId`: string | ID of the user who owns this todo (for backend association)

**Validation Rules**:
- Title must not be empty
- Title must be less than 255 characters
- Description must be less than 1000 characters if provided

**State Transitions**:
- Pending → Completed (when user marks as complete)
- Completed → Pending (when user marks as incomplete)

### User Profile
**Description**: Contains user information and preferences including theme selection

**Fields**:
- `id`: string | Unique identifier for the user
- `username`: string | Username for the user
- `email`: string | Email address for the user
- `themePreference`: "light" | "dark" | User's preferred theme (default: system preference)

**Validation Rules**:
- Username must be unique
- Email must be valid format

### Theme Settings
**Description**: Configuration for light and dark mode appearance and behavior

**Fields**:
- `mode`: "light" | "dark" | Current theme mode
- `systemPreference`: boolean | Whether to follow system preference (default: false)
- `lastUpdated`: Date | When the theme was last changed

**State Transitions**:
- Light → Dark (when user selects dark theme)
- Dark → Light (when user selects light theme)
- Auto → Light/Dark (when system preference changes)

### Application Layout
**Description**: Defines the structure and navigation elements that persist across all pages

**Fields**:
- `theme`: ThemeSettings | Current theme configuration
- `sidebarCollapsed`: boolean | Whether sidebar is collapsed
- `notificationsEnabled`: boolean | Whether notifications are enabled
- `currentRoute`: string | Current page route

## Relationships
- User Profile 1 → * Todo Item (one user to many todos)
- Theme Settings 1 → 1 Application Layout (one theme config per layout)

## Frontend State Management
The frontend will maintain the following state:

### Todo State
- `todos`: TodoItem[] | List of all todos for the current user
- `loading`: boolean | Whether todos are being loaded
- `error`: string | Any error message from API calls
- `filter`: "all" | "active" | "completed" | Current filter for todo list

### Theme State
- `currentTheme`: "light" | "dark" | Currently active theme
- `themePreference`: "light" | "dark" | "system" | User's saved preference
- `isThemeLoading`: boolean | Whether theme is being applied

## API Response Structures

### Todo API Responses
```typescript
// GET /todos response
interface GetTodosResponse {
  data: TodoItem[];
  pagination?: {
    page: number;
    pageSize: number;
    totalCount: number;
  };
}

// POST /todos response
interface CreateTodoResponse {
  data: TodoItem;
}

// PUT /todos/{id} response
interface UpdateTodoResponse {
  data: TodoItem;
}

// DELETE /todos/{id} response
interface DeleteTodoResponse {
  success: boolean;
  message: string;
}
```

### Error Response Structure
```typescript
interface ErrorResponse {
  error: {
    code: string;
    message: string;
    details?: any;
  };
}
```