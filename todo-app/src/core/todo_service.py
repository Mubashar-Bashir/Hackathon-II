"""
Business logic service for the Todo CLI application.

This module provides the core business logic for managing tasks,
including adding, updating, deleting, and querying tasks.
"""

import logging
from typing import List, Optional
from datetime import datetime
from ..models.todo import Task, TaskStatus, Priority, TaskFilter, SortCriteria, SortField, SortOrder
from ..storage.in_memory_storage import InMemoryTaskRepository
from ..storage import TaskRepository

# Configure logging
logger = logging.getLogger(__name__)


class TodoService:
    """
    Service class that implements the business logic for task management.

    This class acts as an intermediary between the UI layer and the
    storage layer, handling all business logic related to task management.
    """

    def __init__(self, repository: TaskRepository):
        """
        Initialize the TodoService with a repository.

        Args:
            repository: An implementation of TaskRepository to handle data storage
        """
        self.repository = repository

    def add_task(self, title: str, description: str = "", priority: Optional[Priority] = Priority.MEDIUM, tags: Optional[List[str]] = None, due_date: Optional[datetime] = None) -> Task:
        """
        Add a new task with the given title and optional organization features.

        Args:
            title: The title of the new task
            description: The description of the new task (optional)
            priority: Priority level (Low, Medium, High; defaults to Medium)
            tags: List of tags for categorization (defaults to empty list)
            due_date: Optional due date (defaults to None)

        Returns:
            The created task with a unique ID and all organization fields
        """
        logger.info(f"Adding new task: {title}")
        # Create a temporary task with a placeholder ID, it will be assigned a real ID by the repository
        temp_task = Task(
            id=0,  # Will be replaced by the repository
            title=title,
            description=description,
            status=TaskStatus.PENDING,
            priority=priority or Priority.MEDIUM,
            tags=tags or [],
            due_date=due_date
        )
        task = self.repository.create_task(temp_task)
        logger.info(f"Task added successfully: {task.title} (ID: {task.id})")
        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Get a task by its ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            The task if found, None otherwise
        """
        logger.debug(f"Retrieving task with ID: {task_id}")
        task = self.repository.get_task(task_id)
        if task:
            logger.debug(f"Task found: {task.title} (ID: {task.id})")
        else:
            logger.warning(f"Task with ID {task_id} not found")
        return task

    def list_tasks(self) -> List[Task]:
        """
        Get all tasks.

        Returns:
            A list of all tasks in the repository
        """
        logger.info("Listing all tasks")
        tasks = self.repository.list_tasks()
        logger.info(f"Retrieved {len(tasks)} tasks")
        return tasks

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None, status: Optional[TaskStatus] = None, priority: Optional[Priority] = None, tags: Optional[List[str]] = None, due_date: Optional[datetime] = None) -> Optional[Task]:
        """
        Update a task's properties.

        Args:
            task_id: The ID of the task to update
            title: New title for the task (optional)
            description: New description for the task (optional)
            status: New status for the task (optional)
            priority: New priority for the task (optional)
            tags: New tags for the task (optional)
            due_date: New due date for the task (optional)

        Returns:
            The updated task if successful, None if task doesn't exist
        """
        logger.info(f"Updating task {task_id} with title={title}, description={description}, status={status}, priority={priority}, tags={tags}, due_date={due_date}")
        existing_task = self.repository.get_task(task_id)
        if not existing_task:
            logger.warning(f"Cannot update task {task_id}: task not found")
            return None

        # Prepare updates
        updates = {}
        if title is not None:
            updates["title"] = title
        if description is not None:
            updates["description"] = description
        if status is not None:
            updates["status"] = status
        if priority is not None:
            updates["priority"] = priority
        if tags is not None:
            updates["tags"] = tags
        if due_date is not None:
            updates["due_date"] = due_date

        # Update the task with the new values
        updated_task_data = existing_task.model_dump()
        updated_task_data.update(updates)
        updated_task = Task(**updated_task_data)

        updated_task = self.repository.update_task(task_id, updated_task)
        if updated_task:
            logger.info(f"Task {task_id} updated successfully")
        return updated_task

    def filter_tasks(self, status: Optional[TaskStatus] = None, priority: Optional[Priority] = None, tags: Optional[List[str]] = None, search_keyword: Optional[str] = None) -> List[Task]:
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
        logger.info(f"Filtering tasks with status={status}, priority={priority}, tags={tags}, search_keyword={search_keyword}")
        all_tasks = self.repository.list_tasks()
        filtered_tasks = []

        for task in all_tasks:
            # Check status filter
            if status is not None and task.status != status:
                continue

            # Check priority filter
            if priority is not None and task.priority != priority:
                continue

            # Check tags filter - task must have ALL specified tags
            if tags is not None and not all(tag in task.tags for tag in tags):
                continue

            # Check search keyword filter - match in title or description
            if search_keyword is not None:
                search_lower = search_keyword.lower()
                if search_lower not in task.title.lower() and search_lower not in task.description.lower():
                    continue

            # If we reach here, the task matches all specified criteria
            filtered_tasks.append(task)

        logger.info(f"Filtered {len(all_tasks)} tasks down to {len(filtered_tasks)} tasks")
        return filtered_tasks

    def sort_tasks(self, tasks: List[Task], sort_field: SortField, sort_order: SortOrder = SortOrder.ASC) -> List[Task]:
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
        logger.info(f"Sorting {len(tasks)} tasks by {sort_field} in {sort_order} order")

        def sort_key(task):
            if sort_field == SortField.DUE_DATE:
                # For due_date, None values should be sorted last
                if task.due_date is None:
                    # Return a high value to sort None dates last
                    # For both ascending and descending, None should be last
                    return (1, datetime.max)  # None values get high priority, pushing them to end
                else:
                    return (0, task.due_date)  # Non-None values get low priority, keeping them first
            elif sort_field == SortField.PRIORITY:
                # Define priority order: HIGH > MEDIUM > LOW (for descending)
                priority_order = {Priority.HIGH: 3, Priority.MEDIUM: 2, Priority.LOW: 1}
                value = priority_order[task.priority]
                return -value if sort_order == SortOrder.DESC else value
            elif sort_field == SortField.STATUS:
                # Define status order: COMPLETE > PENDING (for descending)
                status_order = {TaskStatus.COMPLETE: 2, TaskStatus.PENDING: 1}
                value = status_order[task.status]
                return -value if sort_order == SortOrder.DESC else value
            else:
                # For other fields (title, created_at), use standard comparison
                value = getattr(task, sort_field.value)
                return value

        # Sort based on the key function
        reverse_sort = (sort_order == SortOrder.DESC and sort_field != SortField.DUE_DATE)
        sorted_tasks = sorted(tasks, key=sort_key, reverse=reverse_sort)

        # Special handling for due_date descending: None values should still be last
        if sort_field == SortField.DUE_DATE and sort_order == SortOrder.DESC:
            # Re-sort to ensure None values are at the end even in descending order
            non_none_tasks = [task for task in sorted_tasks if task.due_date is not None]
            none_tasks = [task for task in sorted_tasks if task.due_date is None]
            # Sort non-None tasks in descending order, then append None tasks
            non_none_sorted = sorted(non_none_tasks,
                                   key=lambda t: getattr(t, sort_field.value),
                                   reverse=True)
            sorted_tasks = non_none_sorted + none_tasks

        logger.info(f"Tasks sorted successfully")
        return sorted_tasks

    def list_tasks(self, status: Optional[TaskStatus] = None, priority: Optional[Priority] = None, tags: Optional[List[str]] = None, search_keyword: Optional[str] = None, sort_field: Optional[SortField] = None, sort_order: SortOrder = SortOrder.ASC) -> List[Task]:
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
        logger.info(f"Listing tasks with filters: status={status}, priority={priority}, tags={tags}, search_keyword={search_keyword}, sort_field={sort_field}, sort_order={sort_order}")

        # Start with filtered tasks
        if any([status, priority, tags, search_keyword]):
            tasks = self.filter_tasks(status=status, priority=priority, tags=tags, search_keyword=search_keyword)
        else:
            tasks = self.repository.list_tasks()

        # Apply sorting if requested
        if sort_field is not None:
            tasks = self.sort_tasks(tasks, sort_field, sort_order)

        logger.info(f"Returning {len(tasks)} tasks")
        return tasks

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID.

        Args:
            task_id: The ID of the task to delete

        Returns:
            True if the task was deleted, False if it didn't exist
        """
        logger.info(f"Deleting task with ID: {task_id}")
        success = self.repository.delete_task(task_id)
        if success:
            logger.info(f"Task {task_id} deleted successfully")
        else:
            logger.warning(f"Cannot delete task {task_id}: task not found")
        return success

    def toggle_task_status(self, task_id: int) -> Optional[Task]:
        """
        Toggle a task's status between PENDING and COMPLETE.

        Args:
            task_id: The ID of the task to toggle

        Returns:
            The updated task if successful, None if task doesn't exist
        """
        logger.info(f"Toggling status for task {task_id}")
        task = self.get_task(task_id)
        if not task:
            logger.warning(f"Cannot toggle status for task {task_id}: task not found")
            return None

        new_status = TaskStatus.COMPLETE if task.status == TaskStatus.PENDING else TaskStatus.PENDING
        logger.debug(f"Task {task_id} status changing from {task.status} to {new_status}")
        updated_task = self.update_task(task_id, status=new_status)
        if updated_task:
            logger.info(f"Task {task_id} status toggled successfully to {new_status}")
        return updated_task