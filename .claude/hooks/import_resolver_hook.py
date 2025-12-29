"""
Claude Code Import Resolver Hook
Automatically activates when import errors are detected in Claude Code sessions.
"""

import sys
import os
from pathlib import Path

# Add the project root to the path to import our agent
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from import_resolver_agent import create_claude_code_hook


def on_error_detected(error_text: str):
    """
    Claude Code hook that gets called when an error is detected.
    If the error is import-related, provides contextual help.
    """
    # Create the import resolver hook
    import_resolver_hook = create_claude_code_hook()

    # Try to resolve the error
    resolution_help = import_resolver_hook(error_text)

    if resolution_help:
        # If we have resolution help, return it to Claude Code
        return {
            "type": "import_resolution_help",
            "message": resolution_help,
            "priority": "high"
        }

    # If not an import error, return None to continue normal error handling
    return None


def on_file_analyzed(file_path: str, content: str):
    """
    Claude Code hook that gets called when a file is analyzed.
    Can detect potential import issues before they cause errors.
    """
    # Import the agent
    from import_resolver_agent import ImportResolverAgent

    agent = ImportResolverAgent()

    # Analyze the file content for import issues
    issues = agent.analyze_code_for_import_issues(content, file_path)

    if issues:
        # Filter for potential import issues
        import_issues = [issue for issue in issues if issue.get('type') in ['possible_missing_import', 'relative_import']]

        if import_issues:
            help_messages = []
            for issue in import_issues:
                if issue['type'] == 'possible_missing_import':
                    symbol = issue['symbol']
                    suggestions = issue.get('suggestions', [])
                    if suggestions:
                        help_messages.append(f"💡 Potential missing import for '{symbol}': {suggestions[0]}")
                elif issue['type'] == 'relative_import':
                    module = issue.get('module', '')
                    help_messages.append(f"⚠️ Relative import detected: 'from {'.' * issue.get('level', 0)}{module}' - consider using absolute imports")

            if help_messages:
                return {
                    "type": "import_analysis_warning",
                    "message": "🔍 Import Analysis:\n" + "\n".join(help_messages),
                    "priority": "medium"
                }

    return None


def on_code_completion(code_snippet: str):
    """
    Claude Code hook that gets called during code completion.
    Can suggest imports for symbols being used.
    """
    # Import the agent
    from import_resolver_agent import ImportResolverAgent

    agent = ImportResolverAgent()

    # Analyze the code snippet for undefined symbols
    issues = agent.analyze_code_for_import_issues(code_snippet)

    import_suggestions = []
    for issue in issues:
        if issue['type'] == 'possible_missing_import':
            symbol = issue['symbol']
            suggestions = issue.get('suggestions', [])
            if suggestions:
                import_suggestions.append(suggestions[0])

    if import_suggestions:
        return {
            "type": "import_suggestion",
            "message": f"💡 Consider adding these imports:\n" + "\n".join(f"  {suggestion}" for suggestion in import_suggestions),
            "priority": "low"
        }

    return None


# Backward compatibility function name that might be expected by Claude Code
def user_prompt_submit_hook(error_text: str):
    """
    Legacy hook name for backward compatibility.
    """
    return on_error_detected(error_text)