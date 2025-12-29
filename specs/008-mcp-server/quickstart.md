# Quickstart: MCP Tool Server

## Prerequisites
- Python 3.13+
- MCP SDK installed
- Database with Task model available
- Running backend services

## Installation
1. Ensure MCP SDK is installed in the environment
2. Verify database connectivity
3. Confirm Task model is available

## Running the Server
1. Navigate to the project root
2. Run the MCP server: `python -m mcp.task_tools_server`
3. The server will be available for AI agent connections

## Available Tools
- `add_task`: Create new tasks for users
- `list_tasks`: Retrieve user's tasks with optional filtering
- `update_task`: Modify existing task properties
- `complete_task`: Mark tasks as completed
- `delete_task`: Remove tasks from user's list

## Testing
- Verify each tool responds appropriately with valid parameters
- Test user isolation by using different user IDs
- Confirm error handling with invalid parameters