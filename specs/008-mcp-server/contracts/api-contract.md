# MCP Tools API Contract

## Overview
This document defines the API contract for the 5 MCP tools that enable AI agents to perform task management operations.

## Tool: add_task
### Purpose
Create a new task for a user

### Parameters
- user_id (string, required): The ID of the user for whom to create the task
- title (string, required): The title of the task (1-200 characters)
- description (string, optional): The description of the task (0-1000 characters)

### Request Example
```json
{
  "user_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

### Response
```json
{
  "id": "f1e2d3c4-a5b6-7890-1234-567890fedcba",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "status": "pending",
  "priority": "medium",
  "due_date": null,
  "user_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "created_at": "2025-12-29T15:30:00Z",
  "updated_at": "2025-12-29T15:30:00Z",
  "reminder_sent": false
}
```

## Tool: list_tasks
### Purpose
Retrieve tasks for a user, optionally filtered by status

### Parameters
- user_id (string, required): The ID of the user whose tasks to retrieve
- status (string, optional): Filter by status (pending, in_progress, completed, or null for all)

### Request Example
```json
{
  "user_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "status": "pending"
}
```

### Response
```json
[
  {
    "id": "f1e2d3c4-a5b6-7890-1234-567890fedcba",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "status": "pending",
    "priority": "medium",
    "due_date": null,
    "user_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
    "created_at": "2025-12-29T15:30:00Z",
    "updated_at": "2025-12-29T15:30:00Z",
    "reminder_sent": false
  }
]
```

## Tool: update_task
### Purpose
Update properties of an existing task

### Parameters
- user_id (string, required): The ID of the user who owns the task
- task_id (string, required): The ID of the task to update
- title (string, optional): New title for the task
- description (string, optional): New description for the task
- status (string, optional): New status for the task
- priority (string, optional): New priority for the task
- due_date (string, optional): New due date for the task (ISO 8601 format)

### Request Example
```json
{
  "user_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "task_id": "f1e2d3c4-a5b6-7890-1234-567890fedcba",
  "title": "Buy groceries and fruits",
  "status": "in_progress"
}
```

### Response
```json
{
  "id": "f1e2d3c4-a5b6-7890-1234-567890fedcba",
  "title": "Buy groceries and fruits",
  "description": "Milk, eggs, bread",
  "status": "in_progress",
  "priority": "medium",
  "due_date": null,
  "user_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "created_at": "2025-12-29T15:30:00Z",
  "updated_at": "2025-12-29T15:45:00Z",
  "reminder_sent": false
}
```

## Tool: complete_task
### Purpose
Mark a task as completed

### Parameters
- user_id (string, required): The ID of the user who owns the task
- task_id (string, required): The ID of the task to complete

### Request Example
```json
{
  "user_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "task_id": "f1e2d3c4-a5b6-7890-1234-567890fedcba"
}
```

### Response
```json
{
  "id": "f1e2d3c4-a5b6-7890-1234-567890fedcba",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "status": "completed",
  "priority": "medium",
  "due_date": null,
  "user_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "created_at": "2025-12-29T15:30:00Z",
  "updated_at": "2025-12-29T16:00:00Z",
  "reminder_sent": false
}
```

## Tool: delete_task
### Purpose
Remove a task from the user's list

### Parameters
- user_id (string, required): The ID of the user who owns the task
- task_id (string, required): The ID of the task to delete

### Request Example
```json
{
  "user_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "task_id": "f1e2d3c4-a5b6-7890-1234-567890fedcba"
}
```

### Response
```json
{
  "message": "Task deleted successfully",
  "deleted_task_id": "f1e2d3c4-a5b6-7890-1234-567890fedcba",
  "user_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef"
}
```

## Error Responses
All tools may return error responses in the following format:

```json
{
  "error": "Error message describing the issue",
  "code": "ERROR_CODE"
}
```