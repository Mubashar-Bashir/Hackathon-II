from fastapi.testclient import TestClient
import pytest
from unittest.mock import Mock, patch
from uuid import uuid4

from src.main import app
from src.models.task import TaskCreate, TaskUpdate, TaskRead
from src.services.task_service import TaskService
from src.storage.task_repository import TaskRepository


def test_get_tasks_success():
    """Test getting tasks for authenticated user"""
    client = TestClient(app)

    # Mock the task service
    with patch('src.api.tasks.authenticate_user_from_token') as mock_auth_token, \
         patch('src.api.tasks.get_task_service') as mock_get_task_service:

        # Mock token authentication
        mock_token_data = Mock()
        mock_token_data.user_id = str(uuid4())
        mock_token_data.email = "test@example.com"
        mock_auth_token.return_value = mock_token_data

        # Mock task service
        mock_task_service = Mock(spec=TaskService)
        mock_task_service.get_tasks_for_user.return_value = [
            TaskRead(
                id=uuid4(),
                title="Test Task",
                description="Test Description",
                status="pending",
                priority="medium",
                due_date=None,
                user_id=uuid4(),
                created_at=None,
                updated_at=None
            )
        ]
        mock_get_task_service.return_value = lambda: mock_task_service

        response = client.get(
            "/tasks",
            headers={"Authorization": "Bearer fake-jwt-token"}
        )

        assert response.status_code == 200
        data = response.json()
        assert "tasks" in data
        assert len(data["tasks"]) == 1
        assert data["tasks"][0]["title"] == "Test Task"


def test_create_task_success():
    """Test creating a task for authenticated user"""
    client = TestClient(app)

    # Mock the task service
    with patch('src.api.tasks.authenticate_user_from_token') as mock_auth_token, \
         patch('src.api.tasks.get_task_service') as mock_get_task_service:

        # Mock token authentication
        mock_token_data = Mock()
        mock_token_data.user_id = str(uuid4())
        mock_token_data.email = "test@example.com"
        mock_auth_token.return_value = mock_token_data

        # Mock task service
        mock_task_service = Mock(spec=TaskService)
        mock_task_service.create_task_for_user.return_value = TaskRead(
            id=uuid4(),
            title="New Task",
            description="New Description",
            status="pending",
            priority="medium",
            due_date=None,
            user_id=uuid4(),
            created_at=None,
            updated_at=None
        )
        mock_get_task_service.return_value = lambda: mock_task_service

        response = client.post(
            "/tasks",
            json={
                "title": "New Task",
                "description": "New Description",
                "status": "pending",
                "priority": "medium"
            },
            headers={"Authorization": "Bearer fake-jwt-token"}
        )

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "New Task"


def test_get_task_by_id_success():
    """Test getting a specific task by ID for authenticated user"""
    client = TestClient(app)

    # Mock the task service
    with patch('src.api.tasks.authenticate_user_from_token') as mock_auth_token, \
         patch('src.api.tasks.get_task_service') as mock_get_task_service:

        # Mock token authentication
        mock_token_data = Mock()
        mock_token_data.user_id = str(uuid4())
        mock_token_data.email = "test@example.com"
        mock_auth_token.return_value = mock_token_data

        # Mock task service
        mock_task_service = Mock(spec=TaskService)
        mock_task_service.get_task_for_user.return_value = TaskRead(
            id=uuid4(),
            title="Test Task",
            description="Test Description",
            status="pending",
            priority="medium",
            due_date=None,
            user_id=uuid4(),
            created_at=None,
            updated_at=None
        )
        mock_get_task_service.return_value = lambda: mock_task_service

        task_id = str(uuid4())
        response = client.get(
            f"/tasks/{task_id}",
            headers={"Authorization": "Bearer fake-jwt-token"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test Task"


def test_get_task_by_id_not_found():
    """Test getting a task that doesn't exist or belong to user"""
    client = TestClient(app)

    # Mock the task service
    with patch('src.api.tasks.authenticate_user_from_token') as mock_auth_token, \
         patch('src.api.tasks.get_task_service') as mock_get_task_service:

        # Mock token authentication
        mock_token_data = Mock()
        mock_token_data.user_id = str(uuid4())
        mock_token_data.email = "test@example.com"
        mock_auth_token.return_value = mock_token_data

        # Mock task service - return None (task not found)
        mock_task_service = Mock(spec=TaskService)
        mock_task_service.get_task_for_user.return_value = None
        mock_get_task_service.return_value = lambda: mock_task_service

        task_id = str(uuid4())
        response = client.get(
            f"/tasks/{task_id}",
            headers={"Authorization": "Bearer fake-jwt-token"}
        )

        assert response.status_code == 404


def test_update_task_success():
    """Test updating a task for authenticated user"""
    client = TestClient(app)

    # Mock the task service
    with patch('src.api.tasks.authenticate_user_from_token') as mock_auth_token, \
         patch('src.api.tasks.get_task_service') as mock_get_task_service:

        # Mock token authentication
        mock_token_data = Mock()
        mock_token_data.user_id = str(uuid4())
        mock_token_data.email = "test@example.com"
        mock_auth_token.return_value = mock_token_data

        # Mock task service
        mock_task_service = Mock(spec=TaskService)
        mock_task_service.update_task_for_user.return_value = TaskRead(
            id=uuid4(),
            title="Updated Task",
            description="Updated Description",
            status="in_progress",
            priority="high",
            due_date=None,
            user_id=uuid4(),
            created_at=None,
            updated_at=None
        )
        mock_get_task_service.return_value = lambda: mock_task_service

        task_id = str(uuid4())
        response = client.put(
            f"/tasks/{task_id}",
            json={
                "title": "Updated Task",
                "description": "Updated Description",
                "status": "in_progress",
                "priority": "high"
            },
            headers={"Authorization": "Bearer fake-jwt-token"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Task"


def test_update_task_not_found():
    """Test updating a task that doesn't exist or belong to user"""
    client = TestClient(app)

    # Mock the task service
    with patch('src.api.tasks.authenticate_user_from_token') as mock_auth_token, \
         patch('src.api.tasks.get_task_service') as mock_get_task_service:

        # Mock token authentication
        mock_token_data = Mock()
        mock_token_data.user_id = str(uuid4())
        mock_token_data.email = "test@example.com"
        mock_auth_token.return_value = mock_token_data

        # Mock task service - return None (task not found)
        mock_task_service = Mock(spec=TaskService)
        mock_task_service.update_task_for_user.return_value = None
        mock_get_task_service.return_value = lambda: mock_task_service

        task_id = str(uuid4())
        response = client.put(
            f"/tasks/{task_id}",
            json={
                "title": "Updated Task",
                "description": "Updated Description",
                "status": "in_progress",
                "priority": "high"
            },
            headers={"Authorization": "Bearer fake-jwt-token"}
        )

        assert response.status_code == 404


def test_delete_task_success():
    """Test deleting a task for authenticated user"""
    client = TestClient(app)

    # Mock the task service
    with patch('src.api.tasks.authenticate_user_from_token') as mock_auth_token, \
         patch('src.api.tasks.get_task_service') as mock_get_task_service:

        # Mock token authentication
        mock_token_data = Mock()
        mock_token_data.user_id = str(uuid4())
        mock_token_data.email = "test@example.com"
        mock_auth_token.return_value = mock_token_data

        # Mock task service
        mock_task_service = Mock(spec=TaskService)
        mock_task_service.delete_task_for_user.return_value = True
        mock_get_task_service.return_value = lambda: mock_task_service

        task_id = str(uuid4())
        response = client.delete(
            f"/tasks/{task_id}",
            headers={"Authorization": "Bearer fake-jwt-token"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Task deleted successfully"


def test_delete_task_not_found():
    """Test deleting a task that doesn't exist or belong to user"""
    client = TestClient(app)

    # Mock the task service
    with patch('src.api.tasks.authenticate_user_from_token') as mock_auth_token, \
         patch('src.api.tasks.get_task_service') as mock_get_task_service:

        # Mock token authentication
        mock_token_data = Mock()
        mock_token_data.user_id = str(uuid4())
        mock_token_data.email = "test@example.com"
        mock_auth_token.return_value = mock_token_data

        # Mock task service - return False (deletion failed)
        mock_task_service = Mock(spec=TaskService)
        mock_task_service.delete_task_for_user.return_value = False
        mock_get_task_service.return_value = lambda: mock_task_service

        task_id = str(uuid4())
        response = client.delete(
            f"/tasks/{task_id}",
            headers={"Authorization": "Bearer fake-jwt-token"}
        )

        assert response.status_code == 404