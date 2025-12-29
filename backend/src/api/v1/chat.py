"""
Chat API Endpoint for OpenAI Agents

Implements the chat endpoint that connects user natural language input to
OpenAI agents and MCP tools for task management operations.
"""
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, Any, Optional
from uuid import UUID
import logging

from ...core.security import authenticate_user_from_token
from ...core.database import get_session_dep
from ...models.conversation import Message
from ...agents.task_agent import TaskAgent
from ...agents.conversation_manager import ConversationManager
from ...agents.tool_mapper import ToolMapper
from ...services.mcp_client import MCPClient
from ...core.error_handling import transform_error_to_natural_language


logger = logging.getLogger(__name__)
router = APIRouter()


class ChatRequest(BaseModel):
    """
    Request model for chat endpoint
    """
    message: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    """
    Response model for chat endpoint
    """
    message: str
    conversation_id: str
    tool_execution: Optional[Dict[str, Any]] = None


@router.post("/api/{user_id}/chat", response_model=ChatResponse)
async def chat_endpoint(
    user_id: str,
    request: ChatRequest,
    token_data = Depends(authenticate_user_from_token),
    db_session = Depends(get_session_dep)
):
    """
    Chat endpoint for OpenAI agents to process natural language task operations

    Args:
        user_id: The ID of the user making the request
        request: The chat request containing the message
        token_data: Authenticated user data from JWT token
        db_session: Database session for database operations

    Returns:
        ChatResponse containing the AI response and conversation context
    """
    # Verify that the user_id in the URL matches the authenticated user
    if token_data.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="Access denied: User ID mismatch"
        )

    try:
        # Convert user_id to UUID for database operations
        from uuid import UUID
        user_uuid = UUID(user_id)

        # Initialize components
        task_agent = TaskAgent()
        conversation_manager = ConversationManager(db_session)
        mcp_client = MCPClient()
        tool_mapper = ToolMapper(mcp_client)

        # Get or create conversation
        if request.conversation_id:
            conversation_id = UUID(request.conversation_id)
        else:
            # Create a new conversation
            conversation = conversation_manager.create_conversation(user_uuid)
            conversation_id = conversation.id

        # Get conversation history
        conversation_history = conversation_manager.get_conversation_history(
            conversation_id,
            user_uuid
        )

        # Process the user message with the task agent
        result = task_agent.process_user_message(
            user_id=user_id,
            message=request.message,
            conversation_history=conversation_history
        )

        # Store the user's message in the conversation history
        conversation_manager.store_user_message(
            conversation_id=conversation_id,
            user_id=user_uuid,
            content=request.message
        )

        # Handle the result from the task agent
        if result["type"] == "function_call":
            # Execute the MCP tool
            tool_result = await tool_mapper.execute_tool(
                tool_name=result["name"],
                arguments=result["arguments"]
            )

            # Generate a response based on the tool execution
            if tool_result["error"]:
                # Transform technical error to natural language
                ai_response = transform_error_to_natural_language(tool_result.get("error_result", {}))
            else:
                # Success case - provide natural language confirmation
                tool_name = result["name"].replace("_", " ").title()
                ai_response = f"I've successfully {result['name'].replace('_', ' ')} for you."

            # Store the AI's response in the conversation history
            conversation_manager.store_assistant_message(
                conversation_id=conversation_id,
                user_id=user_uuid,
                content=ai_response
            )

            # Return the response with tool execution info
            return ChatResponse(
                message=ai_response,
                conversation_id=str(conversation_id),
                tool_execution={
                    "name": result["name"],
                    "arguments": result["arguments"],
                    "result": tool_result
                }
            )

        elif result["type"] == "message":
            # Just return the AI's message
            ai_response = result["content"]

            # Store the AI's response in the conversation history
            conversation_manager.store_assistant_message(
                conversation_id=conversation_id,
                user_id=user_uuid,
                content=ai_response
            )

            return ChatResponse(
                message=ai_response,
                conversation_id=str(conversation_id)
            )

        elif result["type"] == "error":
            # Return the error message
            ai_response = result["content"]

            # Store the AI's response in the conversation history
            conversation_manager.store_assistant_message(
                conversation_id=conversation_id,
                user_id=user_uuid,
                content=ai_response
            )

            return ChatResponse(
                message=ai_response,
                conversation_id=str(conversation_id)
            )

        else:
            # Unknown result type
            error_msg = "Unknown response type from task agent"
            logger.error(error_msg)

            # Store the error message in the conversation history
            conversation_manager.store_assistant_message(
                conversation_id=conversation_id,
                user_id=user_uuid,
                content=error_msg
            )

            return ChatResponse(
                message=error_msg,
                conversation_id=str(conversation_id)
            )

    except ValueError as ve:
        logger.error(f"ValueError in chat endpoint: {str(ve)}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")