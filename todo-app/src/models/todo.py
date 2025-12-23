"""
Task data models for the Todo CLI application.

This module defines the Pydantic models used throughout the application
for data validation and serialization.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import Optional, List


class TaskStatus(str, Enum):
    """
    Enum representing the possible statuses of a task.

    Attributes:
        PENDING: Task is pending completion
        COMPLETE: Task has been completed
    """
    PENDING = "pending"
    COMPLETE = "complete"


class Priority(str, Enum):
    """
    Enum representing the priority levels of a task.

    Attributes:
        LOW: Low priority task
        MEDIUM: Medium priority task (default)
        HIGH: High priority task
    """
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class SortField(str, Enum):
    """
    Enum representing the fields by which tasks can be sorted.

    Attributes:
        TITLE: Sort by task title
        PRIORITY: Sort by task priority
        DUE_DATE: Sort by task due date
        CREATED_DATE: Sort by task creation date
        STATUS: Sort by task status
    """
    TITLE = "title"
    PRIORITY = "priority"
    DUE_DATE = "due_date"
    CREATED_DATE = "created_at"
    STATUS = "status"


class SortOrder(str, Enum):
    """
    Enum representing the sort order directions.

    Attributes:
        ASC: Ascending order
        DESC: Descending order
    """
    ASC = "asc"
    DESC = "desc"


class TaskFilter(BaseModel):
    """
    Pydantic model for filtering tasks based on multiple criteria.

    Attributes:
        status: Filter by task status
        priority: Filter by task priority
        tags: Filter by tags (task must have ALL specified tags)
        search_keyword: Filter by substring match in title or description
        due_date_from: Filter tasks with due_date >= this date
        due_date_to: Filter tasks with due_date <= this date
    """
    status: Optional[TaskStatus] = None
    priority: Optional[Priority] = None
    tags: List[str] = Field(default_factory=list)  # Tasks must have ALL these tags
    search_keyword: Optional[str] = None  # Substring match in title or description
    due_date_from: Optional[datetime] = None  # Tasks with due_date >= this date
    due_date_to: Optional[datetime] = None    # Tasks with due_date <= this date


class SortCriteria(BaseModel):
    """
    Pydantic model for defining sort criteria.

    Attributes:
        field: Field to sort by
        order: Sort order (ascending or descending)
    """
    field: SortField
    order: SortOrder = SortOrder.ASC


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
        priority: Priority level of the task (default: MEDIUM)
        tags: List of tags for categorization (default: empty list)
        due_date: Optional due date for the task (default: None)
    """
    id: int
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(default="", max_length=1000)
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    # New fields for organization
    priority: Priority = Priority.MEDIUM  # Default to medium for backward compatibility
    tags: List[str] = Field(
        default_factory=list,
        min_length=0,
        max_length=10,
        description="List of tags for categorization, max 10 tags"
    )  # Empty list for backward compatibility
    due_date: Optional[datetime] = Field(
        default=None,
        description="Optional due date for the task"
    )  # None for backward compatibility

    def __init__(self, **data):
        """
        Initialize the Task with validation for tags.

        Args:
            **data: Task attributes
        """
        # Validate tags if provided
        tags = data.get('tags', [])
        if tags:
            for tag in tags:
                if not isinstance(tag, str):
                    raise ValueError(f"Tag must be a string, got {type(tag)}")
                if len(tag) > 50:
                    raise ValueError(f"Tag '{tag}' exceeds maximum length of 50 characters")
                if not tag.replace('-', '').replace('_', '').isalnum():
                    raise ValueError(f"Tag '{tag}' contains invalid characters. Only alphanumeric, hyphens, and underscores allowed.")

        super().__init__(**data)