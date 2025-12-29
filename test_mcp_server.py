#!/usr/bin/env python3
"""
Test script for MCP Task Tools Server
This script tests the functionality of the MCP server without running it,
by directly calling the functions in the server file.
"""

import sys
import os
import uuid
from datetime import datetime

# Add the project root to the path so we can import the modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_task_operations():
    """Test all task operations in the MCP server"""

    print("Testing MCP Task Tools Server...")

    # Import the functions from the server
    try:
        from mcp.task_tools_server import add_task, list_tasks, update_task, complete_task, delete_task
        print("✅ Successfully imported MCP server functions")
    except ImportError as e:
        print(f"❌ Failed to import MCP server functions: {e}")
        return False

    # Generate a test user ID
    test_user_id = str(uuid.uuid4())
    print(f"Using test user ID: {test_user_id}")

    # Test 1: Add a task
    print("\n--- Test 1: Adding a task ---")
    try:
        task_result = add_task(
            user_id=test_user_id,
            title="Test Task",
            description="This is a test task for verification"
        )
        print(f"✅ Task created successfully: {task_result['title']}")
        print(f"   Task ID: {task_result['id']}")
        assert task_result['user_id'] == test_user_id
        assert task_result['title'] == "Test Task"
        print("✅ User isolation verified - task correctly assigned to user")
    except Exception as e:
        print(f"❌ Failed to add task: {e}")
        return False

    task_id = task_result['id']

    # Test 2: List tasks
    print("\n--- Test 2: Listing tasks ---")
    try:
        tasks = list_tasks(user_id=test_user_id)
        print(f"✅ Found {len(tasks)} tasks for user")
        assert len(tasks) == 1
        assert tasks[0]['id'] == task_id
        print("✅ Task correctly retrieved for user")
    except Exception as e:
        print(f"❌ Failed to list tasks: {e}")
        return False

    # Test 3: Update task
    print("\n--- Test 3: Updating task ---")
    try:
        updated_task = update_task(
            user_id=test_user_id,
            task_id=task_id,
            title="Updated Test Task",
            description="This is an updated test task"
        )
        print(f"✅ Task updated successfully: {updated_task['title']}")
        assert updated_task['title'] == "Updated Test Task"
        assert updated_task['user_id'] == test_user_id
        print("✅ Task correctly updated")
    except Exception as e:
        print(f"❌ Failed to update task: {e}")
        return False

    # Test 4: Complete task
    print("\n--- Test 4: Completing task ---")
    try:
        completed_task = complete_task(
            user_id=test_user_id,
            task_id=task_id
        )
        print(f"✅ Task completed successfully: {completed_task['status']}")
        assert completed_task['status'] == "completed"
        assert completed_task['user_id'] == test_user_id
        print("✅ Task correctly marked as completed")
    except Exception as e:
        print(f"❌ Failed to complete task: {e}")
        return False

    # Test 5: Delete task
    print("\n--- Test 5: Deleting task ---")
    try:
        delete_result = delete_task(
            user_id=test_user_id,
            task_id=task_id
        )
        print(f"✅ Task deleted successfully: {delete_result['message']}")
        assert delete_result['deleted_task_id'] == task_id
        assert delete_result['user_id'] == test_user_id
        print("✅ Task correctly deleted")
    except Exception as e:
        print(f"❌ Failed to delete task: {e}")
        return False

    # Test 6: Verify task is gone
    print("\n--- Test 6: Verifying task deletion ---")
    try:
        remaining_tasks = list_tasks(user_id=test_user_id)
        print(f"✅ Found {len(remaining_tasks)} tasks after deletion")
        assert len(remaining_tasks) == 0
        print("✅ Task was successfully removed from user's list")
    except Exception as e:
        print(f"❌ Failed to verify deletion: {e}")
        return False

    print("\n🎉 All tests passed! MCP Task Tools Server is working correctly.")
    return True

def test_user_isolation():
    """Test that users can't access each other's tasks"""
    print("\n--- Testing User Isolation ---")

    try:
        from mcp.task_tools_server import add_task, list_tasks, complete_task, delete_task
    except ImportError as e:
        print(f"❌ Failed to import MCP server functions: {e}")
        return False

    # Create two different user IDs
    user1_id = str(uuid.uuid4())
    user2_id = str(uuid.uuid4())
    print(f"User 1 ID: {user1_id}")
    print(f"User 2 ID: {user2_id}")

    # Create a task for user 1
    task_result = add_task(
        user_id=user1_id,
        title="User 1 Task",
        description="This task belongs to user 1"
    )
    task_id = task_result['id']
    print(f"✅ Created task for user 1: {task_id}")

    # Verify user 1 can see their task
    user1_tasks = list_tasks(user_id=user1_id)
    assert len(user1_tasks) == 1
    print("✅ User 1 can see their task")

    # Verify user 2 cannot see user 1's task
    user2_tasks = list_tasks(user_id=user2_id)
    assert len(user2_tasks) == 0
    print("✅ User 2 cannot see user 1's task (proper isolation)")

    # Try to complete user 1's task with user 2's ID (should fail)
    try:
        complete_task(user_id=user2_id, task_id=task_id)
        print("❌ User 2 was able to complete user 1's task - this is a security issue!")
        return False
    except ValueError:
        print("✅ User 2 was correctly denied access to user 1's task")

    # Clean up: delete the task with the correct user
    delete_task(user_id=user1_id, task_id=task_id)
    print("✅ Cleaned up test data")

    print("✅ User isolation tests passed!")
    return True

if __name__ == "__main__":
    print("Starting MCP Task Tools Server tests...")

    # Test basic functionality
    success1 = test_task_operations()

    # Test user isolation
    success2 = test_user_isolation()

    if success1 and success2:
        print("\n🎉 All tests passed! The MCP Task Tools Server is fully functional.")
        print("✅ All 5 tools (add_task, list_tasks, update_task, complete_task, delete_task) work correctly")
        print("✅ User isolation is properly enforced")
        print("✅ Database operations work as expected")
        print("✅ Error handling is in place")
    else:
        print("\n❌ Some tests failed. Please check the implementation.")
        sys.exit(1)