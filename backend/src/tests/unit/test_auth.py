from fastapi.testclient import TestClient
import pytest
from unittest.mock import Mock, patch
from uuid import uuid4

from src.models.user import UserCreate, UserRead
from src.services.auth_service import AuthService
from src.storage.user_repository import UserRepository


def test_register_user_success():
    """Test successful user registration"""
    # Mock the user repository
    mock_user_repo = Mock(spec=UserRepository)
    mock_user_repo.get_user_by_email.return_value = None  # No existing user

    # Create user data
    user_data = UserCreate(
        email="test@example.com",
        name="Test User",
        password="SecurePassword123!"
    )

    # Create a mock user to return
    created_user = UserRead(
        id=uuid4(),
        email="test@example.com",
        name="Test User",
        created_at=None,
        updated_at=None
    )
    mock_user_repo.create_user.return_value = created_user

    # Create auth service with mock repository
    auth_service = AuthService(mock_user_repo)

    # Call register_user
    result = auth_service.register_user(user_data)

    # Assertions
    assert result is not None
    assert result.email == "test@example.com"
    mock_user_repo.get_user_by_email.assert_called_once_with("test@example.com")
    mock_user_repo.create_user.assert_called_once()


def test_register_user_already_exists():
    """Test registration fails when user already exists"""
    # Mock the user repository
    mock_user_repo = Mock(spec=UserRepository)

    # Return an existing user
    existing_user = UserRead(
        id=uuid4(),
        email="test@example.com",
        name="Test User",
        created_at=None,
        updated_at=None
    )
    mock_user_repo.get_user_by_email.return_value = existing_user

    # Create user data
    user_data = UserCreate(
        email="test@example.com",
        name="Test User",
        password="SecurePassword123!"
    )

    # Create auth service with mock repository
    auth_service = AuthService(mock_user_repo)

    # Call register_user
    result = auth_service.register_user(user_data)

    # Assertions
    assert result is None  # Should return None when user exists
    mock_user_repo.get_user_by_email.assert_called_once_with("test@example.com")
    mock_user_repo.create_user.assert_not_called()


def test_login_user_success():
    """Test successful user login"""
    # Mock the user repository
    mock_user_repo = Mock(spec=UserRepository)

    # Create a mock user to return
    authenticated_user = UserRead(
        id=uuid4(),
        email="test@example.com",
        name="Test User",
        created_at=None,
        updated_at=None
    )
    mock_user_repo.authenticate_user.return_value = authenticated_user

    # Create auth service with mock repository
    auth_service = AuthService(mock_user_repo)

    # Call login_user
    result = auth_service.login_user("test@example.com", "password123")

    # Assertions
    assert result is not None
    assert "access_token" in result
    assert result["token_type"] == "bearer"
    mock_user_repo.authenticate_user.assert_called_once_with("test@example.com", "password123")


def test_login_user_failure():
    """Test login fails with invalid credentials"""
    # Mock the user repository
    mock_user_repo = Mock(spec=UserRepository)
    mock_user_repo.authenticate_user.return_value = None  # Authentication fails

    # Create auth service with mock repository
    auth_service = AuthService(mock_user_repo)

    # Call login_user with invalid credentials
    result = auth_service.login_user("test@example.com", "wrongpassword")

    # Assertions
    assert result is None  # Should return None when authentication fails
    mock_user_repo.authenticate_user.assert_called_once_with("test@example.com", "wrongpassword")


def test_get_current_user_success():
    """Test getting current user by ID"""
    # Mock the user repository
    mock_user_repo = Mock(spec=UserRepository)

    # Create a mock user to return
    user = UserRead(
        id=uuid4(),
        email="test@example.com",
        name="Test User",
        created_at=None,
        updated_at=None
    )
    mock_user_repo.get_by_id.return_value = user

    # Create auth service with mock repository
    auth_service = AuthService(mock_user_repo)

    # Call get_current_user
    result = auth_service.get_current_user(str(user.id))

    # Assertions
    assert result is not None
    assert result.email == "test@example.com"
    mock_user_repo.get_by_id.assert_called_once()


def test_get_current_user_invalid_id():
    """Test getting current user with invalid ID"""
    # Mock the user repository
    mock_user_repo = Mock(spec=UserRepository)

    # Create auth service with mock repository
    auth_service = AuthService(mock_user_repo)

    # Call get_current_user with invalid UUID string
    result = auth_service.get_current_user("invalid-uuid")

    # Assertions
    assert result is None  # Should return None for invalid UUID
    mock_user_repo.get_by_id.assert_not_called()