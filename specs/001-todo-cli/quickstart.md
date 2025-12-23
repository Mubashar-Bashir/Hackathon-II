# Quickstart Guide: Modular In-Memory Todo CLI System

**Feature**: 001-todo-cli
**Date**: 2025-12-23
**Status**: Complete

## Project Setup

### Prerequisites
- Python 3.13+
- uv package manager

### Installation
1. Clone the repository
2. Navigate to the `todo-app` directory
3. Install dependencies using uv:
   ```bash
   cd todo-app
   uv sync
   ```

### Running the Application
```bash
cd todo-app
uv run python -m main
```

Or to see available commands:
```bash
uv run python -m main --help
```

## Available Commands

### Add a Task
```bash
uv run python -m main add "Task Title" --description "Optional description"
```

### List All Tasks
```bash
uv run python -m main list
```

### Update a Task
```bash
uv run python -m main update 1 --title "New Title" --description "New Description"
```

### Mark Task as Complete/Incomplete
```bash
uv run python -m main complete 1
```

### Delete a Task
```bash
uv run python -m main delete 1
```

## Development

### Running Tests
```bash
cd todo-app
uv run pytest
```

### Running Tests with Coverage
```bash
uv run pytest --cov=src --cov-report=html
```

## Architecture Overview

### Directory Structure
```
todo-app/
├── src/
│   ├── core/           # Business logic
│   ├── models/         # Pydantic models
│   ├── ui/             # CLI interface
│   └── storage/        # Data storage implementations
├── tests/              # Test files
└── pyproject.toml      # Project configuration
```

### Key Components
- **Models**: Pydantic models for data validation
- **Core**: Business logic and service layer
- **Storage**: Abstract repository pattern implementation
- **UI**: CLI interface using Typer

## Example Usage

```bash
# Add a new task
uv run python -m main add "Buy groceries" --description "Milk, bread, eggs"

# List all tasks
uv run python -m main list

# Mark task #1 as complete
uv run python -m main complete 1

# Update task #1
uv run python -m main update 1 --title "Buy groceries - urgent" --description "Milk, bread, eggs, cheese"

# Delete task #1
uv run python -m main delete 1
```

## Troubleshooting

### Common Issues
- **Command not found**: Ensure you're running from the todo-app directory
- **Import errors**: Run `uv sync` to install dependencies
- **Permission errors**: Check file permissions in the project directory