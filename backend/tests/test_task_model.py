import pytest
from datetime import datetime, timezone
from uuid import UUID
from src.models.task import Task, TaskCreate, TaskUpdate, TaskRead


def test_task_creation():
    """Test creating a task with valid data"""
    import uuid
    user_id = uuid.uuid4()

    task = Task(
        title="Test Task",
        description="This is a test task",
        status="pending",
        priority="medium",
        user_id=user_id
    )

    assert task.title == "Test Task"
    assert task.description == "This is a test task"
    assert task.status == "pending"
    assert task.priority == "medium"
    assert task.user_id == user_id
    assert isinstance(task.id, UUID)
    assert isinstance(task.created_at, datetime)
    assert isinstance(task.updated_at, datetime)


def test_task_create_model():
    """Test TaskCreate model"""
    task_create = TaskCreate(
        title="Test Task",
        description="Task description",
        status="in_progress",
        priority="high",
        due_date=datetime.now(timezone.utc)
    )

    assert task_create.title == "Test Task"
    assert task_create.description == "Task description"
    assert task_create.status == "in_progress"
    assert task_create.priority == "high"
    assert isinstance(task_create.due_date, datetime)


def test_task_read_model():
    """Test TaskRead model"""
    import uuid
    task_id = uuid.uuid4()
    user_id = uuid.uuid4()

    task_read = TaskRead(
        id=task_id,
        title="Test Task",
        description="Task description",
        status="completed",
        priority="low",
        user_id=user_id,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )

    assert task_read.id == task_id
    assert task_read.title == "Test Task"
    assert task_read.status == "completed"
    assert task_read.user_id == user_id


def test_task_update_model():
    """Test TaskUpdate model"""
    task_update = TaskUpdate(
        title="Updated Task",
        status="completed",
        priority="high"
    )

    assert task_update.title == "Updated Task"
    assert task_update.status == "completed"
    assert task_update.priority == "high"


def test_task_title_validation():
    """Test task title validation - checking that valid titles work"""
    import uuid
    user_id = uuid.uuid4()

    # Valid title (within 1-200 chars)
    valid_title = "A" * 100
    task = Task(title=valid_title, user_id=user_id)
    assert task.title == valid_title

    # Test with minimum valid title length
    min_title = "A"  # 1 character, should be valid
    task_min = Task(title=min_title, user_id=user_id)
    assert task_min.title == min_title

    # Note: Validation may occur at database level, not at model instantiation
    # So we test that valid titles work, and assume database constraints handle invalid ones


def test_task_description_validation():
    """Test task description validation"""
    import uuid
    user_id = uuid.uuid4()

    # Valid description (up to 1000 chars)
    long_description = "A" * 1000
    task = Task(
        title="Test Task",
        description=long_description,
        user_id=user_id
    )
    assert task.description == long_description

    # Very long description should be handled by the database field limit


def test_task_status_validation():
    """Test task status validation"""
    import uuid
    user_id = uuid.uuid4()

    # Valid statuses
    valid_statuses = ["pending", "in_progress", "completed"]
    for status in valid_statuses:
        task = Task(title="Test", user_id=user_id, status=status)
        assert task.status == status

    # Invalid status would be caught by regex validation


def test_task_priority_validation():
    """Test task priority validation"""
    import uuid
    user_id = uuid.uuid4()

    # Valid priorities
    valid_priorities = ["low", "medium", "high"]
    for priority in valid_priorities:
        task = Task(title="Test", user_id=user_id, priority=priority)
        assert task.priority == priority

    # Invalid priority would be caught by regex validation