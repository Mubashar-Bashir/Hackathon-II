"""
Scheduler service for the Todo CLI application.

This module provides scheduling capabilities for recurring tasks,
due date notifications, and time-based automation features.
"""

import logging
from datetime import datetime
from enum import Enum
from typing import List, Optional
import pendulum
from ..models.todo import Task, TaskStatus
from ..core.notification_adapter import NotificationAdapter


# Configure logging
logger = logging.getLogger(__name__)


class RecurrencePattern(str, Enum):
    """
    Enum representing the possible recurrence patterns for tasks.

    Attributes:
        NONE: No recurrence (default)
        DAILY: Task repeats every day
        WEEKLY: Task repeats every week
        MONTHLY: Task repeats every month
    """
    NONE = "none"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class SchedulerService:
    """
    Service class that implements scheduling logic for recurring tasks
    and due date notifications.
    """

    def __init__(self, notification_adapter: Optional[NotificationAdapter] = None):
        """
        Initialize the SchedulerService with a notification adapter.

        Args:
            notification_adapter: An instance of NotificationAdapter for sending notifications
        """
        self.notification_adapter = notification_adapter or NotificationAdapter()

    def calculate_next_occurrence(self, current_date: datetime, pattern: RecurrencePattern) -> datetime:
        """
        Calculate the next occurrence date based on the recurrence pattern.

        Args:
            current_date: The current date/time
            pattern: The recurrence pattern

        Returns:
            The datetime for the next occurrence
        """
        logger.debug(f"Calculating next occurrence for {pattern} from {current_date}")

        # Use pendulum for robust date calculations
        current = pendulum.instance(current_date)

        if pattern == RecurrencePattern.DAILY:
            next_occurrence = current.add(days=1)
        elif pattern == RecurrencePattern.WEEKLY:
            next_occurrence = current.add(weeks=1)
        elif pattern == RecurrencePattern.MONTHLY:
            next_occurrence = current.add(months=1)
        else:
            # For NONE pattern, return None (no recurrence)
            return None

        logger.debug(f"Next occurrence calculated as: {next_occurrence}")
        return next_occurrence

    def handle_month_end_edge_cases(self, current_date: datetime, pattern: RecurrencePattern) -> datetime:
        """
        Handle month-end edge cases for monthly recurrence patterns.

        Args:
            current_date: The current date/time
            pattern: The recurrence pattern (should be MONTHLY for this to be relevant)

        Returns:
            The datetime for the next occurrence, adjusted for month-end edge cases
        """
        logger.debug(f"Handling month-end edge cases for {current_date} with pattern {pattern}")

        if pattern != RecurrencePattern.MONTHLY:
            # Only apply month-end logic for monthly patterns
            return self.calculate_next_occurrence(current_date, pattern)

        # Use pendulum for proper month-end handling
        current = pendulum.instance(current_date)
        next_month = current.add(months=1)

        # If the original day doesn't exist in the next month (e.g., Jan 31 -> Feb 31 doesn't exist),
        # pendulum automatically adjusts to the last day of the month
        logger.debug(f"Month-end adjusted next occurrence: {next_month}")
        return next_month

    def calculate_leap_year_aware_date(self, current_date: datetime, pattern: RecurrencePattern) -> datetime:
        """
        Calculate the next occurrence with leap year awareness.

        Args:
            current_date: The current date/time
            pattern: The recurrence pattern

        Returns:
            The datetime for the next occurrence, with leap year considerations
        """
        logger.debug(f"Calculating leap year aware date for {current_date} with pattern {pattern}")

        if pattern != RecurrencePattern.MONTHLY:
            # For non-monthly patterns, regular calculation is sufficient
            return self.calculate_next_occurrence(current_date, pattern)

        # Use pendulum which handles leap years automatically
        current = pendulum.instance(current_date)
        next_occurrence = current.add(months=1)

        logger.debug(f"Leap year aware next occurrence: {next_occurrence}")
        return next_occurrence

    def process_recurring_task_completion(self, task: Task) -> Optional[Task]:
        """
        Process a completed recurring task and create the next occurrence if applicable.

        Args:
            task: The completed recurring task

        Returns:
            The new recurring task instance if created, None otherwise
        """
        logger.info(f"Processing recurring task completion for task {task.id}: {task.title}")
        logger.debug(f"Task recurrence pattern: {task.recurrence_pattern} (type: {type(task.recurrence_pattern)})")

        # Check if the task has a recurrence pattern
        if not task.recurrence_pattern or (
            isinstance(task.recurrence_pattern, str) and task.recurrence_pattern == "none"
        ) or (
            hasattr(task.recurrence_pattern, 'value') and task.recurrence_pattern == RecurrencePattern.NONE
        ):
            logger.debug(f"Task {task.id} is not recurring, no new instance needed")
            return None

        try:
            logger.debug(f"Processing recurrence pattern: {task.recurrence_pattern}")
            logger.debug(f"Type of recurrence pattern: {type(task.recurrence_pattern)}")

            # The recurrence_pattern should be an enum, but handle both cases
            if isinstance(task.recurrence_pattern, str):
                logger.debug(f"Recurrence pattern is string, converting: {task.recurrence_pattern.lower()}")
                # If it's a string, convert to enum
                pattern = RecurrencePattern(task.recurrence_pattern.lower())
                logger.debug(f"Converted pattern: {pattern}")
            else:
                logger.debug(f"Recurrence pattern is enum, using directly: {task.recurrence_pattern}")
                # If it's already an enum, use it directly
                pattern = task.recurrence_pattern

            logger.debug(f"Final pattern: {pattern}")
            if pattern == RecurrencePattern.NONE:
                logger.debug(f"Task {task.id} has no recurrence pattern, no new instance needed")
                return None

            # Calculate the next occurrence date based on the current time
            next_occurrence_date = self.calculate_next_occurrence(datetime.now(), pattern)

            # Handle month-end edge cases if it's a monthly pattern
            if pattern == RecurrencePattern.MONTHLY:
                next_occurrence_date = self.handle_month_end_edge_cases(datetime.now(), pattern)

            # Create a new task with the same properties but for the next occurrence
            # Don't include id in the model_dump to avoid validation issues
            new_task_data = task.model_dump()
            new_task_data.pop('id', None)  # Remove ID to generate a new one in the service layer
            new_task_data['status'] = TaskStatus.PENDING  # New task should be pending
            new_task_data['created_at'] = datetime.now()  # New creation time
            new_task_data['updated_at'] = datetime.now()  # New update time
            new_task_data['due_date'] = next_occurrence_date  # Set due date to next occurrence
            new_task_data['recurrence_pattern'] = task.recurrence_pattern  # Preserve recurrence
            new_task_data['reminder_sent'] = False  # Reset reminder status

            # Create and return the new task - the service will assign a new ID
            # We'll return the data structure and let the service create the actual task
            new_task = Task(
                id=0,  # Will be replaced by the service
                title=new_task_data['title'],
                description=new_task_data['description'],
                status=new_task_data['status'],
                created_at=new_task_data['created_at'],
                updated_at=new_task_data['updated_at'],
                priority=new_task_data['priority'],
                tags=new_task_data['tags'],
                due_date=new_task_data['due_date'],
                recurrence_pattern=new_task_data['recurrence_pattern'],
                reminder_sent=new_task_data['reminder_sent'],
                next_occurrence_date=new_task_data['next_occurrence_date']
            )
            logger.info(f"Created new recurring instance for task: {new_task.title}")
            return new_task

        except ValueError as e:
            logger.error(f"ValueError processing recurring task completion for task {task.id}: {e}")
            logger.error(f"Original recurrence pattern was: {task.recurrence_pattern} (type: {type(task.recurrence_pattern)})")
            return None
        except Exception as e:
            logger.error(f"Error processing recurring task completion for task {task.id}: {str(e)}")
            logger.error(f"Original recurrence pattern was: {task.recurrence_pattern} (type: {type(task.recurrence_pattern)})")
            return None

    def check_due_tasks(self, tasks: List[Task]) -> List[Task]:
        """
        Check for tasks that are due or overdue and need notifications.

        Args:
            tasks: List of tasks to check

        Returns:
            List of tasks that are due or overdue
        """
        logger.debug(f"Checking {len(tasks)} tasks for due status")

        current_time = datetime.now()
        due_tasks = []

        for task in tasks:
            if task.due_date and not task.reminder_sent:
                # Check if the task is due (due date is today or in the past)
                if task.due_date <= current_time:
                    due_tasks.append(task)
                    logger.debug(f"Task {task.id} is due: {task.title}")

        logger.info(f"Found {len(due_tasks)} tasks that are due or overdue")
        return due_tasks

    def get_upcoming_tasks(self, tasks: List[Task], days: int = 7) -> List[Task]:
        """
        Get tasks that are due in the next specified number of days.

        Args:
            tasks: List of tasks to check
            days: Number of days to look ahead (default: 7)

        Returns:
            List of tasks due within the specified number of days
        """
        logger.debug(f"Getting upcoming tasks within {days} days")

        current_time = datetime.now()
        future_limit = current_time + pendulum.duration(days=days)
        upcoming_tasks = []

        for task in tasks:
            if task.due_date and not task.reminder_sent:
                # Check if the task is due within the specified number of days
                if current_time <= task.due_date <= future_limit:
                    upcoming_tasks.append(task)
                    logger.debug(f"Task {task.id} is upcoming: {task.title}, due: {task.due_date}")

        # Sort upcoming tasks by due date
        upcoming_tasks.sort(key=lambda x: x.due_date if x.due_date else datetime.max)

        logger.info(f"Found {len(upcoming_tasks)} upcoming tasks within {days} days")
        return upcoming_tasks

    def process_due_task_notifications(self, due_tasks: List[Task]) -> List[bool]:
        """
        Process notifications for due tasks.

        Args:
            due_tasks: List of tasks that are due

        Returns:
            List of boolean results indicating success/failure of notifications
        """
        results = []

        for task in due_tasks:
            try:
                # Send notification for the due task
                success = self.notification_adapter.send_notification(
                    title="Task Due",
                    message=f"Task '{task.title}' is due: {task.due_date.strftime('%Y-%m-%d %H:%M') if task.due_date else 'No due date'}"
                )

                results.append(success)

                if success:
                    logger.info(f"Notification sent for task {task.id}: {task.title}")
                    # In a real implementation, we would update the task's reminder_sent status
                    # task.reminder_sent = True
                else:
                    logger.warning(f"Failed to send notification for task {task.id}: {task.title}")

            except Exception as e:
                logger.error(f"Error sending notification for task {task.id}: {str(e)}")
                results.append(False)

        return results