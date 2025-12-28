# Backend Guidelines

## Stack
- Python 3.13+
- FastAPI (or Typer for CLI apps)
- Pydantic V2
- uv for package management

## Project Structure
- `src/todo_app/` - Main application codebase
- `main.py` - Application entry point
- `models/` - Data models
- `core/` - Business logic
- `storage/` - Data storage implementations
- `ui/` - User interface components (CLI/interactive)

## API Conventions
- Use Typer for CLI applications
- Use Pydantic models for data validation
- Follow dependency injection patterns
- Handle errors gracefully

## Database/Storage
- Use in-memory storage for development (Phase I)
- Abstract storage layer for future SQL implementation (Phase II)

## Running
For CLI app:
python -m src.todo_app.main

For development:
cd backend && python -m pytest tests/