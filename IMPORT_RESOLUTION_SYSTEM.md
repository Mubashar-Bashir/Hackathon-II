# Python Import Resolution System

This project implements a comprehensive solution for Python import resolution issues. It combines multiple approaches to help developers quickly find and fix import problems in their Python projects.

## Components

### 1. Import Registry Skill
- Maintains a registry of all Python modules and symbols in the project
- Provides fast lookup for import paths
- Updates in real-time as the codebase changes

### 2. Enhanced Import Fixer Skill
- Scans for import-related issues
- Converts relative imports to absolute imports where appropriate
- Creates missing `__init__.py` files to establish proper package structure
- Integrates with the import registry for enhanced functionality

### 3. Import Management CLI
- Unified command-line interface for import management
- Combines both skills into a single workflow
- Provides analysis, fixing, and lookup capabilities

## Usage

### Command Line Interface
```bash
# Full import analysis
python import_manager.py analyze

# Find import paths for a symbol
python import_manager.py find TodoService

# Fix import issues
python import_manager.py fix

# Suggest imports matching text
python import_manager.py suggest Task

# Show help
python import_manager.py help
```

### Individual Skills
The system also provides individual skill access:

```bash
# Using import registry skill
python -c "from .claude.skills.import_registry.skill import run_skill; print(run_skill(['.', 'find', 'TodoService']))"

# Using import fixer skill
python -c "from .claude.skills.python_import_fixer.skill import run_skill; print(run_skill(['.']))"
```

## How It Works

1. **Registry Building**: Scans all Python files in the project and creates a mapping of symbols (classes, functions) to their module paths
2. **Issue Detection**: Identifies common import problems like missing `__init__.py` files or problematic relative imports
3. **Resolution**: Provides both automated fixes and manual lookup capabilities
4. **Integration**: Combines both approaches for a comprehensive solution

## Benefits

- **Fast Symbol Lookup**: Find where any class or function is defined instantly
- **Automatic Fixes**: Resolve common import issues automatically
- **Development Aid**: Provides suggestions during development
- **Refactoring Support**: Helps maintain correct imports when restructuring code
- **No Code Changes Required**: Works with existing codebases

## Integration with Development Workflow

1. Run `import_manager.py analyze` to check for import issues
2. Use `import_manager.py find <symbol>` when you need to import a class/function
3. Run `import_manager.py fix` when restructuring code or encountering import errors
4. Use `import_manager.py suggest <text>` for fuzzy matching of imports

This system is particularly useful for:
- Large Python projects with complex import structures
- Teams working with unfamiliar codebases
- Developers refactoring code with multiple modules
- Projects transitioning from relative to absolute imports