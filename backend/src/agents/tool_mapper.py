"""
MCP Tool Mapper for OpenAI Agents

Maps OpenAI function calls to MCP tools for task management operations.
"""
import logging
from typing import Dict, Any, Callable
from ..services.mcp_client import MCPClient  # This will be implemented later
from ..core.error_handling import handle_mcp_tool_error, log_mcp_tool_call, log_mcp_tool_result


logger = logging.getLogger(__name__)


class ToolMapper:
    """
    Maps OpenAI function calls to MCP tools
    """

    def __init__(self, mcp_client: 'MCPClient'):
        self.mcp_client = mcp_client
        self.tools = {
            "add_task": self._add_task,
            "list_tasks": self._list_tasks,
            "update_task": self._update_task,
            "complete_task": self._complete_task,
            "delete_task": self._delete_task
        }

    async def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute an MCP tool based on OpenAI function call

        Args:
            tool_name: The name of the tool to execute
            arguments: Arguments for the tool

        Returns:
            Result of the tool execution
        """
        if tool_name not in self.tools:
            logger.error(f"Unknown tool: {tool_name}")
            return {
                "error": True,
                "error_message": f"Unknown tool: {tool_name}",
                "result": None
            }

        # Log the tool call
        user_id = arguments.get("user_id", "unknown")
        log_mcp_tool_call(tool_name, user_id, arguments)

        try:
            # Execute the appropriate tool function
            result = await self.tools[tool_name](arguments)

            # Log successful result
            log_mcp_tool_result(tool_name, user_id, True, result)

            return {
                "error": False,
                "result": result
            }
        except Exception as e:
            # Handle the error and log it
            error_result = handle_mcp_tool_error(tool_name, e)
            log_mcp_tool_result(tool_name, user_id, False, str(e))

            return {
                "error": True,
                "error_result": error_result,
                "result": None
            }

    async def _add_task(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute add_task MCP tool
        """
        user_id = args.get("user_id")
        title = args.get("title")
        description = args.get("description", "")

        # Validate required parameters
        if not user_id:
            raise ValueError("user_id is required for add_task")
        if not title:
            raise ValueError("title is required for add_task")

        # Call the MCP tool to add the task
        result = await self.mcp_client.add_task(user_id, title, description)
        return result

    async def _list_tasks(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute list_tasks MCP tool
        """
        user_id = args.get("user_id")

        # Validate required parameters
        if not user_id:
            raise ValueError("user_id is required for list_tasks")

        status = args.get("status")

        # Call the MCP tool to list tasks
        result = await self.mcp_client.list_tasks(user_id, status)
        return result

    async def _update_task(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute update_task MCP tool
        """
        user_id = args.get("user_id")
        task_id = args.get("task_id")

        # Validate required parameters
        if not user_id:
            raise ValueError("user_id is required for update_task")
        if not task_id:
            raise ValueError("task_id is required for update_task")

        title = args.get("title")
        description = args.get("description")
        status = args.get("status")

        # Prepare update data
        update_data = {}
        if title is not None:
            update_data["title"] = title
        if description is not None:
            update_data["description"] = description
        if status is not None:
            update_data["status"] = status

        # Call the MCP tool to update the task
        result = await self.mcp_client.update_task(user_id, task_id, update_data)
        return result

    async def _complete_task(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute complete_task MCP tool
        """
        user_id = args.get("user_id")
        task_id = args.get("task_id")

        # Validate required parameters
        if not user_id:
            raise ValueError("user_id is required for complete_task")
        if not task_id:
            raise ValueError("task_id is required for complete_task")

        # Call the MCP tool to complete the task
        result = await self.mcp_client.complete_task(user_id, task_id)
        return result

    async def _delete_task(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute delete_task MCP tool
        """
        user_id = args.get("user_id")
        task_id = args.get("task_id")

        # Validate required parameters
        if not user_id:
            raise ValueError("user_id is required for delete_task")
        if not task_id:
            raise ValueError("task_id is required for delete_task")

        # Call the MCP tool to delete the task
        result = await self.mcp_client.delete_task(user_id, task_id)
        return result