# Data Model: Time & Automation Feature

## 1. Enhanced Task Model

### 1.1 Task Entity
```python
from enum import Enum
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class RecurrencePattern(str, Enum):
    NONE = "none"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

class Task(BaseModel):
    # Existing fields (maintained for backward compatibility)
    id: str
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: str = "medium"  # low, medium, high
    created_at: datetime

    # New fields for time automation features
    due_date: Optional[datetime] = None
    recurrence_pattern: RecurrencePattern = RecurrencePattern.NONE
    reminder_sent: bool = False
    next_occurrence_date: Optional[datetime] = None
```

### 1.2 Field Definitions

#### 1.2.1 Due Date
- **Field**: `due_date: Optional[datetime]`
- **Purpose**: Specifies when the task is due
- **Validation**: If set, must be a valid future date/time
- **Default**: None (optional field)

#### 1.2.2 Recurrence Pattern
- **Field**: `recurrence_pattern: RecurrencePattern`
- **Purpose**: Defines how often the task repeats
- **Validation**: Must be one of the enum values (none, daily, weekly, monthly)
- **Default**: "none" (non-recurring by default)

#### 1.2.3 Reminder Sent
- **Field**: `reminder_sent: bool`
- **Purpose**: Tracks whether a notification has been sent for this due task
- **Validation**: Boolean value only
- **Default**: False

#### 1.2.4 Next Occurrence Date
- **Field**: `next_occurrence_date: Optional[datetime]`
- **Purpose**: Stores the date when the next instance of a recurring task should appear
- **Validation**: If set, must be a valid future date/time
- **Default**: None

## 2. Scheduler Data

### 2.1 Scheduler State
```python
from datetime import datetime
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class SchedulerState:
    last_check: datetime
    pending_notifications: List[str]  # List of task IDs needing notifications
    recurring_tasks_processed: List[str]  # List of task IDs processed for recurrence
```

## 3. Validation Rules

### 3.1 Task Creation Validation
- If `recurrence_pattern` is not "none", the task can have a `due_date`
- If `recurrence_pattern` is "none", `next_occurrence_date` must be None
- `due_date` must be in the future if specified

### 3.2 Task Update Validation
- When marking a recurring task as complete, validate that `next_occurrence_date` is calculated properly
- Prevent modification of `reminder_sent` except through notification system

## 4. Backward Compatibility
- All new fields are optional (with appropriate defaults)
- Existing tasks without new fields continue to function normally
- No changes to existing field types or requirements