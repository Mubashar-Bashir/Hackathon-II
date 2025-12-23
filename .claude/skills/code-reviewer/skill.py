"""
Code Reviewer Skill
Automatically reviews code for quality, best practices, and potential issues
"""

import ast
import re
import json
from pathlib import Path
from typing import List, Dict, Optional

class CodeReviewer:
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.review_criteria = {
            "naming_conventions": [
                r'def [a-z_][a-zA-Z0-9_]*\(',  # Function names should be snake_case
                r'class [A-Z][a-zA-Z0-9]*:',    # Class names should be PascalCase
                r'[a-z_][a-zA-Z0-9_]* = '      # Variable names should be snake_case
            ],
            "potential_bugs": [
                r'==\s*None',      # Should use 'is' instead of '=='
                r'!=\s*None',      # Should use 'is not' instead of '!='
                r'for\s+\w+\s+in\s+range\(\w+\):',  # Potential off-by-one if using length directly
                r'import\s+\*',    # Wildcard imports can cause namespace pollution
            ],
            "performance_issues": [
                r'for.*:\s*if.*:\s*append',  # Inefficient list building in loops
                r'.*\.append\(\)\s+for',    # List comprehension might be better
            ],
            "security_issues": [
                r'eval\(',          # eval is dangerous
                r'exec\(',          # exec is dangerous
                r'os\.system\(',    # Command injection risk
                r'subprocess\..*\(.*\+.*\)',  # Potential command injection
            ]
        }

    def review_file(self, file_path: str) -> List[Dict]:
        """Review a single file for code quality issues"""
        issues = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check for general issues using regex
            issues.extend(self._check_regex_issues(file_path, content))

            # For Python files, do AST analysis
            if file_path.endswith('.py'):
                issues.extend(self._analyze_python_ast(file_path, content))

        except Exception as e:
            issues.append({
                "file": file_path,
                "type": "review_error",
                "message": f"Could not review file {file_path}: {str(e)}"
            })

        return issues

    def _check_regex_issues(self, file_path: str, content: str) -> List[Dict]:
        """Check for issues using regex patterns"""
        issues = []

        for category, patterns in self.review_criteria.items():
            for pattern in patterns:
                matches = re.finditer(pattern, content)
                for match in matches:
                    line_number = content[:match.start()].count('\\n') + 1
                    issues.append({
                        "file": file_path,
                        "type": category,
                        "line": line_number,
                        "code": match.group(0)[:100],
                        "message": f"Potential {category.replace('_', ' ')} issue detected"
                    })

        return issues

    def _analyze_python_ast(self, file_path: str, content: str) -> List[Dict]:
        """Analyze Python code using AST for more sophisticated checks"""
        issues = []

        try:
            tree = ast.parse(content)

            for node in ast.walk(tree):
                # Check for functions with too many parameters
                if isinstance(node, ast.FunctionDef):
                    if len(node.args.args) > 5:
                        issues.append({
                            "file": file_path,
                            "type": "function_complexity",
                            "line": node.lineno,
                            "code": node.name,
                            "message": f"Function '{node.name}' has {len(node.args.args)} parameters, consider reducing complexity"
                        })

                # Check for nested blocks that are too deep
                if isinstance(node, (ast.If, ast.For, ast.While, ast.With, ast.Try)):
                    depth = self._get_node_depth(node, tree)
                    if depth > 3:
                        issues.append({
                            "file": file_path,
                            "type": "nesting_complexity",
                            "line": node.lineno,
                            "code": type(node).__name__,
                            "message": f"Nested block at line {node.lineno} has depth {depth}, consider simplifying"
                        })

                # Check for unused imports
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        name = alias.asname if alias.asname else alias.name
                        if not self._is_name_used(name, tree, node):
                            issues.append({
                                "file": file_path,
                                "type": "unused_import",
                                "line": node.lineno,
                                "code": name,
                                "message": f"Import '{name}' is not used in this file"
                            })

        except SyntaxError:
            issues.append({
                "file": file_path,
                "type": "syntax_error",
                "line": 0,
                "code": "",
                "message": "Syntax error in file, unable to parse AST"
            })

        return issues

    def _get_node_depth(self, node, tree) -> int:
        """Calculate the nesting depth of a node in the AST"""
        depth = 0
        current = node
        while current != tree:
            parent = self._find_parent(current, tree)
            if parent is None:
                break
            if isinstance(parent, (ast.If, ast.For, ast.While, ast.With, ast.Try)):
                depth += 1
            current = parent
        return depth

    def _find_parent(self, node, tree) -> Optional[ast.AST]:
        """Find the parent of a node in the AST"""
        for child in ast.walk(tree):
            for field, value in ast.iter_fields(child):
                if isinstance(value, list):
                    for item in value:
                        if item == node:
                            return child
                elif value == node:
                    return child
        return None

    def _is_name_used(self, name: str, tree, import_node) -> bool:
        """Check if an imported name is used in the code"""
        for node in ast.walk(tree):
            if isinstance(node, (ast.Name, ast.Attribute)):
                if isinstance(node, ast.Name) and node.id == name and node != import_node:
                    return True
                elif isinstance(node, ast.Attribute) and node.attr == name:
                    return True
        return False

    def scan_project(self) -> List[Dict]:
        """Scan the entire project for code quality issues"""
        issues = []

        for ext in ['.py', '.js', '.ts', '.jsx', '.tsx']:
            for file_path in self.project_root.rglob(f"*{ext}"):
                if self._should_skip_file(file_path):
                    continue

                file_issues = self.review_file(str(file_path))
                issues.extend(file_issues)

        return issues

    def _should_skip_file(self, file_path: Path) -> bool:
        """Determine if a file should be skipped during code review"""
        skip_patterns = [
            'node_modules', '__pycache__', '.git', '.vscode', 'dist', 'build',
            'venv', 'env', '.env', 'env.bak', '.venv', 'virtualenv',
            'package-lock.json', 'yarn.lock', '.min.js', 'test_', 'spec_'
        ]

        file_path_str = str(file_path)
        return any(skip_pattern in file_path_str for skip_pattern in skip_patterns)

    def generate_review_report(self, issues: List[Dict]) -> Dict:
        """Generate a comprehensive code review report"""
        report = {
            "summary": {
                "total_files_reviewed": len(set(issue["file"] for issue in issues)),
                "total_issues_found": len(issues),
                "issue_types": {},
                "severity_breakdown": {
                    "critical": 0,
                    "high": 0,
                    "medium": 0,
                    "low": 0
                }
            },
            "issues": issues
        }

        # Count issue types
        for issue in issues:
            issue_type = issue["type"]
            if issue_type not in report["summary"]["issue_types"]:
                report["summary"]["issue_types"][issue_type] = 0
            report["summary"]["issue_types"][issue_type] += 1

            # Categorize severity
            if issue_type in ["security_issues", "syntax_error"]:
                report["summary"]["severity_breakdown"]["critical"] += 1
            elif issue_type in ["potential_bugs", "function_complexity"]:
                report["summary"]["severity_breakdown"]["high"] += 1
            elif issue_type in ["performance_issues", "naming_conventions"]:
                report["summary"]["severity_breakdown"]["medium"] += 1
            else:
                report["summary"]["severity_breakdown"]["low"] += 1

        return report


def run_skill(args: Optional[List[str]] = None) -> str:
    """Main function to run the Code Reviewer skill"""
    project_root = args[0] if args and len(args) > 0 else "."

    reviewer = CodeReviewer(project_root)

    print("🔍 Scanning project for code quality issues...")
    issues = reviewer.scan_project()

    report = reviewer.generate_review_report(issues)

    print(f"✅ Code review completed!")
    print(f"   - Reviewed {report['summary']['total_files_reviewed']} files")
    print(f"   - Found {report['summary']['total_issues_found']} potential issues")
    print(f"   - Critical: {report['summary']['severity_breakdown']['critical']}")
    print(f"   - High: {report['summary']['severity_breakdown']['high']}")
    print(f"   - Medium: {report['summary']['severity_breakdown']['medium']}")
    print(f"   - Low: {report['summary']['severity_breakdown']['low']}")

    if report['summary']['total_issues_found'] > 0:
        print("\\n📋 Detailed Issues:")
        for issue in report['issues'][:10]:  # Show first 10 issues
            print(f"   - {issue['type']} in {issue['file']}:{issue['line']}")

        if len(report['issues']) > 10:
            print(f"   ... and {len(report['issues']) - 10} more issues")

    return json.dumps(report, indent=2)


if __name__ == "__main__":
    import sys
    args = sys.argv[1:] if len(sys.argv) > 1 else None
    print(run_skill(args))