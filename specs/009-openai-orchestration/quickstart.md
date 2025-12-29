# Quickstart: OpenAI Agents Orchestration

## Prerequisites
- Python 3.13+
- OpenAI API key
- Running PostgreSQL database (Neon DB)
- MCP tools from Layer 2 (mcp/task_tools_server.py)
- OpenAI Agents SDK installed
- JWT authentication configured

## Environment Setup
1. Set OpenAI API key: `export OPENAI_API_KEY="your-api-key"`
2. Ensure database connection is configured in backend/.env
3. Install OpenAI Agents SDK: `uv pip install openai-agents`
4. Verify MCP server is running and accessible

## Running the Service
1. Navigate to backend directory: `cd backend`
2. Install dependencies: `uv pip install openai openai-agents`
3. Start the FastAPI server: `uvicorn main:app --reload`
4. The chat endpoint will be available at `/api/{user_id}/chat`

## API Usage
- Send POST request to `/api/{user_id}/chat` with JSON body containing `message`
- The OpenAI agent will process natural language and call appropriate MCP tools via Agents SDK
- Responses include AI message and conversation context

## Testing
- Use curl or Postman to send requests to the chat endpoint
- Verify user isolation by testing with different user IDs
- Test all MCP tool operations through natural language

## Integration with MCP Tools
- The OpenAI agent is configured to call add_task, list_tasks, update_task, complete_task, and delete_task via the OpenAI Agents SDK
- MCP tools are registered as external functions following official patterns
- All tool calls include user_id for proper isolation
- Tool responses are formatted for natural language output