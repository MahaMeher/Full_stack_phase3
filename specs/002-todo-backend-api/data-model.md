# Data Model: Todo Backend API

## Overview
This document defines the data models for the Todo Backend API, including database schema and API request/response structures.

## Core Entities

### Task Entity
**Description**: Represents a user's todo item with properties and state.

#### Database Schema
- **Table Name**: `tasks`
- **Fields**:
  - `id`: UUID (Primary Key, auto-generated)
  - `user_id`: String (Foreign Key reference to user, extracted from JWT)
  - `title`: String (Required, 1-200 characters)
  - `description`: String (Optional, nullable)
  - `completed`: Boolean (Default: false)
  - `created_at`: DateTime (Auto-generated timestamp)
  - `updated_at`: DateTime (Auto-generated timestamp, updated on changes)

#### Relationships
- Belongs to: User (via `user_id` foreign key)
- Access Control: Only the user who owns the task can access it

#### Constraints
- `title` length: 1-200 characters
- `user_id` cannot be null
- `completed` defaults to false
- `created_at` is set on creation
- `updated_at` is updated on any modification

#### Indexes
- Primary Index: `id` (automatically created)
- Foreign Key Index: `user_id` (for efficient user-based filtering)

## API Request/Response Schemas

### Create Task Request
```json
{
  "title": "Task title (required, 1-200 chars)",
  "description": "Optional description",
  "completed": false
}
```

### Update Task Request
```json
{
  "title": "Updated title (required, 1-200 chars)",
  "description": "Updated description (optional)",
  "completed": true
}
```

### Task Response (Single Task)
```json
{
  "id": "uuid-string",
  "user_id": "user-id-from-jwt",
  "title": "Task title",
  "description": "Task description (may be null)",
  "completed": false,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

### List Tasks Response (Multiple Tasks)
```json
[
  {
    "id": "uuid-string",
    "user_id": "user-id-from-jwt",
    "title": "Task title",
    "description": "Task description (may be null)",
    "completed": false,
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z"
  },
  ...
]
```

### Toggle Completion Response
```json
{
  "id": "uuid-string",
  "user_id": "user-id-from-jwt",
  "title": "Task title",
  "description": "Task description (may be null)",
  "completed": true,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

## Validation Rules

### Task Creation
- `title` is required and must be 1-200 characters
- `description` is optional, if provided must be reasonable length (< 1000 chars)
- `completed` is optional, defaults to false

### Task Update
- `title` remains required and must be 1-200 characters
- `description` remains optional
- `completed` can be updated to true or false

### Task Access
- Users can only access tasks with their own `user_id`
- Requests for other users' tasks return 404 (to prevent user enumeration)

## State Transitions

### Task Completion Toggle
- `completed: false` → `completed: true` (when marking as done)
- `completed: true` → `completed: false` (when unmarking as done)

### Task Lifecycle
- Created with `completed: false`
- Can be updated multiple times
- Can be marked as completed or uncompleted
- Can be deleted permanently