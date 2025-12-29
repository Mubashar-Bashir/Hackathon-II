# Quickstart: Monorepo Migration

## Overview
This guide explains how to work with the monorepo structure after migration from the flat project organization.

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

## Migration Verification Steps

### 1. Pre-Migration Backup
```bash
# Create a backup branch before migration
git checkout -b backup-pre-migration
git push origin backup-pre-migration
```

### 2. Migration Execution
```bash
# Run the migration script (to be created)
bash .specify/scripts/migrate-to-monorepo.sh
```

### 3. Post-Migration Verification
```bash
# Verify all tests still pass
cd backend/
python -m pytest tests/

# Verify application functionality
python -m src.todo_app.main --help

# Verify git history preservation
git log --oneline --follow src/todo_app/main.py
```

## Common Commands

### Python Development
```bash
# Install dependencies
cd backend && uv sync

# Run tests
cd backend && python -m pytest

# Format code
cd backend && uv run black src/

# Lint code
cd backend && uv run ruff check src/
```

### Git Operations
```bash
# View file history after migration
git log --follow -p -- backend/src/todo_app/main.py

# Compare with previous structure
git diff HEAD~1 --name-only
```

## Troubleshooting

### Import Errors After Migration
- **Problem**: Python can't find modules after migration
- **Solution**: Update PYTHONPATH or use proper relative imports
- **Command**: `export PYTHONPATH="${PYTHONPATH}:./backend/src"`

### Test Failures
- **Problem**: Tests failing after directory structure change
- **Solution**: Update test paths and fixtures
- **Check**: Ensure test paths reference new directory structure

### Git History Issues
- **Problem**: Commit history not preserved for moved files
- **Solution**: Use `git log --follow` to track file history across moves