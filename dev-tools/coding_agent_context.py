"""
Context-Aware Import Resolution System for Coding Agents
This system provides contextual help for coding agents when they encounter import issues.
"""

import os
import sys
import ast
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class ImportErrorContext:
    """Represents the context of an import error for contextual resolution."""
    error_message: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    code_context: Optional[str] = None
    suggested_fixes: List[str] = None

    def __post_init__(self):
        if self.suggested_fixes is None:
            self.suggested_fixes = []


class CodingAgentImportResolver:
    """
    A context-aware import resolution system for coding agents.
    Automatically detects import issues and provides contextual help.
    """

    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.registry_file = self.project_root / ".import_registry.json"
        self.error_patterns = [
            r"ModuleNotFoundError: No module named '(.+)'",
            r"ImportError: cannot import name '(.+)' from '(.+)'",
            r"NameError: name '(.+)' is not defined",  # Could be due to missing import
        ]

    def detect_import_error(self, error_text: str) -> Optional[ImportErrorContext]:
        """
        Detect if the error is an import-related error and extract context.
        """
        for pattern in self.error_patterns:
            match = re.search(pattern, error_text)
            if match:
                if "ModuleNotFoundError" in error_text:
                    module_name = match.group(1)
                    return ImportErrorContext(
                        error_message=error_text,
                        suggested_fixes=[f"Could not find module: {module_name}"]
                    )
                elif "ImportError" in error_text:
                    name = match.group(1)
                    module = match.group(2) if len(match.groups()) > 1 else ""
                    return ImportErrorContext(
                        error_message=error_text,
                        suggested_fixes=[f"Could not import {name} from {module}"]
                    )
                elif "NameError" in error_text:
                    name = match.group(1)
                    return ImportErrorContext(
                        error_message=error_text,
                        suggested_fixes=[f"Name {name} is not defined - possibly missing import"]
                    )

        return None

    def find_possible_imports(self, symbol_name: str) -> List[str]:
        """
        Find possible import statements for a symbol using the registry.
        """
        if not self.registry_file.exists():
            # Build registry if it doesn't exist
            self._build_registry_from_project()

        try:
            with open(self.registry_file, 'r') as f:
                registry = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

        if symbol_name in registry:
            return [f"from {module} import {symbol_name}" for module in registry[symbol_name]]

        # If exact match not found, try fuzzy matching
        possible_matches = []
        for reg_symbol, modules in registry.items():
            if symbol_name.lower() in reg_symbol.lower() or reg_symbol.lower() in symbol_name.lower():
                for module in modules:
                    possible_matches.append(f"from {module} import {reg_symbol}")

        return possible_matches[:10]  # Limit to 10 suggestions

    def _build_registry_from_project(self):
        """
        Build import registry from the project files.
        """
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

            except (SyntaxError, UnicodeDecodeError):
                continue

        # Save registry
        with open(self.registry_file, "w") as f:
            json.dump(symbols, f, indent=2)

    def provide_contextual_help(self, error_context: ImportErrorContext) -> str:
        """
        Provide contextual help based on the error context.
        """
        help_text = []
        help_text.append("🚨 IMPORT ERROR DETECTED")
        help_text.append(f"Error: {error_context.error_message}")

        # Extract symbol name from error for suggestions
        symbol_name = self._extract_symbol_from_error(error_context.error_message)

        if symbol_name:
            possible_imports = self.find_possible_imports(symbol_name)
            if possible_imports:
                help_text.append(f"\n💡 POSSIBLE IMPORTS FOR '{symbol_name}':")
                for imp in possible_imports[:5]:  # Show top 5 suggestions
                    help_text.append(f"  {imp}")

            # Also suggest files that might contain the symbol
            related_files = self._find_files_containing_symbol(symbol_name)
            if related_files:
                help_text.append(f"\n📁 POSSIBLE SOURCE FILES FOR '{symbol_name}':")
                for file_path in related_files[:3]:  # Show top 3 files
                    help_text.append(f"  {file_path}")

        # Add general help
        help_text.append(f"\n📖 SUGGESTED ACTIONS:")
        help_text.append(f"  1. Check if the module exists in your project")
        help_text.append(f"  2. Verify the import path is correct")
        help_text.append(f"  3. Consider running 'import_manager.py fix' to resolve common issues")
        help_text.append(f"  4. Use 'import_manager.py find {symbol_name}' to locate the symbol")

        return "\n".join(help_text)

    def _extract_symbol_from_error(self, error_message: str) -> Optional[str]:
        """
        Extract the symbol name from an error message.
        """
        # Try to extract from ModuleNotFoundError
        module_match = re.search(r"ModuleNotFoundError: No module named '(.+)'", error_message)
        if module_match:
            return module_match.group(1).split('.')[-1]  # Get the last part of the module path

        # Try to extract from ImportError
        import_match = re.search(r"ImportError: cannot import name '(.+)' from", error_message)
        if import_match:
            return import_match.group(1)

        # Try to extract from NameError
        name_match = re.search(r"NameError: name '(.+)' is not defined", error_message)
        if name_match:
            return name_match.group(1)

        return None

    def _find_files_containing_symbol(self, symbol_name: str) -> List[str]:
        """
        Find files that might contain the symbol.
        """
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

    def analyze_code_for_import_issues(self, code: str, file_path: str = "") -> List[str]:
        """
        Analyze code for potential import issues.
        """
        issues = []

        try:
            tree = ast.parse(code)
        except SyntaxError:
            return ["Syntax error in code - cannot analyze imports"]

        # Check for undefined names that might be missing imports
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                # This is a variable usage - check if it's likely to be a missing import
                if node.id.isupper() or node.id.istitle():  # Likely a class name
                    possible_imports = self.find_possible_imports(node.id)
                    if possible_imports:
                        issues.append(f"Possible missing import for '{node.id}'. Consider: {possible_imports[0]}")

        # Check for import statements that might be problematic
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if node.module and node.level > 0:  # Relative import
                    issues.append(f"Relative import detected: from {'.' * node.level}{node.module}")

        return issues


def create_coding_agent_hook():
    """
    Create a hook function that can be integrated into coding agents
    to automatically detect and resolve import issues.
    """
    def import_resolver_hook(error_text: str) -> Optional[str]:
        """
        Hook function to be called when a coding agent encounters an error.
        Returns contextual help if it's an import issue, None otherwise.
        """
        resolver = CodingAgentImportResolver()

        # Detect if this is an import error
        error_context = resolver.detect_import_error(error_text)

        if error_context:
            # Provide contextual help
            return resolver.provide_contextual_help(error_context)

        return None

    return import_resolver_hook


def main():
    """
    Main function for testing the context-aware import resolver.
    """
    print("🧪 Testing Context-Aware Import Resolver for Coding Agents")
    print("=" * 60)

    resolver = CodingAgentImportResolver()

    # Test 1: Detect ModuleNotFoundError
    print("\n1. Testing ModuleNotFoundError detection:")
    error1 = "ModuleNotFoundError: No module named 'TodoService'"
    context1 = resolver.detect_import_error(error1)
    if context1:
        print(f"   Detected: {context1.error_message}")
        print(f"   Suggested fixes: {context1.suggested_fixes}")

    # Test 2: Find possible imports
    print("\n2. Testing import suggestions:")
    imports = resolver.find_possible_imports("TodoService")
    print(f"   Possible imports for 'TodoService': {imports[:3]}")  # Show first 3

    # Test 3: Provide contextual help
    print("\n3. Testing contextual help:")
    if context1:
        help_text = resolver.provide_contextual_help(context1)
        print(help_text[:500] + "..." if len(help_text) > 500 else help_text)

    # Test 4: Analyze code for import issues
    print("\n4. Testing code analysis:")
    sample_code = """
from ..core.todo_service import TodoService
from nonexistent_module import NonExistentClass

service = TodoService()
obj = NonExistentClass()
"""
    issues = resolver.analyze_code_for_import_issues(sample_code)
    print(f"   Detected issues: {issues}")

    # Test 5: Create and test the hook
    print("\n5. Testing hook function:")
    hook = create_coding_agent_hook()
    result = hook("NameError: name 'Task' is not defined")
    if result:
        print("   Hook returned contextual help:")
        print(result[:300] + "..." if len(result) > 300 else result)


if __name__ == "__main__":
    main()