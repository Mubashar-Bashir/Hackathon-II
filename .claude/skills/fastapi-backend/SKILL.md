---
name: fastapi-backend
description: Comprehensive FastAPI backend development with Pydantic V2, SQLModel ORM, and authentication middleware. Use when building RESTful API endpoints, database models, authentication systems, and backend services with Python 3.13+.
---

# FastAPI Backend Development

## Overview

This skill enables comprehensive FastAPI backend development using Python 3.13+, Pydantic V2 for data validation, and SQLModel for database operations. It provides guidance for creating API endpoints, database models, authentication systems, and backend services following modern Python and FastAPI best practices.

## Core Capabilities

### 1. API Endpoint Development
- Create RESTful API endpoints with proper HTTP methods
- Implement request/response validation with Pydantic models
- Add authentication and authorization middleware
- Handle error responses consistently

### 2. Database Model Design
- Create SQLModel models with proper relationships
- Define database schemas with validation
- Implement CRUD operations with SQLModel
- Handle database migrations and connections

### 3. Authentication & Security
- Implement JWT-based authentication middleware
- Create user registration and login endpoints
- Secure endpoints with proper authorization
- Handle password hashing and validation

### 4. Service Layer Development
- Build business logic in service classes
- Implement proper error handling and logging
- Create reusable service components
- Handle data validation and transformation

## Quick Start

1. Create Pydantic models for request/response validation
2. Define SQLModel database models
3. Implement API endpoints with proper authentication
4. Add service layer for business logic

## API Endpoint Examples

### Basic CRUD Endpoint
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from src.models.task import Task, TaskCreate, TaskUpdate
from src.core.database import get_session
from src.core.security import get_current_user
from src.models.user import User

router = APIRouter()

@router.get("/", response_model=List[Task])
def get_tasks(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    statement = select(Task).where(Task.user_id == current_user.id)
    tasks = session.exec(statement).all()
    return tasks

@router.post("/", response_model=Task)
def create_task(
    task: TaskCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    db_task = Task(
        **task.dict(),
        user_id=current_user.id
    )
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task
```

### Authentication Middleware
```python
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
import jwt
from pydantic import BaseModel

from src.core.config import settings
from src.models.user import User

security = HTTPBearer()

class TokenData(BaseModel):
    username: Optional[str] = None

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        # Fetch user from database
        user = get_user_by_username(username)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
```

## Database Model Examples

### Task Model with SQLModel
```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime
import uuid

if TYPE_CHECKING:
    from src.models.user import User

class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    status: str = Field(default="pending", regex="^(pending|in_progress|completed)$")
    priority: str = Field(default="medium", regex="^(low|medium|high)$")
    due_date: Optional[datetime] = None

class Task(TaskBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    user: "User" = Relationship(back_populates="tasks")

class TaskCreate(TaskBase):
    pass

class TaskUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    status: Optional[str] = Field(default=None, regex="^(pending|in_progress|completed)$")
    priority: Optional[str] = Field(default=None, regex="^(low|medium|high)$")
    due_date: Optional[datetime] = None
```

## Resources

### scripts/
- `generate-endpoint.py` - Generate new API endpoint boilerplate
- `setup-database.py` - Database initialization utility
- `create-model.py` - SQLModel generation utility

### references/
- `fastapi-best-practices.md` - FastAPI development guidelines
- `pydantic-validation.md` - Pydantic validation patterns
- `sqlmodel-guide.md` - SQLModel ORM usage guide

### assets/
- `endpoint-templates/` - API endpoint boilerplate templates
- `model-templates/` - SQLModel structure templates
