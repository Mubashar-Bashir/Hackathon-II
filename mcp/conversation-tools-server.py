#!/usr/bin/env python3
"""
Conversation Tools MCP Server
Provides MCP tools for conversation and message operations
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
from backend.src.models.conversation import Conversation, Message, ConversationCreate, MessageCreate

# Initialize the MCP server
server = Server("conversation-tools-mcp")

def get_user_conversations(user_id: str) -> List[Dict[str, Any]]:
    """Get all conversations for a specific user."""
    with get_session_context() as session:
        user_uuid = uuid.UUID(user_id)
        conversations = session.query(Conversation).filter(Conversation.user_id == user_uuid).all()

        result = []
        for conv in conversations:
            result.append({
                "id": str(conv.id),
                "title": conv.title,
                "user_id": str(conv.user_id),
                "created_at": conv.created_at.isoformat() if conv.created_at else None,
                "updated_at": conv.updated_at.isoformat() if conv.updated_at else None,
                "message_count": len(conv.messages)
            })
        return result

def get_conversation_messages(conversation_id: str) -> List[Dict[str, Any]]:
    """Get all messages for a specific conversation."""
    with get_session_context() as session:
        conv_uuid = uuid.UUID(conversation_id)
        messages = session.query(Message).filter(Message.conversation_id == conv_uuid).order_by(Message.created_at).all()

        result = []
        for msg in messages:
            result.append({
                "id": str(msg.id),
                "role": msg.role,
                "content": msg.content,
                "conversation_id": str(msg.conversation_id),
                "user_id": str(msg.user_id),
                "created_at": msg.created_at.isoformat() if msg.created_at else None,
                "updated_at": msg.updated_at.isoformat() if msg.updated_at else None
            })
        return result

def create_conversation(user_id: str, title: Optional[str] = None) -> Dict[str, Any]:
    """Create a new conversation for a user."""
    with get_session_context() as session:
        conv_create = ConversationCreate(user_id=uuid.UUID(user_id), title=title)
        conversation = Conversation.model_validate(conv_create.model_dump())
        session.add(conversation)
        session.commit()
        session.refresh(conversation)

        return {
            "id": str(conversation.id),
            "title": conversation.title,
            "user_id": str(conversation.user_id),
            "created_at": conversation.created_at.isoformat() if conversation.created_at else None,
            "updated_at": conversation.updated_at.isoformat() if conversation.updated_at else None
        }

def add_message_to_conversation(conversation_id: str, user_id: str, role: str, content: str) -> Dict[str, Any]:
    """Add a message to a conversation."""
    with get_session_context() as session:
        msg_create = MessageCreate(
            role=role,
            content=content,
            conversation_id=uuid.UUID(conversation_id),
            user_id=uuid.UUID(user_id)
        )
        message = Message.model_validate(msg_create.model_dump())
        session.add(message)
        session.commit()
        session.refresh(message)

        return {
            "id": str(message.id),
            "role": message.role,
            "content": message.content,
            "conversation_id": str(message.conversation_id),
            "user_id": str(message.user_id),
            "created_at": message.created_at.isoformat() if message.created_at else None,
            "updated_at": message.updated_at.isoformat() if message.updated_at else None
        }

@server.list_prompts()
async def handle_list_prompts() -> List[Prompt]:
    """List all available conversation tools as MCP prompts."""
    prompts = [
        Prompt(
            name="get_user_conversations",
            title="Get User Conversations",
            description="Retrieve all conversations for a specific user"
        ),
        Prompt(
            name="get_conversation_messages",
            title="Get Conversation Messages",
            description="Retrieve all messages for a specific conversation"
        ),
        Prompt(
            name="create_conversation",
            title="Create Conversation",
            description="Create a new conversation for a user"
        ),
        Prompt(
            name="add_message_to_conversation",
            title="Add Message to Conversation",
            description="Add a message to an existing conversation"
        )
    ]
    return prompts

@server.get_prompt()
async def handle_get_prompt(request: GetPromptRequestParams) -> GetPromptResult:
    """Execute conversation tools and return results."""
    try:
        # Parse the request arguments
        args = json.loads(request.arguments) if request.arguments else {}

        if request.name == "get_user_conversations":
            user_id = args.get("user_id")
            if not user_id:
                return GetPromptResult(
                    messages=[TextContent(role="user", content="Error: user_id is required")]
                )
            result = get_user_conversations(user_id)
            return GetPromptResult(
                messages=[TextContent(role="user", content=json.dumps(result, indent=2))]
            )

        elif request.name == "get_conversation_messages":
            conversation_id = args.get("conversation_id")
            if not conversation_id:
                return GetPromptResult(
                    messages=[TextContent(role="user", content="Error: conversation_id is required")]
                )
            result = get_conversation_messages(conversation_id)
            return GetPromptResult(
                messages=[TextContent(role="user", content=json.dumps(result, indent=2))]
            )

        elif request.name == "create_conversation":
            user_id = args.get("user_id")
            title = args.get("title")
            if not user_id:
                return GetPromptResult(
                    messages=[TextContent(role="user", content="Error: user_id is required")]
                )
            result = create_conversation(user_id, title)
            return GetPromptResult(
                messages=[TextContent(role="user", content=json.dumps(result, indent=2))]
            )

        elif request.name == "add_message_to_conversation":
            conversation_id = args.get("conversation_id")
            user_id = args.get("user_id")
            role = args.get("role")
            content = args.get("content")

            if not all([conversation_id, user_id, role, content]):
                return GetPromptResult(
                    messages=[TextContent(role="user", content="Error: conversation_id, user_id, role, and content are required")]
                )

            if role not in ["user", "assistant"]:
                return GetPromptResult(
                    messages=[TextContent(role="user", content="Error: role must be either 'user' or 'assistant'")]
                )

            result = add_message_to_conversation(conversation_id, user_id, role, content)
            return GetPromptResult(
                messages=[TextContent(role="user", content=json.dumps(result, indent=2))]
            )

        else:
            return GetPromptResult(
                messages=[TextContent(role="user", content=f"Unknown tool: {request.name}")]
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