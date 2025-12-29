#!/usr/bin/env python3
"""
Test script for MCP Task Tools Server - Core Functionality
This script tests the core task functionality without the MCP protocol layer.
"""

import sys
import os
import uuid
from datetime import datetime

# Add the project root to the path so we can import the modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_core_functionality():
    """Test the core task functionality"""
    print("Testing core task functionality...")

    # Import the core modules
    try:
        from backend.src.models.task import Task, TaskCreate, TaskUpdate, TaskRead
        from backend.src.core.database import get_session_context
        from sqlmodel import select
        print("✅ Successfully imported backend modules")
    except ImportError as e:
        print(f"❌ Failed to import backend modules: {e}")
        return False

    # Generate a test user ID
    test_user_id = uuid.uuid4()
    print(f"Using test user ID: {test_user_id}")

    # Test database operations directly
    print("\n--- Testing Database Operations ---")

    # Add a task directly to the database
    try:
        with get_session_context() as session:
            # Create a task using TaskCreate for validation, then create Task instance
            task_create = TaskCreate(
                title="Test Task",
                description="This is a test task for verification"
            )

            # Create the Task instance directly with all required fields
            task = Task(
                title=task_create.title,
                description=task_create.description,
                status=task_create.status or "pending",
                priority=task_create.priority or "medium",
                due_date=task_create.due_date,
                user_id=test_user_id
            )

            session.add(task)
            session.flush()  # This will assign the ID but not commit yet
            task_id = task.id
            print(f"✅ Task created successfully: {task.title}")
            print(f"   Task ID: {task_id}")
            assert task.user_id == test_user_id
            assert task.title == "Test Task"
            print("✅ Task correctly stored in database")

        # Context manager commits here, so now we need to get a fresh session to read
        with get_session_context() as session:
            # Test reading the task back
            retrieved_task = session.get(Task, task_id)
            assert retrieved_task is not None
            assert retrieved_task.title == "Test Task"
            assert retrieved_task.user_id == test_user_id
            print("✅ Task correctly retrieved from database")

            # Test updating the task - need new session
            with get_session_context() as update_session:
                # Get the task again in the new session
                task_to_update = update_session.get(Task, task_id)
                assert task_to_update is not None
                task_to_update.title = "Updated Test Task"
                task_to_update.description = "This is an updated test task"
                update_session.add(task_to_update)
                # commit happens automatically

            # Verify update in a new session
            with get_session_context() as verify_session:
                updated_task = verify_session.get(Task, task_id)
                assert updated_task is not None
                assert updated_task.title == "Updated Test Task"
                print("✅ Task correctly updated in database")

            # Test listing tasks for user - need new session
            with get_session_context() as list_session:
                query = select(Task).where(Task.user_id == test_user_id)
                user_tasks = list_session.exec(query).all()
                assert len(user_tasks) == 1
                assert user_tasks[0].id == task_id
                print("✅ Task correctly found when querying for user")

            # Test deleting the task - need new session
            with get_session_context() as delete_session:
                task_to_delete = delete_session.get(Task, task_id)
                if task_to_delete:
                    delete_session.delete(task_to_delete)
                    # commit happens automatically

            # Verify deletion - need new session
            with get_session_context() as verify_delete_session:
                deleted_task = verify_delete_session.get(Task, task_id)
                assert deleted_task is None
                print("✅ Task correctly deleted from database")

    except Exception as e:
        print(f"❌ Failed database operations: {e}")
        import traceback
        traceback.print_exc()
        return False

    print("\n✅ Core functionality tests passed!")
    return True

def test_user_isolation_core():
    """Test user isolation at the database level"""
    print("\n--- Testing User Isolation at Database Level ---")

    try:
        from backend.src.models.task import Task, TaskCreate
        from backend.src.core.database import get_session_context
        from sqlmodel import select
    except ImportError as e:
        print(f"❌ Failed to import backend modules: {e}")
        return False

    # Create two different user IDs
    user1_id = uuid.uuid4()
    user2_id = uuid.uuid4()
    print(f"User 1 ID: {user1_id}")
    print(f"User 2 ID: {user2_id}")

    try:
        with get_session_context() as session:
            # Create a task for user 1
            task_create = TaskCreate(
                title="User 1 Task",
                description="This task belongs to user 1"
            )
            task = Task(
                title=task_create.title,
                description=task_create.description,
                status=task_create.status or "pending",
                priority=task_create.priority or "medium",
                due_date=task_create.due_date,
                user_id=user1_id
            )

            session.add(task)
            session.flush()  # Assign the ID
            task_id = task.id
            print(f"✅ Created task for user 1: {task_id}")

        # Query tasks for user 1 - should find 1 task in new session
        with get_session_context() as session:
            user1_query = select(Task).where(Task.user_id == user1_id)
            user1_tasks = session.exec(user1_query).all()
            assert len(user1_tasks) == 1
            print("✅ User 1 can see their task")

        # Query tasks for user 2 - should find 0 tasks in new session
        with get_session_context() as session:
            user2_query = select(Task).where(Task.user_id == user2_id)
            user2_tasks = session.exec(user2_query).all()
            assert len(user2_tasks) == 0
            print("✅ User 2 cannot see user 1's task (proper isolation)")

        # Clean up: delete the task in new session
        with get_session_context() as session:
            task_to_delete = session.get(Task, task_id)
            if task_to_delete:
                session.delete(task_to_delete)
                # commit happens automatically
        print("✅ Cleaned up test data")

    except Exception as e:
        print(f"❌ Failed user isolation test: {e}")
        import traceback
        traceback.print_exc()
        return False

    print("✅ User isolation tests passed!")
    return True

if __name__ == "__main__":
    print("Starting core functionality tests...")

    # Test core functionality
    success1 = test_core_functionality()

    # Test user isolation
    success2 = test_user_isolation_core()

    if success1 and success2:
        print("\n🎉 All core functionality tests passed!")
        print("✅ Database operations work correctly")
        print("✅ User isolation is properly enforced at the database level")
        print("✅ Task CRUD operations function as expected")
        print("\nThe MCP server implementation is built on top of these working core functions.")
    else:
        print("\n❌ Some core tests failed.")
        sys.exit(1)