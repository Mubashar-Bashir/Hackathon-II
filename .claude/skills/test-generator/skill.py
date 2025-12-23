"""
Test Generator Skill
Automatically creates test scaffolds for new code
"""

import os
import re
import ast
import json
from pathlib import Path
from typing import List, Dict, Optional

class TestGenerator:
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()

    def analyze_code_structure(self, file_path: str) -> Dict:
        """Analyze a Python file to extract functions and classes for testing"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            tree = ast.parse(content)

            functions = []
            classes = []

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Skip private functions (starting with _)
                    if not node.name.startswith('_'):
                        functions.append({
                            'name': node.name,
                            'line': node.lineno,
                            'args': [arg.arg for arg in node.args.args if arg.arg != 'self'],
                            'has_return': any(isinstance(n, ast.Return) for n in ast.walk(node)),
                            'docstring': ast.get_docstring(node)
                        })

                elif isinstance(node, ast.AsyncFunctionDef):
                    # Handle async functions
                    if not node.name.startswith('_'):
                        functions.append({
                            'name': node.name,
                            'line': node.lineno,
                            'args': [arg.arg for arg in node.args.args if arg.arg != 'self'],
                            'has_return': any(isinstance(n, ast.Return) for n in ast.walk(node)),
                            'docstring': ast.get_docstring(node),
                            'is_async': True
                        })

                elif isinstance(node, ast.ClassDef):
                    # Skip private classes (starting with _)
                    if not node.name.startswith('_'):
                        methods = []
                        for item in node.body:
                            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                                if not item.name.startswith('_'):  # Public methods
                                    methods.append({
                                        'name': item.name,
                                        'line': item.lineno,
                                        'args': [arg.arg for arg in item.args.args if arg.arg != 'self'],
                                        'has_return': any(isinstance(n, ast.Return) for n in ast.walk(item)),
                                        'docstring': ast.get_docstring(item),
                                        'is_async': isinstance(item, ast.AsyncFunctionDef)
                                    })

                        classes.append({
                            'name': node.name,
                            'line': node.lineno,
                            'methods': methods,
                            'docstring': ast.get_docstring(node)
                        })

            return {
                'file': file_path,
                'functions': functions,
                'classes': classes
            }
        except Exception as e:
            return {
                'file': file_path,
                'error': str(e),
                'functions': [],
                'classes': []
            }

    def generate_test_content(self, code_analysis: Dict) -> str:
        """Generate test content based on code analysis"""
        if code_analysis.get('error'):
            return f"# Error analyzing {code_analysis['file']}: {code_analysis['error']}"

        content = []
        content.append('import pytest')
        content.append('from unittest.mock import Mock, patch')
        content.append('')

        # Import the module being tested
        module_path = code_analysis['file'].replace('.py', '').replace('/', '.').replace('\\\\', '.')
        if module_path.startswith('.'):
            module_path = module_path[1:]

        content.append(f'from {module_path} import *')
        content.append('')

        # Generate tests for functions
        for func in code_analysis['functions']:
            content.append(f'# Test for function: {func["name"]}')
            content.append(f'def test_{func["name"]}_with_valid_input():')
            content.append('    """Test the function with valid input parameters."""')

            args = ', '.join([f'param_{arg}=Mock()' for arg in func['args']]) if func['args'] else ''
            content.append(f'    result = {func["name"]}({args})')

            if func['has_return']:
                content.append('    # Add assertions based on expected return value')
                content.append('    assert result is not None  # Replace with actual assertion')
            else:
                content.append('    # Verify function executes without errors')
                content.append('    assert True  # Replace with actual assertion')
            content.append('')

        # Generate tests for classes
        for cls in code_analysis['classes']:
            content.append(f'# Test for class: {cls["name"]}')
            content.append(f'class Test{cls["name"]}:')
            content.append('    """Test cases for the class."""')

            if cls['methods']:
                for method in cls['methods']:
                    content.append(f'    def test_{method["name"]}_with_valid_input(self):')
                    content.append('        """Test the method with valid input parameters."""')

                    args = ', '.join([f'param_{arg}=Mock()' for arg in method['args']]) if method['args'] else ''
                    content.append(f'        obj = {cls["name"]}()')
                    content.append(f'        result = obj.{method["name"]}({args})')

                    if method['has_return']:
                        content.append('        # Add assertions based on expected return value')
                        content.append('        assert result is not None  # Replace with actual assertion')
                    else:
                        content.append('        # Verify method executes without errors')
                        content.append('        assert True  # Replace with actual assertion')
                    content.append('')
            else:
                content.append(f'    def test_{cls["name"]}_instantiation(self):')
                content.append('        """Test that the class can be instantiated."""')
                content.append(f'        obj = {cls["name"]}()')
                content.append('        assert obj is not None')
                content.append('')

        return '\\n'.join(content)

    def create_test_file(self, source_file: str) -> str:
        """Create a test file for a given source file"""
        # Generate test file path
        source_path = Path(source_file)
        test_dir = source_path.parent / 'tests'

        # If no tests directory exists, create a test file in the same directory with 'test_' prefix
        if not test_dir.exists():
            test_file_path = source_path.parent / f'test_{source_path.name}'
        else:
            # Create test file in tests directory
            test_file_path = test_dir / f'test_{source_path.name}'

        # Analyze the source code
        analysis = self.analyze_code_structure(source_file)

        # Generate test content
        test_content = self.generate_test_content(analysis)

        # Write the test file
        with open(test_file_path, 'w', encoding='utf-8') as f:
            f.write(test_content)

        return str(test_file_path)

    def scan_and_generate_tests(self) -> List[Dict]:
        """Scan the project and generate test files for Python modules"""
        results = []

        # Find all Python files except test files
        for py_file in self.project_root.rglob("*.py"):
            if 'test' not in py_file.name and 'conftest' not in py_file.name:
                if self._should_skip_file(py_file):
                    continue

                try:
                    test_file_path = self.create_test_file(str(py_file))
                    results.append({
                        'source_file': str(py_file),
                        'test_file_created': test_file_path,
                        'status': 'success'
                    })
                except Exception as e:
                    results.append({
                        'source_file': str(py_file),
                        'error': str(e),
                        'status': 'error'
                    })

        return results

    def _should_skip_file(self, file_path: Path) -> bool:
        """Determine if a file should be skipped during test generation"""
        skip_patterns = [
            'node_modules', '__pycache__', '.git', '.vscode', 'dist', 'build',
            'venv', 'env', '.env', 'env.bak', '.venv', 'virtualenv',
            'package-lock.json', 'yarn.lock'
        ]

        file_path_str = str(file_path)
        return any(skip_pattern in file_path_str for skip_pattern in skip_patterns)


def run_skill(args: Optional[List[str]] = None) -> str:
    """Main function to run the Test Generator skill"""
    project_root = args[0] if args and len(args) > 0 else "."

    generator = TestGenerator(project_root)

    print("🧪 Scanning project for modules to create tests for...")
    results = generator.scan_and_generate_tests()

    success_count = len([r for r in results if r['status'] == 'success'])
    error_count = len([r for r in results if r['status'] == 'error'])

    print(f"✅ Test generation completed!")
    print(f"   - Created tests for {success_count} modules")
    print(f"   - Encountered errors for {error_count} modules")

    if success_count > 0:
        print("\\n📋 Test files created:")
        for result in results[:5]:  # Show first 5 results
            if result['status'] == 'success':
                print(f"   - {result['test_file_created']} (from {result['source_file']})")

        if success_count > 5:
            print(f"   ... and {success_count - 5} more test files")

    if error_count > 0:
        print("\\n❌ Errors encountered:")
        for result in results:
            if result['status'] == 'error':
                print(f"   - {result['source_file']}: {result['error']}")

    return json.dumps({
        'summary': {
            'total_processed': len(results),
            'success_count': success_count,
            'error_count': error_count
        },
        'details': results
    }, indent=2)


if __name__ == "__main__":
    import sys
    args = sys.argv[1:] if len(sys.argv) > 1 else None
    print(run_skill(args))