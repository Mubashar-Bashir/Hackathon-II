"""
Import Registry Skill
Automatically maintains a registry of all Python modules and symbols in the project
for quick import path resolution.
"""

import os
import ast
import json
from pathlib import Path
from typing import Dict, List, Optional


class ImportRegistrySkill:
    """
    A skill to maintain and use an import registry for the project.
    """

    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.registry_file = self.project_root / ".import_registry.json"
        self.modules = {}

    def build_registry(self) -> Dict:
        """
        Build the import registry by scanning the project.
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
                        # Add module to list if not already present
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
                        elif isinstance(node, ast.Import) and node.names:
                            # This is an import like 'import module'
                            for alias in node.names:
                                imported_name = alias.asname if alias.asname else alias.name
                                if imported_name not in symbols:
                                    symbols[imported_name] = []
                                if alias.name not in symbols[imported_name]:
                                    symbols[imported_name].append(alias.name)

            except (SyntaxError, UnicodeDecodeError):
                continue

        # Save registry
        with open(self.registry_file, "w") as f:
            json.dump(symbols, f, indent=2)

        return symbols

    def find_import_path(self, symbol_name: str) -> List[str]:
        """
        Find import paths for a given symbol.
        """
        if not self.registry_file.exists():
            self.build_registry()

        with open(self.registry_file, "r") as f:
            symbols = json.load(f)

        if symbol_name in symbols:
            return [f"from {module} import {symbol_name}" for module in symbols[symbol_name]]
        return []

    def suggest_import(self, partial_name: str) -> List[str]:
        """
        Suggest imports based on partial name matching.
        """
        if not self.registry_file.exists():
            self.build_registry()

        with open(self.registry_file, "r") as f:
            symbols = json.load(f)

        matches = []
        for symbol_name, modules in symbols.items():
            if partial_name.lower() in symbol_name.lower():
                for module in modules:
                    matches.append(f"from {module} import {symbol_name}")

        return matches

    def get_all_symbols(self) -> Dict[str, List[str]]:
        """
        Get all symbols in the registry with their import paths.
        """
        if not self.registry_file.exists():
            self.build_registry()

        with open(self.registry_file, "r") as f:
            return json.load(f)

    def update_registry(self) -> Dict:
        """
        Update the registry incrementally (for use when files change).
        """
        return self.build_registry()

    def find_file_by_symbol(self, symbol_name: str) -> List[str]:
        """
        Find the file paths where a symbol is defined.
        """
        if not self.registry_file.exists():
            self.build_registry()

        with open(self.registry_file, "r") as f:
            symbols = json.load(f)

        if symbol_name not in symbols:
            return []

        file_paths = []
        for module_name in symbols[symbol_name]:
            # Convert module name back to file path
            file_path = self.project_root / Path(module_name.replace(".", "/") + ".py")
            if file_path.exists():
                file_paths.append(str(file_path))

        return file_paths


def run_skill(args: Optional[List[str]] = None) -> str:
    """
    Main function to run the Import Registry Skill.
    """
    project_root = args[0] if args and len(args) > 0 else "."
    action = args[1] if args and len(args) > 1 else "build"

    registry = ImportRegistrySkill(project_root)

    if action == "build":
        symbols = registry.build_registry()
        return f"✅ Built registry with {len(symbols)} symbols. Registry saved to {registry.registry_file}"
    elif action == "find":
        symbol = args[2] if len(args) > 2 else None
        if symbol:
            imports = registry.find_import_path(symbol)
            if imports:
                return f"🔍 Found import paths for '{symbol}':\n" + "\n".join(f"  {imp}" for imp in imports)
            else:
                return f"❌ No import paths found for '{symbol}'"
        else:
            return "❌ Please provide a symbol name to find (e.g., 'import_registry find TodoService')"
    elif action == "suggest":
        partial = args[2] if len(args) > 2 else None
        if partial:
            imports = registry.suggest_import(partial)
            if imports:
                suggestions = imports[:10]  # Limit to 10 suggestions
                result = f"💡 Suggested imports for '{partial}' (showing first 10):\n"
                result += "\n".join(f"  {imp}" for imp in suggestions)
                if len(imports) > 10:
                    result += f"\n  ... and {len(imports) - 10} more"
                return result
            else:
                return f"❌ No suggestions found for '{partial}'"
        else:
            return "❌ Please provide a partial symbol name to suggest (e.g., 'import_registry suggest Service')"
    elif action == "list":
        symbols = registry.get_all_symbols()
        return f"📋 Registry contains {len(symbols)} symbols: {', '.join(list(symbols.keys())[:20])}{'...' if len(symbols) > 20 else ''}"
    elif action == "update":
        symbols = registry.update_registry()
        return f"🔄 Updated registry with {len(symbols)} symbols"
    elif action == "find-file":
        symbol = args[2] if len(args) > 2 else None
        if symbol:
            files = registry.find_file_by_symbol(symbol)
            if files:
                return f"📁 Files defining '{symbol}':\n" + "\n".join(f"  {f}" for f in files)
            else:
                return f"❌ No files found defining '{symbol}'"
        else:
            return "❌ Please provide a symbol name to find its file (e.g., 'import_registry find-file TodoService')"
    else:
        return """📖 Import Registry Skill Usage:
  import_registry build           - Build the import registry
  import_registry find <symbol>   - Find import paths for a symbol
  import_registry suggest <text>  - Suggest imports matching text
  import_registry list           - List all registered symbols
  import_registry update         - Update the registry
  import_registry find-file <symbol> - Find file containing symbol

Example: import_registry find TodoService
"""


if __name__ == "__main__":
    import sys
    args = sys.argv[1:]
    print(run_skill(args))