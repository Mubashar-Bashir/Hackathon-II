import pytest
from typer.testing import CliRunner
from src.ui.cli import app
from src.core.todo_service import TodoService
from src.storage.in_memory_storage import InMemoryTaskRepository


runner = CliRunner()


def test_add_command():
    """Integration test for the add command"""
    # Create a fresh repository for testing
    repository = InMemoryTaskRepository()
    # We'll mock the global service to use our test repository
    import src.ui.cli as cli_module
    original_service = cli_module.service
    cli_module.service = TodoService(repository)

    try:
        result = runner.invoke(app, ["add", "Test Task", "Test Description"])
        assert result.exit_code == 0
        assert "Added task: Test Task" in result.stdout
    finally:
        # Restore original service
        cli_module.service = original_service


def test_list_command():
    """Integration test for the list command"""
    # Create a fresh repository for testing
    repository = InMemoryTaskRepository()
    # Add some test tasks
    service = TodoService(repository)
    service.add_task("Task 1", "First task")
    service.add_task("Task 2", "Second task")

    # We'll mock the global service to use our test repository
    import src.ui.cli as cli_module
    original_service = cli_module.service
    cli_module.service = service

    try:
        result = runner.invoke(app, ["list-tasks"])
        assert result.exit_code == 0
        assert "Task 1" in result.stdout
        assert "Task 2" in result.stdout
        assert "Todo List" in result.stdout  # Table title
    finally:
        # Restore original service
        cli_module.service = original_service


def test_list_command_empty():
    """Integration test for the list command with no tasks"""
    # Create a fresh repository for testing
    repository = InMemoryTaskRepository()
    # We'll mock the global service to use our test repository
    import src.ui.cli as cli_module
    original_service = cli_module.service
    cli_module.service = TodoService(repository)

    try:
        result = runner.invoke(app, ["list-tasks"])
        assert result.exit_code == 0
        assert "No tasks found" in result.stdout
    finally:
        # Restore original service
        cli_module.service = original_service


def test_complete_command():
    """Integration test for the complete command"""
    # Create a fresh repository for testing
    repository = InMemoryTaskRepository()
    service = TodoService(repository)
    task = service.add_task("Test Task", "Test Description")

    # We'll mock the global service to use our test repository
    import src.ui.cli as cli_module
    original_service = cli_module.service
    cli_module.service = service

    try:
        result = runner.invoke(app, ["complete", str(task.id)])
        assert result.exit_code == 0
        assert f"Task {task.id} marked as complete" in result.stdout
    finally:
        # Restore original service
        cli_module.service = original_service


def test_update_command():
    """Integration test for the update command"""
    # Create a fresh repository for testing
    repository = InMemoryTaskRepository()
    service = TodoService(repository)
    task = service.add_task("Original Title", "Original Description")

    # We'll mock the global service to use our test repository
    import src.ui.cli as cli_module
    original_service = cli_module.service
    cli_module.service = service

    try:
        result = runner.invoke(app, ["update", str(task.id), "--title", "New Title"])
        assert result.exit_code == 0
        assert f"Task {task.id} updated" in result.stdout
    finally:
        # Restore original service
        cli_module.service = original_service


def test_delete_command():
    """Integration test for the delete command"""
    # Create a fresh repository for testing
    repository = InMemoryTaskRepository()
    service = TodoService(repository)
    task = service.add_task("Test Task", "Test Description")

    # We'll mock the global service to use our test repository
    import src.ui.cli as cli_module
    original_service = cli_module.service
    cli_module.service = service

    try:
        result = runner.invoke(app, ["delete", str(task.id)])
        assert result.exit_code == 0
        assert f"Task {task.id} deleted" in result.stdout
    finally:
        # Restore original service
        cli_module.service = original_service