---
name: mcp-task-server-dev
description: Expert in developing Model Context Protocol (MCP) servers that provide standardized tools for AI agents to perform task operations. Use when implementing MCP task servers with add_task, list_tasks, update_task, complete_task, delete_task tools. Handles user isolation, authentication integration, and proper response formatting for AI orchestration.
---

# MCP Task Server Development

## Overview

The MCP Task Server Development skill provides expertise for creating Model Context Protocol (MCP) servers that expose standardized task operations for AI agents. This includes implementing the 5 core tools: add_task, list_tasks, update_task, complete_task, and delete_task with proper user isolation and security.

## Core Capabilities

### 1. MCP Server Implementation

Builds Python-based MCP servers using the official `mcp` library that implement standardized task operations for AI agents.

**Implementation includes:**
- Proper initialization of MCP server with appropriate name
- Implementation of `list_prompts()` to expose available tools
- Implementation of `get_prompt()` to handle tool execution
- Proper error handling and response formatting
- Integration with existing database models

### 2. Task Tool Implementation

Creates the 5 standardized task tools with proper parameters and validation:

- `add_task`: Create new tasks with user_id, title, and optional description
- `list_tasks`: Retrieve tasks with optional status filtering
- `update_task`: Modify task properties with user_id and task_id validation
- `complete_task`: Mark tasks as completed with proper validation
- `delete_task`: Remove tasks with appropriate user verification

### 3. Security and User Isolation

Implements proper user isolation patterns to ensure data security:

- User_id validation on all operations
- Database query scoping with WHERE clauses filtering by user_id
- Verification that tasks belong to requesting user before operations
- Proper authentication integration with existing systems

## MCP Task Server Template

The MCP server should be implemented as follows:

```python
#!/usr/bin/env python3
"""
Task Tools MCP Server
Provides MCP tools for task CRUD operations
"""

import asyncio
import json
import os
from typing import Any, Dict, List, Optional
from datetime import datetime
import uuid

from mcp.server import Server
from mcp.types import TextContent, Prompt, GetPromptResult, GetPromptRequestParams
from mcp import ServerCapabilities, PromptsCapability
from mcp.server.stdio import stdio_server

from backend.src.core.database import get_session_context
from backend.src.models.task import Task, TaskCreate, TaskUpdate, TaskRead
from sqlmodel import select


# Initialize the MCP server
server = Server("task-tools-mcp")


def add_task(user_id: str, title: str, description: Optional[str] = None) -> Dict[str, Any]:
    """Add a new task for a specific user."""
    with get_session_context() as session:
        user_uuid = uuid.UUID(user_id)

        # Create task using TaskCreate model
        task_create = TaskCreate(
            title=title,
            description=description
        )

        # Create task instance with user_id
        task = Task.model_validate(task_create.model_dump())
        task.user_id = user_uuid

        session.add(task)
        session.commit()
        session.refresh(task)

        return {
            "task_id": str(task.id),
            "status": "created",
            "title": task.title
        }


def list_tasks(user_id: str, status: Optional[str] = None) -> List[Dict[str, Any]]:
    """List all tasks for a specific user, optionally filtered by status."""
    with get_session_context() as session:
        user_uuid = uuid.UUID(user_id)

        # Build query with user_id filter
        query = select(Task).where(Task.user_id == user_uuid)

        # Add status filter if provided
        if status:
            query = query.where(Task.status == status)

        tasks = session.exec(query).all()

        result = []
        for task in tasks:
            result.append({
                "id": str(task.id),
                "title": task.title,
                "status": task.status
            })

        return result


def update_task(user_id: str, task_id: str, title: Optional[str] = None,
                description: Optional[str] = None, status: Optional[str] = None,
                priority: Optional[str] = None, due_date: Optional[str] = None) -> Dict[str, Any]:
    """Update a specific task for a user."""
    with get_session_context() as session:
        user_uuid = uuid.UUID(user_id)
        task_uuid = uuid.UUID(task_id)

        # First verify the task belongs to the user
        query = select(Task).where(Task.id == task_uuid, Task.user_id == user_uuid)
        task = session.exec(query).first()

        if not task:
            raise ValueError(f"Task {task_id} not found for user {user_id}")

        # Update only the fields that are provided
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if status is not None:
            task.status = status
        if priority is not None:
            task.priority = priority
        if due_date is not None:
            task.due_date = datetime.fromisoformat(due_date)

        task.updated_at = datetime.now()

        session.add(task)
        session.commit()
        session.refresh(task)

        return {
            "task_id": str(task.id),
            "status": "updated",
            "title": task.title
        }


def complete_task(user_id: str, task_id: str) -> Dict[str, Any]:
    """Mark a specific task as complete for a user."""
    with get_session_context() as session:
        user_uuid = uuid.UUID(user_id)
        task_uuid = uuid.UUID(task_id)

        # First verify the task belongs to the user
        query = select(Task).where(Task.id == task_uuid, Task.user_id == user_uuid)
        task = session.exec(query).first()

        if not task:
            raise ValueError(f"Task {task_id} not found for user {user_id}")

        # Update status to completed
        task.status = "completed"
        task.updated_at = datetime.now()

        session.add(task)
        session.commit()
        session.refresh(task)

        return {
            "task_id": str(task.id),
            "status": "completed",
            "title": task.title
        }


def delete_task(user_id: str, task_id: str) -> Dict[str, Any]:
    """Delete a specific task for a user."""
    with get_session_context() as session:
        user_uuid = uuid.UUID(user_id)
        task_uuid = uuid.UUID(task_id)

        # First verify the task belongs to the user
        query = select(Task).where(Task.id == task_uuid, Task.user_id == user_uuid)
        task = session.exec(query).first()

        if not task:
            raise ValueError(f"Task {task_id} not found for user {user_id}")

        # Delete the task
        session.delete(task)
        session.commit()

        return {
            "task_id": str(task_uuid),
            "status": "deleted",
            "title": task.title
        }


@server.list_prompts()
async def handle_list_prompts() -> List[Prompt]:
    """List all available task tools as MCP prompts."""
    prompts = [
        Prompt(
            name="add_task",
            title="Add Task",
            description="Add a new task for a user. Requires user_id and title. Description is optional."
        ),
        Prompt(
            name="list_tasks",
            title="List Tasks",
            description="List all tasks for a user, optionally filtered by status. Requires user_id. Status is optional (all/pending/completed/in_progress)."
        ),
        Prompt(
            name="update_task",
            title="Update Task",
            description="Update a specific task for a user. Requires user_id and task_id. Other fields are optional."
        ),
        Prompt(
            name="complete_task",
            title="Complete Task",
            description="Mark a specific task as completed for a user. Requires user_id and task_id."
        ),
        Prompt(
            name="delete_task",
            title="Delete Task",
            description="Delete a specific task for a user. Requires user_id and task_id."
        )
    ]
    return prompts


@server.get_prompt()
async def handle_get_prompt(request: GetPromptRequestParams) -> GetPromptResult:
    """Execute task tools and return results."""
    try:
        # Parse the request arguments
        args = json.loads(request.arguments) if request.arguments else {}

        if request.name == "add_task":
            user_id = args.get("user_id")
            title = args.get("title")
            description = args.get("description")

            if not user_id or not title:
                return GetPromptResult(
                    messages=[TextContent(role="user", content="Error: user_id and title are required")]
                )

            result = add_task(user_id, title, description)
            return GetPromptResult(
                messages=[TextContent(role="user", content=json.dumps(result, indent=2))]
            )

        elif request.name == "list_tasks":
            user_id = args.get("user_id")
            status = args.get("status")  # Optional filter

            if not user_id:
                return GetPromptResult(
                    messages=[TextContent(role="user", content="Error: user_id is required")]
                )

            result = list_tasks(user_id, status)
            return GetPromptResult(
                messages=[TextContent(role="user", content=json.dumps(result, indent=2))]
            )

        elif request.name == "update_task":
            user_id = args.get("user_id")
            task_id = args.get("task_id")
            title = args.get("title")
            description = args.get("description")
            status = args.get("status")
            priority = args.get("priority")
            due_date = args.get("due_date")

            if not user_id or not task_id:
                return GetPromptResult(
                    messages=[TextContent(role="user", content="Error: user_id and task_id are required")]
                )

            result = update_task(user_id, task_id, title, description, status, priority, due_date)
            return GetPromptResult(
                messages=[TextContent(role="user", content=json.dumps(result, indent=2))]
            )

        elif request.name == "complete_task":
            user_id = args.get("user_id")
            task_id = args.get("task_id")

            if not user_id or not task_id:
                return GetPromptResult(
                    messages=[TextContent(role="user", content="Error: user_id and task_id are required")]
                )

            result = complete_task(user_id, task_id)
            return GetPromptResult(
                messages=[TextContent(role="user", content=json.dumps(result, indent=2))]
            )

        elif request.name == "delete_task":
            user_id = args.get("user_id")
            task_id = args.get("task_id")

            if not user_id or not task_id:
                return GetPromptResult(
                    messages=[TextContent(role="user", content="Error: user_id and task_id are required")]
                )

            result = delete_task(user_id, task_id)
            return GetPromptResult(
                messages=[TextContent(role="user", content=json.dumps(result, indent=2))]
            )

        else:
            return GetPromptResult(
                messages=[TextContent(role="user", content=f"Unknown tool: {request.name}")]
            )

    except ValueError as e:
        # Handle validation errors (like task not found for user)
        return GetPromptResult(
            messages=[TextContent(role="user", content=f"Validation error: {str(e)}")]
        )
    except Exception as e:
        return GetPromptResult(
            messages=[TextContent(role="user", content=f"Error executing tool {request.name}: {str(e)}")]
        )


def main():
    """Main entry point for the MCP server."""
    capabilities = ServerCapabilities(
        prompts=PromptsCapability()
    )

    async def run():
        async with stdio_server(server, capabilities) as (read_stream, write_stream):
            await server.run(
                read_stream=read_stream,
                write_stream=write_stream,
                initialization_options=None
            )

    asyncio.run(run)


if __name__ == "__main__":
    main()
```

## Security Best Practices

When implementing MCP task servers, always follow these security practices:

1. **User ID Validation**: Every operation must validate that the user_id matches the task's owner
2. **Database Query Scoping**: Use WHERE clauses that filter by user_id in all database queries
3. **Input Validation**: Validate all parameters using Pydantic models before processing
4. **Error Handling**: Return appropriate error messages without exposing internal details
5. **Stateless Operations**: Each tool call should independently fetch data from the database

## Response Format Requirements

All tools must return responses in the format specified in the requirements:
- `add_task`: {"task_id": id, "status": "created", "title": title}
- `list_tasks`: [{"id": id, "title": title, "status": status}, ...]
- `update_task`: {"task_id": id, "status": "updated", "title": title}
- `complete_task`: {"task_id": id, "status": "completed", "title": title}
- `delete_task`: {"task_id": id, "status": "deleted", "title": title}

## Common Issues and Solutions

### Issue 1: Context Manager Missing Decorator
**Problem**: The `get_session_context()` function was defined as a generator but used as a context manager with `with` statements without the `@contextmanager` decorator.
**Solution**: Add the `@contextmanager` decorator from `contextlib` to the function.
**Error**: `TypeError: 'generator' object does not support the context manager protocol`

### Issue 2: Model Validation Error
**Problem**: The `Task` model requires a `user_id` field, but when using `Task.model_validate(task_create.model_dump())`, the `user_id` was not included in the validation data.
**Solution**: Create the `Task` instance directly with all required fields instead of using model validation from `TaskCreate`.
**Error**: `pydantic_core._pydantic_core.ValidationError: 1 validation error for Task user_id Field required`

### Issue 3: Session Management and Refresh
**Problem**: After adding an object to the session, calling `session.refresh()` before the transaction was committed resulted in an error.
**Solution**: Use `session.flush()` to assign IDs without committing, then use separate sessions for different operations since the context manager commits and closes the session.
**Error**: `sqlalchemy.exc.InvalidRequestError: Instance is not persistent within this Session`

### Issue 4: Database Connection
**Problem**: Tests failed due to missing PostgreSQL database connection.
**Solution**: For testing purposes, use mocking to verify logic without requiring a running database, or ensure the database is properly configured and running.
**Error**: `psycopg2.OperationalError: connection to server at "localhost" failed: Connection refused`

### Issue 5: Duplicate Import Statement
**Problem**: The `contextlib` import was duplicated in the file.
**Solution**: Remove the duplicate import and ensure imports are at the top of the file.

## Best Practices

1. **Always use `@contextmanager` decorator** when creating generator functions intended for `with` statements.
2. **Understand model relationships** - `TaskCreate` vs `Task` models have different required fields.
3. **Proper session management** - Use `flush()` for ID assignment, separate sessions for different operations when using context managers.
4. **Database setup** - Ensure the database is running before executing database-dependent tests.
5. **Model validation** - Be aware of which fields are required vs optional in different model classes.
6. **Error handling** - Always consider database connection failures and implement proper error handling.

## Usage

1. Create the MCP server implementation file (e.g., `mcp/task_tools_server.py`)
2. Implement all 5 required tools with proper user isolation
3. Test the server with sample tool calls
4. Integrate with the existing backend infrastructure
5. Ensure proper authentication and authorization