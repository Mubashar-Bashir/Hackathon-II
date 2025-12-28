# Data Model: Todo App with Authentication and Task Management

## Entity: User
**Description**: Represents a registered user account in the system

### Fields:
- **id**: UUID (Primary Key) - Unique identifier for the user
- **email**: String (Unique, 255 chars) - User's email address for login
- **name**: String (Optional, 255 chars) - User's display name
- **password_hash**: String (255 chars) - Bcrypt-hashed password
- **created_at**: DateTime (Auto-generated) - Account creation timestamp
- **updated_at**: DateTime (Auto-generated) - Last update timestamp

### Relationships:
- **tasks**: One-to-Many (User has many Tasks)

### Validation Rules:
- Email must be valid email format
- Email must be unique across all users
- Name is optional but limited to 255 characters if provided
- Password must be hashed using bcrypt before storage

## Entity: Task
**Description**: Represents a todo item created by a user

### Fields:
- **id**: UUID (Primary Key) - Unique identifier for the task
- **title**: String (Required, 1-200 chars) - Task title/description
- **description**: Text (Optional, max 1000 chars) - Detailed task description
- **status**: String (Enum: "pending", "in_progress", "completed") - Current task status
- **priority**: String (Enum: "low", "medium", "high") - Task priority level
- **due_date**: DateTime (Optional) - Deadline for task completion
- **user_id**: UUID (Foreign Key) - References the owning user
- **created_at**: DateTime (Auto-generated) - Task creation timestamp
- **updated_at**: DateTime (Auto-generated) - Last update timestamp

### Relationships:
- **user**: Many-to-One (Task belongs to one User)

### Validation Rules:
- Title is required and must be between 1-200 characters
- Description is optional but limited to 1000 characters
- Status must be one of: "pending", "in_progress", "completed"
- Priority must be one of: "low", "medium", "high"
- Due date is optional but if provided must be a valid future/past date
- User_id must reference an existing user in the system

## State Transitions

### Task Status Transitions:
- **pending** → **in_progress**: When user starts working on task
- **in_progress** → **completed**: When user finishes task
- **completed** → **in_progress**: When user needs to reopen task
- **in_progress** → **pending**: When user decides to postpone task

### Validation on Transitions:
- Only the task owner can change the status
- Status transitions must follow the defined paths above

## Indexes

### Required Database Indexes:
- **users.email**: Unique index for fast user lookup by email
- **tasks.user_id**: Index for efficient user-specific task queries
- **tasks.status**: Index for filtering tasks by status
- **tasks.due_date**: Index for sorting and filtering by deadline
- **tasks.created_at**: Index for chronological task ordering

## API Contract Mapping

### User Entity → Authentication Endpoints:
- **POST /auth/register**: Creates User entity from email, name, password
- **POST /auth/login**: Validates User credentials and returns JWT
- **GET /auth/me**: Returns authenticated User details

### Task Entity → Task Management Endpoints:
- **GET /api/{user_id}/tasks**: Queries Tasks filtered by user_id
- **POST /api/{user_id}/tasks**: Creates Task with specified user_id
- **GET /api/{user_id}/tasks/{id}**: Gets Task by id with user_id validation
- **PUT /api/{user_id}/tasks/{id}**: Updates Task with user_id validation
- **DELETE /api/{user_id}/tasks/{id}**: Deletes Task with user_id validation
- **PATCH /api/{user_id}/tasks/{id}/complete**: Toggles Task status with user validation