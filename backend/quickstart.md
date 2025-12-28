# Quickstart Guide: New Monorepo Structure

## Overview
This guide explains how to work with the new monorepo structure after migration from the flat project organization.

## Directory Structure
```
backend/                 # Phase I todo application codebase
├── src/
│   └── todo_app/        # Main application code
├── tests/               # Application tests
├── pyproject.toml       # Project dependencies
└── README.md            # Backend documentation

frontend/                # Future Phase III web interface
├── src/
├── package.json
└── README.md

specs/                   # Feature specifications
├── 001-todo-cli/
├── 002-mcp-server/
└── 003-monorepo-migration/

.specify/                # Spec-Kit configuration
└── [Spec-Kit files]

.history/                # Historical records
├── prompts/             # Prompt History Records
└── adr/                 # Architecture Decision Records
```

## Development Workflow

### 1. Setting up the Environment
```bash
# Navigate to backend directory
cd backend/

# Install dependencies with uv
uv sync

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 2. Running the Application
```bash
# From the backend directory
python -m src.todo_app.main

# Or using the CLI directly
python -m todo_app.main
```

### 3. Running Tests
```bash
# From the backend directory
python -m pytest tests/
```

### 4. Using Spec-Kit Commands
```bash
# From the repository root
/sp.specify    # Create/update feature specifications
/sp.plan       # Create technical implementation plans
/sp.tasks      # Generate task breakdowns
/sp.implement  # Execute implementation tasks
```
