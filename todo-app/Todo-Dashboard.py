#!/usr/bin/env python3
"""
Todo Dashboard - Interactive CLI Interface for Todo App
A colorful, feature-rich dashboard for managing tasks with priorities, tags, and due dates
Maintains in-memory data consistency during the session
"""

import os
import sys
from datetime import datetime
import time

# ANSI color codes for colorful output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BRIGHT = '\033[1m'

def print_colored(text, color, end='\n'):
    """Print colored text"""
    print(f"{color}{text}{Colors.ENDC}", end=end)

def clear_screen():
    """Clear the terminal screen"""
    os.system('clear' if os.name == 'posix' else 'cls')

def show_header():
    """Display the dashboard header"""
    clear_screen()
    print_colored("╔" + "═" * 78 + "╗", Colors.HEADER)
    print_colored("║", Colors.HEADER, "")
    print_colored("                        📝 TODO DASHBOARD - INTERACTIVE CLI", Colors.OKBLUE)
    print_colored("║", Colors.HEADER, "")
    print_colored("╠" + "═" * 78 + "╣", Colors.HEADER)
    print_colored("║", Colors.HEADER, "")
    print_colored("║  🎯 Features: Priorities, Tags, Due Dates, Filtering & Sorting", Colors.OKGREEN)
    print_colored("║", Colors.HEADER, "")
    print_colored("╚" + "═" * 78 + "╝", Colors.HEADER)
    print()

def show_dashboard(tasks_manager):
    """Display the dashboard with current task statistics"""
    tasks = tasks_manager.get_all_tasks()

    print_colored("📊 DASHBOARD STATISTICS", Colors.OKCYAN)
    print_colored("┌" + "─" * 35 + "┐", Colors.OKCYAN)
    print_colored(f"│ Total Tasks: {len(tasks):<24} │", Colors.OKCYAN)

    pending_tasks = sum(1 for task in tasks if task.status == 'pending')
    complete_tasks = sum(1 for task in tasks if task.status == 'complete')

    print_colored(f"│ Pending: {pending_tasks:<28} │", Colors.WARNING)
    print_colored(f"│ Completed: {complete_tasks:<26} │", Colors.OKGREEN)

    high_tasks = sum(1 for task in tasks if task.priority == 'high')
    medium_tasks = sum(1 for task in tasks if task.priority == 'medium')
    low_tasks = sum(1 for task in tasks if task.priority == 'low')

    print_colored("├" + "─" * 35 + "┤", Colors.OKCYAN)
    print_colored(f"│ 🟢 Low Priority: {low_tasks:<18} │", Colors.OKGREEN)
    print_colored(f"│ 🟡 Medium Priority: {medium_tasks:<15} │", Colors.OKCYAN)
    print_colored(f"│ 🔴 High Priority: {high_tasks:<17} │", Colors.FAIL)
    print_colored("└" + "─" * 35 + "┘", Colors.OKCYAN)
    print()

def show_menu():
    """Display the main menu"""
    print_colored("📋 MAIN MENU", Colors.OKCYAN)
    print_colored("┌" + "─" * 50 + "┐", Colors.OKCYAN)
    print_colored("│", Colors.OKCYAN, "")
    print_colored("│ 1. ➕ Add New Task", Colors.OKGREEN)
    print_colored("│ 2. 📋 List All Tasks", Colors.OKGREEN)
    print_colored("│ 3. 🔍 Filter & Search Tasks", Colors.OKGREEN)
    print_colored("│ 4. 📌 Update Task", Colors.OKGREEN)
    print_colored("│ 5. ✅ Complete Task", Colors.OKGREEN)
    print_colored("│ 6. 🗑️ Delete Task", Colors.OKGREEN)
    print_colored("│ 7. 📊 Dashboard Overview", Colors.OKGREEN)
    print_colored("│ 8. ❓ Help & Documentation", Colors.WARNING)
    print_colored("│ 0. 🚪 Exit", Colors.FAIL)
    print_colored("│", Colors.OKCYAN, "")
    print_colored("└" + "─" * 50 + "┘", Colors.OKCYAN)
    print()

class Task:
    """Task model to represent a task in memory"""
    def __init__(self, task_id, title, description="", status="pending", priority="medium", tags=None, due_date=None):
        self.id = task_id
        self.title = title
        self.description = description
        self.status = status
        self.priority = priority
        self.tags = tags or []
        self.due_date = due_date
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

class TasksManager:
    """In-memory task manager to maintain state during session"""
    def __init__(self):
        self.tasks = {}
        self.next_id = 1
        self.priority_colors = {
            'low': '🟢',
            'medium': '🟡',
            'high': '🔴'
        }
        self.status_symbols = {
            'pending': '❌',
            'complete': '✅'
        }

    def add_task(self, title, description="", priority="medium", tags=None, due_date=None):
        """Add a new task"""
        task = Task(
            task_id=self.next_id,
            title=title,
            description=description,
            priority=priority,
            tags=tags or [],
            due_date=due_date
        )
        self.tasks[self.next_id] = task
        self.next_id += 1
        return task

    def get_task(self, task_id):
        """Get a task by ID"""
        return self.tasks.get(task_id)

    def get_all_tasks(self):
        """Get all tasks"""
        return list(self.tasks.values())

    def update_task(self, task_id, title=None, description=None, status=None, priority=None, tags=None, due_date=None):
        """Update a task"""
        task = self.get_task(task_id)
        if not task:
            return None

        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if status is not None:
            task.status = status
        if priority is not None:
            task.priority = priority
        if tags is not None:
            task.tags = tags
        if due_date is not None:
            task.due_date = due_date

        task.updated_at = datetime.now()
        return task

    def delete_task(self, task_id):
        """Delete a task"""
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False

    def toggle_task_status(self, task_id):
        """Toggle task status between pending and complete"""
        task = self.get_task(task_id)
        if not task:
            return None

        task.status = 'complete' if task.status == 'pending' else 'pending'
        task.updated_at = datetime.now()
        return task

    def filter_tasks(self, status=None, priority=None, tags=None, search_keyword=None):
        """Filter tasks based on criteria"""
        filtered_tasks = self.get_all_tasks()

        if status:
            filtered_tasks = [task for task in filtered_tasks if task.status == status]

        if priority:
            filtered_tasks = [task for task in filtered_tasks if task.priority == priority]

        if tags:
            # Tasks must have ALL specified tags
            for tag in tags:
                filtered_tasks = [task for task in filtered_tasks if tag in task.tags]

        if search_keyword:
            search_lower = search_keyword.lower()
            filtered_tasks = [
                task for task in filtered_tasks
                if search_lower in task.title.lower() or search_lower in task.description.lower()
            ]

        return filtered_tasks

    def sort_tasks(self, tasks, sort_field='created_at', sort_order='asc'):
        """Sort tasks by specified field"""
        reverse = sort_order == 'desc'

        if sort_field == 'priority':
            priority_order = {'high': 3, 'medium': 2, 'low': 1}
            sorted_tasks = sorted(tasks,
                                key=lambda t: priority_order.get(t.priority, 0),
                                reverse=reverse)
        elif sort_field == 'due_date':
            # Handle None dates - they should appear last
            def sort_key(task):
                if task.due_date is None:
                    return (1, datetime.max) if sort_order == 'asc' else (0, datetime.min)
                return (0, task.due_date) if sort_order == 'asc' else (1, task.due_date)
            sorted_tasks = sorted(tasks, key=sort_key)
        elif sort_field == 'status':
            status_order = {'complete': 2, 'pending': 1}
            sorted_tasks = sorted(tasks,
                                key=lambda t: status_order.get(t.status, 0),
                                reverse=reverse)
        elif sort_field == 'title':
            sorted_tasks = sorted(tasks,
                                key=lambda t: t.title.lower(),
                                reverse=reverse)
        else:  # created_at
            sorted_tasks = sorted(tasks,
                                key=lambda t: t.created_at,
                                reverse=reverse)

        return sorted_tasks

    def display_tasks(self, tasks, title="Task List"):
        """Display tasks in a formatted table"""
        if not tasks:
            print_colored("📭 No tasks found.", Colors.WARNING)
            return

        print_colored(f"📋 {title}", Colors.OKCYAN)
        print_colored("┌" + "─" * 80 + "┐", Colors.OKCYAN)
        print_colored(f"│ {'ID':<3} │ {'Title':<20} │ {'Status':<10} │ {'Priority':<10} │ {'Tags':<15} │", Colors.OKCYAN)

        for task in tasks:
            status_symbol = self.status_symbols.get(task.status, '❓')
            priority_emoji = self.priority_colors.get(task.priority, '❓')
            tags_str = ", ".join(task.tags[:3])  # Show first 3 tags
            if len(task.tags) > 3:
                tags_str += "..."

            print_colored(f"│ {task.id:<3} │ {task.title[:18]:<20} │ {status_symbol} {task.status:<7} │ {priority_emoji} {task.priority:<7} │ {tags_str:<15} │", Colors.OKCYAN)

        print_colored("└" + "─" * 80 + "┘", Colors.OKCYAN)
        print()

def add_task_interactive(tasks_manager):
    """Interactive task addition"""
    print_colored("\n➕ ADD NEW TASK", Colors.OKCYAN)
    print_colored("┌" + "─" * 40 + "┐", Colors.OKCYAN)

    title = input("│ Enter task title: ").strip()
    if not title:
        print_colored("│ ❌ Title cannot be empty!", Colors.FAIL)
        print_colored("└" + "─" * 40 + "┘", Colors.OKCYAN)
        return

    description = input("│ Enter task description (optional): ").strip()

    print_colored("│", Colors.OKCYAN)
    print_colored("│ Select priority:", Colors.WARNING)
    print_colored("│ 1. 🟢 Low", Colors.OKGREEN)
    print_colored("│ 2. 🟡 Medium (default)", Colors.OKCYAN)
    print_colored("│ 3. 🔴 High", Colors.FAIL)
    priority_choice = input("│ Enter choice (1-3, default 2): ").strip()

    priority_map = {"1": "low", "2": "medium", "3": "high"}
    priority = priority_map.get(priority_choice, "medium")

    tags_input = input("│ Enter tags (comma separated, optional): ").strip()
    tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()] if tags_input else []

    due_date_input = input("│ Enter due date (YYYY-MM-DD, optional): ").strip()
    due_date = None
    if due_date_input:
        try:
            due_date = datetime.strptime(due_date_input, "%Y-%m-%d")
        except ValueError:
            print_colored("│ ⚠️ Invalid date format, ignoring...", Colors.WARNING)

    print_colored("└" + "─" * 40 + "┘", Colors.OKCYAN)

    try:
        task = tasks_manager.add_task(
            title=title,
            description=description,
            priority=priority,
            tags=tags,
            due_date=due_date
        )
        print_colored(f"\n✅ Task added successfully! ID: {task.id}", Colors.OKGREEN)
    except Exception as e:
        print_colored(f"\n❌ Error adding task: {str(e)}", Colors.FAIL)

def list_tasks_interactive(tasks_manager):
    """Interactive task listing with filters"""
    print_colored("\n📋 LIST TASKS", Colors.OKCYAN)
    print_colored("┌" + "─" * 50 + "┐", Colors.OKCYAN)
    print_colored("│ Filter options (press Enter to skip):", Colors.WARNING)

    status = input("│ Status (pending/complete): ").strip().lower()
    if status and status not in ["pending", "complete"]:
        status = None

    priority = input("│ Priority (low/medium/high): ").strip().lower()
    if priority and priority not in ["low", "medium", "high"]:
        priority = None

    tag_input = input("│ Tag (comma separated): ").strip()
    tags = [tag.strip() for tag in tag_input.split(",") if tag.strip()] if tag_input else None

    search = input("│ Search keyword: ").strip()

    sort_by = input("│ Sort by (title/priority/due_date/status/created_at, default created_at): ").strip()
    if sort_by and sort_by not in ["title", "priority", "due_date", "status", "created_at"]:
        sort_by = "created_at"
    elif not sort_by:
        sort_by = "created_at"

    sort_order = input("│ Sort order (asc/desc, default asc): ").strip().lower()
    if sort_order and sort_order not in ["asc", "desc"]:
        sort_order = "asc"
    elif not sort_order:
        sort_order = "asc"

    print_colored("└" + "─" * 50 + "┘", Colors.OKCYAN)

    # Apply filters
    filtered_tasks = tasks_manager.get_all_tasks()
    if status or priority or tags or search:
        filtered_tasks = tasks_manager.filter_tasks(
            status=status if status else None,
            priority=priority if priority else None,
            tags=tags if tags else None,
            search_keyword=search if search else None
        )

    # Apply sorting
    sorted_tasks = tasks_manager.sort_tasks(filtered_tasks, sort_by, sort_order)

    tasks_manager.display_tasks(sorted_tasks, f"Filtered Tasks ({len(sorted_tasks)} found)")

def filter_search_menu(tasks_manager):
    """Interactive filtering and search menu"""
    print_colored("\n🔍 FILTER & SEARCH TASKS", Colors.OKCYAN)
    print_colored("┌" + "─" * 50 + "┐", Colors.OKCYAN)
    print_colored("│ 1. 📅 Filter by Status", Colors.OKGREEN)
    print_colored("│ 2. ⭐ Filter by Priority", Colors.OKGREEN)
    print_colored("│ 3. 🏷️ Filter by Tag", Colors.OKGREEN)
    print_colored("│ 4. 🔍 Search by Keyword", Colors.OKGREEN)
    print_colored("│ 5. 📈 Sort Tasks", Colors.OKGREEN)
    print_colored("│ 6. 🔄 Combined Filters", Colors.OKGREEN)
    print_colored("│ 0. ◀️ Back to Main Menu", Colors.WARNING)
    print_colored("└" + "─" * 50 + "┘", Colors.OKCYAN)

    choice = input("\nEnter your choice: ").strip()

    if choice == "1":
        status = input("Enter status (pending/complete): ").strip().lower()
        if status in ["pending", "complete"]:
            filtered_tasks = tasks_manager.filter_tasks(status=status)
            tasks_manager.display_tasks(filtered_tasks, f"Tasks with status: {status}")
        else:
            print_colored("❌ Invalid status!", Colors.FAIL)

    elif choice == "2":
        priority = input("Enter priority (low/medium/high): ").strip().lower()
        if priority in ["low", "medium", "high"]:
            filtered_tasks = tasks_manager.filter_tasks(priority=priority)
            tasks_manager.display_tasks(filtered_tasks, f"Tasks with priority: {priority}")
        else:
            print_colored("❌ Invalid priority!", Colors.FAIL)

    elif choice == "3":
        tag = input("Enter tag: ").strip()
        if tag:
            filtered_tasks = tasks_manager.filter_tasks(tags=[tag])
            tasks_manager.display_tasks(filtered_tasks, f"Tasks with tag: {tag}")
        else:
            print_colored("❌ Tag cannot be empty!", Colors.FAIL)

    elif choice == "4":
        keyword = input("Enter search keyword: ").strip()
        if keyword:
            filtered_tasks = tasks_manager.filter_tasks(search_keyword=keyword)
            tasks_manager.display_tasks(filtered_tasks, f"Search results for: {keyword}")
        else:
            print_colored("❌ Keyword cannot be empty!", Colors.FAIL)

    elif choice == "5":
        print("Sort by (title/priority/due_date/status/created_at): ", end="")
        field = input().strip()
        if field not in ["title", "priority", "due_date", "status", "created_at"]:
            field = "created_at"
        print("Order (asc/desc, default asc): ", end="")
        order = input().strip() or "asc"
        if order not in ["asc", "desc"]:
            order = "asc"

        all_tasks = tasks_manager.get_all_tasks()
        sorted_tasks = tasks_manager.sort_tasks(all_tasks, field, order)
        tasks_manager.display_tasks(sorted_tasks, f"Tasks sorted by {field} ({order})")

    elif choice == "6":
        list_tasks_interactive(tasks_manager)

    elif choice == "0":
        return
    else:
        print_colored("❌ Invalid choice!", Colors.FAIL)

def update_task_interactive(tasks_manager):
    """Interactive task update"""
    print_colored("\n📌 UPDATE TASK", Colors.OKCYAN)
    print_colored("┌" + "─" * 40 + "┐", Colors.OKCYAN)

    try:
        task_id = int(input("│ Enter task ID to update: "))
    except ValueError:
        print_colored("│ ❌ Invalid task ID!", Colors.FAIL)
        print_colored("└" + "─" * 40 + "┘", Colors.OKCYAN)
        return

    task = tasks_manager.get_task(task_id)
    if not task:
        print_colored(f"│ ❌ Task with ID {task_id} not found!", Colors.FAIL)
        print_colored("└" + "─" * 40 + "┘", Colors.OKCYAN)
        return

    print_colored("│ Current task:", Colors.WARNING)
    print_colored(f"│ ID: {task.id} | Title: {task.title} | Status: {task.status} | Priority: {task.priority}", Colors.OKCYAN)

    print_colored("│ Enter new values (press Enter to keep current):", Colors.WARNING)
    title = input("│ New title: ").strip()
    title = title if title else task.title

    description = input("│ New description: ").strip()
    description = description if description else task.description

    print("│ New priority (low/medium/high, Enter to keep current): ", end="")
    priority = input().strip().lower()
    priority = priority if priority in ["low", "medium", "high"] else task.priority

    tags_input = input("│ New tags (comma separated, Enter to keep current): ").strip()
    tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()] if tags_input else task.tags

    due_date_input = input("│ New due date (YYYY-MM-DD, Enter to keep current): ").strip()
    if due_date_input:
        try:
            due_date = datetime.strptime(due_date_input, "%Y-%m-%d")
        except ValueError:
            print_colored("│ ⚠️ Invalid date format, keeping current...", Colors.WARNING)
            due_date = task.due_date
    else:
        due_date = task.due_date

    print_colored("└" + "─" * 40 + "┘", Colors.OKCYAN)

    try:
        updated_task = tasks_manager.update_task(
            task_id=task_id,
            title=title,
            description=description,
            priority=priority,
            tags=tags,
            due_date=due_date
        )
        if updated_task:
            print_colored(f"\n✅ Task {task_id} updated successfully!", Colors.OKGREEN)
        else:
            print_colored(f"\n❌ Error updating task {task_id}!", Colors.FAIL)
    except Exception as e:
        print_colored(f"\n❌ Error updating task: {str(e)}", Colors.FAIL)

def complete_task_interactive(tasks_manager):
    """Interactive task completion"""
    print_colored("\n✅ COMPLETE TASK", Colors.OKCYAN)
    print_colored("┌" + "─" * 40 + "┐", Colors.OKCYAN)

    try:
        task_id = int(input("│ Enter task ID to complete: "))
    except ValueError:
        print_colored("│ ❌ Invalid task ID!", Colors.FAIL)
        print_colored("└" + "─" * 40 + "┘", Colors.OKCYAN)
        return

    task = tasks_manager.get_task(task_id)
    if not task:
        print_colored(f"│ ❌ Task with ID {task_id} not found!", Colors.FAIL)
        print_colored("└" + "─" * 40 + "┘", Colors.OKCYAN)
        return

    print_colored("└" + "─" * 40 + "┘", Colors.OKCYAN)

    updated_task = tasks_manager.toggle_task_status(task_id)
    if updated_task:
        status = "completed" if updated_task.status == 'complete' else "marked as pending"
        print_colored(f"\n✅ Task {task_id} {status}!", Colors.OKGREEN)
    else:
        print_colored(f"\n❌ Error completing task {task_id}!", Colors.FAIL)

def delete_task_interactive(tasks_manager):
    """Interactive task deletion"""
    print_colored("\n🗑️ DELETE TASK", Colors.OKCYAN)
    print_colored("┌" + "─" * 40 + "┐", Colors.OKCYAN)

    try:
        task_id = int(input("│ Enter task ID to delete: "))
    except ValueError:
        print_colored("│ ❌ Invalid task ID!", Colors.FAIL)
        print_colored("└" + "─" * 40 + "┘", Colors.OKCYAN)
        return

    task = tasks_manager.get_task(task_id)
    if not task:
        print_colored(f"│ ❌ Task with ID {task_id} not found!", Colors.FAIL)
        print_colored("└" + "─" * 40 + "┘", Colors.OKCYAN)
        return

    confirm = input(f"│ Are you sure you want to delete task '{task.title}'? (y/N): ").strip().lower()
    if confirm == 'y':
        success = tasks_manager.delete_task(task_id)
        if success:
            print_colored("│ 🗑️ Task deleted successfully!", Colors.OKGREEN)
        else:
            print_colored("│ ❌ Error deleting task!", Colors.FAIL)
    else:
        print_colored("│ ❌ Deletion cancelled.", Colors.WARNING)

    print_colored("└" + "─" * 40 + "┘", Colors.OKCYAN)

def show_help():
    """Show help and documentation"""
    clear_screen()
    print_colored("╔" + "═" * 78 + "╗", Colors.HEADER)
    print_colored("║", Colors.HEADER, "")
    print_colored("                        ❓ HELP & DOCUMENTATION", Colors.OKBLUE)
    print_colored("║", Colors.HEADER, "")
    print_colored("╠" + "═" * 78 + "╣", Colors.HEADER)
    print_colored("║", Colors.HEADER, "")
    print_colored("║ FEATURES:", Colors.OKCYAN)
    print_colored("║ • Add tasks with priority levels (Low, Medium, High)", Colors.OKGREEN)
    print_colored("║ • Tag tasks with multiple labels for organization", Colors.OKGREEN)
    print_colored("║ • Set due dates for tasks", Colors.OKGREEN)
    print_colored("║ • Filter tasks by status, priority, or tags", Colors.OKGREEN)
    print_colored("║ • Search tasks by keyword in title or description", Colors.OKGREEN)
    print_colored("║ • Sort tasks by various criteria", Colors.OKGREEN)
    print_colored("║ • Color-coded priority display", Colors.OKGREEN)
    print_colored("║", Colors.HEADER, "")
    print_colored("║ PRIORITY LEVELS:", Colors.WARNING)
    print_colored("║   🟢 Low: Less important tasks", Colors.OKGREEN)
    print_colored("║   🟡 Medium: Normal priority (default)", Colors.OKCYAN)
    print_colored("║   🔴 High: Most important tasks", Colors.FAIL)
    print_colored("║", Colors.HEADER, "")
    print_colored("║ SORT OPTIONS:", Colors.WARNING)
    print_colored("║   • title: Alphabetical by task title", Colors.OKGREEN)
    print_colored("║   • priority: By priority level", Colors.OKGREEN)
    print_colored("║   • due_date: By due date (null dates appear last)", Colors.OKGREEN)
    print_colored("║   • status: By completion status", Colors.OKGREEN)
    print_colored("║   • created_at: By creation date", Colors.OKGREEN)
    print_colored("║", Colors.HEADER, "")
    print_colored("║ DATE FORMAT:", Colors.WARNING)
    print_colored("║   • YYYY-MM-DD (e.g., 2025-12-31)", Colors.OKGREEN)
    print_colored("║", Colors.HEADER, "")
    print_colored("║", Colors.HEADER, "")
    print_colored("╚" + "═" * 78 + "╝", Colors.HEADER)
    print()
    input("Press Enter to return to main menu...")

def main():
    """Main function to run the Todo Dashboard"""
    # Initialize the tasks manager to maintain in-memory state
    tasks_manager = TasksManager()

    while True:
        show_header()
        show_dashboard(tasks_manager)
        show_menu()

        try:
            choice = input("Enter your choice: ").strip()
        except (EOFError, KeyboardInterrupt):
            print_colored("\n\n👋 Thank you for using Todo Dashboard! Goodbye!", Colors.OKGREEN)
            print_colored("   📝 Made with ❤️ for better task management", Colors.OKCYAN)
            break

        if choice == "1":
            add_task_interactive(tasks_manager)
            input("\nPress Enter to continue...")
        elif choice == "2":
            tasks_manager.display_tasks(tasks_manager.get_all_tasks(), "All Tasks")
            input("\nPress Enter to continue...")
        elif choice == "3":
            filter_search_menu(tasks_manager)
            input("\nPress Enter to continue...")
        elif choice == "4":
            update_task_interactive(tasks_manager)
            input("\nPress Enter to continue...")
        elif choice == "5":
            complete_task_interactive(tasks_manager)
            input("\nPress Enter to continue...")
        elif choice == "6":
            delete_task_interactive(tasks_manager)
            input("\nPress Enter to continue...")
        elif choice == "7":
            # Just refresh the dashboard
            pass
        elif choice == "8":
            show_help()
        elif choice == "0":
            print_colored("\n👋 Thank you for using Todo Dashboard! Goodbye!", Colors.OKGREEN)
            print_colored("   📝 Made with ❤️ for better task management", Colors.OKCYAN)
            break
        else:
            print_colored("❌ Invalid choice! Please try again.", Colors.FAIL)
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()