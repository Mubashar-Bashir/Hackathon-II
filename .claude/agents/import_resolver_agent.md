# Import Resolver Agent

## Overview
The Import Resolver Agent is an automated assistant that detects and resolves Python import issues in real-time. It activates automatically when coding agents encounter import-related errors, providing contextual help and solutions.

## Activation Triggers
The agent activates automatically when it detects:

1. **Import Errors**:
   - `ModuleNotFoundError: No module named '...'`
   - `ImportError: cannot import name '...' from '...'`
   - `NameError: name '...' is not defined` (when it's likely a missing import)

2. **Code Analysis**:
   - Undefined class names that might exist in the project
   - Relative import patterns that could be problematic
   - Import statements that reference non-existent modules

## Capabilities

### 1. Error Detection
- Scans error messages to identify import-related issues
- Analyzes code to detect potential import problems
- Provides context-aware suggestions

### 2. Import Resolution
- Searches the project registry for available imports
- Suggests correct import statements for missing symbols
- Provides file location information for symbols

### 3. Contextual Help
- Explains the nature of the import error
- Suggests specific fixes based on the error context
- Provides links to relevant files and documentation

## Usage in Coding Sessions

### Automatic Activation
When a coding agent encounters an import error, the Import Resolver Agent will:

1. **Detect** the import issue from error messages
2. **Analyze** the context of the error
3. **Provide** specific suggestions and solutions
4. **Guide** the user to the correct import statements

### Manual Activation
The agent can also be manually invoked with:
- `@import_resolver analyze` - Analyze current code for import issues
- `@import_resolver find <symbol>` - Find import paths for a symbol
- `@import_resolver fix` - Suggest fixes for import problems

## Integration with Project Registry
The agent uses the project's import registry (`.import_registry.json`) to:
- Map symbols to their module locations
- Provide accurate import suggestions
- Detect duplicate or conflicting definitions
- Maintain up-to-date import information

## Example Workflow

### Scenario: Missing Import
**Error**: `NameError: name 'TodoService' is not defined`

**Agent Response**:
```
🚨 IMPORT ERROR DETECTED
Error: NameError: name 'TodoService' is not defined

💡 POSSIBLE IMPORTS FOR 'TodoService':
  from src.core.todo_service import TodoService

📁 POSSIBLE SOURCE FILES FOR 'TodoService':
  src/core/todo_service.py

📖 SUGGESTED ACTIONS:
  1. Add 'from src.core.todo_service import TodoService' to your imports
  2. Check if the module exists in your project
  3. Consider running 'import_manager.py fix' to resolve common issues
```

### Scenario: Module Not Found
**Error**: `ModuleNotFoundError: No module named 'utils.helpers'`

**Agent Response**:
```
🚨 IMPORT ERROR DETECTED
Error: ModuleNotFoundError: No module named 'utils.helpers'

🔍 ANALYSIS:
  - The module 'utils.helpers' cannot be found
  - This might be due to incorrect path or missing __init__.py

📁 POSSIBLE SIMILAR MODULES:
  - src/utils/helpers.py
  - src/helpers/utils.py
  - utils.py

📖 SUGGESTED ACTIONS:
  1. Check if the file exists with the correct path
  2. Verify that __init__.py files exist in the package directories
  3. Run 'import_manager.py fix' to create missing package files
  4. Consider using absolute imports instead of relative imports
```

## Configuration
The agent is pre-configured to work with the existing import management system and requires no additional setup. It automatically detects the project structure and maintains its registry.

## Integration Points
- Works with existing Python import fixer skill
- Integrates with import registry system
- Compatible with development workflow tools
- Supports both relative and absolute import patterns

## Best Practices
- The agent suggests solutions but allows developers to make the final decision
- Provides educational context about import systems
- Maintains consistency with existing project import patterns
- Helps prevent import-related bugs during development