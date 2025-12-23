"""
Python Import Path Fixer Skill
Automatically detects and fixes Python import path issues in Python projects
"""

import os
import sys
import importlib.util
from pathlib import Path
import ast
import json
from typing import List, Dict, Tuple, Optional


class PythonImportFixer:
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.src_dir = self.project_root / "src"

    def scan_for_import_issues(self) -> List[Dict]:
        """Scan project for import-related issues"""
        issues = []

        # Look for all Python files in src directory
        for py_file in self.src_dir.rglob("*.py"):
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Parse the AST to find import statements
                try:
                    tree = ast.parse(content)
                except SyntaxError:
                    issues.append({
                        "file": str(py_file),
                        "type": "syntax_error",
                        "message": f"Syntax error in file: {py_file}"
                    })
                    continue

                # Check for problematic import patterns
                for node in ast.walk(tree):
                    if isinstance(node, ast.ImportFrom) and node.level > 0:
                        # Relative import detected
                        if node.module is None:  # This is a relative import
                            rel_level = "." * node.level
                            issues.append({
                                "file": str(py_file),
                                "type": "relative_import",
                                "relative_level": node.level,
                                "relative_path": rel_level,
                                "message": f"Relative import with {node.level} dots in {py_file}"
                            })

            except Exception as e:
                issues.append({
                    "file": str(py_file),
                    "type": "read_error",
                    "message": f"Could not read file {py_file}: {str(e)}"
                })

        return issues

    def fix_relative_imports(self) -> Dict:
        """Convert relative imports to absolute imports where appropriate"""
        changes = {"converted_imports": [], "failed_conversions": []}

        for py_file in self.src_dir.rglob("*.py"):
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    original_content = f.read()

                # Parse and modify imports
                modified_content = self._convert_relative_imports_in_file(py_file, original_content)

                if modified_content != original_content:
                    # Save the modified content
                    with open(py_file, 'w', encoding='utf-8') as f:
                        f.write(modified_content)

                    changes["converted_imports"].append(str(py_file))

            except Exception as e:
                changes["failed_conversions"].append({
                    "file": str(py_file),
                    "error": str(e)
                })

        return changes

    def _convert_relative_imports_in_file(self, file_path: Path, content: str) -> str:
        """Convert relative imports in a specific file to absolute imports"""
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return content  # Return unchanged if syntax error

        # Calculate the module path from src
        relative_to_src = file_path.relative_to(self.src_dir)
        module_parts = str(relative_to_src.parent).split(os.sep)
        if module_parts == ['.']:  # Current directory
            module_parts = []

        # Find the deepest parent package that contains this file
        current_module_parts = [part for part in module_parts if part != '.']

        # Build mapping for relative imports
        lines = content.splitlines(keepends=True)
        modified_lines = lines[:]

        # Process import nodes in reverse order to preserve line numbers
        import_nodes = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.level > 0 and node.module is None:
                import_nodes.append(node)

        # Sort by line number in descending order
        import_nodes.sort(key=lambda x: x.lineno, reverse=True)

        for node in import_nodes:
            line_idx = node.lineno - 1  # Line numbers are 1-indexed

            if line_idx >= len(lines):
                continue

            original_line = lines[line_idx]

            # Calculate target module based on relative import
            target_parts = current_module_parts[:-node.level] if node.level < len(current_module_parts) else []

            # Add the imported module parts
            imported_parts = [alias.name for alias in node.names]
            imported_module = '.'.join(imported_parts) if imported_parts else ""

            # Construct absolute import
            if target_parts:
                abs_module = '.'.join(['src'] + target_parts)
            else:
                abs_module = 'src'

            # If there's a specific module being imported, add it
            if node.module:
                abs_module = f"{abs_module}.{node.module}"

            new_import = f"from {abs_module} import "
            new_import += ', '.join(alias.name for alias in node.names)
            if node.names and any(alias.asname for alias in node.names):
                new_import = f"from {abs_module} import " + ', '.join(
                    f"{alias.name} as {alias.asname}" if alias.asname else alias.name
                    for alias in node.names
                )

            modified_lines[line_idx] = new_import + '\n'

        return ''.join(modified_lines)

    def create_package_structure(self) -> Dict:
        """Create missing __init__.py files to establish proper package structure"""
        created_files = []
        skipped_dirs = ['__pycache__', '.git', '.vscode', 'node_modules', 'build', 'dist', '__pycache__']

        for dir_path in self.src_dir.rglob("*"):
            if dir_path.is_dir() and dir_path.name not in skipped_dirs:
                init_file = dir_path / "__init__.py"
                if not init_file.exists():
                    with open(init_file, 'w', encoding='utf-8') as f:
                        f.write('"""Auto-generated package init file"""\n')
                    created_files.append(str(init_file))

        # Also ensure root src has __init__.py
        src_init = self.src_dir / "__init__.py"
        if not src_init.exists():
            with open(src_init, 'w', encoding='utf-8') as f:
                f.write('"""Auto-generated package init file"""\n')
            created_files.append(str(src_init))

        return {"created_files": created_files}

    def check_environment_variables(self) -> List[Dict]:
        """Check for common environment variable configuration issues"""
        issues = []

        # Check if .env file exists
        env_file = self.project_root / ".env"
        if not env_file.exists():
            issues.append({
                "type": "missing_env_file",
                "message": "Environment file (.env) not found in project root"
            })
        else:
            # Check for common problematic values
            with open(env_file, 'r') as f:
                env_content = f.read()

            if "DEBUG=" in env_content or 'DEBUG=""' in env_content:
                issues.append({
                    "type": "empty_debug_var",
                    "message": "DEBUG environment variable is empty, which can cause validation errors"
                })

        return issues

    def integrate_with_registry(self) -> Dict:
        """Integrate with import registry for enhanced import resolution"""
        changes = {"registry_integration": []}

        # Check if import registry exists
        registry_file = self.project_root / ".import_registry.json"
        if not registry_file.exists():
            changes["registry_integration"].append("No import registry found, consider running import_registry build")
            return changes

        # Load the registry
        with open(registry_file, 'r') as f:
            registry = json.load(f)

        # Suggest potential improvements based on registry
        suggestions = []
        for symbol, modules in registry.items():
            if len(modules) > 1:  # Multiple definitions found
                suggestions.append({
                    "type": "duplicate_symbol",
                    "symbol": symbol,
                    "modules": modules,
                    "message": f"Symbol '{symbol}' found in multiple modules: {modules}"
                })

        changes["registry_integration"] = suggestions
        return changes

    def fix_environment_variables(self) -> Dict:
        """Fix common environment variable issues"""
        changes = {"fixed_vars": [], "errors": []}

        env_file = self.project_root / ".env"
        if not env_file.exists():
            changes["errors"].append("No .env file found to fix")
            return changes

        with open(env_file, 'r') as f:
            lines = f.readlines()

        modified = False
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith("DEBUG=") and stripped in ["DEBUG=", 'DEBUG=""', 'DEBUG=\'\'']:
                lines[i] = "DEBUG=False\n"  # Set a default value
                changes["fixed_vars"].append("DEBUG")
                modified = True

        if modified:
            with open(env_file, 'w') as f:
                f.writelines(lines)

        return changes


def run_skill(args: Optional[List[str]] = None) -> str:
    """Main function to run the Python Import Path Fixer skill"""
    project_root = args[0] if args and len(args) > 0 else "."

    fixer = PythonImportFixer(project_root)

    result = {
        "project_root": str(fixer.project_root),
        "actions_performed": {}
    }

    # Step 1: Scan for import issues
    print("🔍 Scanning for import issues...")
    issues = fixer.scan_for_import_issues()
    result["detected_issues"] = issues
    print(f"   Found {len(issues)} potential import issues")

    # Step 2: Create proper package structure
    print("📦 Creating proper package structure...")
    pkg_result = fixer.create_package_structure()
    result["actions_performed"]["package_structure"] = pkg_result
    print(f"   Created {len(pkg_result['created_files'])} __init__.py files")

    # Step 3: Fix relative imports
    print("🔄 Converting relative imports to absolute...")
    import_changes = fixer.fix_relative_imports()
    result["actions_performed"]["import_changes"] = import_changes
    print(f"   Converted {len(import_changes['converted_imports'])} import statements")

    # Step 4: Check environment variables
    print("🔧 Checking environment variables...")
    env_issues = fixer.check_environment_variables()
    result["environment_issues"] = env_issues
    print(f"   Found {len(env_issues)} environment variable issues")

    # Step 5: Fix environment variables
    if env_issues:
        print("🔧 Fixing environment variables...")
        env_changes = fixer.fix_environment_variables()
        result["actions_performed"]["env_changes"] = env_changes
        print(f"   Fixed {len(env_changes['fixed_vars'])} environment variables")

    # Step 6: Integrate with import registry
    print("🔗 Integrating with import registry...")
    registry_integration = fixer.integrate_with_registry()
    result["actions_performed"]["registry_integration"] = registry_integration
    print(f"   Registry integration completed")

    # Summary
    print("\n✅ Python Import Path Fixer completed!")
    print(f"   - Found {len(issues)} import issues")
    print(f"   - Created {len(pkg_result['created_files'])} package files")
    print(f"   - Converted {len(import_changes['converted_imports'])} imports")
    print(f"   - Fixed {len(env_changes['fixed_vars'])} environment variables")
    print(f"   - Performed registry integration")

    return json.dumps(result, indent=2)


if __name__ == "__main__":
    import sys
    args = sys.argv[1:] if len(sys.argv) > 1 else None
    print(run_skill(args))