"""
Import Resolver Agent
An automated agent that detects and resolves Python import issues in real-time.
"""

import os
import sys
import ast
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Callable
from dataclasses import dataclass


@dataclass
class ImportResolutionResult:
    """Result of an import resolution attempt."""
    success: bool
    suggestions: List[str]
    error_message: str = ""
    context: Dict = None


class ImportResolverAgent:
    """
    An agent that automatically detects and resolves import issues for coding agents.
    """

    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.registry_file = self.project_root / ".import_registry.json"
        self.error_patterns = [
            r"ModuleNotFoundError: No module named '(.+)'",
            r"ImportError: cannot import name '(.+)' from '(.+)'",
            r"ImportError: cannot import name '(.+)'",
            r"NameError: name '(.+)' is not defined",  # Could be due to missing import
        ]
        self._load_or_build_registry()

    def _load_or_build_registry(self):
        """Load the registry or build it if it doesn't exist."""
        if not self.registry_file.exists():
            self._build_registry_from_project()

    def _build_registry_from_project(self):
        """Build import registry from the project files."""
        symbols = {}

        for py_file in self.project_root.rglob("*.py"):
            if any(part.startswith(".") or part in ["venv", ".venv", "__pycache__"] for part in py_file.parts):
                continue

            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    content = f.read()

                tree = ast.parse(content)

                # Extract module path
                rel_path = py_file.relative_to(self.project_root)
                module_parts = []
                for part in rel_path.parts:
                    if part.endswith(".py"):
                        module_parts.append(part[:-3])
                    else:
                        module_parts.append(part)
                module_name = ".".join(module_parts)

                # Find all classes and functions
                for node in ast.walk(tree):
                    if isinstance(node, (ast.ClassDef, ast.FunctionDef)):
                        symbol_name = node.name
                        if symbol_name not in symbols:
                            symbols[symbol_name] = []
                        if module_name not in symbols[symbol_name]:
                            symbols[symbol_name].append(module_name)

                    # Also capture imports to know what's available
                    elif isinstance(node, (ast.Import, ast.ImportFrom)):
                        if isinstance(node, ast.ImportFrom) and node.names:
                            # This is an import like 'from module import symbol'
                            if node.module:
                                imported_module = node.module
                                for alias in node.names:
                                    imported_name = alias.asname if alias.asname else alias.name
                                    if imported_name not in symbols:
                                        symbols[imported_name] = []
                                    if imported_module not in symbols[imported_name]:
                                        symbols[imported_name].append(imported_module)

            except (SyntaxError, UnicodeDecodeError):
                continue

        # Save registry
        with open(self.registry_file, "w") as f:
            json.dump(symbols, f, indent=2)

    def detect_import_error(self, error_text: str) -> Optional[Dict]:
        """
        Detect if the error is an import-related error and extract context.
        """
        for pattern in self.error_patterns:
            match = re.search(pattern, error_text)
            if match:
                error_type = "unknown"
                symbol_name = ""
                module_name = ""

                if "ModuleNotFoundError" in error_text:
                    error_type = "module_not_found"
                    symbol_name = match.group(1)
                elif "ImportError" in error_text:
                    error_type = "import_error"
                    symbol_name = match.group(1)
                    if len(match.groups()) > 1:
                        module_name = match.group(2)
                elif "NameError" in error_text:
                    error_type = "name_error"
                    symbol_name = match.group(1)

                return {
                    "error_type": error_type,
                    "symbol_name": symbol_name,
                    "module_name": module_name,
                    "full_error": error_text
                }

        return None

    def resolve_import_issue(self, error_context: Dict) -> ImportResolutionResult:
        """
        Resolve an import issue based on the error context.
        """
        symbol_name = error_context["symbol_name"]
        error_type = error_context["error_type"]

        # Find possible imports for the symbol
        possible_imports = self._find_possible_imports(symbol_name)
        suggestions = []

        if possible_imports:
            suggestions.extend(possible_imports[:5])  # Limit to top 5 suggestions
        else:
            # If no exact match, try fuzzy matching
            fuzzy_matches = self._find_fuzzy_matches(symbol_name)
            suggestions.extend(fuzzy_matches[:5])

        # Find related files
        related_files = self._find_files_containing_symbol(symbol_name)[:3]

        # Create resolution context
        context = {
            "symbol_name": symbol_name,
            "error_type": error_type,
            "possible_imports": possible_imports[:5],
            "related_files": related_files,
            "suggestions": suggestions
        }

        success = len(suggestions) > 0
        error_message = f"No suggestions found for symbol '{symbol_name}'" if not success else ""

        return ImportResolutionResult(
            success=success,
            suggestions=suggestions,
            error_message=error_message,
            context=context
        )

    def _find_possible_imports(self, symbol_name: str) -> List[str]:
        """Find possible import statements for a symbol using the registry."""
        try:
            with open(self.registry_file, 'r') as f:
                registry = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

        if symbol_name in registry:
            return [f"from {module} import {symbol_name}" for module in registry[symbol_name]]

        return []

    def _find_fuzzy_matches(self, symbol_name: str) -> List[str]:
        """Find fuzzy matches for a symbol name."""
        try:
            with open(self.registry_file, 'r') as f:
                registry = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

        possible_matches = []
        for reg_symbol, modules in registry.items():
            if symbol_name.lower() in reg_symbol.lower() or reg_symbol.lower() in symbol_name.lower():
                for module in modules:
                    possible_matches.append(f"from {module} import {reg_symbol}")

        return possible_matches[:10]  # Limit to 10 suggestions

    def _find_files_containing_symbol(self, symbol_name: str) -> List[str]:
        """Find files that might contain the symbol."""
        files = []

        for py_file in self.project_root.rglob("*.py"):
            if any(part.startswith(".") or part in ["venv", ".venv", "__pycache__"] for part in py_file.parts):
                continue

            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    content = f.read()

                # Check if symbol exists in file content
                if symbol_name.lower() in content.lower():
                    files.append(str(py_file.relative_to(self.project_root)))

            except UnicodeDecodeError:
                continue

        return files

    def search_files_by_content(self, search_term: str, max_results: int = 10) -> List[Dict]:
        """
        Search files by content for a specific term.
        """
        results = []

        for py_file in self.project_root.rglob("*.py"):
            if any(part.startswith(".") or part in ["venv", ".venv", "__pycache__"] for part in py_file.parts):
                continue

            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    content = f.read()

                # Find all occurrences of the search term
                lines = content.splitlines()
                for line_num, line in enumerate(lines, 1):
                    if search_term.lower() in line.lower():
                        results.append({
                            "file": str(py_file.relative_to(self.project_root)),
                            "line_number": line_num,
                            "line_content": line.strip(),
                            "context": self._get_line_context(lines, line_num)
                        })

                        if len(results) >= max_results:
                            return results

            except UnicodeDecodeError:
                continue

        return results

    def _get_line_context(self, lines: List[str], line_num: int, context_lines: int = 2) -> str:
        """Get context around a specific line."""
        start = max(0, line_num - 1 - context_lines)
        end = min(len(lines), line_num + context_lines)

        context_lines_content = []
        for i in range(start, end):
            prefix = ">>> " if i == line_num - 1 else "    "
            context_lines_content.append(f"{prefix}{i+1:3d}: {lines[i].strip()}")

        return "\n".join(context_lines_content)

    def find_symbol_definition(self, symbol_name: str) -> List[Dict]:
        """
        Find where a symbol is defined in the codebase (classes, functions, variables).
        """
        definitions = []

        for py_file in self.project_root.rglob("*.py"):
            if any(part.startswith(".") or part in ["venv", ".venv", "__pycache__"] for part in py_file.parts):
                continue

            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    content = f.read()

                tree = ast.parse(content)
                lines = content.splitlines()

                for node in ast.walk(tree):
                    # Look for class definitions
                    if isinstance(node, ast.ClassDef) and node.name == symbol_name:
                        definitions.append({
                            "type": "class",
                            "name": node.name,
                            "file": str(py_file.relative_to(self.project_root)),
                            "line": node.lineno,
                            "context": self._get_line_context(lines, node.lineno)
                        })
                    # Look for function definitions
                    elif isinstance(node, ast.FunctionDef) and node.name == symbol_name:
                        definitions.append({
                            "type": "function",
                            "name": node.name,
                            "file": str(py_file.relative_to(self.project_root)),
                            "line": node.lineno,
                            "context": self._get_line_context(lines, node.lineno)
                        })
                    # Look for variable assignments at module level
                    elif isinstance(node, ast.Assign) and hasattr(node.targets[0], 'id'):
                        if node.targets[0].id == symbol_name:
                            definitions.append({
                                "type": "variable",
                                "name": node.targets[0].id,
                                "file": str(py_file.relative_to(self.project_root)),
                                "line": node.lineno,
                                "context": self._get_line_context(lines, node.lineno)
                            })

            except (SyntaxError, UnicodeDecodeError):
                continue

        return definitions

    def search_by_file_pattern(self, pattern: str) -> List[str]:
        """
        Search for files matching a pattern.
        """
        import fnmatch

        matches = []
        for py_file in self.project_root.rglob("*.py"):
            if any(part.startswith(".") or part in ["venv", ".venv", "__pycache__"] for part in py_file.parts):
                continue

            relative_path = py_file.relative_to(self.project_root)
            if fnmatch.fnmatch(str(relative_path), f"*{pattern}*") or pattern.lower() in str(relative_path).lower():
                matches.append(str(relative_path))

        return matches[:20]  # Limit to 20 results

    def analyze_code_for_import_issues(self, code: str, file_path: str = "") -> List[Dict]:
        """
        Analyze code for potential import issues.
        """
        issues = []

        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return [{"type": "syntax_error", "message": f"Syntax error: {str(e)}", "location": file_path}]

        # Check for undefined names that might be missing imports
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                # This is a variable usage - check if it's likely to be a missing import
                if node.id.isupper() or node.id.istitle() or len(node.id) > 2:  # Likely a class/function name
                    possible_imports = self._find_possible_imports(node.id)
                    if possible_imports:
                        issues.append({
                            "type": "possible_missing_import",
                            "symbol": node.id,
                            "suggestions": possible_imports[:3],
                            "location": getattr(node, 'lineno', 'unknown')
                        })

        # Check for import statements that might be problematic
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if node.module and node.level > 0:  # Relative import
                    issues.append({
                        "type": "relative_import",
                        "module": node.module,
                        "level": node.level,
                        "location": getattr(node, 'lineno', 'unknown')
                    })

        return issues

    def provide_contextual_help(self, resolution_result: ImportResolutionResult) -> str:
        """Provide contextual help based on resolution result."""
        if not resolution_result.success:
            return f"❌ {resolution_result.error_message}"

        context = resolution_result.context
        symbol_name = context["symbol_name"]
        error_type = context["error_type"]

        help_text = []
        help_text.append(f"🚨 {error_type.upper().replace('_', ' ')} DETECTED")
        help_text.append(f"Symbol: {symbol_name}")

        if context["possible_imports"]:
            help_text.append(f"\n💡 POSSIBLE IMPORTS:")
            for imp in context["possible_imports"]:
                help_text.append(f"  {imp}")

        if context["related_files"]:
            help_text.append(f"\n📁 RELATED FILES:")
            for file_path in context["related_files"]:
                help_text.append(f"  {file_path}")

        if context["suggestions"]:
            help_text.append(f"\n🔧 SUGGESTED FIXES:")
            for i, suggestion in enumerate(context["suggestions"], 1):
                help_text.append(f"  {i}. {suggestion}")

        help_text.append(f"\n📖 NEXT STEPS:")
        help_text.append(f"  1. Add the suggested import to your file")
        help_text.append(f"  2. Verify the module exists in your project")
        help_text.append(f"  3. Run 'import_manager.py fix' for comprehensive import fixing")

        return "\n".join(help_text)

    def auto_resolve_error(self, error_text: str) -> Optional[str]:
        """
        Automatically resolve an error if it's import-related.
        """
        error_context = self.detect_import_error(error_text)
        if not error_context:
            return None  # Not an import error

        resolution_result = self.resolve_import_issue(error_context)
        return self.provide_contextual_help(resolution_result)

    def get_import_suggestions(self, symbol_name: str) -> List[str]:
        """
        Get import suggestions for a symbol without error context.
        """
        return self._find_possible_imports(symbol_name)[:10]


def create_claude_code_hook() -> Callable:
    """
    Create a hook function that can be integrated into Claude Code
    to automatically detect and resolve import issues.
    """
    agent = ImportResolverAgent()

    def claude_code_import_hook(error_text: str) -> Optional[str]:
        """
        Hook function for Claude Code integration.
        Returns contextual help if it's an import issue, None otherwise.
        """
        return agent.auto_resolve_error(error_text)

    return claude_code_import_hook


class IntegratedImportResolver:
    """
    An integrated resolver that combines the import resolver agent with
    the existing import management system.
    """

    def __init__(self, project_root: str = "."):
        self.agent = ImportResolverAgent(project_root)
        self.project_root = Path(project_root).resolve()

    def resolve_import_error(self, error_text: str) -> Dict:
        """
        Resolve an import error using both agent and existing tools.
        """
        # Use the agent to get initial resolution
        agent_resolution = self.agent.auto_resolve_error(error_text)

        # If it's an import error, also suggest using the import manager
        error_context = self.agent.detect_import_error(error_text)
        if error_context:
            additional_suggestions = [
                f"Run: python {self.project_root}/import_manager.py analyze",
                f"Run: python {self.project_root}/import_manager.py fix"
            ]

            if error_context.get("symbol_name"):
                additional_suggestions.append(
                    f"Find symbol: python {self.project_root}/import_manager.py find {error_context['symbol_name']}"
                )

            return {
                "agent_resolution": agent_resolution,
                "additional_suggestions": additional_suggestions,
                "combined_help": self._combine_help(agent_resolution, additional_suggestions)
            }

        return {
            "agent_resolution": agent_resolution,
            "additional_suggestions": [],
            "combined_help": agent_resolution
        }

    def _combine_help(self, agent_help: str, additional_suggestions: List[str]) -> str:
        """
        Combine agent help with additional suggestions.
        """
        if not agent_help:
            return "No specific import resolution provided.\n" + "\n".join(additional_suggestions)

        combined = [agent_help]
        if additional_suggestions:
            combined.append("\n🔧 ADDITIONAL COMMANDS TO TRY:")
            combined.extend([f"  {suggestion}" for suggestion in additional_suggestions])

        return "\n".join(combined)

    def search_symbol(self, symbol_name: str) -> Dict:
        """
        Search for a symbol using both registry and file analysis.
        """
        # Get import suggestions from registry
        import_suggestions = self.agent.get_import_suggestions(symbol_name)

        # Find symbol definitions in code
        symbol_definitions = self.agent.find_symbol_definition(symbol_name)

        # Search files containing the symbol
        file_search_results = self.agent.search_files_by_content(symbol_name, max_results=5)

        return {
            "import_suggestions": import_suggestions,
            "symbol_definitions": symbol_definitions,
            "file_search_results": file_search_results,
            "all_results": {
                "import_suggestions": import_suggestions,
                "symbol_definitions": symbol_definitions,
                "file_search_results": file_search_results
            }
        }

    def analyze_file(self, file_path: str) -> Dict:
        """
        Analyze a file for import issues using both systems.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Use agent analysis
            agent_issues = self.agent.analyze_code_for_import_issues(content, file_path)

            # Additional analysis could be added here

            return {
                "agent_analysis": agent_issues,
                "summary": f"Found {len(agent_issues)} potential issues in {file_path}"
            }
        except Exception as e:
            return {
                "error": str(e),
                "summary": f"Error analyzing file: {str(e)}"
            }


def main():
    """
    Main function for testing the Import Resolver Agent.
    """
    print("🧪 Testing Import Resolver Agent")
    print("=" * 50)

    agent = ImportResolverAgent()

    # Test 1: Detect and resolve ModuleNotFoundError
    print("\n1. Testing ModuleNotFoundError resolution:")
    error1 = "ModuleNotFoundError: No module named 'TodoService'"
    result1 = agent.auto_resolve_error(error1)
    if result1:
        print(result1[:300] + "..." if len(result1) > 300 else result1)

    # Test 2: Detect and resolve NameError
    print("\n2. Testing NameError resolution:")
    error2 = "NameError: name 'Task' is not defined"
    result2 = agent.auto_resolve_error(error2)
    if result2:
        print(result2[:300] + "..." if len(result2) > 300 else result2)

    # Test 3: Analyze code for import issues
    print("\n3. Testing code analysis:")
    sample_code = """
from ..core.todo_service import TodoService
from nonexistent_module import NonExistentClass

service = TodoService()
obj = NonExistentClass()
"""
    issues = agent.analyze_code_for_import_issues(sample_code)
    print(f"   Detected {len(issues)} issues:")
    for issue in issues:
        print(f"     - {issue}")

    # Test 4: Create and test the Claude Code hook
    print("\n4. Testing Claude Code hook:")
    hook = create_claude_code_hook()
    hook_result = hook("ImportError: cannot import name 'TaskStatus' from 'models'")
    if hook_result:
        print("   Hook returned contextual help:")
        print(hook_result[:200] + "..." if len(hook_result) > 200 else hook_result)

    # Test 5: Test the integrated resolver
    print("\n5. Testing Integrated Import Resolver:")
    integrated_resolver = IntegratedImportResolver()

    # Test error resolution
    integrated_result = integrated_resolver.resolve_import_error("NameError: name 'TodoService' is not defined")
    print(f"   Integrated resolution success: {'agent_resolution' in integrated_result}")

    # Test symbol search
    symbol_search = integrated_resolver.search_symbol("TodoService")
    print(f"   Found {len(symbol_search['import_suggestions'])} import suggestions for 'TodoService'")
    print(f"   Found {len(symbol_search['symbol_definitions'])} symbol definitions")

    # Test file analysis
    import_manager_path = Path(__file__).parent / "import_manager.py"
    if import_manager_path.exists():
        file_analysis = integrated_resolver.analyze_file(str(import_manager_path))
        print(f"   File analysis: {file_analysis.get('summary', 'No analysis available')}")

    print(f"\n✅ Import Resolver Agent is ready for integration!")


if __name__ == "__main__":
    main()