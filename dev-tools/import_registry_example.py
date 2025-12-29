"""
Example of a registry-based import system to help with import path resolution.
This demonstrates the concept of maintaining a registry of all modules in a project.
"""

import os
import ast
import json
from pathlib import Path
from typing import Dict, List, Optional


class ImportRegistry:
    """
    A registry that maintains information about all Python modules in a project
    to help with import path resolution.
    """

    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.registry_file = self.project_root / ".import_registry.json"
        self.modules = {}

    def scan_project(self) -> Dict[str, str]:
        """
        Scan the project for all Python modules and create a registry mapping
        module names to their file paths.
        """
        modules = {}

        # Find all Python files in the project (excluding virtual environments)
        for py_file in self.project_root.rglob("*.py"):
            if any(part.startswith('.') or part in ['venv', '.venv'] for part in py_file.parts):
                continue

            # Calculate the module path relative to project root
            rel_path = py_file.relative_to(self.project_root)

            # Convert file path to module name (e.g., src/core/todo_service.py -> src.core.todo_service)
            module_parts = []
            for part in rel_path.parts:
                if part.endswith('.py'):
                    module_parts.append(part[:-3])  # Remove .py extension
                else:
                    module_parts.append(part)

            module_name = '.'.join(module_parts)
            modules[module_name] = str(rel_path)

        self.modules = modules
        return modules

    def save_registry(self):
        """Save the registry to a file for later use."""
        with open(self.registry_file, 'w') as f:
            json.dump(self.modules, f, indent=2)

    def load_registry(self) -> Dict[str, str]:
        """Load the registry from a file."""
        if self.registry_file.exists():
            with open(self.registry_file, 'r') as f:
                self.modules = json.load(f)
                return self.modules
        return {}

    def find_import_path(self, class_or_function: str) -> List[str]:
        """
        Find potential import paths for a given class or function name.
        This would require parsing the AST of each file to find the actual contents.
        """
        potential_modules = []

        # For each module in the registry, check if it contains the requested class/function
        for module_name, file_path in self.modules.items():
            full_path = self.project_root / file_path

            if full_path.exists():
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Parse the AST to find if this file contains the requested class/function
                    try:
                        tree = ast.parse(content)
                        for node in ast.walk(tree):
                            if isinstance(node, (ast.ClassDef, ast.FunctionDef)):
                                if node.name == class_or_function:
                                    potential_modules.append(module_name)
                                    break
                    except SyntaxError:
                        continue
                except Exception:
                    continue

        return potential_modules

    def suggest_import(self, class_or_function: str) -> List[str]:
        """
        Suggest import statements for a given class or function name.
        """
        modules = self.find_import_path(class_or_function)
        suggestions = []

        for module in modules:
            suggestions.append(f"from {module} import {class_or_function}")

        return suggestions


# Example usage:
if __name__ == "__main__":
    # Initialize registry for the current project
    registry = ImportRegistry(".")

    # Scan the project to build the registry
    print("🔍 Scanning project for Python modules...")
    modules = registry.scan_project()
    print(f"   Found {len(modules)} modules")

    # Save the registry
    registry.save_registry()
    print(f"💾 Registry saved to {registry.registry_file}")

    # Example: Find where TodoService is defined
    print("\n🔍 Looking for 'TodoService'...")
    suggestions = registry.suggest_import("TodoService")
    if suggestions:
        print("   Possible imports:")
        for suggestion in suggestions:
            print(f"     {suggestion}")
    else:
        print("   No matches found")

    # Example: Find where Task is defined
    print("\n🔍 Looking for 'Task'...")
    suggestions = registry.suggest_import("Task")
    if suggestions:
        print("   Possible imports:")
        for suggestion in suggestions:
            print(f"     {suggestion}")
    else:
        print("   No matches found")