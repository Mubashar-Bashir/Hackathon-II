"""
In-memory storage implementation for the Todo CLI application.

This module provides an in-memory implementation of the TaskRepository
interface, storing tasks in a dictionary for Phase I of the application.
"""

import logging
from typing import List, Optional
from ..models.todo import Task
from . import TaskRepository

# Configure logging
logger = logging.getLogger(__name__)


class InMemoryTaskRepository(TaskRepository):
    """
    In-memory implementation of the TaskRepository interface.

    This class stores tasks in memory using a dictionary, with automatic
    ID generation for new tasks. This implementation is suitable for
    Phase I and can be replaced with a persistent storage solution in
    future phases.
    """

    def __init__(self):
        """
        Initialize the in-memory task repository.

        Creates an empty dictionary to store tasks and initializes
        the ID counter to 1.
        """
        self._tasks = {}
        self._next_id = 1

    def create_task(self, task: Task) -> Task:
        """
        Create a new task in storage.

        Args:
            task: The task to create (without a valid ID)

        Returns:
            The created task with a new, unique ID
        """
        logger.info(f"Creating new task: {task.title}")
        task_id = self._next_id
        self._next_id += 1
        new_task = task.model_copy(update={"id": task_id})
        self._tasks[task_id] = new_task
        logger.info(f"Task created successfully: {new_task.title} (ID: {new_task.id})")
        return new_task

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a task by its ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            The task if found, None otherwise
        """
        logger.debug(f"Retrieving task with ID: {task_id}")
        task = self._tasks.get(task_id)
        if task:
            logger.debug(f"Task found: {task.title} (ID: {task.id})")
        else:
            logger.debug(f"Task with ID {task_id} not found")
        return task

    def update_task(self, task_id: int, task: Task) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: The ID of the task to update
            task: The updated task object

        Returns:
            The updated task if successful, None if task doesn't exist
        """
        logger.info(f"Updating task with ID: {task_id}")
        if task_id not in self._tasks:
            logger.warning(f"Cannot update task {task_id}: task not found")
            return None
        self._tasks[task_id] = task
        logger.info(f"Task {task_id} updated successfully")
        return task

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID.

        Args:
            task_id: The ID of the task to delete

        Returns:
            True if the task was deleted, False if it didn't exist
        """
        logger.info(f"Deleting task with ID: {task_id}")
        if task_id not in self._tasks:
            logger.warning(f"Cannot delete task {task_id}: task not found")
            return False
        del self._tasks[task_id]
        logger.info(f"Task {task_id} deleted successfully")
        return True

    def list_tasks(self) -> List[Task]:
        """
        Get all tasks from storage.

        Returns:
            A list of all tasks in the repository
        """
        task_count = len(self._tasks)
        logger.info(f"Listing all tasks: {task_count} tasks found")
        return list(self._tasks.values())