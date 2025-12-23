"""
Security Auditor Skill
Automatically scans for OWASP security issues and common vulnerabilities
"""

import os
import re
import json
from pathlib import Path
from typing import List, Dict, Optional

class SecurityAuditor:
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.security_patterns = {
            "hardcoded_secrets": [
                r'password\s*=\s*["\'][^"\']{3,}["\']',
                r'api_key\s*=\s*["\'][^"\']{3,}["\']',
                r'secret\s*=\s*["\'][^"\']{3,}["\']',
                r'token\s*=\s*["\'][^"\']{3,}["\']',
                r'auth_token\s*=\s*["\'][^"\']{3,}["\']',
                r'access_key\s*=\s*["\'][^"\']{3,}["\']',
            ],
            "sql_injection": [
                r'cursor\.execute\(.*\+.*\)',
                r'cursor\.execute\(.*format\(.*\)\)',
                r'cursor\.execute\(f["\'].*{.*}.*["\']\)',
            ],
            "xss_potential": [
                r'return.*render.*request\.',
                r'return.*template.*request\.',
                r'\.html\(|\.xml\(|\.body\s*=\s*request\.',
            ],
            "path_traversal": [
                r'open\([^)]*request\.',
                r'\.read\([^)]*request\.',
                r'os\.path\.join\([^)]*request\.',
            ],
            "insecure_cryptography": [
                r'hashlib\.md5\(',
                r'hashlib\.sha1\(',
                r'hashlib\.sha\(',
                r'crypto\.Cipher\.ARC4\(',
            ]
        }

        self.file_extensions = ['.py', '.js', '.ts', '.jsx', '.tsx', '.html', '.htm', '.json', '.yaml', '.yml', '.env', '.cfg', '.conf']

    def scan_project(self) -> List[Dict]:
        """Scan project for security vulnerabilities"""
        issues = []

        for ext in self.file_extensions:
            for file_path in self.project_root.rglob(f"*{ext}"):
                if self._should_skip_file(file_path):
                    continue

                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()

                    file_issues = self._scan_file_for_issues(file_path, content)
                    issues.extend(file_issues)

                except Exception as e:
                    issues.append({
                        "file": str(file_path),
                        "type": "scan_error",
                        "message": f"Could not scan file {file_path}: {str(e)}"
                    })

        return issues

    def _should_skip_file(self, file_path: Path) -> bool:
        """Determine if a file should be skipped during security scan"""
        skip_patterns = [
            'node_modules', '__pycache__', '.git', '.vscode', 'dist', 'build',
            'venv', 'env', '.env', 'env.bak', '.venv', 'virtualenv',
            'package-lock.json', 'yarn.lock', '.min.js'
        ]

        file_path_str = str(file_path)
        return any(skip_pattern in file_path_str for skip_pattern in skip_patterns)

    def _scan_file_for_issues(self, file_path: Path, content: str) -> List[Dict]:
        """Scan a specific file for security issues"""
        issues = []

        for issue_type, patterns in self.security_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    line_number = content[:match.start()].count('\n') + 1
                    issues.append({
                        "file": str(file_path),
                        "type": issue_type,
                        "line": line_number,
                        "code": match.group(0)[:100],  # First 100 chars of match
                        "message": f"Potential {issue_type.replace('_', ' ')} vulnerability detected"
                    })

        return issues

    def generate_security_report(self, issues: List[Dict]) -> Dict:
        """Generate a comprehensive security report"""
        report = {
            "summary": {
                "total_files_scanned": len(set(issue["file"] for issue in issues)),
                "total_issues_found": len(issues),
                "issue_types": {},
                "severity_breakdown": {
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
            if issue_type in ["hardcoded_secrets", "sql_injection"]:
                report["summary"]["severity_breakdown"]["high"] += 1
            elif issue_type in ["xss_potential", "path_traversal"]:
                report["summary"]["severity_breakdown"]["medium"] += 1
            else:
                report["summary"]["severity_breakdown"]["low"] += 1

        return report


def run_skill(args: Optional[List[str]] = None) -> str:
    """Main function to run the Security Auditor skill"""
    project_root = args[0] if args and len(args) > 0 else "."

    auditor = SecurityAuditor(project_root)

    print("🔍 Scanning project for security vulnerabilities...")
    issues = auditor.scan_project()

    report = auditor.generate_security_report(issues)

    print(f"✅ Security scan completed!")
    print(f"   - Scanned {report['summary']['total_files_scanned']} files")
    print(f"   - Found {report['summary']['total_issues_found']} potential security issues")
    print(f"   - High severity: {report['summary']['severity_breakdown']['high']}")
    print(f"   - Medium severity: {report['summary']['severity_breakdown']['medium']}")
    print(f"   - Low severity: {report['summary']['severity_breakdown']['low']}")

    if report['summary']['total_issues_found'] > 0:
        print("\n📋 Detailed Issues:")
        for issue in report['issues'][:10]:  # Show first 10 issues
            print(f"   - {issue['type']} in {issue['file']}:{issue['line']}")

        if len(report['issues']) > 10:
            print(f"   ... and {len(report['issues']) - 10} more issues")

    return json.dumps(report, indent=2)


if __name__ == "__main__":
    import sys
    args = sys.argv[1:] if len(sys.argv) > 1 else None
    print(run_skill(args))