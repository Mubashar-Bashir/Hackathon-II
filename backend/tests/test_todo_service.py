import pytest
from src.todo_app.models.todo import Task, TaskStatus
from src.todo_app.storage.in_memory_storage import InMemoryTaskRepository
from src.todo_app.core.todo_service import TodoService


def test_create_task():
    """Test creating a new task"""
    repository = InMemoryTaskRepository()
    service = TodoService(repository)

    task = service.add_task("Test task", "This is a test")

    assert task.title == "Test task"
    assert task.description == "This is a test"
    assert task.status == TaskStatus.PENDING
    assert task.id == 1  # First task should get ID 1


def test_get_task():
    """Test retrieving a task by ID"""
    repository = InMemoryTaskRepository()
    service = TodoService(repository)

    created_task = service.add_task("Test task", "This is a test")
    retrieved_task = service.get_task(created_task.id)

    assert retrieved_task is not None
    assert retrieved_task.id == created_task.id
    assert retrieved_task.title == created_task.title


def test_list_tasks():
    """Test listing all tasks"""
    repository = InMemoryTaskRepository()
    service = TodoService(repository)

    service.add_task("Task 1", "First task")
    service.add_task("Task 2", "Second task")

    tasks = service.list_tasks()

    assert len(tasks) == 2
    titles = [task.title for task in tasks]
    assert "Task 1" in titles
    assert "Task 2" in titles


def test_update_task():
    """Test updating a task"""
    repository = InMemoryTaskRepository()
    service = TodoService(repository)

    task = service.add_task("Original title", "Original description")
    updated_task = service.update_task(task.id, title="Updated title")

    assert updated_task is not None
    assert updated_task.title == "Updated title"
    assert updated_task.description == "Original description"  # Should remain unchanged


def test_delete_task():
    """Test deleting a task"""
    repository = InMemoryTaskRepository()
    service = TodoService(repository)

    task = service.add_task("Test task", "This is a test")
    success = service.delete_task(task.id)

    assert success is True
    assert service.get_task(task.id) is None


def test_toggle_task_status():
    """Test toggling task status"""
    repository = InMemoryTaskRepository()
    service = TodoService(repository)

    task = service.add_task("Test task", "This is a test")
    assert task.status == TaskStatus.PENDING

    toggled_task = service.toggle_task_status(task.id)
    assert toggled_task.status == TaskStatus.COMPLETE

    toggled_task_again = service.toggle_task_status(task.id)
    assert toggled_task_again.status == TaskStatus.PENDING