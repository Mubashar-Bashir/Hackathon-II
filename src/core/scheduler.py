"""
Scheduler service for the Todo CLI application.

This module handles the logic for determining what needs to be rescheduled
and what needs reminders, particularly focusing on recurring tasks and
due date notifications.
"""

import logging
from datetime import datetime, timedelta
from typing import List, Optional
from ..models.todo import Task
from .todo_service import TodoService


# Configure logging
logger = logging.getLogger(__name__)


class SchedulerService:
    """
    Service class that handles scheduling logic for recurring tasks and reminders.
    """

    def __init__(self, todo_service: TodoService):
        """
        Initialize the SchedulerService with a todo service.

        Args:
            todo_service: An instance of TodoService to interact with tasks
        """
        self.todo_service = todo_service

    def calculate_next_occurrence(self, task: Task, last_occurrence: datetime) -> Optional[datetime]:
        """
        Calculate the next occurrence date for a recurring task based on its pattern.

        Args:
            task: The recurring task
            last_occurrence: The date when the task last occurred

        Returns:
            The next occurrence date, or None if the task is not recurring
        """
        if not task.recurrence_pattern:
            return None

        pattern = task.recurrence_pattern.upper()

        if pattern == "DAILY":
            return last_occurrence + timedelta(days=1)
        elif pattern == "WEEKLY":
            return last_occurrence + timedelta(weeks=1)
        elif pattern == "MONTHLY":
            # Calculate next month, handling month-end edge cases
            next_month = last_occurrence.month + 1
            next_year = last_occurrence.year

            if next_month > 12:
                next_month = 1
                next_year += 1

            # Handle month-end scenarios (e.g., Jan 31 -> Feb 28/29)
            next_day = last_occurrence.day
            max_days_in_month = self._days_in_month(next_year, next_month)

            # If the target day doesn't exist in the next month, use the last day of that month
            if next_day > max_days_in_month:
                next_day = max_days_in_month

            return last_occurrence.replace(year=next_year, month=next_month, day=next_day)
        else:
            logger.warning(f"Unknown recurrence pattern: {pattern}")
            return None

    def _days_in_month(self, year: int, month: int) -> int:
        """
        Calculate the number of days in a given month, accounting for leap years.

        Args:
            year: The year
            month: The month (1-12)

        Returns:
            Number of days in the month
        """
        if month in [1, 3, 5, 7, 8, 10, 12]:
            return 31
        elif month in [4, 6, 9, 11]:
            return 30
        elif month == 2:
            return 29 if self._is_leap_year(year) else 28
        else:
            raise ValueError(f"Invalid month: {month}")

    def _is_leap_year(self, year: int) -> bool:
        """
        Determine if a year is a leap year.

        Args:
            year: The year to check

        Returns:
            True if the year is a leap year, False otherwise
        """
        # A year is a leap year if divisible by 4, except for end-of-century years
        # which must also be divisible by 400
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

    def check_due_tasks(self) -> List[Task]:
        """
        Check for tasks that are due and need notification.

        Returns:
            List of tasks that are due now
        """
        all_tasks = self.todo_service.list_tasks()
        due_tasks = []

        now = datetime.now()

        for task in all_tasks:
            if task.due_date and not task.reminder_sent:
                # Check if the task is due (within a small window to account for timing)
                if task.due_date <= now:
                    due_tasks.append(task)

        return due_tasks

    def process_recurring_task_completion(self, task_id: int) -> Optional[Task]:
        """
        Process the completion of a recurring task by creating the next occurrence.

        Args:
            task_id: ID of the completed recurring task

        Returns:
            The newly created task instance, or None if the original task wasn't recurring
        """
        original_task = self.todo_service.get_task(task_id)
        if not original_task or not original_task.recurrence_pattern:
            return None

        # Calculate the next occurrence date
        next_occurrence = self.calculate_next_occurrence(original_task, datetime.now())
        if not next_occurrence:
            return None

        # Create a new task with the same properties but for the next occurrence
        new_task = self.todo_service.add_task(
            title=original_task.title,
            description=original_task.description,
            priority=original_task.priority,
            tags=original_task.tags,
            due_date=next_occurrence
        )

        logger.info(f"Created new instance of recurring task {original_task.title} for {next_occurrence}")
        return new_task

    def get_upcoming_tasks(self, days: int = 7) -> List[Task]:
        """
        Get all tasks due in the next specified number of days.

        Args:
            days: Number of days to look ahead (default: 7)

        Returns:
            List of tasks due in the next 'days' days, sorted chronologically
        """
        all_tasks = self.todo_service.list_tasks()
        upcoming_tasks = []

        now = datetime.now()
        future_date = now + timedelta(days=days)

        for task in all_tasks:
            if task.due_date and now < task.due_date <= future_date:
                upcoming_tasks.append(task)

        # Sort by due date
        upcoming_tasks.sort(key=lambda t: t.due_date if t.due_date else datetime.max)

        return upcoming_tasks