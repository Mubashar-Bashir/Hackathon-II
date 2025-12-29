#!/usr/bin/env python3
# Script to set up Better Auth configuration for the application

import os
import sys
from pathlib import Path

def setup_auth():
    # Create directory structure if it doesn't exist
    os.makedirs("src/core", exist_ok=True)
    os.makedirs("src/api", exist_ok=True)

    # Generate auth configuration
    config_content = '''from pydantic import BaseSettings
import os

class AuthSettings(BaseSettings):
    """Authentication settings for Better Auth."""
    BETTER_AUTH_SECRET: str = os.getenv("BETTER_AUTH_SECRET", "your-default-secret-key-change-in-production")
    JWT_EXPIRATION_HOURS: int = int(os.getenv("JWT_EXPIRATION_HOURS", "24"))
    ALGORITHM: str = "HS256"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./auth.db")

    class Config:
        env_file = ".env"

settings = AuthSettings()
'''

    with open("src/core/auth_config.py", "w") as f:
        f.write(config_content)

    # Generate auth service
    service_content = '''from datetime import datetime, timedelta
from typing import Optional
import jwt
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.core.auth_config import settings
from src.models.user import User

security = HTTPBearer()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a new access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRATION_HOURS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.BETTER_AUTH_SECRET, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> dict:
    """Verify and decode JWT token."""
    try:
        payload = jwt.decode(
            token,
            settings.BETTER_AUTH_SECRET,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Get current user from JWT token."""
    token = credentials.credentials
    payload = verify_token(token)
    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    # In a real implementation, you would fetch the user from the database
    # user = get_user_by_id(user_id)
    # if user is None:
    #     raise HTTPException(status_code=401, detail="User not found")
    # return user

    # For now, return a mock user
    return User(id=user_id, email=payload.get("email", "unknown@example.com"))
'''

    with open("src/core/auth_service.py", "w") as f:
        f.write(service_content)

    # Generate auth API endpoints
    api_content = '''from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Optional
from datetime import timedelta

from src.core.auth_service import create_access_token, get_current_user
from src.models.user import User
from src.models.auth import Token, UserCreate, UserLogin

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=Token)
async def register(user_data: UserCreate):
    """Register a new user."""
    # In a real implementation, you would:
    # 1. Check if user already exists
    # 2. Hash the password
    # 3. Save user to database
    # 4. Generate access token
    # For now, returning a mock response
    access_token = create_access_token(data={"user_id": "mock_user_id", "email": user_data.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Authenticate user and return access token."""
    # In a real implementation, you would:
    # 1. Verify user credentials against database
    # 2. Generate access token if valid
    # For now, returning a mock response
    access_token = create_access_token(data={"user_id": "mock_user_id", "email": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """Logout the current user."""
    # In a real implementation, you might add the token to a blacklist
    return {"message": "Successfully logged out"}

@router.get("/me", response_model=User)
async def get_user(current_user: User = Depends(get_current_user)):
    """Get current user information."""
    return current_user
'''

    with open("src/api/auth.py", "w") as f:
        f.write(api_content)

    # Generate auth models
    models_content = '''from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[str] = None
    email: Optional[str] = None

class UserCreate(BaseModel):
    email: str
    password: str
    name: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str
'''

    os.makedirs("src/models", exist_ok=True)
    with open("src/models/auth.py", "w") as f:
        f.write(models_content)

    print("Better Auth setup completed!")
    print("- Configuration: src/core/auth_config.py")
    print("- Service: src/core/auth_service.py")
    print("- API: src/api/auth.py")
    print("- Models: src/models/auth.py")

if __name__ == "__main__":
    setup_auth()