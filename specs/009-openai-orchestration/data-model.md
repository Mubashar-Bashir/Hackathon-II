# Data Model: OpenAI Agents Orchestration

## Conversation and Message Integration
- **Primary Model**: Conversation and Message (from backend/src/models/conversation.py)
- **Fields Used**:
  - Conversation: id (UUID), user_id (UUID), title (string), created_at (datetime), updated_at (datetime)
  - Message: id (UUID), conversation_id (UUID), user_id (UUID), role (string: "user"/"assistant"), content (string), created_at (datetime)

## OpenAI Agents SDK Integration
- **Agent Configuration**: OpenAI Agents SDK with MCP connector patterns
- **Tool Definitions**: MCP tools registered as external functions via SDK
- **Context Window**: Conversation history managed through DB queries to avoid token limits

## MCP Tool Parameters (as External Functions)
- **add_task**: user_id (required), title (required), description (optional)
- **list_tasks**: user_id (required), status (optional filter)
- **update_task**: user_id (required), task_id (required), title/description/status/priority/due_date (optional)
- **complete_task**: user_id (required), task_id (required)
- **delete_task**: user_id (required), task_id (required)

## Integration Points
- **Authentication**: JWT token extracted from request, user_id passed to all MCP tool calls
- **History Management**: Conversation history fetched from DB before each AI interaction
- **Response Storage**: User messages and AI responses stored in Message table
- **User Isolation**: All operations filtered by user_id to ensure data separation
- **MCP Protocol**: Tools accessed via official MCP connector patterns following OpenAI Agents SDK

## Validation Rules
- All MCP tool calls must include validated user_id
- Conversation access restricted to owning user
- Message content must be non-empty
- Proper error responses stored for failed operations
- MCP tool parameters validated via Pydantic schemas