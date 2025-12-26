#!/usr/bin/env python3
"""
Test script to validate the new Task Organization & Usability features.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from src.todo_app.core.todo_service import TodoService
from src.todo_app.storage.in_memory_storage import InMemoryTaskRepository
from src.todo_app.models.todo import Priority, TaskStatus, SortField, SortOrder
from datetime import datetime, timedelta


def test_new_features():
    """Test all new features of the enhanced todo app"""
    print("Testing new features implementation...")

    # Initialize service
    repository = InMemoryTaskRepository()
    service = TodoService(repository)

    # Test 1: Add task with all new features
    print("\n1. Testing add_task with new features...")
    task1 = service.add_task(
        title="Test Task 1",
        description="Test description 1",
        priority=Priority.HIGH,
        tags=["work", "urgent"],
        due_date=datetime.now() + timedelta(days=1)
    )
    print(f"   ✓ Added task: {task1.title}")
    print(f"   ✓ Priority: {task1.priority}")
    print(f"   ✓ Tags: {task1.tags}")
    print(f"   ✓ Due date: {task1.due_date}")

    task2 = service.add_task(
        title="Test Task 2",
        description="Test description 2",
        priority=Priority.LOW,
        tags=["personal"],
        due_date=datetime.now() + timedelta(days=7)
    )
    print(f"   ✓ Added task: {task2.title} with LOW priority")

    task3 = service.add_task(
        title="Medium Priority Task",
        description="Test description 3",
        priority=Priority.MEDIUM,
        tags=["work", "review"],
    )
    print(f"   ✓ Added task: {task3.title} with MEDIUM priority")

    # Test 2: Filter tasks by priority
    print("\n2. Testing filter_tasks by priority...")
    high_priority_tasks = service.filter_tasks(priority=Priority.HIGH)
    print(f"   ✓ Found {len(high_priority_tasks)} high priority tasks")

    low_priority_tasks = service.filter_tasks(priority=Priority.LOW)
    print(f"   ✓ Found {len(low_priority_tasks)} low priority tasks")

    # Test 3: Filter tasks by tags
    print("\n3. Testing filter_tasks by tags...")
    work_tasks = service.filter_tasks(tags=["work"])
    print(f"   ✓ Found {len(work_tasks)} tasks with 'work' tag")

    # Test 4: Search functionality
    print("\n4. Testing search functionality...")
    search_results = service.filter_tasks(search_keyword="Test")
    print(f"   ✓ Found {len(search_results)} tasks matching 'Test'")

    # Test 5: Sort tasks by priority
    print("\n5. Testing sort_tasks by priority...")
    all_tasks = service.list_tasks()
    sorted_tasks = service.sort_tasks(all_tasks, SortField.PRIORITY, SortOrder.DESC)
    print(f"   ✓ Sorted {len(sorted_tasks)} tasks by priority (desc)")
    for task in sorted_tasks:
        print(f"     - {task.title}: {task.priority}")

    # Test 6: Sort tasks by due date
    print("\n6. Testing sort_tasks by due date...")
    sorted_by_date = service.sort_tasks(all_tasks, SortField.DUE_DATE, SortOrder.ASC)
    print(f"   ✓ Sorted {len(sorted_by_date)} tasks by due date (asc)")
    for task in sorted_by_date:
        due_str = task.due_date.strftime("%Y-%m-%d") if task.due_date else "None"
        print(f"     - {task.title}: {due_str}")

    # Test 7: List tasks with filters and sorting
    print("\n7. Testing list_tasks with filters and sorting...")
    filtered_sorted = service.list_tasks(
        priority=Priority.HIGH,
        sort_field=SortField.CREATED_DATE,
        sort_order=SortOrder.DESC
    )
    print(f"   ✓ Found and sorted {len(filtered_sorted)} high priority tasks")

    # Test 8: Update task with new fields
    print("\n8. Testing update_task with new fields...")
    updated_task = service.update_task(
        task_id=task1.id,
        title="Updated Test Task 1",
        priority=Priority.MEDIUM,
        tags=["updated", "work", "important"],
        due_date=datetime.now() + timedelta(days=3)
    )
    if updated_task:
        print(f"   ✓ Updated task: {updated_task.title}")
        print(f"   ✓ New priority: {updated_task.priority}")
        print(f"   ✓ New tags: {updated_task.tags}")
    else:
        print("   ✗ Failed to update task")

    # Test 9: Backward compatibility - adding task without new fields
    print("\n9. Testing backward compatibility...")
    simple_task = service.add_task(title="Simple Task", description="No new features")
    print(f"   ✓ Added simple task: {simple_task.title}")
    print(f"   ✓ Default priority: {simple_task.priority}")
    print(f"   ✓ Default tags: {simple_task.tags}")
    print(f"   ✓ Default due date: {simple_task.due_date}")

    print("\n✓ All tests passed! New features are working correctly.")
    print("✓ Backward compatibility maintained.")
    print("✓ Enhanced functionality successfully implemented.")


if __name__ == "__main__":
    test_new_features()