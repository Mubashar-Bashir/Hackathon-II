"""
Task data models for the Todo CLI application.

This module defines the Pydantic models used throughout the application
for data validation and serialization.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import Optional


class TaskStatus(str, Enum):
    """
    Enum representing the possible statuses of a task.

    Attributes:
        PENDING: Task is pending completion
        COMPLETE: Task has been completed
    """
    PENDING = "pending"
    COMPLETE = "complete"


class Task(BaseModel):
    """
    Pydantic model representing a single todo task.

    Attributes:
        id: Unique identifier for the task
        title: Title of the task (required, 1-200 characters)
        description: Optional description of the task (0-1000 characters)
        status: Current status of the task (pending or complete)
        created_at: Timestamp when the task was created
        updated_at: Timestamp when the task was last updated
    """
    id: int
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(default="", max_length=1000)
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)