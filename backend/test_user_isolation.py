#!/usr/bin/env python3
"""
Test script to validate user isolation in the todo app.
This script tests that users can only see and modify their own tasks.
"""
from src.todo_app.core.todo_service import TodoService
from src.todo_app.storage.in_memory_storage import InMemoryTaskRepository

def test_user_isolation():
    """Test that users can only access their own tasks."""
    print("Testing User Isolation in Todo App")
    print("=" * 40)

    # Create a single repository that will be shared
    repository = InMemoryTaskRepository()
    service = TodoService(repository)

    # Test 1: User 1 creates tasks
    print("\n1. Testing User 1 creating tasks...")
    user1_task1 = service.add_task("User 1 Task 1", "Description for user 1", user_id=1)
    user1_task2 = service.add_task("User 1 Task 2", "Description for user 1", user_id=1)
    print(f"   ✓ User 1 created tasks: {user1_task1.title}, {user1_task2.title}")

    # Test 2: User 2 creates tasks
    print("\n2. Testing User 2 creating tasks...")
    user2_task1 = service.add_task("User 2 Task 1", "Description for user 2", user_id=2)
    user2_task2 = service.add_task("User 2 Task 2", "Description for user 2", user_id=2)
    print(f"   ✓ User 2 created tasks: {user2_task1.title}, {user2_task2.title}")

    # Test 3: User 1 should only see their own tasks
    print("\n3. Testing User 1 can only see their own tasks...")
    user1_tasks = service.list_tasks(user_id=1)
    print(f"   ✓ User 1 sees {len(user1_tasks)} tasks: {[t.title for t in user1_tasks]}")
    assert len(user1_tasks) == 2, f"User 1 should see 2 tasks, but sees {len(user1_tasks)}"
    assert all(task.user_id == 1 for task in user1_tasks), "User 1 should only see tasks with user_id=1"

    # Test 4: User 2 should only see their own tasks
    print("\n4. Testing User 2 can only see their own tasks...")
    user2_tasks = service.list_tasks(user_id=2)
    print(f"   ✓ User 2 sees {len(user2_tasks)} tasks: {[t.title for t in user2_tasks]}")
    assert len(user2_tasks) == 2, f"User 2 should see 2 tasks, but sees {len(user2_tasks)}"
    assert all(task.user_id == 2 for task in user2_tasks), "User 2 should only see tasks with user_id=2"

    # Test 5: User 1 cannot update User 2's task
    print("\n5. Testing User 1 cannot update User 2's task...")
    update_result = service.update_task(user2_task1.id, user_id=1, title="Hacked Task")
    print(f"   ✓ Update result: {update_result}")
    assert update_result is None, "User 1 should not be able to update User 2's task"

    # Verify User 2's task remains unchanged
    user2_task1_fresh = service.get_task(user2_task1.id)
    assert user2_task1_fresh.title == "User 2 Task 1", "User 2's task should remain unchanged"
    print("   ✓ User 2's task remains unchanged")

    # Test 6: User 2 cannot delete User 1's task
    print("\n6. Testing User 2 cannot delete User 1's task...")
    delete_result = service.delete_task(user1_task1.id, user_id=2)
    print(f"   ✓ Delete result: {delete_result}")
    assert delete_result is False, "User 2 should not be able to delete User 1's task"

    # Verify User 1's task still exists
    user1_task1_fresh = service.get_task(user1_task1.id)
    assert user1_task1_fresh is not None, "User 1's task should still exist"
    print("   ✓ User 1's task still exists")

    # Test 7: User 1 can update their own task
    print("\n7. Testing User 1 can update their own task...")
    update_result = service.update_task(user1_task1.id, user_id=1, title="Updated User 1 Task")
    print(f"   ✓ Update result: {update_result is not None}")
    assert update_result is not None, "User 1 should be able to update their own task"
    assert update_result.title == "Updated User 1 Task", "Task title should be updated"
    print(f"   ✓ Task updated to: {update_result.title}")

    # Test 8: User 1 can delete their own task
    print("\n8. Testing User 1 can delete their own task...")
    delete_result = service.delete_task(user1_task2.id, user_id=1)
    print(f"   ✓ Delete result: {delete_result}")
    assert delete_result is True, "User 1 should be able to delete their own task"

    # Verify the task is gone
    deleted_task = service.get_task(user1_task2.id)
    assert deleted_task is None, "Deleted task should not exist"
    print("   ✓ Task successfully deleted")

    # Test 9: Verify final task counts
    print("\n9. Testing final task counts...")
    final_user1_tasks = service.list_tasks(user_id=1)
    final_user2_tasks = service.list_tasks(user_id=2)
    print(f"   ✓ User 1 final tasks: {len(final_user1_tasks)}")
    print(f"   ✓ User 2 final tasks: {len(final_user2_tasks)}")
    assert len(final_user1_tasks) == 1, f"User 1 should have 1 task remaining, but has {len(final_user1_tasks)}"
    assert len(final_user2_tasks) == 2, f"User 2 should have 2 tasks remaining, but has {len(final_user2_tasks)}"

    print("\n" + "=" * 40)
    print("✓ All User Isolation Tests PASSED!")
    print("✓ Users can only see, update, and delete their own tasks")
    print("✓ Cross-user access is properly prevented")

if __name__ == "__main__":
    test_user_isolation()