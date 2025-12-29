"""
Error Handling Utilities for MCP Tool Failures

Provides utilities for handling errors from MCP tool calls and transforming
them into user-friendly natural language responses.
"""
import logging
from typing import Dict, Any, Optional
from fastapi import HTTPException


logger = logging.getLogger(__name__)


class MCPTaskError(Exception):
    """
    Custom exception for MCP tool failures
    """
    def __init__(self, message: str, tool_name: str, original_error: Optional[Exception] = None):
        self.message = message
        self.tool_name = tool_name
        self.original_error = original_error
        super().__init__(self.message)


def handle_mcp_tool_error(tool_name: str, error: Exception) -> Dict[str, Any]:
    """
    Handle an MCP tool error and return a structured error response

    Args:
        tool_name: Name of the tool that failed
        error: The original error that occurred

    Returns:
        Dictionary containing error information
    """
    logger.error(f"MCP tool {tool_name} failed: {str(error)}", exc_info=True)

    # Create a user-friendly error message based on the tool and error
    error_type = type(error).__name__

    if "authentication" in str(error).lower() or "unauthorized" in str(error).lower():
        user_message = f"I'm sorry, but I couldn't authenticate your request to update your tasks. Please make sure you're logged in correctly."
    elif "permission" in str(error).lower() or "forbidden" in str(error).lower():
        user_message = f"I'm sorry, but you don't have permission to perform this action. You can only manage your own tasks."
    elif "not found" in str(error).lower():
        user_message = f"I couldn't find the task you're looking for. Could you check if the task exists and try again?"
    elif "timeout" in str(error).lower():
        user_message = f"I'm having trouble connecting to the task system right now. Please try your request again in a moment."
    elif "connection" in str(error).lower():
        user_message = f"I'm having trouble connecting to the task system. Please check your connection and try again."
    else:
        user_message = f"Something went wrong while processing your request. I've logged the issue and we'll look into it."

    return {
        "error": True,
        "tool_name": tool_name,
        "error_type": error_type,
        "user_message": user_message,
        "technical_details": str(error)
    }


def transform_error_to_natural_language(error_result: Dict[str, Any]) -> str:
    """
    Transform technical error information to natural language response

    Args:
        error_result: Dictionary containing error information

    Returns:
        Natural language error response
    """
    if not error_result.get("error"):
        return "Operation completed successfully."

    tool_name = error_result.get("tool_name", "operation")
    user_message = error_result.get("user_message", "An error occurred.")

    return user_message


def validate_mcp_tool_response(response: Dict[str, Any], expected_keys: list) -> bool:
    """
    Validate that an MCP tool response contains expected keys

    Args:
        response: The response from an MCP tool
        expected_keys: List of keys that should be present in the response

    Returns:
        True if response is valid, False otherwise
    """
    if not isinstance(response, dict):
        logger.error(f"Invalid response type: {type(response)}")
        return False

    for key in expected_keys:
        if key not in response:
            logger.error(f"Missing expected key '{key}' in MCP tool response: {response}")
            return False

    return True


def safe_execute_mcp_tool(tool_func, *args, **kwargs) -> Dict[str, Any]:
    """
    Safely execute an MCP tool with proper error handling

    Args:
        tool_func: The tool function to execute
        *args: Arguments to pass to the function
        **kwargs: Keyword arguments to pass to the function

    Returns:
        Result from the tool execution with error handling
    """
    try:
        result = tool_func(*args, **kwargs)
        return {
            "success": True,
            "result": result
        }
    except Exception as e:
        logger.error(f"Error in safe_execute_mcp_tool: {str(e)}", exc_info=True)
        return {
            "success": False,
            "error": str(e)
        }


def log_mcp_tool_call(tool_name: str, user_id: str, parameters: Dict[str, Any]):
    """
    Log MCP tool calls for monitoring and debugging

    Args:
        tool_name: Name of the tool being called
        user_id: ID of the user making the call
        parameters: Parameters being passed to the tool
    """
    logger.info(f"MCP tool call: {tool_name} for user {user_id} with parameters: {list(parameters.keys())}")


def log_mcp_tool_result(tool_name: str, user_id: str, success: bool, result: Any):
    """
    Log MCP tool results for monitoring and debugging

    Args:
        tool_name: Name of the tool that was called
        user_id: ID of the user
        success: Whether the tool call was successful
        result: Result of the tool call
    """
    status = "SUCCESS" if success else "FAILURE"
    logger.info(f"MCP tool result: {tool_name} for user {user_id} - {status}")