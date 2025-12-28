import logging
from typing import List, Optional
from uuid import UUID

from ..models.task import TaskCreate, TaskUpdate, TaskRead
from ..storage.task_repository import TaskRepository


class TaskService:
    """
    Service for handling task operations with user validation.
    Ensures users can only access their own tasks.
    """

    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository
        self.logger = logging.getLogger(__name__)

    def get_tasks_for_user(
        self,
        user_id: UUID,
        offset: int = 0,
        limit: int = 100,
        status: Optional[str] = None
    ) -> List[TaskRead]:
        """
        Get all tasks for a specific user with optional filtering.
        """
        self.logger.debug(f"Retrieving tasks for user {user_id}, offset={offset}, limit={limit}, status={status}")

        tasks = self.task_repository.get_tasks_by_user(
            user_id=user_id,
            offset=offset,
            limit=limit,
            status=status
        )

        self.logger.info(f"Retrieved {len(tasks)} tasks for user {user_id}")
        return tasks

    def get_task_for_user(self, user_id: UUID, task_id: UUID) -> Optional[TaskRead]:
        """
        Get a specific task for a user by ID.
        Returns None if the task doesn't belong to the user.
        """
        self.logger.debug(f"Retrieving task {task_id} for user {user_id}")

        task = self.task_repository.get_task_by_user_and_id(
            user_id=user_id,
            task_id=task_id
        )

        if task:
            self.logger.debug(f"Successfully retrieved task {task_id} for user {user_id}")
        else:
            self.logger.warning(f"Task {task_id} not found or doesn't belong to user {user_id}")

        return task

    def create_task_for_user(self, task: TaskCreate, user_id: UUID) -> TaskRead:
        """
        Create a task associated with a specific user.
        """
        self.logger.info(f"Creating task for user {user_id} with title: {task.title}")

        created_task = self.task_repository.create_task_for_user(task, user_id)

        self.logger.info(f"Successfully created task {created_task.id} for user {user_id}")
        return created_task

    def update_task_for_user(
        self,
        user_id: UUID,
        task_id: UUID,
        task_update: TaskUpdate
    ) -> Optional[TaskRead]:
        """
        Update a task if it belongs to the user.
        Returns None if the user doesn't own the task.
        """
        self.logger.info(f"Updating task {task_id} for user {user_id}")

        updated_task = self.task_repository.update_task_for_user(
            user_id=user_id,
            task_id=task_id,
            task=task_update
        )

        if updated_task:
            self.logger.info(f"Successfully updated task {task_id} for user {user_id}")
        else:
            self.logger.warning(f"Failed to update task {task_id} for user {user_id} - task not found or access denied")

        return updated_task

    def delete_task_for_user(self, user_id: UUID, task_id: UUID) -> bool:
        """
        Delete a task if it belongs to the user.
        Returns True if successful, False if the user doesn't own the task.
        """
        self.logger.info(f"Deleting task {task_id} for user {user_id}")

        success = self.task_repository.delete_task_for_user(
            user_id=user_id,
            task_id=task_id
        )

        if success:
            self.logger.info(f"Successfully deleted task {task_id} for user {user_id}")
        else:
            self.logger.warning(f"Failed to delete task {task_id} for user {user_id} - task not found or access denied")

        return success

    def toggle_task_completion(self, user_id: UUID, task_id: UUID) -> Optional[TaskRead]:
        """
        Toggle the completion status of a task for a user.
        Returns the updated task if successful, None if the user doesn't own the task.
        """
        self.logger.info(f"Toggling completion status for task {task_id} for user {user_id}")

        # Get the current task
        current_task = self.task_repository.get_task_by_user_and_id(user_id, task_id)
        if not current_task:
            self.logger.warning(f"Failed to toggle completion for task {task_id} - task not found or access denied")
            return None

        # Determine the new status
        new_status = "completed" if current_task.status != "completed" else "in_progress"
        self.logger.debug(f"Changing task {task_id} status from {current_task.status} to {new_status}")

        # Update the task status
        task_update = TaskUpdate(status=new_status)
        updated_task = self.task_repository.update_task_for_user(user_id, task_id, task_update)

        if updated_task:
            self.logger.info(f"Successfully toggled completion status for task {task_id} - new status: {updated_task.status}")
        else:
            self.logger.error(f"Failed to update task {task_id} status after toggle operation")

        return updated_task