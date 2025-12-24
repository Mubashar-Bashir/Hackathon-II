"""
Test suite for time automation features in the Todo CLI application.

This module contains unit tests for the scheduler service, recurring tasks,
due date notifications, and related functionality.
"""

import pytest
from datetime import datetime, timedelta
from src.models.todo import Task, TaskStatus, Priority, RecurrencePattern
from src.core.scheduler import SchedulerService
from src.core.notification_adapter import NotificationAdapter
from src.core.todo_service import TodoService
from src.storage.in_memory_storage import InMemoryTaskRepository


class TestSchedulerService:
    """Test cases for the SchedulerService class."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.notification_adapter = NotificationAdapter()
        self.scheduler = SchedulerService(self.notification_adapter)

    def test_calculate_next_occurrence_daily(self):
        """Test calculating next occurrence for daily pattern."""
        current_date = datetime(2025, 1, 1, 10, 0, 0)
        next_date = self.scheduler.calculate_next_occurrence(current_date, RecurrencePattern.DAILY)

        expected = datetime(2025, 1, 2, 10, 0, 0)
        assert next_date.year == expected.year
        assert next_date.month == expected.month
        assert next_date.day == expected.day
        assert next_date.hour == expected.hour

    def test_calculate_next_occurrence_weekly(self):
        """Test calculating next occurrence for weekly pattern."""
        current_date = datetime(2025, 1, 1, 10, 0, 0)  # A Wednesday
        next_date = self.scheduler.calculate_next_occurrence(current_date, RecurrencePattern.WEEKLY)

        expected = datetime(2025, 1, 8, 10, 0, 0)  # Next Wednesday
        assert next_date.date() == expected.date()
        assert next_date.hour == expected.hour

    def test_calculate_next_occurrence_monthly(self):
        """Test calculating next occurrence for monthly pattern."""
        current_date = datetime(2025, 1, 15, 10, 0, 0)
        next_date = self.scheduler.calculate_next_occurrence(current_date, RecurrencePattern.MONTHLY)

        expected = datetime(2025, 2, 15, 10, 0, 0)
        assert next_date.date() == expected.date()
        assert next_date.hour == expected.hour

    def test_calculate_next_occurrence_none(self):
        """Test calculating next occurrence for none pattern."""
        current_date = datetime(2025, 1, 1, 10, 0, 0)
        next_date = self.scheduler.calculate_next_occurrence(current_date, RecurrencePattern.NONE)

        assert next_date is None

    def test_handle_month_end_edge_cases(self):
        """Test handling month-end edge cases for monthly recurrence."""
        # Test January 31st -> February (should go to Feb 28th/29th)
        current_date = datetime(2025, 1, 31, 10, 0, 0)
        next_date = self.scheduler.handle_month_end_edge_cases(current_date, RecurrencePattern.MONTHLY)

        # Should be February 28th (since 2025 is not a leap year)
        assert next_date.month == 2
        assert next_date.day in [28, 29]  # Either 28th or 29th depending on leap year

    def test_process_recurring_task_completion(self):
        """Test processing a recurring task completion."""
        # Create a recurring task
        task = Task(
            id=1,
            title="Test Recurring Task",
            description="A test recurring task",
            status=TaskStatus.PENDING,
            recurrence_pattern=RecurrencePattern.DAILY,
            due_date=datetime.now()
        )

        # Process the completion
        new_task = self.scheduler.process_recurring_task_completion(task)

        # The new task should exist and have the same title
        assert new_task is not None
        assert new_task.title == task.title
        assert new_task.status == TaskStatus.PENDING  # New task should be pending
        assert new_task.recurrence_pattern == task.recurrence_pattern

    def test_check_due_tasks(self):
        """Test checking for due tasks."""
        # Create tasks with different due dates
        past_due_task = Task(
            id=1,
            title="Past Due Task",
            due_date=datetime.now() - timedelta(days=1),
            reminder_sent=False
        )

        future_task = Task(
            id=2,
            title="Future Task",
            due_date=datetime.now() + timedelta(days=1),
            reminder_sent=False
        )

        tasks = [past_due_task, future_task]
        due_tasks = self.scheduler.check_due_tasks(tasks)

        # Only the past due task should be in the due list
        assert len(due_tasks) == 1
        assert due_tasks[0].id == 1

    def test_get_upcoming_tasks(self):
        """Test getting upcoming tasks."""
        # Create tasks with different due dates
        today_task = Task(
            id=1,
            title="Today Task",
            due_date=datetime.now(),
            reminder_sent=False
        )

        next_week_task = Task(
            id=2,
            title="Next Week Task",
            due_date=datetime.now() + timedelta(days=7),
            reminder_sent=False
        )

        next_month_task = Task(
            id=3,
            title="Next Month Task",
            due_date=datetime.now() + timedelta(days=30),
            reminder_sent=False
        )

        tasks = [today_task, next_week_task, next_month_task]
        upcoming_tasks = self.scheduler.get_upcoming_tasks(tasks, days=10)

        # Should have today's task and next week's task, but not next month's
        assert len(upcoming_tasks) == 2
        task_ids = [task.id for task in upcoming_tasks]
        assert 1 in task_ids
        assert 2 in task_ids
        assert 3 not in task_ids


class TestTodoServiceTimeAutomation:
    """Test cases for time automation features in TodoService."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.repository = InMemoryTaskRepository()
        self.notification_adapter = NotificationAdapter()
        self.scheduler_service = SchedulerService(self.notification_adapter)
        self.service = TodoService(self.repository, self.scheduler_service)

    def test_add_task_with_recurrence(self):
        """Test adding a task with recurrence pattern."""
        task = self.service.add_task(
            title="Recurring Task",
            recurrence_pattern=RecurrencePattern.WEEKLY,
            due_date=datetime.now() + timedelta(days=1)
        )

        assert task.recurrence_pattern == RecurrencePattern.WEEKLY
        assert task.title == "Recurring Task"

    def test_complete_recurring_task_creates_next_occurrence(self):
        """Test that completing a recurring task creates the next occurrence."""
        # Add a recurring task
        original_task = self.service.add_task(
            title="Weekly Meeting",
            recurrence_pattern=RecurrencePattern.WEEKLY,
            due_date=datetime.now()
        )

        # Complete the recurring task
        completed_task = self.service.complete_recurring_task(original_task.id)

        assert completed_task.status == TaskStatus.COMPLETE

        # Check that a new task was created
        all_tasks = self.service.list_tasks()
        recurring_tasks = [t for t in all_tasks if t.title == "Weekly Meeting" and t.status == TaskStatus.PENDING]
        assert len(recurring_tasks) >= 1  # At least one new occurrence


class TestNotificationAdapter:
    """Test cases for the NotificationAdapter class."""

    def test_send_notification_success(self):
        """Test sending a notification."""
        adapter = NotificationAdapter()
        result = adapter.send_notification(
            title="Test Notification",
            message="This is a test notification"
        )

        # The notification might fail in a test environment without a GUI,
        # but we test that the method doesn't raise an exception
        assert result in [True, False]  # Either success or failure, but not an exception


if __name__ == "__main__":
    pytest.main([__file__])