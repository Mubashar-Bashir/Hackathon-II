"""
Alternative approaches to Python import resolution and file searching.

This file demonstrates several different methods for resolving import paths
and quickly finding files in Python projects.
"""

import os
import ast
import sys
from pathlib import Path
from typing import List, Dict, Optional
import importlib.util


class ImportResolutionAlternatives:
    """
    Demonstrates various approaches to Python import resolution and file searching.
    """

    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()

    def approach_1_ast_analysis(self) -> Dict[str, str]:
        """
        Approach 1: AST-based analysis to map all classes/functions to their modules.
        This is similar to the registry approach but more sophisticated.
        """
        print("Approach 1: AST-based analysis")

        symbols = {}  # Maps symbol names to module paths

        for py_file in self.project_root.rglob("*.py"):
            if any(part.startswith('.') or part in ['venv', '.venv', '__pycache__'] for part in py_file.parts):
                continue

            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                tree = ast.parse(content)

                # Extract relative module path
                rel_path = py_file.relative_to(self.project_root)
                module_parts = []
                for part in rel_path.parts:
                    if part.endswith('.py'):
                        module_parts.append(part[:-3])
                    else:
                        module_parts.append(part)
                module_name = '.'.join(module_parts)

                # Find all classes and functions in the file
                for node in ast.walk(tree):
                    if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.Assign)):
                        if isinstance(node, (ast.ClassDef, ast.FunctionDef)):
                            symbol_name = node.name
                        elif isinstance(node, ast.Assign):
                            # For variable assignments, get the first target name
                            if node.targets and hasattr(node.targets[0], 'id'):
                                symbol_name = node.targets[0].id
                            else:
                                continue
                        else:
                            continue

                        # Store symbol with its module
                        if symbol_name not in symbols:
                            symbols[symbol_name] = []
                        symbols[symbol_name].append(module_name)

            except (SyntaxError, UnicodeDecodeError):
                continue

        return symbols

    def approach_2_dynamic_import_verification(self, module_name: str, symbol_name: str) -> bool:
        """
        Approach 2: Dynamic verification of imports at runtime.
        """
        print(f"Approach 2: Verifying import - from {module_name} import {symbol_name}")

        try:
            spec = importlib.util.find_spec(module_name)
            if spec is None:
                return False

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Check if the symbol exists in the module
            return hasattr(module, symbol_name)
        except (ImportError, AttributeError, ModuleNotFoundError):
            return False

    def approach_3_path_manipulation(self):
        """
        Approach 3: Proper sys.path management for import resolution.
        """
        print("Approach 3: Managing sys.path for proper imports")

        # Add project root to Python path if not already there
        project_root_str = str(self.project_root)
        if project_root_str not in sys.path:
            sys.path.insert(0, project_root_str)
            print(f"  Added {project_root_str} to sys.path")

        # Add src directory to Python path if it exists
        src_path = self.project_root / "src"
        if src_path.exists() and str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))
            print(f"  Added {src_path} to sys.path")

        return sys.path

    def approach_4_fuzzy_file_search(self, target_name: str) -> List[Path]:
        """
        Approach 4: Fuzzy file searching based on name patterns.
        """
        print(f"Approach 4: Fuzzy searching for files containing '{target_name}'")

        matches = []

        for py_file in self.project_root.rglob("*.py"):
            if any(part.startswith('.') or part in ['venv', '.venv', '__pycache__'] for part in py_file.parts):
                continue

            # Check if filename contains the target name (case-insensitive)
            if target_name.lower() in py_file.name.lower():
                matches.append(py_file)

            # Also check file contents for the target name
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read().lower()
                if target_name.lower() in content:
                    if py_file not in matches:
                        matches.append(py_file)
            except UnicodeDecodeError:
                continue

        return matches

    def approach_5_lsp_integration(self, file_path: str, line: int, char: int):
        """
        Approach 5: Integration with Language Server Protocol for import resolution.
        (This would typically be done with an external LSP server)
        """
        print(f"Approach 5: LSP integration for {file_path}:{line}:{char}")
        print("  This would typically connect to a Python LSP server like Pylsp or Jedi")
        # In practice, this would use the LSP tool available in Claude Code

    def approach_6_caching_and_indexing(self) -> Dict:
        """
        Approach 6: Caching and indexing system for fast lookup.
        """
        print("Approach 6: Creating a persistent cache/index for imports")

        # This would typically create a more sophisticated index
        # with metadata about all symbols in the project
        index = {
            "last_updated": str(Path.cwd() / "last_scan_time"),
            "file_count": 0,
            "symbol_count": 0,
            "modules": {},
            "symbol_locations": {}
        }

        # Count Python files
        py_files = list(self.project_root.rglob("*.py"))
        index["file_count"] = len([f for f in py_files if not any(part.startswith('.') or part in ['venv', '.venv', '__pycache__'] for part in f.parts)])

        # This would be expanded with actual indexing logic
        return index


# Example usage
if __name__ == "__main__":
    resolver = ImportResolutionAlternatives(".")

    print("🔍 Demonstrating Alternative Import Resolution Approaches\n")

    # Approach 1: AST Analysis
    symbols = resolver.approach_1_ast_analysis()
    print(f"  Found {len(symbols)} unique symbols in the project")
    if 'TodoService' in symbols:
        print(f"  TodoService can be imported from: {symbols['TodoService']}")
    if 'Task' in symbols:
        print(f"  Task can be imported from: {symbols['Task']}")
    print()

    # Approach 2: Dynamic Verification
    exists = resolver.approach_2_dynamic_import_verification('src.core.todo_service', 'TodoService')
    print(f"  Import verification result: {exists}\n")

    # Approach 3: Path Management
    paths = resolver.approach_3_path_manipulation()
    print(f"  Current sys.path has {len(paths)} entries\n")

    # Approach 4: Fuzzy Search
    matches = resolver.approach_4_fuzzy_file_search('todo_service')
    print(f"  Found {len(matches)} files related to 'todo_service':")
    for match in matches[:3]:  # Show first 3 matches
        print(f"    {match}")
    print()

    # Approach 5: LSP Integration
    resolver.approach_5_lsp_integration("src/ui/cli.py", 6, 10)
    print()

    # Approach 6: Caching and Indexing
    index = resolver.approach_6_caching_and_indexing()
    print(f"  Index created with {index['file_count']} Python files\n")

    print("💡 Each approach has its own advantages:")
    print("   - AST Analysis: Precise symbol mapping but requires parsing all files")
    print("   - Dynamic Verification: Runtime validation but can be slow")
    print("   - Path Management: Simple but requires proper setup")
    print("   - Fuzzy Search: Quick file location but less precise")
    print("   - LSP Integration: Professional-grade but needs external tools")
    print("   - Caching: Fast lookups but needs maintenance")