# Data Model: Modular In-Memory Todo CLI System

**Feature**: 001-todo-cli
**Date**: 2025-12-23
**Status**: Complete

## Core Entities

### Task Entity
**Description**: Represents a single todo item in the system

**Fields**:
- `id: int` - Unique identifier for the task (auto-generated)
- `title: str` - Required title of the task (min length: 1, max length: 200)
- `description: str` - Optional description of the task (default: empty string, max length: 1000)
- `status: TaskStatus` - Current status of the task (enum: PENDING, COMPLETE)
- `created_at: datetime` - Timestamp when the task was created (auto-generated)
- `updated_at: datetime` - Timestamp when the task was last updated (auto-generated)

**Validation Rules**:
- Title must not be empty or whitespace-only
- Title must be between 1 and 200 characters
- Description must be between 0 and 1000 characters
- ID must be unique within the system
- Status must be one of the allowed values (PENDING, COMPLETE)

**State Transitions**:
- PENDING → COMPLETE (when task is marked as complete)
- COMPLETE → PENDING (when task is marked as incomplete)

**Pydantic Model**:
```python
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import Optional

class TaskStatus(str, Enum):
    PENDING = "pending"
    COMPLETE = "complete"

class Task(BaseModel):
    id: int
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(default="", max_length=1000)
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
```

### TaskList Entity
**Description**: Represents a collection of tasks with utility methods

**Fields**:
- `tasks: List[Task]` - List of all tasks in the system

**Methods**:
- `add_task(task: Task) -> None` - Add a new task to the list
- `get_task(task_id: int) -> Optional[Task]` - Retrieve a task by ID
- `update_task(task_id: int, updates: Dict) -> bool` - Update task fields
- `delete_task(task_id: int) -> bool` - Remove task by ID
- `get_all_tasks() -> List[Task]` - Get all tasks
- `get_tasks_by_status(status: TaskStatus) -> List[Task]` - Filter tasks by status

## Repository Interface

### TaskRepository Protocol
**Description**: Abstract interface for task storage operations

**Methods**:
- `create_task(task: Task) -> Task` - Create a new task in storage
- `get_task(task_id: int) -> Optional[Task]` - Retrieve task by ID
- `update_task(task_id: int, task: Task) -> Optional[Task]` - Update existing task
- `delete_task(task_id: int) -> bool` - Delete task by ID
- `list_tasks() -> List[Task]` - Get all tasks from storage

## Service Layer Models

### TaskCreateRequest
**Description**: Request model for creating new tasks

**Fields**:
- `title: str` - Title of the new task
- `description: Optional[str]` - Optional description

### TaskUpdateRequest
**Description**: Request model for updating existing tasks

**Fields**:
- `title: Optional[str]` - New title (if updating)
- `description: Optional[str]` - New description (if updating)
- `status: Optional[TaskStatus]` - New status (if updating)

## Validation Rules Summary

1. **Task Creation**: Title is required and must be 1-200 characters
2. **Task Update**: At least one field must be provided for update
3. **Task ID**: Must be unique and positive integer
4. **Task Status**: Only PENDING or COMPLETE values allowed
5. **Description**: Optional, 0-1000 characters maximum

## Data Flow Patterns

### Input Validation Flow
1. CLI input → Request model validation (Pydantic)
2. Validated data → Service layer
3. Service layer → Repository layer
4. Repository → Storage

### Error Handling Flow
1. Validation errors → User-friendly error messages
2. Business logic errors → Appropriate status codes/messages
3. Storage errors → Graceful degradation with error reporting