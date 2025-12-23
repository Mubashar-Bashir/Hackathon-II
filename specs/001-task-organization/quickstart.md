# Quickstart Guide: Task Organization & Usability

## New Features Overview

The Task Organization & Usability feature adds the following capabilities to your Todo CLI application:

- **Priority Levels**: Assign Low, Medium, or High priority to tasks
- **Tags**: Add multiple tags to tasks for categorization
- **Due Dates**: Set optional due dates for tasks
- **Advanced Filtering**: Filter tasks by priority, status, tags, and keywords
- **Sorting**: Sort tasks by due date, priority, title, and other fields

## Enhanced Task Creation

### Adding Tasks with Organization Features

```bash
# Add a task with priority and tags
todo add "Complete project proposal" "Write and submit the Q4 project proposal" --priority high --tags work important

# Add a task with due date
todo add "Team meeting" "Weekly team sync" --due-date 2025-01-15T10:00:00.000Z

# Add a task with multiple features
todo add "Fix critical bug" "Resolve login issue reported by users" --priority high --tags urgent bug --due-date 2025-01-10T18:00:00.000Z
```

## Filtering and Searching

### Filter Tasks by Priority
```bash
# List only high priority tasks
todo list --priority high

# List tasks with specific status and priority
todo list --status pending --priority high
```

### Search Tasks by Keyword
```bash
# Search for tasks containing "project"
todo list --search project

# Combine search with other filters
todo list --search "meeting" --priority medium
```

### Filter by Tags
```bash
# List tasks with specific tags
todo list --tag work
todo list --tag urgent --tag bug  # Tasks with both tags
```

## Sorting Tasks

### Sort by Different Criteria
```bash
# Sort by priority (High to Low)
todo list --sort-by priority --sort-order desc

# Sort by due date (earliest first)
todo list --sort-by due_date --sort-order asc

# Sort by title alphabetically
todo list --sort-by title --sort-order asc
```

## Combined Operations

### Complex Filtering and Sorting
```bash
# List pending high-priority work tasks, sorted by due date
todo list --status pending --priority high --tag work --sort-by due_date --sort-order asc

# Search for "report" tasks, sorted by priority
todo list --search report --sort-by priority --sort-order desc
```

## Backward Compatibility

All existing functionality continues to work exactly as before:

```bash
# These commands work exactly as before
todo add "Simple task"
todo list
todo complete 1
todo update 1 --title "Updated title"
todo delete 1
```

## Field Validation

### Tag Validation Rules
- Tags must be 1-50 characters long
- Only alphanumeric characters, hyphens, and underscores allowed
- Maximum of 10 tags per task

### Due Date Format
- Must be in ISO 8601 format: YYYY-MM-DDTHH:MM:SS.sssZ
- Example: 2025-01-15T10:30:00.000Z

## Example Workflows

### Daily Task Management
```bash
# Add today's tasks with priorities and tags
todo add "Morning standup" "Team sync meeting" --priority medium --tags work --due-date 2025-01-15T09:00:00.000Z
todo add "Code review" "Review PRs from team" --priority high --tags work

# View today's high-priority tasks
todo list --priority high --status pending

# Find all work-related tasks
todo list --tag work --sort-by priority --sort-order desc
```

### Project Management
```bash
# Add project tasks with relevant tags
todo add "Design database schema" --priority high --tags project database design --due-date 2025-01-20T17:00:00.000Z

# Track project progress
todo list --tag project --sort-by due_date --sort-order asc

# Find urgent project tasks
todo list --tag project --tag urgent --status pending
```