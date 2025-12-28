from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone
import uuid


class TaskBase(SQLModel):
    """Base model for Task with common fields"""
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    status: str = Field(default="pending", regex="^(pending|in_progress|completed)$", index=True)
    priority: str = Field(default="medium", regex="^(low|medium|high)$")
    due_date: Optional[datetime] = Field(default=None, index=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", index=True)


class Task(TaskBase, table=True):
    """Task model for database storage"""
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), index=True)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), index=True)


class TaskRead(TaskBase):
    """Task model for API responses"""
    id: uuid.UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class TaskCreate(SQLModel):
    """Task model for creation requests - does not include user_id (set by backend)"""
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    status: Optional[str] = Field(default="pending", regex="^(pending|in_progress|completed)$")
    priority: Optional[str] = Field(default="medium", regex="^(low|medium|high)$")
    due_date: Optional[datetime] = Field(default=None)


class TaskUpdate(SQLModel):
    """Task model for update requests"""
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    status: Optional[str] = Field(default=None, regex="^(pending|in_progress|completed)$")
    priority: Optional[str] = Field(default=None, regex="^(low|medium|high)$")
    due_date: Optional[datetime] = Field(default=None)