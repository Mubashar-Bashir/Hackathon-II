from typing import List, Optional
from uuid import UUID
from sqlmodel import Session, select

from .base_repository import BaseRepository
from ..models.task import Task, TaskRead, TaskCreate, TaskUpdate


class TaskRepository(BaseRepository[Task, TaskRead, TaskCreate, TaskUpdate]):
    """
    Repository for Task operations with user filtering capabilities.
    Implements data isolation between users.
    """

    def __init__(self, session: Session):
        super().__init__(session)

    @property
    def model(self) -> type[Task]:
        return Task

    @property
    def read_model(self) -> type[TaskRead]:
        return TaskRead

    def get_tasks_by_user(self, user_id: UUID, offset: int = 0, limit: int = 100, status: Optional[str] = None) -> List[TaskRead]:
        """Get all tasks for a specific user with optional status filtering"""
        statement = select(Task).where(Task.user_id == user_id)

        if status:
            statement = statement.where(Task.status == status)

        statement = statement.offset(offset).limit(limit)
        results = self.session.exec(statement).all()
        return [TaskRead.model_validate(obj) for obj in results]

    def get_task_by_user_and_id(self, user_id: UUID, task_id: UUID) -> Optional[TaskRead]:
        """Get a specific task for a user by ID (ensures user owns the task)"""
        statement = select(Task).where(Task.user_id == user_id, Task.id == task_id)
        result = self.session.exec(statement).first()
        if result:
            return TaskRead.model_validate(result)
        return None

    def create_task_for_user(self, task: TaskCreate, user_id: UUID) -> TaskRead:
        """Create a task associated with a specific user"""
        # Create a Task object from TaskCreate data and add the user_id
        db_task = Task(
            **task.model_dump(),
            user_id=user_id
        )
        self.session.add(db_task)
        self.session.commit()
        self.session.refresh(db_task)
        return TaskRead.model_validate(db_task)

    def update_task_for_user(self, user_id: UUID, task_id: UUID, task: TaskUpdate) -> Optional[TaskRead]:
        """Update a task if it belongs to the user"""
        db_task = self.session.get(Task, task_id)
        if not db_task or db_task.user_id != user_id:
            return None

        update_data = task.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_task, field, value)

        self.session.add(db_task)
        self.session.commit()
        self.session.refresh(db_task)
        return TaskRead.model_validate(db_task)

    def delete_task_for_user(self, user_id: UUID, task_id: UUID) -> bool:
        """Delete a task if it belongs to the user"""
        db_task = self.session.get(Task, task_id)
        if not db_task or db_task.user_id != user_id:
            return False

        self.session.delete(db_task)
        self.session.commit()
        return True