"""
Business logic service for the Todo CLI application.

This module provides the core business logic for managing tasks,
including adding, updating, deleting, and querying tasks.
"""

import logging
from typing import List, Optional
from ..models.todo import Task, TaskStatus
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

    def add_task(self, title: str, description: str = "") -> Task:
        """
        Add a new task with the given title and description.

        Args:
            title: The title of the new task
            description: The description of the new task (optional)

        Returns:
            The created task with a unique ID
        """
        logger.info(f"Adding new task: {title}")
        # Create a temporary task with a placeholder ID, it will be assigned a real ID by the repository
        temp_task = Task(
            id=0,  # Will be replaced by the repository
            title=title,
            description=description,
            status=TaskStatus.PENDING
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

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None, status: Optional[TaskStatus] = None) -> Optional[Task]:
        """
        Update a task's properties.

        Args:
            task_id: The ID of the task to update
            title: New title for the task (optional)
            description: New description for the task (optional)
            status: New status for the task (optional)

        Returns:
            The updated task if successful, None if task doesn't exist
        """
        logger.info(f"Updating task {task_id} with title={title}, description={description}, status={status}")
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

        # Update the task with the new values
        updated_task_data = existing_task.model_dump()
        updated_task_data.update(updates)
        updated_task = Task(**updated_task_data)

        updated_task = self.repository.update_task(task_id, updated_task)
        if updated_task:
            logger.info(f"Task {task_id} updated successfully")
        return updated_task

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