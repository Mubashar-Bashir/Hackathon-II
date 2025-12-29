"""
Conversation Manager for OpenAI Agents

Handles conversation history retrieval and storage using the database models.
"""
from typing import List, Dict, Any
from datetime import datetime
from ..models.conversation import Conversation, Message
from sqlmodel import Session, select, func
from uuid import UUID


class ConversationManager:
    """
    Manages conversation history in the database
    """

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_conversation_history(self, conversation_id: UUID, user_id: UUID, limit: int = 50) -> List[Dict[str, str]]:
        """
        Retrieve conversation history for a specific conversation and user

        Args:
            conversation_id: The ID of the conversation
            user_id: The ID of the user (for security)
            limit: Maximum number of messages to retrieve

        Returns:
            List of message dictionaries with role and content
        """
        # Ensure user can only access their own conversation history
        statement = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .where(Message.user_id == user_id)
            .order_by(Message.created_at.desc())
            .limit(limit)
        )

        results = self.db_session.exec(statement).all()

        # Convert to the format expected by the OpenAI API
        history = []
        for message in reversed(results):  # Reverse to get chronological order
            history.append({
                "role": message.role,
                "content": message.content
            })

        return history

    def store_user_message(self, conversation_id: UUID, user_id: UUID, content: str) -> Message:
        """
        Store a user message in the conversation history

        Args:
            conversation_id: The ID of the conversation
            user_id: The ID of the user
            content: The message content

        Returns:
            The created Message object
        """
        message = Message(
            conversation_id=conversation_id,
            user_id=user_id,
            role="user",
            content=content
        )

        self.db_session.add(message)
        self.db_session.commit()
        self.db_session.refresh(message)

        return message

    def store_assistant_message(self, conversation_id: UUID, user_id: UUID, content: str) -> Message:
        """
        Store an assistant message in the conversation history

        Args:
            conversation_id: The ID of the conversation
            user_id: The ID of the user
            content: The message content

        Returns:
            The created Message object
        """
        message = Message(
            conversation_id=conversation_id,
            user_id=user_id,
            role="assistant",
            content=content
        )

        self.db_session.add(message)
        self.db_session.commit()
        self.db_session.refresh(message)

        return message

    def create_conversation(self, user_id: UUID, title: str = "") -> Conversation:
        """
        Create a new conversation for a user

        Args:
            user_id: The ID of the user
            title: Optional title for the conversation

        Returns:
            The created Conversation object
        """
        if not title:
            title = f"Conversation {datetime.now().strftime('%Y-%m-%d %H:%M')}"

        conversation = Conversation(
            user_id=user_id,
            title=title
        )

        self.db_session.add(conversation)
        self.db_session.commit()
        self.db_session.refresh(conversation)

        return conversation