"""
Interactive CLI interface for the Todo application.

This module provides an interactive menu-driven interface for the todo app.
"""
from rich.console import Console
from rich.table import Table
from ..core.todo_service import TodoService
from ..storage.in_memory_storage import InMemoryTaskRepository
from ..models.todo import TaskStatus

console = Console()

class InteractiveTodoCLI:
    def __init__(self):
        self.repository = InMemoryTaskRepository()
        self.service = TodoService(self.repository)
        self.running = True

    def display_menu(self):
        """Display the main menu options."""
        console.print("\n[bold blue]=== Todo CLI Application ===[/bold blue]")
        console.print("1. Add Todo")
        console.print("2. List Todos")
        console.print("3. Update Todo")
        console.print("4. Delete Todo")
        console.print("5. Mark Todo Complete/Incomplete")
        console.print("0. Exit")
        console.print("[bold]Please select an option (0-5):[/bold]", end=" ")

    def add_todo(self):
        """Add a new todo interactively."""
        try:
            title = console.input("Enter todo title: ").strip()
            if not title:
                console.print("[red]Title cannot be empty![/red]")
                return

            description = console.input("Enter todo description (optional): ").strip()

            task = self.service.add_task(title, description)
            console.print(f"[green]✓[/green] Added task: {task.title} (ID: {task.id})")
        except KeyboardInterrupt:
            console.print("\n[yellow]Operation cancelled.[/yellow]")

    def list_todos(self):
        """List all todos in a table format."""
        tasks = self.service.list_tasks()

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

    def update_todo(self):
        """Update a todo interactively."""
        try:
            if not self.service.list_tasks():
                console.print("[yellow]No tasks available to update.[/yellow]")
                return

            task_id = int(console.input("Enter task ID to update: "))
            task = self.service.get_task(task_id)

            if not task:
                console.print(f"[red]Task with ID {task_id} not found.[/red]")
                return

            console.print(f"Current task: {task.title}")
            new_title = console.input(f"Enter new title (current: '{task.title}', press Enter to keep current): ").strip()
            new_description = console.input(f"Enter new description (current: '{task.description}', press Enter to keep current): ").strip()

            # Only update fields that were provided
            title = new_title if new_title else None
            description = new_description if new_description else None

            updated_task = self.service.update_task(task_id, title=title, description=description)
            if updated_task:
                console.print(f"[green]✓[/green] Task {task_id} updated successfully")
            else:
                console.print(f"[red]✗[/red] Failed to update task {task_id}")
        except ValueError:
            console.print("[red]Please enter a valid task ID (number).[/red]")
        except KeyboardInterrupt:
            console.print("\n[yellow]Operation cancelled.[/yellow]")

    def delete_todo(self):
        """Delete a todo interactively."""
        try:
            if not self.service.list_tasks():
                console.print("[yellow]No tasks available to delete.[/yellow]")
                return

            task_id = int(console.input("Enter task ID to delete: "))
            success = self.service.delete_task(task_id)

            if success:
                console.print(f"[green]✓[/green] Task {task_id} deleted")
            else:
                console.print(f"[red]✗[/red] Task with ID {task_id} not found")
        except ValueError:
            console.print("[red]Please enter a valid task ID (number).[/red]")
        except KeyboardInterrupt:
            console.print("\n[yellow]Operation cancelled.[/yellow]")

    def toggle_status(self):
        """Toggle task status interactively."""
        try:
            if not self.service.list_tasks():
                console.print("[yellow]No tasks available to update.[/yellow]")
                return

            task_id = int(console.input("Enter task ID to toggle status: "))
            task = self.service.get_task(task_id)

            if not task:
                console.print(f"[red]Task with ID {task_id} not found.[/red]")
                return

            new_task = self.service.toggle_task_status(task_id)
            if new_task:
                status = "complete" if new_task.status == TaskStatus.COMPLETE else "pending"
                console.print(f"[green]✓[/green] Task {task_id} marked as {status}")
            else:
                console.print(f"[red]✗[/red] Failed to update task {task_id}")
        except ValueError:
            console.print("[red]Please enter a valid task ID (number).[/red]")
        except KeyboardInterrupt:
            console.print("\n[yellow]Operation cancelled.[/yellow]")

    def run(self):
        """Run the interactive CLI."""
        console.print("[bold green]Welcome to the Todo CLI Application![/bold green]")

        while self.running:
            try:
                self.display_menu()
                choice = console.input().strip()

                if choice == '0':
                    console.print("[bold green]Goodbye![/bold green]")
                    self.running = False
                elif choice == '1':
                    self.add_todo()
                elif choice == '2':
                    self.list_todos()
                elif choice == '3':
                    self.update_todo()
                elif choice == '4':
                    self.delete_todo()
                elif choice == '5':
                    self.toggle_status()
                else:
                    console.print("[red]Invalid option. Please select 0-5.[/red]")

            except KeyboardInterrupt:
                console.print("\n[bold green]\nGoodbye![/bold green]")
                self.running = False
            except Exception as e:
                console.print(f"[red]An error occurred: {str(e)}[/red]")


def main():
    """Main function to run the interactive CLI."""
    app = InteractiveTodoCLI()
    app.run()


if __name__ == "__main__":
    main()