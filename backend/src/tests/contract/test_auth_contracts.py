import jwt
import pytest
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from src.core.security import create_access_token, verify_token, decode_token_payload
from src.core.config import settings


def test_jwt_token_creation():
    """Test that JWT tokens are created with correct structure and data"""
    user_data = {
        "user_id": str(uuid4()),
        "email": "test@example.com"
    }

    token = create_access_token(data=user_data)

    # Verify the token was created
    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 0

    # Verify the token can be decoded
    decoded = jwt.decode(token, settings.better_auth_secret, algorithms=["HS256"])
    assert decoded["user_id"] == user_data["user_id"]
    assert decoded["email"] == user_data["email"]
    assert "exp" in decoded


def test_jwt_token_expiration():
    """Test that JWT tokens have correct expiration"""
    user_data = {
        "user_id": str(uuid4()),
        "email": "test@example.com"
    }

    # Create token with specific expiration
    expire_delta = timedelta(hours=1)
    token = create_access_token(data=user_data, expires_delta=expire_delta)

    decoded = jwt.decode(token, settings.better_auth_secret, algorithms=["HS256"])
    expected_exp = datetime.now(timezone.utc) + expire_delta
    actual_exp = datetime.fromtimestamp(decoded["exp"], tz=timezone.utc)

    # Allow for small time differences (account for processing time)
    assert abs((expected_exp - actual_exp).total_seconds()) < 60


def test_jwt_token_verification_valid():
    """Test that valid JWT tokens are verified successfully"""
    user_data = {
        "user_id": str(uuid4()),
        "email": "test@example.com"
    }

    token = create_access_token(data=user_data)
    payload = verify_token(token)

    assert payload is not None
    assert payload["user_id"] == user_data["user_id"]
    assert payload["email"] == user_data["email"]


def test_jwt_token_verification_invalid_secret():
    """Test that tokens with wrong secret are not verified"""
    user_data = {
        "user_id": str(uuid4()),
        "email": "test@example.com"
    }

    # Create token with correct secret
    token = create_access_token(data=user_data)

    # Try to verify with wrong secret
    # Temporarily change the secret for this test
    original_secret = settings.better_auth_secret
    settings.better_auth_secret = "wrong-secret"

    try:
        payload = verify_token(token)
        assert payload is None
    finally:
        # Restore original secret
        settings.better_auth_secret = original_secret


def test_jwt_token_verification_expired():
    """Test that expired JWT tokens are not verified"""
    user_data = {
        "user_id": str(uuid4()),
        "email": "test@example.com"
    }

    # Create an expired token
    expired_payload = {**user_data, "exp": datetime.now(timezone.utc) - timedelta(hours=1)}
    token = jwt.encode(expired_payload, settings.better_auth_secret, algorithm="HS256")

    payload = verify_token(token)
    assert payload is None


def test_jwt_token_decoding_without_verification():
    """Test that tokens can be decoded without verification (for public info)"""
    user_data = {
        "user_id": str(uuid4()),
        "email": "test@example.com"
    }

    token = create_access_token(data=user_data)
    payload = decode_token_payload(token)

    # Should be able to decode without verification
    assert payload is not None
    assert payload["user_id"] == user_data["user_id"]
    assert payload["email"] == user_data["email"]


def test_jwt_token_structure():
    """Test that JWT tokens follow expected structure"""
    user_data = {
        "user_id": str(uuid4()),
        "email": "test@example.com"
    }

    token = create_access_token(data=user_data)

    # JWT has three parts separated by dots
    parts = token.split('.')
    assert len(parts) == 3

    # Each part should be non-empty
    for part in parts:
        assert len(part) > 0


def test_jwt_token_with_default_expiration():
    """Test that JWT tokens use default expiration when not specified"""
    user_data = {
        "user_id": str(uuid4()),
        "email": "test@example.com"
    }

    token = create_access_token(data=user_data)  # No expires_delta specified
    decoded = jwt.decode(token, settings.better_auth_secret, algorithms=["HS256"])

    expected_exp = datetime.now(timezone.utc) + timedelta(hours=settings.jwt_expiration_hours)
    actual_exp = datetime.fromtimestamp(decoded["exp"], tz=timezone.utc)

    # Allow for small time differences (account for processing time)
    assert abs((expected_exp - actual_exp).total_seconds()) < 60


def test_jwt_token_custom_expiration():
    """Test that JWT tokens respect custom expiration times"""
    user_data = {
        "user_id": str(uuid4()),
        "email": "test@example.com"
    }

    custom_expire = timedelta(minutes=30)
    token = create_access_token(data=user_data, expires_delta=custom_expire)
    decoded = jwt.decode(token, settings.better_auth_secret, algorithms=["HS256"])

    expected_exp = datetime.now(timezone.utc) + custom_expire
    actual_exp = datetime.fromtimestamp(decoded["exp"], tz=timezone.utc)

    # Allow for small time differences (account for processing time)
    assert abs((expected_exp - actual_exp).total_seconds()) < 60


def test_jwt_token_multiple_fields():
    """Test that JWT tokens can contain multiple custom fields"""
    user_data = {
        "user_id": str(uuid4()),
        "email": "test@example.com",
        "role": "user",
        "permissions": ["read", "write"]
    }

    token = create_access_token(data=user_data)
    payload = verify_token(token)

    assert payload is not None
    assert payload["user_id"] == user_data["user_id"]
    assert payload["email"] == user_data["email"]
    assert payload["role"] == user_data["role"]
    assert payload["permissions"] == user_data["permissions"]