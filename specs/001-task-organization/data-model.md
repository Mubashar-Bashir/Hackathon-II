# Data Model: Task Organization & Usability

## Updated Task Entity

### Task Model
```python
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import Optional, List

class TaskStatus(str, Enum):
    PENDING = "pending"
    COMPLETE = "complete"

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"  # Default priority
    HIGH = "high"

class Task(BaseModel):
    id: int
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(default="", max_length=1000)
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    # New fields for organization
    priority: Priority = Priority.MEDIUM  # Default to medium for backward compatibility
    tags: List[str] = Field(default_factory=list)  # Empty list for backward compatibility
    due_date: Optional[datetime] = None  # None for backward compatibility
```

### Field Validations
- **priority**: Must be one of Low, Medium, High enum values
- **tags**: List of strings with validation:
  - Each tag must be 1-50 characters
  - Only alphanumeric characters, hyphens, and underscores allowed
  - Maximum of 10 tags per task
- **due_date**: Optional datetime field, if provided must be valid ISO 8601 format

## Filtering and Sorting Parameters

### Filter Criteria
```python
from typing import Optional, List
from datetime import datetime

class TaskFilter(BaseModel):
    status: Optional[TaskStatus] = None
    priority: Optional[Priority] = None
    tags: List[str] = Field(default_factory=list)  # Tasks must have ALL these tags
    search_keyword: Optional[str] = None  # Substring match in title or description
    due_date_from: Optional[datetime] = None  # Tasks with due_date >= this date
    due_date_to: Optional[datetime] = None    # Tasks with due_date <= this date
```

### Sort Options
```python
class SortField(str, Enum):
    TITLE = "title"
    PRIORITY = "priority"
    DUE_DATE = "due_date"
    CREATED_DATE = "created_at"
    STATUS = "status"

class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"

class SortCriteria(BaseModel):
    field: SortField
    order: SortOrder = SortOrder.ASC
```

## Backward Compatibility Strategy

### Default Values for Existing Tasks
When existing tasks (without the new fields) are loaded:
- `priority` defaults to `Priority.MEDIUM`
- `tags` defaults to empty list `[]`
- `due_date` defaults to `None`

### Migration Considerations
- No database migration needed (in-memory storage)
- New fields are optional with defaults
- Existing functionality remains unchanged