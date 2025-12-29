from fastapi.testclient import TestClient
import pytest
from unittest.mock import Mock, patch
from uuid import uuid4

from src.models.task import TaskCreate, TaskUpdate, TaskRead
from src.services.task_service import TaskService
from src.storage.task_repository import TaskRepository


def test_get_tasks_for_user():
    """Test getting tasks for a specific user"""
    # Mock the task repository
    mock_task_repo = Mock(spec=TaskRepository)

    # Create mock tasks to return
    mock_tasks = [
        TaskRead(
            id=uuid4(),
            title="Test Task 1",
            description="Description 1",
            status="pending",
            priority="medium",
            user_id=uuid4(),
            created_at=None,
            updated_at=None
        )
    ]
    mock_task_repo.get_tasks_by_user.return_value = mock_tasks

    # Create task service with mock repository
    task_service = TaskService(mock_task_repo)

    # Call get_tasks_for_user
    user_id = uuid4()
    result = task_service.get_tasks_for_user(user_id)

    # Assertions
    assert result is not None
    assert len(result) == 1
    assert result[0].title == "Test Task 1"
    mock_task_repo.get_tasks_by_user.assert_called_once_with(
        user_id=user_id,
        offset=0,
        limit=100,
        status=None
    )


def test_get_task_for_user_success():
    """Test getting a specific task for a user"""
    # Mock the task repository
    mock_task_repo = Mock(spec=TaskRepository)

    # Create a mock task to return
    mock_task = TaskRead(
        id=uuid4(),
        title="Test Task",
        description="Description",
        status="pending",
        priority="medium",
        user_id=uuid4(),
        created_at=None,
        updated_at=None
    )
    mock_task_repo.get_task_by_user_and_id.return_value = mock_task

    # Create task service with mock repository
    task_service = TaskService(mock_task_repo)

    # Call get_task_for_user
    user_id = uuid4()
    task_id = uuid4()
    result = task_service.get_task_for_user(user_id, task_id)

    # Assertions
    assert result is not None
    assert result.title == "Test Task"
    mock_task_repo.get_task_by_user_and_id.assert_called_once_with(
        user_id=user_id,
        task_id=task_id
    )


def test_get_task_for_user_not_found():
    """Test getting a task that doesn't belong to the user"""
    # Mock the task repository
    mock_task_repo = Mock(spec=TaskRepository)
    mock_task_repo.get_task_by_user_and_id.return_value = None  # Task not found

    # Create task service with mock repository
    task_service = TaskService(mock_task_repo)

    # Call get_task_for_user
    user_id = uuid4()
    task_id = uuid4()
    result = task_service.get_task_for_user(user_id, task_id)

    # Assertions
    assert result is None
    mock_task_repo.get_task_by_user_and_id.assert_called_once_with(
        user_id=user_id,
        task_id=task_id
    )


def test_create_task_for_user():
    """Test creating a task for a user"""
    # Mock the task repository
    mock_task_repo = Mock(spec=TaskRepository)

    # Create a mock task to return
    created_task = TaskRead(
        id=uuid4(),
        title="New Task",
        description="New Description",
        status="pending",
        priority="medium",
        user_id=uuid4(),
        created_at=None,
        updated_at=None
    )
    mock_task_repo.create_task_for_user.return_value = created_task

    # Create task service with mock repository
    task_service = TaskService(mock_task_repo)

    # Create task data
    task_data = TaskCreate(
        title="New Task",
        description="New Description",
        status="pending",
        priority="medium",
        user_id=uuid4()
    )

    # Call create_task_for_user
    result = task_service.create_task_for_user(task_data)

    # Assertions
    assert result is not None
    assert result.title == "New Task"
    mock_task_repo.create_task_for_user.assert_called_once()


def test_update_task_for_user_success():
    """Test updating a task that belongs to the user"""
    # Mock the task repository
    mock_task_repo = Mock(spec=TaskRepository)

    # Create a mock updated task to return
    updated_task = TaskRead(
        id=uuid4(),
        title="Updated Task",
        description="Updated Description",
        status="in_progress",
        priority="high",
        user_id=uuid4(),
        created_at=None,
        updated_at=None
    )
    mock_task_repo.update_task_for_user.return_value = updated_task

    # Create task service with mock repository
    task_service = TaskService(mock_task_repo)

    # Create task update data
    task_update = TaskUpdate(
        title="Updated Task",
        description="Updated Description",
        status="in_progress",
        priority="high"
    )

    # Call update_task_for_user
    user_id = uuid4()
    task_id = uuid4()
    result = task_service.update_task_for_user(user_id, task_id, task_update)

    # Assertions
    assert result is not None
    assert result.title == "Updated Task"
    mock_task_repo.update_task_for_user.assert_called_once_with(
        user_id=user_id,
        task_id=task_id,
        task=task_update
    )


def test_update_task_for_user_not_found():
    """Test updating a task that doesn't belong to the user"""
    # Mock the task repository
    mock_task_repo = Mock(spec=TaskRepository)
    mock_task_repo.update_task_for_user.return_value = None  # Update failed

    # Create task service with mock repository
    task_service = TaskService(mock_task_repo)

    # Create task update data
    task_update = TaskUpdate(
        title="Updated Task",
        description="Updated Description",
        status="in_progress",
        priority="high"
    )

    # Call update_task_for_user
    user_id = uuid4()
    task_id = uuid4()
    result = task_service.update_task_for_user(user_id, task_id, task_update)

    # Assertions
    assert result is None
    mock_task_repo.update_task_for_user.assert_called_once_with(
        user_id=user_id,
        task_id=task_id,
        task=task_update
    )


def test_delete_task_for_user_success():
    """Test deleting a task that belongs to the user"""
    # Mock the task repository
    mock_task_repo = Mock(spec=TaskRepository)
    mock_task_repo.delete_task_for_user.return_value = True  # Deletion successful

    # Create task service with mock repository
    task_service = TaskService(mock_task_repo)

    # Call delete_task_for_user
    user_id = uuid4()
    task_id = uuid4()
    result = task_service.delete_task_for_user(user_id, task_id)

    # Assertions
    assert result is True
    mock_task_repo.delete_task_for_user.assert_called_once_with(
        user_id=user_id,
        task_id=task_id
    )


def test_delete_task_for_user_not_found():
    """Test deleting a task that doesn't belong to the user"""
    # Mock the task repository
    mock_task_repo = Mock(spec=TaskRepository)
    mock_task_repo.delete_task_for_user.return_value = False  # Deletion failed

    # Create task service with mock repository
    task_service = TaskService(mock_task_repo)

    # Call delete_task_for_user
    user_id = uuid4()
    task_id = uuid4()
    result = task_service.delete_task_for_user(user_id, task_id)

    # Assertions
    assert result is False
    mock_task_repo.delete_task_for_user.assert_called_once_with(
        user_id=user_id,
        task_id=task_id
    )