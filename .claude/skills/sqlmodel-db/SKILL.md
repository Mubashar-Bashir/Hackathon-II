---
name: sqlmodel-db
description: Comprehensive SQLModel ORM development with Neon PostgreSQL integration. Use when designing database schemas, creating models with relationships, implementing CRUD operations, and managing database connections with SQLModel for Python applications.
---

# SQLModel Database Development

## Overview

This skill enables comprehensive SQLModel ORM development with Neon PostgreSQL integration. It provides guidance for creating database models with proper relationships, implementing CRUD operations, handling database connections, and managing schema migrations using SQLModel which combines SQLAlchemy and Pydantic.

## Core Capabilities

### 1. Model Design
- Create SQLModel models with proper field validation
- Define relationships between models
- Implement inheritance and abstract models
- Handle UUID primary keys and timestamps

### 2. Database Operations
- Implement CRUD operations with SQLModel
- Write complex queries with filtering and joins
- Handle transactions and connection pooling
- Manage database sessions properly

### 3. Schema Management
- Create database migration scripts
- Handle schema evolution and versioning
- Manage index creation and optimization
- Handle data seeding and initial setup

### 4. Connection Management
- Configure database connection pools
- Handle Neon PostgreSQL specific settings
- Implement connection health checks
- Manage connection lifecycle

## Quick Start

1. Define your SQLModel models with proper relationships
2. Create database session management
3. Implement CRUD operations using SQLModel
4. Set up connection pooling and error handling

## Model Design Examples

### Basic Model with Relationships
```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid

class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False)
    name: Optional[str] = Field(default=None, max_length=100)

class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    tasks: List["Task"] = Relationship(back_populates="user")

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
    user: User = Relationship(back_populates="tasks")

class TaskCreate(TaskBase):
    pass

class TaskUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    status: Optional[str] = Field(default=None, regex="^(pending|in_progress|completed)$")
    priority: Optional[str] = Field(default=None, regex="^(low|medium|high)$")
    due_date: Optional[datetime] = None
```

### CRUD Operations
```python
from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID

def create_user(session: Session, user_data: UserCreate) -> User:
    """Create a new user in the database."""
    user = User.from_orm(user_data)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def get_user_by_id(session: Session, user_id: UUID) -> Optional[User]:
    """Get a user by their ID."""
    statement = select(User).where(User.id == user_id)
    return session.exec(statement).first()

def get_user_tasks(session: Session, user_id: UUID) -> List[Task]:
    """Get all tasks for a specific user."""
    statement = select(Task).where(Task.user_id == user_id)
    return session.exec(statement).all()

def update_task(session: Session, task_id: UUID, task_data: TaskUpdate) -> Optional[Task]:
    """Update a task with new data."""
    task = session.get(Task, task_id)
    if task:
        update_data = task_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)
        session.add(task)
        session.commit()
        session.refresh(task)
    return task

def delete_task(session: Session, task_id: UUID) -> bool:
    """Delete a task by ID."""
    task = session.get(Task, task_id)
    if task:
        session.delete(task)
        session.commit()
        return True
    return False
```

### Database Session Management
```python
from sqlmodel import create_engine, Session
from contextlib import contextmanager
from typing import Generator

# Create engine with Neon PostgreSQL settings
def create_db_engine(database_url: str):
    """Create a database engine with appropriate settings for Neon PostgreSQL."""
    return create_engine(
        database_url,
        # Connection pooling settings
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,  # Verify connections before use
        pool_recycle=300,    # Recycle connections after 5 minutes
    )

@contextmanager
def get_session_context(engine) -> Generator[Session, None, None]:
    """Context manager for database sessions."""
    with Session(engine) as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

# Usage example
def get_user_with_tasks(user_id: UUID, engine) -> Optional[User]:
    """Get user with their tasks using session context."""
    with get_session_context(engine) as session:
        statement = select(User).where(User.id == user_id).join(Task)
        return session.exec(statement).first()
```

## Resources

### scripts/
- `generate-model.py` - Generate new SQLModel model boilerplate
- `migrate-db.py` - Database migration utility
- `seed-data.py` - Data seeding script

### references/
- `sqlmodel-best-practices.md` - SQLModel development guidelines
- `neon-postgres.md` - Neon PostgreSQL specific settings
- `relationship-patterns.md` - SQLModel relationship examples

### assets/
- `model-templates/` - SQLModel structure templates
- `migration-templates/` - Database migration templates
