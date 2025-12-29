# API Contracts: Task Organization & Usability

## Core Service Method Contracts

### Enhanced TodoService Methods

#### 1. Enhanced add_task method
```python
def add_task(
    self,
    title: str,
    description: str = "",
    priority: Optional[Priority] = Priority.MEDIUM,
    tags: Optional[List[str]] = None,
    due_date: Optional[datetime] = None
) -> Task:
    """
    Add a new task with organization features.

    Args:
        title: The title of the new task (required, 1-200 chars)
        description: The description of the new task (optional, 0-1000 chars)
        priority: Priority level (Low, Medium, High; defaults to Medium)
        tags: List of tags for categorization (defaults to empty list)
        due_date: Optional due date (defaults to None)

    Returns:
        The created task with a unique ID and all organization fields

    Raises:
        ValueError: If title is empty or exceeds length limits
        ValueError: If tags don't meet validation criteria
        ValueError: If due_date format is invalid
    """
```

#### 2. New filter_tasks method
```python
def filter_tasks(
    self,
    status: Optional[TaskStatus] = None,
    priority: Optional[Priority] = None,
    tags: Optional[List[str]] = None,
    search_keyword: Optional[str] = None
) -> List[Task]:
    """
    Filter tasks based on multiple criteria.

    Args:
        status: Filter by task status (PENDING/COMPLETE)
        priority: Filter by priority level
        tags: Filter by tags (task must have ALL specified tags)
        search_keyword: Filter by substring match in title/description

    Returns:
        List of tasks matching all specified criteria
    """
```

#### 3. New sort_tasks method
```python
def sort_tasks(
    self,
    tasks: List[Task],
    sort_field: SortField,
    sort_order: SortOrder = SortOrder.ASC
) -> List[Task]:
    """
    Sort tasks by specified field and order.

    Args:
        tasks: List of tasks to sort
        sort_field: Field to sort by (title, priority, due_date, etc.)
        sort_order: Sort order (ASC/DESC)

    Returns:
        List of tasks sorted according to criteria

    Special handling:
        - When sorting by due_date, tasks with None due_date appear last
    """
```

#### 4. Enhanced list_tasks method
```python
def list_tasks(
    self,
    status: Optional[TaskStatus] = None,
    priority: Optional[Priority] = None,
    tags: Optional[List[str]] = None,
    search_keyword: Optional[str] = None,
    sort_field: Optional[SortField] = None,
    sort_order: SortOrder = SortOrder.ASC
) -> List[Task]:
    """
    Get all tasks with optional filtering and sorting.

    Args:
        status: Filter by task status
        priority: Filter by priority level
        tags: Filter by tags (task must have ALL specified tags)
        search_keyword: Filter by substring match in title/description
        sort_field: Sort by specified field
        sort_order: Sort order (ASC/DESC)

    Returns:
        List of tasks matching criteria, sorted as requested
    """
```

## CLI Command Contracts

### Enhanced CLI Commands

#### 1. Enhanced add command
```
todo add "Task Title" "Task Description"
    [--priority {low,medium,high}]
    [--tags TAG1 TAG2 ...]
    [--due-date YYYY-MM-DDTHH:MM:SS.sssZ]
```

#### 2. Enhanced list command
```
todo list
    [--status {pending,complete}]
    [--priority {low,medium,high}]
    [--tag TAG] (can be used multiple times)
    [--search KEYWORD]
    [--sort-by {title,priority,due_date,created_at,status}]
    [--sort-order {asc,desc}]
```

#### 3. New filter command (alternative to enhanced list)
```
todo filter
    [--status {pending,complete}]
    [--priority {low,medium,high}]
    [--tag TAG] (can be used multiple times)
    [--search KEYWORD]
    [--sort-by {title,priority,due_date,created_at,status}]
    [--sort-order {asc,desc}]
```

## Error Contracts

### Standard Error Responses
- **400 Bad Request**: Invalid input parameters
- **404 Not Found**: Task with specified ID does not exist
- **500 Internal Server Error**: Unexpected system error

### Validation Error Messages
- "Priority must be one of: low, medium, high"
- "Tags must be alphanumeric with hyphens/underscores only, 1-50 chars each"
- "Due date must be in ISO 8601 format: YYYY-MM-DDTHH:MM:SS.sssZ"
- "Task title is required and must be 1-200 characters"
- "Task description exceeds maximum length of 1000 characters"