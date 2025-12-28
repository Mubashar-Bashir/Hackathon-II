# API Documentation: Todo App with Authentication and Task Management

## Base URL
`http://localhost:8000` (for development)

## Authentication
All endpoints except `/auth/register`, `/auth/login`, and `/health` require JWT authentication.
Include the token in the Authorization header: `Authorization: Bearer <token>`

## Endpoints

### Authentication

#### POST /auth/register
Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "name": "User Name",
  "password": "securepassword"
}
```

**Response:**
```json
{
  "user_id": "uuid-string",
  "email": "user@example.com",
  "message": "User registered successfully"
}
```

#### POST /auth/login
Authenticate user and return JWT token.

**Form Data:**
- username: email address
- password: password

**Response:**
```json
{
  "access_token": "jwt-token-string",
  "token_type": "bearer",
  "expires_in": 86400
}
```

#### GET /auth/me
Get authenticated user information.

**Response:**
```json
{
  "id": "uuid-string",
  "email": "user@example.com",
  "name": "User Name",
  "created_at": "2025-12-28T00:00:00.000000+00:00",
  "updated_at": "2025-12-28T00:00:00.000000+00:00"
}
```

### Tasks

#### GET /tasks/
Get all tasks for the authenticated user with optional filtering.

**Query Parameters:**
- offset (optional, default: 0)
- limit (optional, default: 20, max: 100)
- status_filter (optional, one of: pending, in_progress, completed)

**Response:**
```json
{
  "tasks": [...],
  "total": 10,
  "offset": 0,
  "limit": 20
}
```

#### POST /tasks/
Create a new task for the authenticated user.

**Request Body:**
```json
{
  "title": "Task Title",
  "description": "Task description (optional)",
  "status": "pending", // optional, default: pending
  "priority": "medium", // optional, one of: low, medium, high
  "due_date": "2025-12-31T23:59:59.000Z" // optional
}
```

**Response:**
```json
{
  "id": "uuid-string",
  "title": "Task Title",
  "description": "Task description",
  "status": "pending",
  "priority": "medium",
  "due_date": "2025-12-31T23:59:59.000Z",
  "user_id": "uuid-string",
  "created_at": "2025-12-28T00:00:00.000000+00:00",
  "updated_at": "2025-12-28T00:00:00.000000+00:00"
}
```

#### GET /tasks/{task_id}
Get a specific task by ID for the authenticated user.

**Response:**
```json
{
  "id": "uuid-string",
  "title": "Task Title",
  "description": "Task description",
  "status": "pending",
  "priority": "medium",
  "due_date": "2025-12-31T23:59:59.000Z",
  "user_id": "uuid-string",
  "created_at": "2025-12-28T00:00:00.000000+00:00",
  "updated_at": "2025-12-28T00:00:00.000000+00:00"
}
```

#### PUT /tasks/{task_id}
Update a specific task for the authenticated user.

**Request Body:**
```json
{
  "title": "Updated Title",
  "description": "Updated description",
  "status": "in_progress",
  "priority": "high",
  "due_date": "2025-12-31T23:59:59.000Z"
}
```

**Response:**
```json
{
  "id": "uuid-string",
  "title": "Updated Title",
  "description": "Updated description",
  "status": "in_progress",
  "priority": "high",
  "due_date": "2025-12-31T23:59:59.000Z",
  "user_id": "uuid-string",
  "created_at": "2025-12-28T00:00:00.000000+00:00",
  "updated_at": "2025-12-28T00:00:00.000000+00:00"
}
```

#### DELETE /tasks/{task_id}
Delete a specific task for the authenticated user.

**Response:**
```json
{
  "message": "Task deleted successfully"
}
```

#### PATCH /tasks/{task_id}
Toggle the completion status of a task for the authenticated user.

**Response:**
```json
{
  "id": "uuid-string",
  "title": "Task Title",
  "description": "Task description",
  "status": "completed", // or "in_progress" depending on previous state
  "priority": "medium",
  "due_date": "2025-12-31T23:59:59.000Z",
  "user_id": "uuid-string",
  "created_at": "2025-12-28T00:00:00.000000+00:00",
  "updated_at": "2025-12-28T00:00:00.000000+00:00"
}
```

### Health Check

#### GET /health
Check the health status of the API.

**Response:**
```json
{
  "status": "healthy",
  "version": "0.1.0"
}
```

## Error Responses

All error responses follow this format:
```json
{
  "detail": "Error message"
}
```

Common HTTP status codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 409: Conflict
- 500: Internal Server Error