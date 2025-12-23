# Modular In-Memory Todo CLI System

A command-line interface application for managing todo tasks with a clean, modular architecture following hexagonal design principles.

## Features

- Add new tasks with title and description
- List all tasks in a tabular format
- Mark tasks as complete/incomplete
- Update task details
- Delete tasks
- Clean, professional CLI interface using Typer and Rich

## Prerequisites

- Python 3.13+
- uv package manager

## Installation

1. Clone the repository
2. Navigate to the project directory
3. Install dependencies using uv:

```bash
cd todo-app
uv sync
```

Or install using pip:

```bash
pip install typer rich pydantic
```

## Usage

### Add a new task

```bash
python -m todo_app.main add "Task title" --description "Task description"
```

### List all tasks

```bash
python -m todo_app.main list-tasks
```

### Mark a task as complete/incomplete

```bash
python -m todo_app.main complete 1
```

### Update a task

```bash
python -m todo_app.main update --task-id 1 --title "New title" --description "New description"
```

### Delete a task

```bash
python -m todo_app.main delete 1
```

## Architecture

This application follows a hexagonal architecture pattern with the following layers:

- **Models**: Pydantic data models for task validation
- **Core**: Business logic and service layer
- **Storage**: Abstract repository pattern with in-memory implementation
- **UI**: CLI interface using Typer

## Development

This project uses the following technologies:

- **Python 3.13+**: For type safety and modern language features
- **Typer**: For building the CLI interface
- **Rich**: For beautiful terminal output
- **Pydantic V2**: For data validation and serialization
- **uv**: For fast package management

## Testing

To run tests:

```bash
pytest
```

## License

[Specify your license here]