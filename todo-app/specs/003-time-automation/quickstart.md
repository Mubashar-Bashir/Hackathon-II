# Quickstart Guide: Time & Automation Feature

## 1. Setup and Installation

### 1.1 Dependencies
Install the required dependencies for the time automation feature:

```bash
pip install pendulum plyer
```

### 1.2 Project Structure
The feature will extend the existing project structure:

```
src/
├── core/
│   ├── todo_service.py          # Enhanced with recurring task methods
│   ├── scheduler.py             # New: Handles recurring logic and due date checks
│   └── notification_adapter.py  # New: Cross-platform notification delivery
├── models/
│   └── todo.py                 # Enhanced with recurrence fields
└── ui/
    └── cli.py                  # Enhanced with new commands and options
```

## 2. Implementation Steps

### 2.1 Phase 1: Data Model Extensions
1. Update the Task model in `src/models/todo.py` with new fields:
   - `recurrence_pattern`: String enum (DAILY, WEEKLY, MONTHLY, NONE)
   - `due_date`: DateTime field for due dates
   - `reminder_sent`: Boolean flag for notification status
   - `next_occurrence_date`: DateTime for next recurring task

2. Update TodoService in `src/core/todo_service.py` to handle new fields

### 2.2 Phase 2: Scheduler Service
1. Create `src/core/scheduler.py` with:
   - `calculate_next_occurrence()` method for recurrence logic
   - `check_due_tasks()` method for identifying tasks needing notifications
   - `process_recurring_task_completion()` for handling completed recurring tasks
   - Month-end and leap year handling

### 2.3 Phase 3: Notification System
1. Create `src/core/notification_adapter.py` with:
   - Cross-platform notification using plyer
   - `send_notification()` method
   - Notification preferences handling

### 2.4 Phase 4: CLI Enhancements
1. Update `src/ui/cli.py` with:
   - Extended `add` command with `--recurrence` and `--due-date` options
   - Enhanced task listing with due date and recurrence indicators
   - New `upcoming` command for next 7 days view

## 3. Key Implementation Patterns

### 3.1 Event-Triggered Architecture
- When CLI commands are executed, scheduler checks for due tasks
- No continuous background processing (minimizes resource usage)
- Optional background daemon capability for real-time notifications

### 3.2 Month-End Handling
```python
def calculate_next_occurrence(self, task: Task, last_occurrence: datetime) -> Optional[datetime]:
    # Handle month-end scenarios (e.g., Jan 31 → Feb 28/29)
    next_month = last_occurrence.month + 1
    next_year = last_occurrence.year

    if next_month > 12:
        next_month = 1
        next_year += 1

    next_day = last_occurrence.day
    max_days_in_month = self._days_in_month(next_year, next_month)

    # If the target day doesn't exist in the next month, use the last day of that month
    if next_day > max_days_in_month:
        next_day = max_days_in_month

    return last_occurrence.replace(year=next_year, month=next_month, day=next_day)
```

### 3.3 Leap Year Handling
```python
def _is_leap_year(self, year: int) -> bool:
    # A year is a leap year if divisible by 4, except for end-of-century years
    # which must also be divisible by 400
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
```

## 4. Testing Approach

### 4.1 Unit Tests
- Test recurrence calculation logic with edge cases
- Test notification sending functionality
- Test month-end and leap year scenarios

### 4.2 Integration Tests
- Test end-to-end recurring task creation and completion
- Test notification triggering for due tasks
- Test "Next 7 Days" view functionality

### 4.3 Performance Tests
- Verify due task checking completes under 100ms
- Verify "Next 7 Days" view loads under 200ms

## 5. Security Considerations

- Time-based data has same security requirements as other task data
- No special encryption needed beyond standard user authentication
- Notification system should respect user privacy settings

## 6. Common Issues and Solutions

### 6.1 Date Calculation Issues
- Issue: Month-end recurrence fails (Jan 31 → Feb 31 doesn't exist)
- Solution: Use next valid date (Jan 31 → Feb 28/29)

### 6.2 Notification Failures
- Issue: Notifications fail to appear on some platforms
- Solution: Implement graceful degradation with console fallback

### 6.3 Performance Issues
- Issue: Due task checking takes too long
- Solution: Optimize queries and implement caching for frequently accessed data

## 7. Verification Commands

```bash
# Test basic functionality still works
todo list
todo add "Regular task"
todo complete 1

# Test new functionality
todo add "Weekly meeting" --recurrence weekly --due-date "2025-01-06T10:00"
todo upcoming
todo list --show-due-soon

# Test edge cases
todo add "Monthly review" --recurrence monthly --due-date "2025-01-31"
todo add "Leap year task" --recurrence yearly --due-date "2024-02-29"
```