from fastapi.testclient import TestClient
import pytest
from unittest.mock import Mock, patch
from uuid import uuid4

from src.main import app
from src.models.user import UserCreate, UserRead
from src.services.auth_service import AuthService
from src.storage.user_repository import UserRepository


def test_register_user_success():
    """Test successful user registration via API"""
    client = TestClient(app)

    # Mock the auth service
    with patch('src.api.auth.get_auth_service') as mock_get_auth_service:
        mock_auth_service = Mock(spec=AuthService)
        mock_auth_service.register_user.return_value = UserRead(
            id=uuid4(),
            email="test@example.com",
            name="Test User",
            created_at=None,
            updated_at=None
        )
        mock_get_auth_service.return_value = lambda: mock_auth_service

        response = client.post(
            "/auth/register",
            json={
                "email": "test@example.com",
                "name": "Test User",
                "password": "SecurePassword123!"
            }
        )

        assert response.status_code == 201
        data = response.json()
        assert "user_id" in data
        assert data["email"] == "test@example.com"
        assert data["message"] == "User registered successfully"


def test_register_user_already_exists():
    """Test user registration fails when user already exists"""
    client = TestClient(app)

    # Mock the auth service
    with patch('src.api.auth.get_auth_service') as mock_get_auth_service:
        mock_auth_service = Mock(spec=AuthService)
        mock_auth_service.register_user.return_value = None  # User already exists
        mock_get_auth_service.return_value = lambda: mock_auth_service

        response = client.post(
            "/auth/register",
            json={
                "email": "test@example.com",
                "name": "Test User",
                "password": "SecurePassword123!"
            }
        )

        assert response.status_code == 409  # Conflict
        data = response.json()
        assert "detail" in data


def test_login_user_success():
    """Test successful user login via API"""
    client = TestClient(app)

    # Mock the auth service
    with patch('src.api.auth.get_auth_service') as mock_get_auth_service:
        mock_auth_service = Mock(spec=AuthService)
        mock_auth_service.login_user.return_value = {
            "access_token": "fake-jwt-token",
            "token_type": "bearer",
            "expires_in": 86400
        }
        mock_get_auth_service.return_value = lambda: mock_auth_service

        response = client.post(
            "/auth/login",
            data={
                "email": "test@example.com",
                "password": "SecurePassword123!"
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"


def test_login_user_failure():
    """Test user login fails with invalid credentials"""
    client = TestClient(app)

    # Mock the auth service
    with patch('src.api.auth.get_auth_service') as mock_get_auth_service:
        mock_auth_service = Mock(spec=AuthService)
        mock_auth_service.login_user.return_value = None  # Login failed
        mock_get_auth_service.return_value = lambda: mock_auth_service

        response = client.post(
            "/auth/login",
            data={
                "email": "test@example.com",
                "password": "wrongpassword"
            }
        )

        assert response.status_code == 401  # Unauthorized
        data = response.json()
        assert "detail" in data


def test_get_current_user_success():
    """Test getting current user info via API"""
    client = TestClient(app)

    # Mock the auth service
    with patch('src.api.auth.authenticate_user_from_token') as mock_auth_token, \
         patch('src.api.auth.get_auth_service') as mock_get_auth_service:

        # Mock token authentication
        mock_token_data = Mock()
        mock_token_data.user_id = str(uuid4())
        mock_token_data.email = "test@example.com"
        mock_auth_token.return_value = mock_token_data

        # Mock auth service
        mock_auth_service = Mock(spec=AuthService)
        mock_auth_service.get_current_user.return_value = UserRead(
            id=uuid4(),
            email="test@example.com",
            name="Test User",
            created_at=None,
            updated_at=None
        )
        mock_get_auth_service.return_value = lambda: mock_auth_service

        response = client.get(
            "/auth/me",
            headers={"Authorization": "Bearer fake-jwt-token"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"


def test_logout_success():
    """Test logout endpoint"""
    client = TestClient(app)

    response = client.post(
        "/auth/logout",
        headers={"Authorization": "Bearer fake-jwt-token"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Successfully logged out"


def test_health_check():
    """Test health check endpoint"""
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"