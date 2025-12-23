import typer
import logging
from typing import Optional
from rich.console import Console
from rich.table import Table
from ..core.todo_service import TodoService
from ..storage.in_memory_storage import InMemoryTaskRepository
from ..models.todo import TaskStatus

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create a global console instance
console = Console()

# Initialize the service with in-memory storage
repository = InMemoryTaskRepository()
service = TodoService(repository)

app = typer.Typer(help="A command-line interface for managing todo tasks")

@app.command(help="Add a new task with the given title and description")
def add(title: str = typer.Argument(..., help="The title of the task"),
        description: Optional[str] = typer.Argument(default="", help="The description of the task")):
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

        task = service.add_task(title.strip(), description.strip() if description else "")
        logger.info(f"Added task: {task.title} (ID: {task.id})")
        console.print(f"[green]✓[/green] Added task: {task.title} (ID: {task.id})")
    except Exception as e:
        logger.error(f"Error adding task: {str(e)}")
        console.print(f"[red]✗[/red] Error adding task: {str(e)}")
        raise typer.Exit(code=1)

@app.command(help="List all tasks in a tabular format")
def list_tasks():
    """List all tasks in a tabular format"""
    try:
        tasks = service.list_tasks()
        logger.info(f"Retrieved {len(tasks)} tasks")

        if not tasks:
            console.print("[yellow]No tasks found.[/yellow]")
            return

        table = Table(title="Todo List")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Title", style="magenta")
        table.add_column("Description", style="green")
        table.add_column("Status", style="bold")
        table.add_column("Created", style="dim")

        for task in tasks:
            status = "[red]✗ PENDING[/red]" if task.status == TaskStatus.PENDING else "[green]✓ COMPLETE[/green]"
            table.add_row(
                str(task.id),
                task.title,
                task.description,
                status,
                task.created_at.strftime("%Y-%m-%d %H:%M")
            )

        console.print(table)
    except Exception as e:
        logger.error(f"Error listing tasks: {str(e)}")
        console.print(f"[red]✗[/red] Error listing tasks: {str(e)}")
        raise typer.Exit(code=1)

@app.command(help="Mark a task as complete/incomplete")
def complete(task_id: int = typer.Argument(..., help="The ID of the task to mark as complete/incomplete")):
    """Mark a task as complete/incomplete"""
    try:
        task = service.toggle_task_status(task_id)
        if task:
            status = "complete" if task.status == TaskStatus.COMPLETE else "pending"
            logger.info(f"Task {task_id} marked as {status}")
            console.print(f"[green]✓[/green] Task {task_id} marked as {status}")
        else:
            logger.warning(f"Task with ID {task_id} not found")
            console.print(f"[red]✗[/red] Task with ID {task_id} not found")
    except Exception as e:
        logger.error(f"Error toggling task status: {str(e)}")
        console.print(f"[red]✗[/red] Error toggling task status: {str(e)}")
        raise typer.Exit(code=1)

@app.command(help="Update a task's title or description")
def update(task_id: int = typer.Argument(..., help="The ID of the task to update"),
          title: Optional[str] = typer.Option(None, "--title", "-t", help="New title for the task"),
          description: Optional[str] = typer.Option(None, "--description", "-d", help="New description for the task")):
    """Update a task's title or description"""
    try:
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

        task = service.update_task(task_id, title=title, description=description)
        if task:
            logger.info(f"Task {task_id} updated")
            console.print(f"[green]✓[/green] Task {task_id} updated")
        else:
            logger.warning(f"Task with ID {task_id} not found")
            console.print(f"[red]✗[/red] Task with ID {task_id} not found")
    except Exception as e:
        logger.error(f"Error updating task: {str(e)}")
        console.print(f"[red]✗[/red] Error updating task: {str(e)}")
        raise typer.Exit(code=1)

@app.command(help="Delete a task by ID")
def delete(task_id: int = typer.Argument(..., help="The ID of the task to delete")):
    """Delete a task by ID"""
    try:
        success = service.delete_task(task_id)
        if success:
            logger.info(f"Task {task_id} deleted")
            console.print(f"[green]✓[/green] Task {task_id} deleted")
        else:
            logger.warning(f"Task with ID {task_id} not found")
            console.print(f"[red]✗[/red] Task with ID {task_id} not found")
    except Exception as e:
        logger.error(f"Error deleting task: {str(e)}")
        console.print(f"[red]✗[/red] Error deleting task: {str(e)}")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()