# API Contract: Task Management Endpoints

## Base URL
`/tasks`

## Authentication
All endpoints require valid JWT token in Authorization header:
```
Authorization: Bearer {jwt_token}
```

## Endpoints

### GET /tasks
**Description**: Get all tasks for the authenticated user

**Query Parameters**:
- `status` (optional): Filter by status (pending, in_progress, completed)
- `limit` (optional): Number of tasks to return (default: 20, max: 100)
- `offset` (optional): Number of tasks to skip (for pagination)

**Success Response (200)**:
```json
{
  "tasks": [
    {
      "id": "uuid-string",
      "title": "Task Title",
      "description": "Task description",
      "status": "pending",
      "priority": "medium",
      "due_date": "2023-12-31T10:00:00Z",
      "user_id": "user-uuid-string",
      "created_at": "2023-12-01T10:00:00Z",
      "updated_at": "2023-12-01T10:00:00Z"
    }
  ],
  "total": 1,
  "offset": 0,
  "limit": 20
}
```

**Error Responses**:
- 401: UNAUTHORIZED - Invalid or expired token

### POST /tasks
**Description**: Create a new task for the authenticated user

**Request**:
```json
{
  "title": "New Task",
  "description": "Task description",
  "status": "pending",
  "priority": "medium",
  "due_date": "2023-12-31T10:00:00Z"
}
```

**Request Validation**:
- Title: Required, 1-200 characters
- Description: Optional, max 1000 characters
- Status: Optional, defaults to "pending", must be valid status
- Priority: Optional, defaults to "medium", must be valid priority
- Due date: Optional, must be valid datetime format

**Success Response (201)**:
```json
{
  "id": "uuid-string",
  "title": "New Task",
  "description": "Task description",
  "status": "pending",
  "priority": "medium",
  "due_date": "2023-12-31T10:00:00Z",
  "user_id": "user-uuid-string",
  "created_at": "2023-12-01T10:00:00Z",
  "updated_at": "2023-12-01T10:00:00Z"
}
```

**Error Responses**:
- 401: UNAUTHORIZED - Invalid or expired token
- 400: VALIDATION_ERROR - Invalid input data

### GET /tasks/{id}
**Description**: Get a specific task by ID

**Path Parameters**:
- `id`: Task UUID

**Success Response (200)**:
```json
{
  "id": "uuid-string",
  "title": "Task Title",
  "description": "Task description",
  "status": "pending",
  "priority": "medium",
  "due_date": "2023-12-31T10:00:00Z",
  "user_id": "user-uuid-string",
  "created_at": "2023-12-01T10:00:00Z",
  "updated_at": "2023-12-01T10:00:00Z"
}
```

**Error Responses**:
- 401: UNAUTHORIZED - Invalid or expired token
- 403: FORBIDDEN - User doesn't own this task
- 404: NOT_FOUND - Task doesn't exist

### PUT /tasks/{id}
**Description**: Update a specific task

**Path Parameters**:
- `id`: Task UUID

**Request**:
```json
{
  "title": "Updated Task Title",
  "description": "Updated description",
  "status": "in_progress",
  "priority": "high",
  "due_date": "2023-12-31T10:00:00Z"
}
```

**Success Response (200)**:
```json
{
  "id": "uuid-string",
  "title": "Updated Task Title",
  "description": "Updated description",
  "status": "in_progress",
  "priority": "high",
  "due_date": "2023-12-31T10:00:00Z",
  "user_id": "user-uuid-string",
  "created_at": "2023-12-01T10:00:00Z",
  "updated_at": "2023-12-02T10:00:00Z"
}
```

**Error Responses**:
- 401: UNAUTHORIZED - Invalid or expired token
- 403: FORBIDDEN - User doesn't own this task
- 404: NOT_FOUND - Task doesn't exist
- 400: VALIDATION_ERROR - Invalid input data

### DELETE /tasks/{id}
**Description**: Delete a specific task

**Path Parameters**:
- `id`: Task UUID

**Success Response (200)**:
```json
{
  "message": "Task deleted successfully"
}
```

**Error Responses**:
- 401: UNAUTHORIZED - Invalid or expired token
- 403: FORBIDDEN - User doesn't own this task
- 404: NOT_FOUND - Task doesn't exist