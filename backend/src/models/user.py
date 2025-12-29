from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone
import uuid


class UserBase(SQLModel):
    """Base model for User with common fields"""
    email: str = Field(unique=True, index=True)
    name: Optional[str] = Field(default=None)


class User(UserBase, table=True):
    """User model for database storage"""
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    password_hash: str  # Store hashed password


class UserRead(UserBase):
    """User model for API responses"""
    id: uuid.UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class UserCreate(UserBase):
    """User model for creation requests"""
    password: str


class UserUpdate(SQLModel):
    """User model for update requests"""
    name: Optional[str] = None
    email: Optional[str] = None