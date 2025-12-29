# Data Model: MCP Tool Server

## Task Entity Integration
- **Primary Model**: Task (from backend/src/models/task.py)
- **Fields Used**:
  - id: UUID (primary key)
  - title: String (1-200 chars)
  - description: String (optional, 0-1000 chars)
  - status: Enum (pending, in_progress, completed)
  - priority: Enum (low, medium, high)
  - due_date: DateTime (optional)
  - user_id: UUID (foreign key for user isolation)
  - created_at: DateTime
  - updated_at: DateTime
  - reminder_sent: Boolean

## MCP Tool Parameters
- **Common Parameter**: user_id (UUID string) - required for all operations
- **add_task**: user_id (required), title (required), description (optional)
- **list_tasks**: user_id (required), status (optional filter)
- **update_task**: user_id (required), task_id (required), title/description/status/priority/due_date (optional)
- **complete_task**: user_id (required), task_id (required)
- **delete_task**: user_id (required), task_id (required)

## Response Format
- All tools return structured JSON responses
- Error responses include descriptive messages
- Success responses include relevant entity data