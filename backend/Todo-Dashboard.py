#!/usr/bin/env python3
"""
Todo Dashboard - Interactive CLI Interface for Todo App
A colorful, feature-rich dashboard for managing tasks with priorities, tags, and due dates
Maintains in-memory data consistency during the session
"""

import os
import sys
from datetime import datetime, timedelta
import time

# Try to import i18n module, fallback if not available
try:
    from src.todo_app.core.i18n import i18n_service, Language
    I18N_AVAILABLE = True
except ImportError:
    I18N_AVAILABLE = False
    print("Warning: i18n module not available. Urdu translation features will be disabled.")

# Global variable to track Urdu view mode
urdu_view_mode = False

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

def get_translation(key, urdu_mode=False):
    """Get translation for a key if i18n is available"""
    if I18N_AVAILABLE:
        return i18n_service.get_translation(key, urdu_mode=urdu_mode)
    else:
        # Return English default if i18n is not available
        translation_map = {
            'dashboard': 'Dashboard',
            'dashboard_ur': 'ڈیش بورڈ',
            'total_tasks': 'Total Tasks',
            'total_tasks_ur': 'کل ٹاسکس',
            'pending': 'Pending',
            'pending_ur': 'زیر التوا',
            'completed': 'Completed',
            'completed_ur': 'مکمل',
            'low_priority': 'Low Priority',
            'low_priority_ur': 'کم اہمیت',
            'medium_priority': 'Medium Priority',
            'medium_priority_ur': 'درمیانی اہمیت',
            'high_priority': 'High Priority',
            'high_priority_ur': 'اعلیٰ اہمیت',
            'main_menu': 'Main Menu',
            'main_menu_ur': 'مرکزی مینو',
            'add_task': 'Add New Task',
            'add_task_ur': 'نیا ٹاسک شامل کریں',
            'list_tasks': 'List All Tasks',
            'list_tasks_ur': 'تمام ٹاسکس کی فہرست',
            'filter_search': 'Filter & Search Tasks',
            'filter_search_ur': 'فلٹر اور تلاش ٹاسکس',
            'update_task': 'Update Task',
            'update_task_ur': 'ٹاسک اپ ڈیٹ کریں',
            'complete_task': 'Complete Task',
            'complete_task_ur': 'ٹاسک مکمل کریں',
            'delete_task': 'Delete Task',
            'delete_task_ur': 'ٹاسک حذف کریں',
            'dashboard_overview': 'Dashboard Overview',
            'dashboard_overview_ur': 'ڈیش بورڈ کا جائزہ',
            'help': 'Help & Documentation',
            'help_ur': 'مدد اور دستاویزات',
            'exit': 'Exit',
            'exit_ur': 'باہر نکلیں',
            'no_tasks_found': 'No tasks found.',
            'no_tasks_found_ur': 'کوئی ٹاسک نہیں ملا۔',
            'task_added': 'Task added successfully!',
            'task_added_ur': 'ٹاسک کامیابی سے شامل کیا گیا!',
            'task_updated': 'Task updated successfully!',
            'task_updated_ur': 'ٹاسک کامیابی سے اپ ڈیٹ ہو گیا!',
            'task_deleted': 'Task deleted successfully!',
            'task_deleted_ur': 'ٹاسک کامیابی سے حذف ہو گیا!',
            'task_completed': 'Task completed!',
            'task_completed_ur': 'ٹاسک مکمل ہو گیا!',
            'urdu_mode_enabled': 'Urdu view mode enabled',
            'urdu_mode_enabled_ur': 'اُردو ویو موڈ فعال',
            'urdu_mode_disabled': 'Urdu view mode disabled',
            'urdu_mode_disabled_ur': 'اُردو ویو موڈ غیر فعال',
        }
        # Return Urdu translation if requested and available, otherwise English
        if urdu_mode:
            urdu_key = key + '_ur'
            return translation_map.get(urdu_key, translation_map.get(key, key))
        else:
            return translation_map.get(key, key)

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

    # Use translation for dashboard title
    dashboard_title = get_translation('dashboard', urdu_view_mode)
    print_colored(f"📊 {dashboard_title} STATISTICS", Colors.OKCYAN)
    print_colored("┌" + "─" * 45 + "┐", Colors.OKCYAN)

    total_tasks_label = get_translation('total_tasks', urdu_view_mode)
    print_colored(f"│ {total_tasks_label}: {len(tasks):<34} │", Colors.OKCYAN)

    pending_tasks = sum(1 for task in tasks if task.status == 'pending')
    complete_tasks = sum(1 for task in tasks if task.status == 'complete')

    pending_label = get_translation('pending', urdu_view_mode)
    completed_label = get_translation('completed', urdu_view_mode)
    print_colored(f"│ {pending_label}: {pending_tasks:<38} │", Colors.WARNING)
    print_colored(f"│ {completed_label}: {complete_tasks:<36} │", Colors.OKGREEN)

    high_tasks = sum(1 for task in tasks if task.priority == 'high')
    medium_tasks = sum(1 for task in tasks if task.priority == 'medium')
    low_tasks = sum(1 for task in tasks if task.priority == 'low')

    print_colored("├" + "─" * 45 + "┤", Colors.OKCYAN)

    low_priority_label = get_translation('low_priority', urdu_view_mode)
    medium_priority_label = get_translation('medium_priority', urdu_view_mode)
    high_priority_label = get_translation('high_priority', urdu_view_mode)

    print_colored(f"│ 🟢 {low_priority_label}: {low_tasks:<28} │", Colors.OKGREEN)
    print_colored(f"│ 🟡 {medium_priority_label}: {medium_tasks:<25} │", Colors.OKCYAN)
    print_colored(f"│ 🔴 {high_priority_label}: {high_tasks:<27} │", Colors.FAIL)

    # Add recurring tasks statistics
    recurring_tasks = sum(1 for task in tasks if task.recurrence_pattern != 'none')
    print_colored("├" + "─" * 45 + "┤", Colors.OKCYAN)
    print_colored(f"│ 📅 Recurring Tasks: {recurring_tasks:<27} │", Colors.OKCYAN)

    # Add due tasks statistics
    now = datetime.now()
    due_tasks = sum(1 for task in tasks if task.due_date and task.due_date <= now and task.status == 'pending')
    print_colored(f"│ ⏰ Overdue Tasks: {due_tasks:<29} │", Colors.FAIL)

    print_colored("└" + "─" * 45 + "┘", Colors.OKCYAN)
    print()

def show_menu():
    """Display the main menu"""
    menu_title = get_translation('main_menu', urdu_view_mode)
    print_colored(f"📋 {menu_title}", Colors.OKCYAN)
    print_colored("┌" + "─" * 50 + "┐", Colors.OKCYAN)
    print_colored("│", Colors.OKCYAN, "")

    add_task_label = get_translation('add_task', urdu_view_mode)
    list_tasks_label = get_translation('list_tasks', urdu_view_mode)
    filter_search_label = get_translation('filter_search', urdu_view_mode)
    update_task_label = get_translation('update_task', urdu_view_mode)
    complete_task_label = get_translation('complete_task', urdu_view_mode)
    delete_task_label = get_translation('delete_task', urdu_view_mode)
    dashboard_overview_label = get_translation('dashboard_overview', urdu_view_mode)
    help_label = get_translation('help', urdu_view_mode)
    exit_label = get_translation('exit', urdu_view_mode)

    # Add Urdu toggle label
    urdu_toggle_label = "🌐 Toggle Urdu View" if not urdu_view_mode else "🌐 Toggle English View"

    print_colored(f"│ 1. ➕ {add_task_label}", Colors.OKGREEN)
    print_colored(f"│ 2. 📋 {list_tasks_label}", Colors.OKGREEN)
    print_colored(f"│ 3. 🔍 {filter_search_label}", Colors.OKGREEN)
    print_colored(f"│ 4. 📌 {update_task_label}", Colors.OKGREEN)
    print_colored(f"│ 5. ✅ {complete_task_label}", Colors.OKGREEN)
    print_colored(f"│ 6. 🗑️ {delete_task_label}", Colors.OKGREEN)
    print_colored(f"│ 7. 📊 {dashboard_overview_label}", Colors.OKGREEN)
    print_colored(f"│ 8. 📅 Upcoming Tasks", Colors.OKGREEN)
    print_colored(f"│ 9. 🌐 Toggle Urdu View", Colors.WARNING)  # Urdu toggle option
    print_colored(f"│ 10. ❓ {help_label}", Colors.WARNING)
    print_colored(f"│ 0. 🚪 {exit_label}", Colors.FAIL)
    print_colored("│", Colors.OKCYAN, "")
    print_colored("└" + "─" * 50 + "┘", Colors.OKCYAN)
    print()

from enum import Enum

class RecurrencePattern(str, Enum):
    """Enum for recurrence patterns"""
    NONE = "none"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

class Task:
    """Task model to represent a task in memory"""
    def __init__(self, task_id, title, description="", status="pending", priority="medium", tags=None, due_date=None, recurrence_pattern=None, reminder_sent=False, next_occurrence_date=None):
        self.id = task_id
        self.title = title
        self.description = description
        self.status = status
        self.priority = priority
        self.tags = tags or []
        self.due_date = due_date
        self.recurrence_pattern = recurrence_pattern or RecurrencePattern.NONE
        self.reminder_sent = reminder_sent
        self.next_occurrence_date = next_occurrence_date
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
        self.recurrence_symbols = {
            'none': '🔹',
            'daily': '📅',
            'weekly': '🗓️',
            'monthly': '📅'
        }

    def add_task(self, title, description="", priority="medium", tags=None, due_date=None, recurrence_pattern=None, reminder_sent=False, next_occurrence_date=None):
        """Add a new task"""
        task = Task(
            task_id=self.next_id,
            title=title,
            description=description,
            priority=priority,
            tags=tags or [],
            due_date=due_date,
            recurrence_pattern=recurrence_pattern,
            reminder_sent=reminder_sent,
            next_occurrence_date=next_occurrence_date
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

    def update_task(self, task_id, title=None, description=None, status=None, priority=None, tags=None, due_date=None, recurrence_pattern=None, reminder_sent=None, next_occurrence_date=None):
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
        if recurrence_pattern is not None:
            task.recurrence_pattern = recurrence_pattern
        if reminder_sent is not None:
            task.reminder_sent = reminder_sent
        if next_occurrence_date is not None:
            task.next_occurrence_date = next_occurrence_date

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
            no_tasks_label = get_translation('no_tasks_found', urdu_view_mode)
            print_colored(f"📭 {no_tasks_label}", Colors.WARNING)
            return

        print_colored(f"📋 {title}", Colors.OKCYAN)
        status_label = get_translation('status', urdu_view_mode) or "Status"
        priority_label = get_translation('priority', urdu_view_mode) or "Priority"
        print_colored("┌" + "─" * 100 + "┐", Colors.OKCYAN)
        print_colored(f"│ {'ID':<3} │ {'Title':<15} │ {status_label:<10} │ {priority_label:<10} │ {'Due Date':<12} │ {'Recurrence':<12} │ {'Tags':<15} │", Colors.OKCYAN)

        for task in tasks:
            status_symbol = self.status_symbols.get(task.status, '❓')
            # Use translation for status and priority labels
            status_text = get_translation(task.status, urdu_view_mode)
            priority_text = get_translation(task.priority, urdu_view_mode)
            priority_emoji = self.priority_colors.get(task.priority, '❓')
            recurrence_emoji = self.recurrence_symbols.get(task.recurrence_pattern, '❓')
            tags_str = ", ".join(task.tags[:2])  # Show first 2 tags due to space constraints
            if len(task.tags) > 2:
                tags_str += "..."

            # Format due date
            due_date_str = task.due_date.strftime("%Y-%m-%d") if task.due_date else "None"
            recurrence_str = task.recurrence_pattern if task.recurrence_pattern else "None"

            print_colored(f"│ {task.id:<3} │ {task.title[:13]:<15} │ {status_symbol} {status_text:<7} │ {priority_emoji} {priority_text:<7} │ {due_date_str:<12} │ {recurrence_emoji} {recurrence_str:<8} │ {tags_str:<15} │", Colors.OKCYAN)

        print_colored("└" + "─" * 100 + "┘", Colors.OKCYAN)
        print()

def add_task_interactive(tasks_manager):
    """Interactive task addition"""
    print_colored("\n➕ ADD NEW TASK", Colors.OKCYAN)
    print_colored("┌" + "─" * 50 + "┐", Colors.OKCYAN)

    title = input("│ Enter task title: ").strip()
    if not title:
        print_colored("│ ❌ Title cannot be empty!", Colors.FAIL)
        print_colored("└" + "─" * 50 + "┘", Colors.OKCYAN)
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

    print_colored("│", Colors.OKCYAN)
    print_colored("│ Select recurrence pattern:", Colors.WARNING)
    print_colored("│ 1. 🔹 None (default)", Colors.OKCYAN)
    print_colored("│ 2. 📅 Daily", Colors.OKGREEN)
    print_colored("│ 3. 🗓️ Weekly", Colors.OKGREEN)
    print_colored("│ 4. 📆 Monthly", Colors.OKGREEN)
    recurrence_choice = input("│ Enter choice (1-4, default 1): ").strip()

    recurrence_map = {"1": "none", "2": "daily", "3": "weekly", "4": "monthly"}
    recurrence_pattern = recurrence_map.get(recurrence_choice, "none")

    print_colored("└" + "─" * 50 + "┘", Colors.OKCYAN)

    try:
        task = tasks_manager.add_task(
            title=title,
            description=description,
            priority=priority,
            tags=tags,
            due_date=due_date,
            recurrence_pattern=recurrence_pattern
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
    print_colored("┌" + "─" * 50 + "┐", Colors.OKCYAN)

    try:
        task_id = int(input("│ Enter task ID to update: "))
    except ValueError:
        print_colored("│ ❌ Invalid task ID!", Colors.FAIL)
        print_colored("└" + "─" * 50 + "┘", Colors.OKCYAN)
        return

    task = tasks_manager.get_task(task_id)
    if not task:
        print_colored(f"│ ❌ Task with ID {task_id} not found!", Colors.FAIL)
        print_colored("└" + "─" * 50 + "┘", Colors.OKCYAN)
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

    print("│ New recurrence pattern (none/daily/weekly/monthly, Enter to keep current): ", end="")
    recurrence_pattern = input().strip().lower()
    recurrence_pattern = recurrence_pattern if recurrence_pattern in ["none", "daily", "weekly", "monthly"] else task.recurrence_pattern

    print_colored("└" + "─" * 50 + "┘", Colors.OKCYAN)

    try:
        updated_task = tasks_manager.update_task(
            task_id=task_id,
            title=title,
            description=description,
            priority=priority,
            tags=tags,
            due_date=due_date,
            recurrence_pattern=recurrence_pattern
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
    print_colored("┌" + "─" * 50 + "┐", Colors.OKCYAN)

    try:
        task_id = int(input("│ Enter task ID to complete: "))
    except ValueError:
        print_colored("│ ❌ Invalid task ID!", Colors.FAIL)
        print_colored("└" + "─" * 50 + "┘", Colors.OKCYAN)
        return

    task = tasks_manager.get_task(task_id)
    if not task:
        print_colored(f"│ ❌ Task with ID {task_id} not found!", Colors.FAIL)
        print_colored("└" + "─" * 50 + "┘", Colors.OKCYAN)
        return

    print_colored("│ Task details:", Colors.WARNING)
    print_colored(f"│ Title: {task.title}", Colors.OKCYAN)
    print_colored(f"│ Recurrence: {task.recurrence_pattern}", Colors.OKCYAN)
    print_colored("│", Colors.OKCYAN)
    if task.recurrence_pattern != "none":
        print_colored("│ This is a recurring task. Complete and create next occurrence? (y/N): ", Colors.WARNING, end="")
        create_next = input().strip().lower()
        if create_next == 'y':
            # Complete the current task and create the next occurrence
            updated_task = tasks_manager.toggle_task_status(task_id)
            if updated_task:
                # Create a new task with the same properties but for the next occurrence
                next_occurrence_date = calculate_next_occurrence(datetime.now(), task.recurrence_pattern)
                new_task = tasks_manager.add_task(
                    title=task.title,
                    description=task.description,
                    priority=task.priority,
                    tags=task.tags,
                    due_date=next_occurrence_date,
                    recurrence_pattern=task.recurrence_pattern
                )
                print_colored(f"\n✅ Task {task_id} completed and next occurrence created (ID: {new_task.id})!", Colors.OKGREEN)
            else:
                print_colored(f"\n❌ Error completing task {task_id}!", Colors.FAIL)
        else:
            updated_task = tasks_manager.toggle_task_status(task_id)
            if updated_task:
                status = "completed" if updated_task.status == 'complete' else "marked as pending"
                print_colored(f"\n✅ Task {task_id} {status}!", Colors.OKGREEN)
            else:
                print_colored(f"\n❌ Error completing task {task_id}!", Colors.FAIL)
    else:
        updated_task = tasks_manager.toggle_task_status(task_id)
        if updated_task:
            status = "completed" if updated_task.status == 'complete' else "marked as pending"
            print_colored(f"\n✅ Task {task_id} {status}!", Colors.OKGREEN)
        else:
            print_colored(f"\n❌ Error completing task {task_id}!", Colors.FAIL)

    print_colored("└" + "─" * 50 + "┘", Colors.OKCYAN)

def calculate_next_occurrence(current_date, pattern):
    """Calculate the next occurrence date based on the recurrence pattern."""
    if pattern == "daily":
        return current_date + timedelta(days=1)
    elif pattern == "weekly":
        return current_date + timedelta(weeks=1)
    elif pattern == "monthly":
        # Calculate next month, handling month-end edge cases
        next_month = current_date.month + 1
        next_year = current_date.year
        if next_month > 12:
            next_month = 1
            next_year += 1
        # Handle month-end scenarios (e.g., Jan 31 -> Feb 28/29)
        next_day = current_date.day
        max_days_in_month = days_in_month(next_year, next_month)
        if next_day > max_days_in_month:
            next_day = max_days_in_month
        return current_date.replace(year=next_year, month=next_month, day=next_day)
    else:
        return None

def days_in_month(year, month):
    """Calculate the number of days in a given month."""
    if month in [1, 3, 5, 7, 8, 10, 12]:
        return 31
    elif month in [4, 6, 9, 11]:
        return 30
    elif month == 2:
        return 29 if is_leap_year(year) else 28
    else:
        raise ValueError(f"Invalid month: {month}")

def is_leap_year(year):
    """Determine if a year is a leap year."""
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

def upcoming_tasks_view(tasks_manager):
    """Display upcoming tasks due in the next 7 days"""
    print_colored("\n📅 UPCOMING TASKS", Colors.OKCYAN)
    print_colored("┌" + "─" * 100 + "┐", Colors.OKCYAN)

    days = input("│ Enter number of days to look ahead (default 7): ").strip()
    try:
        days = int(days) if days else 7
    except ValueError:
        days = 7

    print_colored("└" + "─" * 100 + "┘", Colors.OKCYAN)

    all_tasks = tasks_manager.get_all_tasks()
    upcoming_tasks = []
    now = datetime.now()
    future_limit = now + timedelta(days=days)

    for task in all_tasks:
        if task.due_date and task.status == 'pending':
            if now <= task.due_date <= future_limit:
                upcoming_tasks.append(task)

    # Sort by due date
    upcoming_tasks.sort(key=lambda t: t.due_date if t.due_date else datetime.max)

    if not upcoming_tasks:
        print_colored(f"\n📭 No tasks are due in the next {days} days.", Colors.WARNING)
        return

    tasks_manager.display_tasks(upcoming_tasks, f"Upcoming Tasks ({days} Days)")

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


def toggle_urdu_view():
    """Toggle Urdu view mode for priority and status labels"""
    global urdu_view_mode
    urdu_view_mode = not urdu_view_mode

    if urdu_view_mode:
        mode_status = get_translation('urdu_mode_enabled', True)
    else:
        mode_status = get_translation('urdu_mode_disabled', False)

    print_colored(f"\n🌐 {mode_status}", Colors.OKGREEN)
    input("\nPress Enter to continue...")

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
            upcoming_tasks_view(tasks_manager)
            input("\nPress Enter to continue...")
        elif choice == "9":
            toggle_urdu_view()  # Toggle Urdu view mode
        elif choice == "10":
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