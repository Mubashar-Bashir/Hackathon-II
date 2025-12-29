import pytest
from unittest.mock import Mock, patch
from uuid import UUID
from src.services.auth_service import AuthService
from src.models.user import UserCreate, UserRead
from src.storage.user_repository import UserRepository


def test_register_user_success():
    """Test successful user registration"""
    # Mock the user repository
    mock_user_repo = Mock(spec=UserRepository)
    mock_user_repo.get_user_by_email.return_value = None  # User doesn't exist

    # Mock the created user
    created_user = UserRead(
        id=UUID("12345678-1234-5678-1234-567812345678"),
        email="test@example.com",
        name="Test User"
    )
    mock_user_repo.create_user.return_value = created_user

    # Create auth service with mocked repository
    auth_service = AuthService(mock_user_repo)

    # Create user data for registration
    user_data = UserCreate(
        email="test@example.com",
        name="Test User",
        password="securepassword"
    )

    # Call register_user
    result = auth_service.register_user(user_data)

    # Assertions
    assert result == created_user
    mock_user_repo.get_user_by_email.assert_called_once_with("test@example.com")
    mock_user_repo.create_user.assert_called_once_with(user_data)


def test_register_user_already_exists():
    """Test user registration when user already exists"""
    # Mock the user repository
    mock_user_repo = Mock(spec=UserRepository)

    # Mock an existing user
    existing_user = UserRead(
        id=UUID("12345678-1234-5678-1234-567812345678"),
        email="test@example.com",
        name="Test User"
    )
    mock_user_repo.get_user_by_email.return_value = existing_user

    # Create auth service with mocked repository
    auth_service = AuthService(mock_user_repo)

    # Create user data for registration
    user_data = UserCreate(
        email="test@example.com",
        name="Test User",
        password="securepassword"
    )

    # Call register_user
    result = auth_service.register_user(user_data)

    # Assertions
    assert result is None
    mock_user_repo.get_user_by_email.assert_called_once_with("test@example.com")
    mock_user_repo.create_user.assert_not_called()


def test_login_user_success():
    """Test successful user login"""
    # Mock the user repository
    mock_user_repo = Mock(spec=UserRepository)

    # Mock the authenticated user
    authenticated_user = UserRead(
        id=UUID("12345678-1234-5678-1234-567812345678"),
        email="test@example.com",
        name="Test User"
    )
    mock_user_repo.authenticate_user.return_value = authenticated_user

    # Create auth service with mocked repository
    auth_service = AuthService(mock_user_repo)

    # Call login_user
    result = auth_service.login_user("test@example.com", "securepassword")

    # Assertions
    assert result is not None
    assert "access_token" in result
    assert result["token_type"] == "bearer"
    mock_user_repo.authenticate_user.assert_called_once_with("test@example.com", "securepassword")


def test_login_user_failure():
    """Test user login failure with wrong credentials"""
    # Mock the user repository
    mock_user_repo = Mock(spec=UserRepository)
    mock_user_repo.authenticate_user.return_value = None

    # Create auth service with mocked repository
    auth_service = AuthService(mock_user_repo)

    # Call login_user with wrong credentials
    result = auth_service.login_user("test@example.com", "wrongpassword")

    # Assertions
    assert result is None
    mock_user_repo.authenticate_user.assert_called_once_with("test@example.com", "wrongpassword")


def test_get_current_user_success():
    """Test getting current user by ID"""
    # Mock the user repository
    mock_user_repo = Mock(spec=UserRepository)

    # Mock the user
    user = UserRead(
        id=UUID("12345678-1234-5678-1234-567812345678"),
        email="test@example.com",
        name="Test User"
    )
    mock_user_repo.get_by_id.return_value = user

    # Create auth service with mocked repository
    auth_service = AuthService(mock_user_repo)

    # Call get_current_user
    result = auth_service.get_current_user(str(user.id))

    # Assertions
    assert result == user
    mock_user_repo.get_by_id.assert_called_once_with(user.id)


def test_get_current_user_invalid_id():
    """Test getting current user with invalid ID"""
    # Mock the user repository
    mock_user_repo = Mock(spec=UserRepository)

    # Create auth service with mocked repository
    auth_service = AuthService(mock_user_repo)

    # Call get_current_user with invalid ID
    result = auth_service.get_current_user("invalid-uuid")

    # Assertions
    assert result is None
    mock_user_repo.get_by_id.assert_not_called()


def test_get_current_user_not_found():
    """Test getting current user that doesn't exist"""
    # Mock the user repository
    mock_user_repo = Mock(spec=UserRepository)
    mock_user_repo.get_by_id.return_value = None

    # Create auth service with mocked repository
    auth_service = AuthService(mock_user_repo)

    # Call get_current_user
    result = auth_service.get_current_user("12345678-1234-5678-1234-567812345678")

    # Assertions
    assert result is None
    mock_user_repo.get_by_id.assert_called_once()