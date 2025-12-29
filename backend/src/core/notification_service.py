"""
Notification service for the Todo Web API application.

This module provides notification capabilities for the web-based todo application,
including due date reminders, task completion notifications, and system alerts.
"""
import logging
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from ..models.task import TaskRead
from ..todo_app.core.notification_adapter import NotificationAdapter
from ..todo_app.core.scheduler import SchedulerService


class NotificationService:
    """
    Service class that provides notification capabilities for the web API.
    """

    def __init__(self, notification_adapter: Optional[NotificationAdapter] = None):
        """
        Initialize the NotificationService with a notification adapter.

        Args:
            notification_adapter: An instance of NotificationAdapter for sending notifications
        """
        self.notification_adapter = notification_adapter or NotificationAdapter()
        self.scheduler_service = SchedulerService(notification_adapter)
        self.logger = logging.getLogger(__name__)

    def _convert_api_status_to_cli_status(self, api_status: str) -> 'CliTaskStatus':
        """
        Convert API status values to CLI TaskStatus enum values.

        API uses: "pending", "in_progress", "completed"
        CLI uses: "pending", "complete"
        """
        from ..todo_app.models.todo import TaskStatus as CliTaskStatus

        if api_status == "completed":
            return CliTaskStatus.COMPLETE
        elif api_status == "pending":
            return CliTaskStatus.PENDING
        elif api_status == "in_progress":
            # CLI doesn't have in_progress, so map to pending for now
            return CliTaskStatus.PENDING
        else:
            # Default to pending for any unknown status
            return CliTaskStatus.PENDING

    def send_task_created_notification(self, task: TaskRead, user_name: str = "User") -> bool:
        """
        Send a notification when a task is created.

        Args:
            task: The created task
            user_name: Name of the user who created the task

        Returns:
            True if notification was sent successfully, False otherwise
        """
        title = "Task Created"
        message = f"New task created: '{task.title}'"

        self.logger.info(f"Sending task creation notification for task {task.id}: {task.title}")
        return self.notification_adapter.send_notification(title, message)

    def send_task_updated_notification(self, task: TaskRead) -> bool:
        """
        Send a notification when a task is updated.

        Args:
            task: The updated task

        Returns:
            True if notification was sent successfully, False otherwise
        """
        title = "Task Updated"
        message = f"Task updated: '{task.title}'"

        self.logger.info(f"Sending task update notification for task {task.id}: {task.title}")
        return self.notification_adapter.send_notification(title, message)

    def send_task_completed_notification(self, task: TaskRead) -> bool:
        """
        Send a notification when a task is completed.

        Args:
            task: The completed task

        Returns:
            True if notification was sent successfully, False otherwise
        """
        title = "Task Completed"
        message = f"Congratulations! You completed task: '{task.title}'"

        self.logger.info(f"Sending task completion notification for task {task.id}: {task.title}")
        return self.notification_adapter.send_notification(title, message)

    def send_task_deleted_notification(self, task_title: str) -> bool:
        """
        Send a notification when a task is deleted.

        Args:
            task_title: The title of the deleted task

        Returns:
            True if notification was sent successfully, False otherwise
        """
        title = "Task Deleted"
        message = f"Task deleted: '{task_title}'"

        self.logger.info(f"Sending task deletion notification for task: {task_title}")
        return self.notification_adapter.send_notification(title, message)

    def check_and_send_due_task_notifications(self, tasks: List[TaskRead]) -> List[bool]:
        """
        Check for tasks that are due or overdue and send notifications.

        Args:
            tasks: List of tasks to check

        Returns:
            List of boolean results indicating success/failure of notifications
        """
        self.logger.debug(f"Checking {len(tasks)} tasks for due status notifications")

        # Convert API TaskRead models to CLI Task models for scheduler compatibility
        from ..todo_app.models.todo import Task as CliTask, TaskStatus as CliTaskStatus, Priority as CliPriority
        from ..todo_app.core.scheduler import RecurrencePattern as CliRecurrencePattern
        from datetime import datetime

        # Convert API TaskRead objects to CLI Task objects
        cli_tasks = []
        for task in tasks:
            cli_task = CliTask(
                id=int(task.id) if hasattr(task, 'id') and task.id else 0,
                title=task.title,
                description=task.description or "",
                status=self._convert_api_status_to_cli_status(task.status) if hasattr(task, 'status') else CliTaskStatus.PENDING,
                priority=CliPriority(task.priority) if hasattr(task, 'priority') else CliPriority.MEDIUM,
                due_date=task.due_date,
                reminder_sent=getattr(task, 'reminder_sent', False),  # Use getattr to handle missing attribute
                created_at=task.created_at if hasattr(task, 'created_at') else datetime.now(),
                updated_at=task.updated_at if hasattr(task, 'updated_at') else datetime.now(),
                user_id=int(getattr(task, 'user_id', 1)),  # Default user_id
                tags=getattr(task, 'tags', []),
                recurrence_pattern=getattr(task, 'recurrence_pattern', CliRecurrencePattern.NONE),
                next_occurrence_date=getattr(task, 'next_occurrence_date', None)
            )
            cli_tasks.append(cli_task)

        due_tasks = self.scheduler_service.check_due_tasks(cli_tasks)
        results = self.scheduler_service.process_due_task_notifications(due_tasks)

        self.logger.info(f"Processed notifications for {len(due_tasks)} due tasks")
        return results

    def check_and_send_upcoming_task_notifications(self, tasks: List[TaskRead], days: int = 1) -> List[bool]:
        """
        Check for tasks that are due soon and send notifications.

        Args:
            tasks: List of tasks to check
            days: Number of days to look ahead (default: 1 for tomorrow)

        Returns:
            List of boolean results indicating success/failure of notifications
        """
        self.logger.debug(f"Checking {len(tasks)} tasks for upcoming notifications within {days} days")

        # Convert API TaskRead models to CLI Task models for scheduler compatibility
        from ..todo_app.models.todo import Task as CliTask, TaskStatus as CliTaskStatus, Priority as CliPriority
        from ..todo_app.core.scheduler import RecurrencePattern as CliRecurrencePattern
        from datetime import datetime

        # Convert API TaskRead objects to CLI Task objects
        cli_tasks = []
        for task in tasks:
            cli_task = CliTask(
                id=int(task.id) if hasattr(task, 'id') and task.id else 0,
                title=task.title,
                description=task.description or "",
                status=self._convert_api_status_to_cli_status(task.status) if hasattr(task, 'status') else CliTaskStatus.PENDING,
                priority=CliPriority(task.priority) if hasattr(task, 'priority') else CliPriority.MEDIUM,
                due_date=task.due_date,
                reminder_sent=getattr(task, 'reminder_sent', False),  # Use getattr to handle missing attribute
                created_at=task.created_at if hasattr(task, 'created_at') else datetime.now(),
                updated_at=task.updated_at if hasattr(task, 'updated_at') else datetime.now(),
                user_id=int(getattr(task, 'user_id', 1)),  # Default user_id
                tags=getattr(task, 'tags', []),
                recurrence_pattern=getattr(task, 'recurrence_pattern', CliRecurrencePattern.NONE),
                next_occurrence_date=getattr(task, 'next_occurrence_date', None)
            )
            cli_tasks.append(cli_task)

        upcoming_tasks = self.scheduler_service.get_upcoming_tasks(cli_tasks, days)
        results = []

        for task in upcoming_tasks:
            title = "Task Due Soon"
            message = f"Task '{task.title}' is due soon: {task.due_date.strftime('%Y-%m-%d %H:%M') if task.due_date else 'No due date'}"

            success = self.notification_adapter.send_notification(title, message)
            results.append(success)

            if success:
                self.logger.info(f"Upcoming task notification sent for task {task.id}: {task.title}")
            else:
                self.logger.warning(f"Failed to send upcoming task notification for task {task.id}: {task.title}")

        self.logger.info(f"Processed {len(upcoming_tasks)} upcoming task notifications")
        return results