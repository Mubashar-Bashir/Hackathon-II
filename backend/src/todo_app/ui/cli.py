import typer
import logging
from typing import Optional, List
from datetime import datetime
from rich.console import Console
from rich.table import Table
from ..core.todo_service import TodoService
from ..storage.in_memory_storage import InMemoryTaskRepository
from ..models.todo import TaskStatus, Priority, RecurrencePattern
from ..core.scheduler import SchedulerService, RecurrencePattern as SchedulerRecurrencePattern
from ..core.notification_adapter import NotificationAdapter
from ..core.i18n import i18n_service, Language

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create a global console instance
console = Console()

# Initialize the services with in-memory storage
repository = InMemoryTaskRepository()
notification_adapter = NotificationAdapter()
scheduler_service = SchedulerService(notification_adapter)
service = TodoService(repository, scheduler_service)

# Global variable to track Urdu view mode
urdu_view_mode = False

app = typer.Typer(help="A command-line interface for managing todo tasks")

@app.command(help="Add a new task with the given title and description")
def add(title: str = typer.Argument(..., help="The title of the task"),
        description: Optional[str] = typer.Argument(default="", help="The description of the task"),
        user_id: int = typer.Option(1, "--user-id", "-u", help="ID of the user creating the task (default: 1)"),
        priority: Optional[Priority] = typer.Option(None, "--priority", "-p", help="Priority level (low, medium, high)"),
        tags: Optional[List[str]] = typer.Option(None, "--tag", "-t", help="Tags for the task (can be used multiple times)"),
        due_date: Optional[str] = typer.Option(None, "--due-date", "-d", help="Due date in ISO format (YYYY-MM-DD)"),
        recurrence: Optional[RecurrencePattern] = typer.Option(None, "--recurrence", "-r", help="Recurrence pattern (none, daily, weekly, monthly)")):
    """Add a new task with the given title and description"""
    try:
        # Additional validation
        if not title or title.strip() == "":
            logger.error("Task title cannot be empty or whitespace only")
            console.print("[red]✗[/red] Task title cannot be empty or whitespace only")
            raise typer.Exit(code=1)

        if len(title.strip()) > 200:
            logger.error("Task title exceeds maximum length of 200 characters")
            console.print("[red]✗[/red] Task title exceeds maximum length of 200 characters")
            raise typer.Exit(code=1)

        if description and len(description) > 1000:
            logger.error("Task description exceeds maximum length of 1000 characters")
            console.print("[red]✗[/red] Task description exceeds maximum length of 1000 characters")
            raise typer.Exit(code=1)

        # Parse due date if provided
        parsed_due_date = None
        if due_date:
            try:
                parsed_due_date = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
            except ValueError:
                logger.error(f"Invalid date format: {due_date}. Expected ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)")
                console.print(f"[red]✗[/red] Invalid date format: {due_date}. Expected ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)")
                raise typer.Exit(code=1)

        # Parse recurrence pattern
        parsed_recurrence = recurrence or RecurrencePattern.NONE

        task = service.add_task(
            title.strip(),
            description.strip() if description else "",
            user_id=user_id,
            priority=priority,
            tags=tags,
            due_date=parsed_due_date,
            recurrence_pattern=parsed_recurrence
        )
        logger.info(f"Added task: {task.title} (ID: {task.id}) for user {user_id}")
        console.print(f"[green]✓[/green] Added task: {task.title} (ID: {task.id}) for user {user_id}")
    except Exception as e:
        logger.error(f"Error adding task: {str(e)}")
        console.print(f"[red]✗[/red] Error adding task: {str(e)}")
        raise typer.Exit(code=1)


@app.command(help="Mark a task as complete/incomplete")
def complete(task_id: int = typer.Argument(..., help="The ID of the task to mark as complete/incomplete"),
             user_id: int = typer.Option(1, "--user-id", "-u", help="ID of the user completing the task (default: 1)"),
             recurring: bool = typer.Option(False, "--recurring", "-r", help="Handle recurring task completion (creates next occurrence)")):
    """Mark a task as complete/incomplete"""
    try:
        if recurring:
            # Handle recurring task completion
            task = service.complete_recurring_task(task_id, user_id=user_id)
            if task:
                logger.info(f"Recurring task {task_id} marked as complete and next occurrence created for user {user_id}")
                console.print(f"[green]✓[/green] Recurring task {task_id} marked as complete and next occurrence created for user {user_id}")
            else:
                logger.warning(f"Task with ID {task_id} not found or error occurred for user {user_id}")
                console.print(f"[red]✗[/red] Task with ID {task_id} not found or error occurred for user {user_id}")
        else:
            # Handle regular task completion
            task = service.toggle_task_status(task_id, user_id=user_id)
            if task:
                status = "complete" if task.status == TaskStatus.COMPLETE else "pending"
                logger.info(f"Task {task_id} marked as {status} for user {user_id}")
                console.print(f"[green]✓[/green] Task {task_id} marked as {status} for user {user_id}")
            else:
                logger.warning(f"Task with ID {task_id} not found for user {user_id}")
                console.print(f"[red]✗[/red] Task with ID {task_id} not found for user {user_id}")
    except Exception as e:
        logger.error(f"Error completing task: {str(e)}")
        console.print(f"[red]✗[/red] Error completing task: {str(e)}")
        raise typer.Exit(code=1)

@app.command(help="Update a task's title, description, priority, tags, due date, or recurrence pattern")
def update(
    task_id: int = typer.Argument(..., help="The ID of the task to update"),
    user_id: int = typer.Option(1, "--user-id", "-u", help="ID of the user updating the task (default: 1)"),
    title: Optional[str] = typer.Option(None, "--title", "-t", help="New title for the task"),
    description: Optional[str] = typer.Option(None, "--description", "-d", help="New description for the task"),
    priority: Optional[Priority] = typer.Option(None, "--priority", "-p", help="New priority for the task (low, medium, high)"),
    tags: Optional[List[str]] = typer.Option(None, "--tag", help="New tags for the task (can be used multiple times)"),
    due_date: Optional[str] = typer.Option(None, "--due-date", help="New due date in ISO format (YYYY-MM-DD)"),
    recurrence: Optional[RecurrencePattern] = typer.Option(None, "--recurrence", "-r", help="New recurrence pattern (none, daily, weekly, monthly)")
):
    """Update a task's title or description"""
    try:
        # Parse due date if provided
        parsed_due_date = None
        if due_date:
            try:
                parsed_due_date = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
            except ValueError:
                logger.error(f"Invalid date format: {due_date}. Expected ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)")
                console.print(f"[red]✗[/red] Invalid date format: {due_date}. Expected ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)")
                raise typer.Exit(code=1)

        # Validate input if provided
        if title is not None:
            title = title.strip()
            if not title:
                logger.error("Task title cannot be empty or whitespace only")
                console.print("[red]✗[/red] Task title cannot be empty or whitespace only")
                raise typer.Exit(code=1)
            if len(title) > 200:
                logger.error("Task title exceeds maximum length of 200 characters")
                console.print("[red]✗[/red] Task title exceeds maximum length of 200 characters")
                raise typer.Exit(code=1)

        if description is not None:
            description = description.strip()
            if len(description) > 1000:
                logger.error("Task description exceeds maximum length of 1000 characters")
                console.print("[red]✗[/red] Task description exceeds maximum length of 1000 characters")
                raise typer.Exit(code=1)

        task = service.update_task(
            task_id,
            user_id=user_id,
            title=title,
            description=description,
            priority=priority,
            tags=tags,
            due_date=parsed_due_date,
            recurrence_pattern=recurrence
        )
        if task:
            logger.info(f"Task {task_id} updated for user {user_id}")
            console.print(f"[green]✓[/green] Task {task_id} updated for user {user_id}")
        else:
            logger.warning(f"Task with ID {task_id} not found for user {user_id}")
            console.print(f"[red]✗[/red] Task with ID {task_id} not found for user {user_id}")
    except Exception as e:
        logger.error(f"Error updating task: {str(e)}")
        console.print(f"[red]✗[/red] Error updating task: {str(e)}")
        raise typer.Exit(code=1)

@app.command(help="Delete a task by ID")
def delete(task_id: int = typer.Argument(..., help="The ID of the task to delete"),
          user_id: int = typer.Option(1, "--user-id", "-u", help="ID of the user deleting the task (default: 1)")):
    """Delete a task by ID"""
    try:
        success = service.delete_task(task_id, user_id=user_id)
        if success:
            logger.info(f"Task {task_id} deleted for user {user_id}")
            console.print(f"[green]✓[/green] Task {task_id} deleted for user {user_id}")
        else:
            logger.warning(f"Task with ID {task_id} not found for user {user_id}")
            console.print(f"[red]✗[/red] Task with ID {task_id} not found for user {user_id}")
    except Exception as e:
        logger.error(f"Error deleting task: {str(e)}")
        console.print(f"[red]✗[/red] Error deleting task: {str(e)}")
        raise typer.Exit(code=1)


@app.command(help="Toggle Urdu view mode for priority labels")
def view_urdu():
    """Toggle Urdu view mode for priority labels"""
    global urdu_view_mode
    urdu_view_mode = not urdu_view_mode
    mode_status = "enabled" if urdu_view_mode else "disabled"
    urdu_status = "فعال" if urdu_view_mode else "غیر فعال"
    console.print(f"[green]✓[/green] Urdu view mode {mode_status} (اُردو موڈ {urdu_status})")


@app.command(help="List all tasks in a tabular format with optional Urdu translation")
def list_tasks(
    user_id: int = typer.Option(1, "--user-id", "-u", help="ID of the user viewing tasks (default: 1)"),
    status: Optional[TaskStatus] = typer.Option(None, "--status", help="Filter by status (pending, complete)"),
    priority: Optional[Priority] = typer.Option(None, "--priority", help="Filter by priority (low, medium, high)"),
    tag: Optional[List[str]] = typer.Option(None, "--tag", help="Filter by tag (can be used multiple times)"),
    search: Optional[str] = typer.Option(None, "--search", "-s", help="Search in title or description"),
    sort_by: Optional[str] = typer.Option(None, "--sort-by", help="Sort by field (title, priority, due_date, created_at, status)"),
    sort_order: Optional[str] = typer.Option("asc", "--sort-order", help="Sort order (asc, desc)"),
    urdu: bool = typer.Option(False, "--urdu", help="Display priority labels in Urdu")
):
    """List all tasks in a tabular format with optional Urdu translation for priority labels"""
    try:
        from ..models.todo import SortField, SortOrder

        # Map string sort field to enum
        sort_field = None
        if sort_by:
            try:
                sort_field = SortField(sort_by.lower())
            except ValueError:
                logger.error(f"Invalid sort field: {sort_by}. Valid options: title, priority, due_date, created_at, status")
                console.print(f"[red]✗[/red] Invalid sort field: {sort_by}. Valid options: title, priority, due_date, created_at, status")
                raise typer.Exit(code=1)

        # Map string sort order to enum
        sort_order_enum = SortOrder.ASC
        if sort_order and sort_order.lower() == "desc":
            sort_order_enum = SortOrder.DESC

        tasks = service.list_tasks(
            user_id=user_id,
            status=status,
            priority=priority,
            tags=tag,
            search_keyword=search,
            sort_field=sort_field,
            sort_order=sort_order_enum
        )
        logger.info(f"Retrieved {len(tasks)} tasks")

        if not tasks:
            console.print(f"[yellow]{i18n_service.get_translation('no_tasks', urdu_mode=urdu or urdu_view_mode)}[/yellow]")
            return

        # Determine if we should use Urdu based on the urdu flag or global urdu_view_mode
        use_urdu = urdu or urdu_view_mode
        table_title = i18n_service.get_translation('list', urdu_mode=use_urdu)
        table = Table(title=table_title)

        # Add columns with appropriate labels
        table.add_column(i18n_service.get_translation('id', urdu_mode=use_urdu), style="cyan", no_wrap=True)
        table.add_column(i18n_service.get_translation('title', urdu_mode=use_urdu), style="magenta")
        table.add_column(i18n_service.get_translation('description', urdu_mode=use_urdu), style="green")
        table.add_column(i18n_service.get_translation('status', urdu_mode=use_urdu), style="bold")
        table.add_column(i18n_service.get_translation('priority', urdu_mode=use_urdu), style="bold")
        table.add_column(i18n_service.get_translation('tags', urdu_mode=use_urdu), style="dim")
        table.add_column(i18n_service.get_translation('due_date', urdu_mode=use_urdu), style="dim")
        table.add_column(i18n_service.get_translation('created', urdu_mode=use_urdu), style="dim")

        for task in tasks:
            # Get priority label in Urdu if enabled
            priority_label = i18n_service.get_priority_translation(task.priority.value, urdu_mode=use_urdu)

            # Color code priority
            priority_color_map = {
                'High': "[red]HIGH[/red]",
                'Medium': "[yellow]MEDIUM[/yellow]",
                'Low': "[green]LOW[/green]",
                'اعلی': "[red]اعلی[/red]",
                'درمیانہ': "[yellow]درمیانہ[/yellow]",
                'کم': "[green]کم[/green]"
            }
            priority_color = priority_color_map.get(priority_label, priority_label)
            if not priority_label.startswith('['):  # Only apply color if not already colored
                if priority_label in ['High', 'اعلی']:
                    priority_color = "[red]{}[/red]".format(priority_label)
                elif priority_label in ['Medium', 'درمیانہ']:
                    priority_color = "[yellow]{}[/yellow]".format(priority_label)
                elif priority_label in ['Low', 'کم']:
                    priority_color = "[green]{}[/green]".format(priority_label)

            # Format due date
            due_date_str = task.due_date.strftime("%Y-%m-%d") if task.due_date else "None"

            # Format tags
            tags_str = ", ".join(task.tags) if task.tags else "None"

            # Get status label in Urdu if enabled
            status_label = i18n_service.get_status_translation(task.status.value, urdu_mode=use_urdu)
            status_str = f"[red]✗ {status_label}[/red]" if task.status == TaskStatus.PENDING else f"[green]✓ {status_label}[/green]"

            table.add_row(
                str(task.id),
                task.title,
                task.description,
                status_str,
                priority_color,
                tags_str,
                due_date_str,
                task.created_at.strftime("%Y-%m-%d %H:%M")
            )

        console.print(table)
    except Exception as e:
        logger.error(f"Error listing tasks: {str(e)}")
        console.print(f"[red]✗[/red] Error listing tasks: {str(e)}")
        raise typer.Exit(code=1)


@app.command(help="Show upcoming tasks due in the next specified number of days")
def upcoming(user_id: int = typer.Option(1, "--user-id", "-u", help="ID of the user viewing upcoming tasks (default: 1)"),
             days: int = typer.Option(7, "--days", "-d", min=1, max=30, help="Number of days to look ahead (default: 7, max: 30)")):
    """Show upcoming tasks due in the next specified number of days"""
    try:
        # Get only the user's tasks
        user_tasks = service.list_tasks(user_id=user_id)

        # Get upcoming tasks using the scheduler service
        upcoming_tasks = scheduler_service.get_upcoming_tasks(user_tasks, days)

        if not upcoming_tasks:
            console.print(f"[yellow]No tasks are due in the next {days} days for user {user_id}.[/yellow]")
            return

        table = Table(title=f"Upcoming Tasks for User {user_id} (Next {days} Days)")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Title", style="magenta")
        table.add_column("Description", style="green")
        table.add_column("Status", style="bold")
        table.add_column("Priority", style="bold")
        table.add_column("Tags", style="dim")
        table.add_column("Due Date", style="dim")
        table.add_column("Recurrence", style="dim")

        for task in upcoming_tasks:
            # Color code priority
            priority_color = {
                Priority.HIGH: "[red]HIGH[/red]",
                Priority.MEDIUM: "[yellow]MEDIUM[/yellow]",
                Priority.LOW: "[green]LOW[/green]"
            }.get(task.priority, str(task.priority))

            # Format due date
            due_date_str = task.due_date.strftime("%Y-%m-%d %H:%M") if task.due_date else "None"

            # Format tags
            tags_str = ", ".join(task.tags) if task.tags else "None"

            # Format recurrence
            recurrence_str = task.recurrence_pattern.value if task.recurrence_pattern else "None"

            status_str = "[red]✗ PENDING[/red]" if task.status == TaskStatus.PENDING else "[green]✓ COMPLETE[/green]"

            table.add_row(
                str(task.id),
                task.title,
                task.description,
                status_str,
                priority_color,
                tags_str,
                due_date_str,
                recurrence_str
            )

        console.print(table)
    except Exception as e:
        logger.error(f"Error showing upcoming tasks: {str(e)}")
        console.print(f"[red]✗[/red] Error showing upcoming tasks: {str(e)}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()