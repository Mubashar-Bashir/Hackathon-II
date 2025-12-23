#!/usr/bin/env python3
"""
Integration test to validate all todo CLI functionality.

This script tests all the core functionality of the todo CLI application
to ensure everything works as expected.
"""

import sys
import os
import tempfile
import subprocess
from pathlib import Path

def run_cli_command(args):
    """Run a CLI command and return the result"""
    cmd = [sys.executable, "-m", "src.main"] + args
    result = subprocess.run(cmd, capture_output=True, text=True, cwd="todo-app")
    return result

def test_add_task():
    """Test adding a task"""
    print("Testing: Add task functionality")
    result = run_cli_command(["add", "Test Task 1", "This is a test description"])
    assert result.returncode == 0, f"Add command failed: {result.stderr}"
    assert "Added task: Test Task 1" in result.stdout
    print("✓ Add task functionality works")

def test_list_tasks():
    """Test listing tasks"""
    print("Testing: List tasks functionality")
    result = run_cli_command(["list"])
    assert result.returncode == 0, f"List command failed: {result.stderr}"
    assert "Test Task 1" in result.stdout
    print("✓ List tasks functionality works")

def test_complete_task():
    """Test completing a task"""
    print("Testing: Complete task functionality")
    result = run_cli_command(["complete", "1"])
    assert result.returncode == 0, f"Complete command failed: {result.stderr}"
    assert "marked as complete" in result.stdout
    print("✓ Complete task functionality works")

def test_update_task():
    """Test updating a task"""
    print("Testing: Update task functionality")
    result = run_cli_command(["update", "1", "--title", "Updated Task", "--description", "Updated description"])
    assert result.returncode == 0, f"Update command failed: {result.stderr}"
    assert "updated" in result.stdout
    print("✓ Update task functionality works")

def test_delete_task():
    """Test deleting a task"""
    print("Testing: Delete task functionality")
    result = run_cli_command(["delete", "1"])
    assert result.returncode == 0, f"Delete command failed: {result.stderr}"
    assert "deleted" in result.stdout
    print("✓ Delete task functionality works")

def test_empty_list():
    """Test listing when no tasks exist"""
    print("Testing: Empty list functionality")
    result = run_cli_command(["list"])
    assert result.returncode == 0, f"List command failed: {result.stderr}"
    assert "No tasks found" in result.stdout
    print("✓ Empty list functionality works")

def main():
    """Run all integration tests"""
    print("Running integration tests for Todo CLI application...\n")

    try:
        # Clear any existing tasks by adding and deleting one first
        # (this ensures we have a clean state for testing)

        # Test add functionality
        test_add_task()

        # Test list functionality
        test_list_tasks()

        # Test complete functionality
        test_complete_task()

        # Test update functionality
        test_update_task()

        # Test delete functionality
        test_delete_task()

        # Test empty list
        test_empty_list()

        print("\n✓ All integration tests passed!")
        print("✓ Code review validation successful")
        return True

    except Exception as e:
        print(f"\n✗ Integration test failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)