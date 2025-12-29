"""
OpenAI Agent Orchestrator for Task Management

This module implements the main orchestrator for OpenAI agents that handles
natural language processing and MCP tool execution for task management operations.
"""
import os
import logging
from typing import Dict, Any, List, Optional
from openai import OpenAI
from pydantic import BaseModel, Field
from ..core.openai_config import get_openai_client


logger = logging.getLogger(__name__)


class TaskAgent:
    """
    Main orchestrator for OpenAI agent that manages task operations
    """

    def __init__(self):
        self.client = get_openai_client()
        self.model = os.getenv("OPENAI_MODEL", "gpt-4-turbo")

    def process_user_message(
        self,
        user_id: str,
        message: str,
        conversation_history: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """
        Process a user message and return an AI response

        Args:
            user_id: The ID of the user
            message: The user's message
            conversation_history: Previous conversation history

        Returns:
            Dictionary containing the AI response and any tool execution results
        """
        # Prepare the messages for the OpenAI API
        formatted_history = []
        for msg in conversation_history:
            formatted_history.append({
                "role": msg["role"],
                "content": msg["content"]
            })

        # Add the current user message
        formatted_history.append({
            "role": "user",
            "content": message
        })

        # Define available functions (MCP tools)
        functions = [
            {
                "name": "add_task",
                "description": "Add a new task for the user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The user ID"},
                        "title": {"type": "string", "description": "The task title"},
                        "description": {"type": "string", "description": "The task description"}
                    },
                    "required": ["user_id", "title"]
                }
            },
            {
                "name": "list_tasks",
                "description": "List tasks for the user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The user ID"},
                        "status": {"type": "string", "description": "Filter by task status"}
                    },
                    "required": ["user_id"]
                }
            },
            {
                "name": "update_task",
                "description": "Update an existing task",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The user ID"},
                        "task_id": {"type": "string", "description": "The task ID"},
                        "title": {"type": "string", "description": "The new task title"},
                        "description": {"type": "string", "description": "The new task description"},
                        "status": {"type": "string", "description": "The new task status"}
                    },
                    "required": ["user_id", "task_id"]
                }
            },
            {
                "name": "complete_task",
                "description": "Mark a task as complete",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The user ID"},
                        "task_id": {"type": "string", "description": "The task ID"}
                    },
                    "required": ["user_id", "task_id"]
                }
            },
            {
                "name": "delete_task",
                "description": "Delete a task",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The user ID"},
                        "task_id": {"type": "string", "description": "The task ID"}
                    },
                    "required": ["user_id", "task_id"]
                }
            }
        ]

        try:
            # Call the OpenAI API with function calling
            response = self.client.chat.completions.create(
                model=self.model,
                messages=formatted_history,
                functions=functions,
                function_call="auto",  # Let the model decide when to call functions
                temperature=0.7
            )

            # Process the response
            response_message = response.choices[0].message

            # If the model wants to call a function
            if response_message.function_call:
                function_name = response_message.function_call.name
                function_args = response_message.function_call.arguments

                # Execute the function with user_id included
                import json
                args_dict = json.loads(function_args)

                # Ensure user_id is passed to all function calls
                args_dict["user_id"] = user_id

                # Return the function call to be handled by the MCP tools
                return {
                    "type": "function_call",
                    "name": function_name,
                    "arguments": args_dict,
                    "message": response_message.content or ""
                }
            else:
                # Return the assistant's message
                return {
                    "type": "message",
                    "content": response_message.content or ""
                }

        except Exception as e:
            logger.error(f"Error processing user message: {str(e)}")
            return {
                "type": "error",
                "content": "I encountered an error processing your request. Please try again."
            }