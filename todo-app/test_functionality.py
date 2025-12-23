#!/usr/bin/env python3
"""
Quick test script to demonstrate the todo app functionality.
"""
from src.core.todo_service import TodoService
from src.storage.in_memory_storage import InMemoryTaskRepository

def main():
    print("Testing Todo App functionality...")

    # Create a service with in-memory storage
    repository = InMemoryTaskRepository()
    service = TodoService(repository)

    # Add a task
    print("\n1. Adding a task:")
    task = service.add_task("Test Task", "This is a test task")
    print(f"   Added task: {task.title} (ID: {task.id})")

    # List tasks
    print("\n2. Listing all tasks:")
    tasks = service.list_tasks()
    for t in tasks:
        status = "COMPLETE" if t.status == "complete" else "PENDING"
        print(f"   ID: {t.id}, Title: {t.title}, Status: {status}")

    # Update a task
    print("\n3. Updating the task:")
    updated_task = service.update_task(task.id, title="Updated Task Title")
    print(f"   Updated task: {updated_task.title}")

    # Toggle task status
    print("\n4. Toggling task status:")
    toggled_task = service.toggle_task_status(task.id)
    status = "COMPLETE" if toggled_task.status == "complete" else "PENDING"
    print(f"   Task status is now: {status}")

    # Delete the task
    print("\n5. Deleting the task:")
    success = service.delete_task(task.id)
    print(f"   Task deleted: {success}")

    # List tasks again
    print("\n6. Listing tasks after deletion:")
    tasks = service.list_tasks()
    print(f"   Number of tasks: {len(tasks)}")

    print("\nAll functionality tested successfully!")

if __name__ == "__main__":
    main()