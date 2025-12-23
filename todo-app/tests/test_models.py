import pytest
from datetime import datetime
from src.models.todo import Task, TaskStatus


def test_task_creation():
    """Test creating a task with valid data"""
    task = Task(
        id=1,
        title="Test Task",
        description="This is a test task",
        status=TaskStatus.PENDING
    )

    assert task.id == 1
    assert task.title == "Test Task"
    assert task.description == "This is a test task"
    assert task.status == TaskStatus.PENDING
    assert isinstance(task.created_at, datetime)
    assert isinstance(task.updated_at, datetime)


def test_task_title_validation():
    """Test task title validation"""
    # Test with valid title
    task = Task(
        id=1,
        title="Valid Title",
        description="",
        status=TaskStatus.PENDING
    )
    assert task.title == "Valid Title"

    # Test with empty title (should fail validation)
    with pytest.raises(ValueError):
        Task(
            id=1,
            title="",
            description="",
            status=TaskStatus.PENDING
        )

    # Test with very long title (should fail validation)
    with pytest.raises(ValueError):
        Task(
            id=1,
            title="a" * 201,  # More than 200 characters
            description="",
            status=TaskStatus.PENDING
        )


def test_task_description_validation():
    """Test task description validation"""
    # Test with long description (should work up to 1000 chars)
    long_description = "a" * 1000
    task = Task(
        id=1,
        title="Test Task",
        description=long_description,
        status=TaskStatus.PENDING
    )
    assert task.description == long_description

    # Test with description that's too long (should fail)
    with pytest.raises(ValueError):
        Task(
            id=1,
            title="Test Task",
            description="a" * 1001,  # More than 1000 characters
            status=TaskStatus.PENDING
        )


def test_task_status_values():
    """Test task status enum values"""
    task_pending = Task(
        id=1,
        title="Test Task",
        description="",
        status=TaskStatus.PENDING
    )
    assert task_pending.status == TaskStatus.PENDING

    task_complete = Task(
        id=1,
        title="Test Task",
        description="",
        status=TaskStatus.COMPLETE
    )
    assert task_complete.status == TaskStatus.COMPLETE