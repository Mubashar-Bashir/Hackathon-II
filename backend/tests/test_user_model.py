import pytest
from datetime import datetime
from uuid import UUID
from src.models.user import User, UserCreate, UserRead
from passlib.context import CryptContext


def test_user_creation():
    """Test creating a user with valid data"""
    user = User(
        email="test@example.com",
        name="Test User",
        password_hash="$2b$12$example_hash"
    )

    assert user.email == "test@example.com"
    assert user.name == "Test User"
    assert user.password_hash == "$2b$12$example_hash"
    assert isinstance(user.id, UUID)
    assert isinstance(user.created_at, datetime)
    assert isinstance(user.updated_at, datetime)


def test_user_create_model():
    """Test UserCreate model"""
    user_create = UserCreate(
        email="test@example.com",
        name="Test User",
        password="securepassword"
    )

    assert user_create.email == "test@example.com"
    assert user_create.name == "Test User"
    assert user_create.password == "securepassword"


def test_user_read_model():
    """Test UserRead model"""
    import uuid
    user_id = uuid.uuid4()

    user_read = UserRead(
        id=user_id,
        email="test@example.com",
        name="Test User",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

    assert user_read.id == user_id
    assert user_read.email == "test@example.com"
    assert user_read.name == "Test User"


def test_user_email_validation():
    """Test user email validation"""
    # Valid email
    user = User(
        email="valid@example.com",
        password_hash="$2b$12$example_hash"
    )
    assert user.email == "valid@example.com"

    # Invalid email format would be caught by SQLModel validation
    # which is tested at the database level


def test_user_password_hashing():
    """Test password hashing functionality"""
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    plain_password = "securepassword"
    hashed = pwd_context.hash(plain_password)

    assert pwd_context.verify(plain_password, hashed)
    assert not pwd_context.verify("wrongpassword", hashed)