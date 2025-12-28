# Todo Application Backend

This is the backend component of the todo application in the monorepo structure.

## Structure

- `src/todo_app/` - Main application source code
- `tests/` - Application tests
- `pyproject.toml` - Project dependencies and configuration

## Setup

1. Navigate to this directory: `cd backend/`
2. Install dependencies: `uv sync` (or `pip install -e .`)
3. Activate virtual environment if needed

## Usage

Run the application:
```bash
python -m src.todo_app.main
```

Or if installed in development mode:
```bash
todo
```

## Development

Run tests:
```bash
python -m pytest tests/
```