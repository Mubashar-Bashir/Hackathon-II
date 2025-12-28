# Data Model: Phase II: Core - Neon DB Schema & Better Auth JWT Integration

## Task Entity

### Fields
- `id`: UUID (Primary Key) - Unique identifier for each task
- `title`: String (1-200 characters) - Task title as specified in requirements
- `description`: String (max 1000 characters, optional) - Task description as specified in requirements
- `status`: String (enum: pending, in_progress, completed) - Current status of the task
- `priority`: String (enum: low, medium, high) - Task priority level
- `due_date`: DateTime (optional) - Deadline for the task
- `user_id`: UUID (Foreign Key) - Links task to the user who created it
- `created_at`: DateTime - Timestamp when task was created
- `updated_at`: DateTime - Timestamp when task was last updated

### Relationships
- One User to Many Tasks (one-to-many relationship)
- Task belongs to one User via user_id foreign key

### Validation Rules
- Title: Required, 1-200 characters
- Description: Optional, max 1000 characters
- Status: Must be one of [pending, in_progress, completed]
- Priority: Must be one of [low, medium, high]
- User association: Task must be associated with valid user_id

## User Entity (via Better Auth)

### Fields
- `id`: UUID (Primary Key) - Unique user identifier from Better Auth
- `email`: String - User's email address for authentication
- `name`: String (optional) - User's display name
- `created_at`: DateTime - When user account was created
- `updated_at`: DateTime - When user account was last updated

### State Transitions
- Unauthenticated → Authenticated (via JWT token validation)
- Valid Token → Active Session (for duration of token validity)
- Invalid Token → Unauthorized (access denied)

## Security Considerations
- All tasks must have a user_id that matches the authenticated user
- Cross-user data access must be prevented
- JWT tokens must be validated before any task operations