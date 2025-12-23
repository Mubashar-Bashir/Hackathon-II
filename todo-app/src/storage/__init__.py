"""Storage package for Todo App."""

from abc import ABC, abstractmethod
from typing import List, Optional
from ..models.todo import Task


class TaskRepository(ABC):
    @abstractmethod
    def create_task(self, task: Task) -> Task:
        """Create a new task in storage"""
        pass

    @abstractmethod
    def get_task(self, task_id: int) -> Optional[Task]:
        """Retrieve task by ID"""
        pass

    @abstractmethod
    def update_task(self, task_id: int, task: Task) -> Optional[Task]:
        """Update existing task"""
        pass

    @abstractmethod
    def delete_task(self, task_id: int) -> bool:
        """Delete task by ID"""
        pass

    @abstractmethod
    def list_tasks(self) -> List[Task]:
        """Get all tasks from storage"""
        pass