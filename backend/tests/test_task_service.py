import pytest
from unittest.mock import Mock
from uuid import UUID
from src.services.task_service import TaskService
from src.models.task import TaskCreate, TaskUpdate, TaskRead
from src.storage.task_repository import TaskRepository


def test_get_tasks_for_user():
    """Test getting tasks for a user"""
    # Mock the task repository
    mock_task_repo = Mock(spec=TaskRepository)

    # Mock tasks
    task1 = TaskRead(
        id=UUID("12345678-1234-5678-1234-567812345678"),
        title="Task 1",
        description="Description 1",
        status="pending",
        priority="medium",
        user_id=UUID("87654321-4321-8765-4321-876543214321")
    )
    task2 = TaskRead(
        id=UUID("87654321-4321-8765-4321-876543214321"),
        title="Task 2",
        description="Description 2",
        status="completed",
        priority="high",
        user_id=UUID("87654321-4321-8765-4321-876543214321")
    )
    mock_task_repo.get_tasks_by_user.return_value = [task1, task2]

    # Create task service with mocked repository
    task_service = TaskService(mock_task_repo)

    # Call get_tasks_for_user
    user_id = UUID("87654321-4321-8765-4321-876543214321")
    result = task_service.get_tasks_for_user(user_id)

    # Assertions
    assert len(result) == 2
    assert result[0] == task1
    assert result[1] == task2
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

    # Mock task
    task = TaskRead(
        id=UUID("12345678-1234-5678-1234-567812345678"),
        title="Task 1",
        description="Description 1",
        status="pending",
        priority="medium",
        user_id=UUID("87654321-4321-8765-4321-876543214321")
    )
    mock_task_repo.get_task_by_user_and_id.return_value = task

    # Create task service with mocked repository
    task_service = TaskService(mock_task_repo)

    # Call get_task_for_user
    user_id = UUID("87654321-4321-8765-4321-876543214321")
    task_id = UUID("12345678-1234-5678-1234-567812345678")
    result = task_service.get_task_for_user(user_id, task_id)

    # Assertions
    assert result == task
    mock_task_repo.get_task_by_user_and_id.assert_called_once_with(
        user_id=user_id,
        task_id=task_id
    )


def test_get_task_for_user_not_found():
    """Test getting a task that doesn't belong to the user"""
    # Mock the task repository
    mock_task_repo = Mock(spec=TaskRepository)
    mock_task_repo.get_task_by_user_and_id.return_value = None

    # Create task service with mocked repository
    task_service = TaskService(mock_task_repo)

    # Call get_task_for_user
    user_id = UUID("87654321-4321-8765-4321-876543214321")
    task_id = UUID("12345678-1234-5678-1234-567812345678")
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

    # Mock task creation
    created_task = TaskRead(
        id=UUID("12345678-1234-5678-1234-567812345678"),
        title="New Task",
        description="New Description",
        status="pending",
        priority="medium",
        user_id=UUID("87654321-4321-8765-4321-876543214321")
    )
    mock_task_repo.create_task_for_user.return_value = created_task

    # Create task service with mocked repository
    task_service = TaskService(mock_task_repo)

    # Create task data
    task_data = TaskCreate(
        title="New Task",
        description="New Description",
        status="pending",
        priority="medium"
    )

    # Call create_task_for_user
    user_id = UUID("87654321-4321-8765-4321-876543214321")
    result = task_service.create_task_for_user(task_data, user_id)

    # Assertions
    assert result == created_task
    mock_task_repo.create_task_for_user.assert_called_once_with(task_data, user_id)


def test_update_task_for_user_success():
    """Test updating a task for a user"""
    # Mock the task repository
    mock_task_repo = Mock(spec=TaskRepository)

    # Mock updated task
    updated_task = TaskRead(
        id=UUID("12345678-1234-5678-1234-567812345678"),
        title="Updated Task",
        description="Updated Description",
        status="completed",
        priority="high",
        user_id=UUID("87654321-4321-8765-4321-876543214321")
    )
    mock_task_repo.update_task_for_user.return_value = updated_task

    # Create task service with mocked repository
    task_service = TaskService(mock_task_repo)

    # Create task update data
    task_update = TaskUpdate(
        title="Updated Task",
        status="completed",
        priority="high"
    )

    # Call update_task_for_user
    user_id = UUID("87654321-4321-8765-4321-876543214321")
    task_id = UUID("12345678-1234-5678-1234-567812345678")
    result = task_service.update_task_for_user(user_id, task_id, task_update)

    # Assertions
    assert result == updated_task
    mock_task_repo.update_task_for_user.assert_called_once_with(
        user_id=user_id,
        task_id=task_id,
        task=task_update
    )


def test_update_task_for_user_not_found():
    """Test updating a task that doesn't belong to the user"""
    # Mock the task repository
    mock_task_repo = Mock(spec=TaskRepository)
    mock_task_repo.update_task_for_user.return_value = None

    # Create task service with mocked repository
    task_service = TaskService(mock_task_repo)

    # Create task update data
    task_update = TaskUpdate(
        title="Updated Task",
        status="completed",
        priority="high"
    )

    # Call update_task_for_user
    user_id = UUID("87654321-4321-8765-4321-876543214321")
    task_id = UUID("12345678-1234-5678-1234-567812345678")
    result = task_service.update_task_for_user(user_id, task_id, task_update)

    # Assertions
    assert result is None
    mock_task_repo.update_task_for_user.assert_called_once_with(
        user_id=user_id,
        task_id=task_id,
        task=task_update
    )


def test_delete_task_for_user_success():
    """Test deleting a task for a user"""
    # Mock the task repository
    mock_task_repo = Mock(spec=TaskRepository)
    mock_task_repo.delete_task_for_user.return_value = True

    # Create task service with mocked repository
    task_service = TaskService(mock_task_repo)

    # Call delete_task_for_user
    user_id = UUID("87654321-4321-8765-4321-876543214321")
    task_id = UUID("12345678-1234-5678-1234-567812345678")
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
    mock_task_repo.delete_task_for_user.return_value = False

    # Create task service with mocked repository
    task_service = TaskService(mock_task_repo)

    # Call delete_task_for_user
    user_id = UUID("87654321-4321-8765-4321-876543214321")
    task_id = UUID("12345678-1234-5678-1234-567812345678")
    result = task_service.delete_task_for_user(user_id, task_id)

    # Assertions
    assert result is False
    mock_task_repo.delete_task_for_user.assert_called_once_with(
        user_id=user_id,
        task_id=task_id
    )


def test_toggle_task_completion_success():
    """Test toggling task completion status"""
    # Mock the task repository
    mock_task_repo = Mock(spec=TaskRepository)

    # Mock current task (pending)
    current_task = TaskRead(
        id=UUID("12345678-1234-5678-1234-567812345678"),
        title="Test Task",
        description="Test Description",
        status="pending",
        priority="medium",
        user_id=UUID("87654321-4321-8765-4321-876543214321")
    )
    mock_task_repo.get_task_by_user_and_id.return_value = current_task

    # Mock updated task (completed)
    updated_task = TaskRead(
        id=UUID("12345678-1234-5678-1234-567812345678"),
        title="Test Task",
        description="Test Description",
        status="completed",  # Changed to completed
        priority="medium",
        user_id=UUID("87654321-4321-8765-4321-876543214321")
    )
    mock_task_repo.update_task_for_user.return_value = updated_task

    # Create task service with mocked repository
    task_service = TaskService(mock_task_repo)

    # Call toggle_task_completion
    user_id = UUID("87654321-4321-8765-4321-876543214321")
    task_id = UUID("12345678-1234-5678-1234-567812345678")
    result = task_service.toggle_task_completion(user_id, task_id)

    # Assertions
    assert result == updated_task
    assert result.status == "completed"  # Status should be toggled to completed
    mock_task_repo.get_task_by_user_and_id.assert_called_once_with(user_id, task_id)
    # update_task_for_user should be called with status="completed"
    mock_task_repo.update_task_for_user.assert_called_once()


def test_toggle_task_completion_not_found():
    """Test toggling completion for a task that doesn't exist"""
    # Mock the task repository
    mock_task_repo = Mock(spec=TaskRepository)
    mock_task_repo.get_task_by_user_and_id.return_value = None

    # Create task service with mocked repository
    task_service = TaskService(mock_task_repo)

    # Call toggle_task_completion
    user_id = UUID("87654321-4321-8765-4321-876543214321")
    task_id = UUID("12345678-1234-5678-1234-567812345678")
    result = task_service.toggle_task_completion(user_id, task_id)

    # Assertions
    assert result is None
    mock_task_repo.get_task_by_user_and_id.assert_called_once_with(user_id, task_id)
    mock_task_repo.update_task_for_user.assert_not_called()