# Data Model: Todo App Enhancement

## Overview
This document defines the data structures and relationships for the enhanced todo application, including the new priority and category features.

## Core Entities

### Todo Item
The primary entity representing a user task.

**Fields**:
- `id`: string - Unique identifier for the todo item
- `title`: string - The title or description of the task
- `description`: string (optional) - Additional details about the task
- `completed`: boolean - Whether the task is marked as complete
- `priority`: enum (high, medium, low) - Priority level of the task
- `category`: string - Category assigned to the task (can be predefined or custom)
- `createdAt`: Date - Timestamp when the task was created
- `updatedAt`: Date - Timestamp when the task was last updated

**Validation Rules**:
- `title` is required and must be between 1-200 characters
- `priority` must be one of the allowed values: 'high', 'medium', 'low'
- `category` is required and must be between 1-50 characters
- `completed` defaults to false

**State Transitions**:
- `incomplete` → `complete`: When user marks task as done
- `complete` → `incomplete`: When user unmarks completed task

### Category
Represents a grouping mechanism for organizing tasks.

**Fields**:
- `name`: string - The name of the category
- `isCustom`: boolean - Whether this is a user-defined category or predefined
- `createdAt`: Date - Timestamp when the category was created

**Predefined Categories**:
- work
- personal
- shopping

**Validation Rules**:
- `name` is required and must be between 1-50 characters
- Custom category names must be unique per user

### Priority Level
Represents the importance of a task.

**Values**:
- high: Most urgent tasks requiring immediate attention
- medium: Regular tasks with normal urgency
- low: Less important tasks that can be delayed

## Relationships
- One Todo Item belongs to one Category
- One Priority Level applies to one Todo Item

## Data Storage Schema
The data will be stored in browser local storage with the following structure:

```
{
  "todos": [
    {
      "id": "unique-id",
      "title": "Task title",
      "description": "Task description",
      "completed": false,
      "priority": "high",
      "category": "work",
      "createdAt": "2026-02-02T10:00:00Z",
      "updatedAt": "2026-02-02T10:00:00Z"
    }
  ],
  "categories": [
    {
      "name": "work",
      "isCustom": false,
      "createdAt": "2026-02-02T10:00:00Z"
    }
  ]
}
```

## API Contract Elements
The frontend will manage this data structure, with potential future backend API endpoints following similar patterns:

### Todo Operations
- GET /api/todos - Retrieve all todos for the authenticated user
- POST /api/todos - Create a new todo
- PUT /api/todos/{id} - Update an existing todo
- DELETE /api/todos/{id} - Delete a todo
- PATCH /api/todos/{id}/toggle-complete - Toggle completion status

### Category Operations
- GET /api/categories - Retrieve all available categories
- POST /api/categories - Create a new custom category