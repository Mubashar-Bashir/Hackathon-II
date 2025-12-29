#!/usr/bin/env python3
"""
Script to create an MCP server for task operations
"""

import os
import sys
from pathlib import Path


def create_mcp_server(output_path: str):
    """Create a new MCP server implementation for task operations."""

    mcp_server_content = '''#!/usr/bin/env python3
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
'''

    # Write the file
    with open(output_path, 'w') as f:
        f.write(mcp_server_content)

    print(f"MCP server created at: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python create-mcp-server.py <output_path>")
        sys.exit(1)

    output_path = sys.argv[1]
    create_mcp_server(output_path)