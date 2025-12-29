from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime, timezone
import uuid
from pydantic import field_validator
from .user import User


class ConversationBase(SQLModel):
    """Base model for Conversation with common fields"""
    title: Optional[str] = Field(default=None, max_length=200)
    user_id: uuid.UUID = Field(foreign_key="user.id", index=True)


class Conversation(ConversationBase, table=True):
    """Conversation model for database storage"""
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), index=True)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), index=True)

    # Relationship to messages
    messages: List["Message"] = Relationship(back_populates="conversation", cascade_delete=True)


class ConversationRead(ConversationBase):
    """Conversation model for API responses"""
    id: uuid.UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    message_count: int = 0  # Computed field


class ConversationCreate(SQLModel):
    """Conversation model for creation requests"""
    title: Optional[str] = Field(default=None, max_length=200)
    user_id: uuid.UUID  # Will be set by backend from JWT token


class MessageBase(SQLModel):
    """Base model for Message with common fields"""
    role: str = Field(index=True)  # user or assistant
    content: str = Field(min_length=1, max_length=5000)
    conversation_id: uuid.UUID = Field(foreign_key="conversation.id", index=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", index=True)  # Added for security

    @field_validator('role')
    @classmethod
    def validate_role(cls, v):
        if v not in ['user', 'assistant']:
            raise ValueError(f'Role must be "user" or "assistant", got: {v}')
        return v

    @field_validator('content')
    @classmethod
    def validate_content_length(cls, v):
        if len(v) < 1:
            raise ValueError('Content must be at least 1 character long')
        if len(v) > 5000:
            raise ValueError('Content must be no more than 5000 characters long')
        return v


class Message(MessageBase, table=True):
    """Message model for database storage"""
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), index=True)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), index=True)

    # Relationship to conversation
    conversation: Optional[Conversation] = Relationship(back_populates="messages")


class MessageRead(MessageBase):
    """Message model for API responses"""
    id: uuid.UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class MessageCreate(SQLModel):
    """Message model for creation requests"""
    role: str = Field(regex="^(user|assistant)$")
    content: str = Field(min_length=1, max_length=5000)
    conversation_id: uuid.UUID
    user_id: uuid.UUID  # Will be set by backend from JWT token