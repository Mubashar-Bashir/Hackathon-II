import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

from .config import settings


# JWT utility functions
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token with the given data and expiration.
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # Default to 24 hours if not specified
        expire = datetime.now(timezone.utc) + timedelta(hours=settings.jwt_expiration_hours)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.better_auth_secret, algorithm="HS256")
    return encoded_jwt


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Verify a JWT token and return the payload if valid.
    """
    try:
        payload = jwt.decode(token, settings.better_auth_secret, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except Exception:  # PyJWT uses various exception types
        return None


def decode_token_payload(token: str) -> Optional[Dict[str, Any]]:
    """
    Decode a JWT token without verifying its signature (use with caution).
    """
    try:
        payload = jwt.decode(token, options={"verify_signature": False})
        return payload
    except jwt.InvalidTokenError:
        return None


# Authentication scheme
security = HTTPBearer()


class TokenData(BaseModel):
    user_id: str
    email: str


def get_current_user_from_token(credentials: HTTPAuthorizationCredentials) -> Optional[TokenData]:
    """
    Extract user information from the JWT token in the Authorization header.
    """
    token = credentials.credentials
    payload = verify_token(token)

    if payload is None:
        return None

    user_id: str = payload.get("user_id")
    email: str = payload.get("email")

    if user_id is None or email is None:
        return None

    token_data = TokenData(user_id=user_id, email=email)
    return token_data


def authenticate_user_from_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> TokenData:
    """
    Authenticate user from JWT token, raising HTTPException if invalid.
    """
    token_data = get_current_user_from_token(credentials)

    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return token_data