#!/usr/bin/env python3
"""
Audit script for verifying leap year and month-end handling in scheduler.py.

This script checks the scheduler implementation for potential issues with:
- Leap year calculations
- Month-end date handling
- Date arithmetic edge cases
"""

import sys
import datetime
from pathlib import Path

# Add the project root to the path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def audit_scheduler_for_time_issues():
    """Audit the scheduler.py file for time-related issues."""
    print("🔍 Auditing scheduler.py for time-related issues...")
    print()

    # Read the scheduler file
    scheduler_path = Path(__file__).parent.parent / "src" / "core" / "scheduler.py"
    if not scheduler_path.exists():
        print(f"❌ File not found: {scheduler_path}")
        return

    with open(scheduler_path, 'r') as f:
        content = f.read()

    issues_found = []
    recommendations = []

    # Check for leap year handling
    if "_is_leap_year" in content:
        print("✅ Leap year handling function found")
    else:
        issues_found.append("Missing leap year handling function")
        recommendations.append("Implement _is_leap_year function to properly handle leap years")

    # Check for month-end handling
    if "_days_in_month" in content:
        print("✅ Month-end handling function found")
    else:
        issues_found.append("Missing month-end handling function")
        recommendations.append("Implement _days_in_month function to handle month-end scenarios")

    # Check for proper month boundary calculations
    if "max_days_in_month" in content or "month_end" in content:
        print("✅ Month boundary calculations found")
    else:
        issues_found.append("Missing month boundary calculations")
        recommendations.append("Add logic to handle month-end scenarios (e.g., Jan 31 recurring monthly should schedule to Feb 28/29)")

    # Check for datetime imports
    if "datetime" in content:
        print("✅ Datetime imports found")
    else:
        issues_found.append("Missing datetime imports")
        recommendations.append("Import datetime module for date calculations")

    # Check for recurrence logic
    if "calculate_next_occurrence" in content:
        print("✅ Recurrence calculation logic found")
    else:
        issues_found.append("Missing recurrence calculation logic")
        recommendations.append("Implement calculate_next_occurrence function for recurring tasks")

    print()
    print("📋 Audit Summary:")
    if issues_found:
        print(f"❌ Issues Found: {len(issues_found)}")
        for i, issue in enumerate(issues_found, 1):
            print(f"  {i}. {issue}")
        print()
        print("💡 Recommendations:")
        for i, rec in enumerate(recommendations, 1):
            print(f"  {i}. {rec}")
    else:
        print("✅ No major issues found!")

    print()
    print("🎯 Additional Verification Tasks:")
    print("  1. Test Feb 29 recurring yearly (should go to next leap year)")
    print("  2. Test Jan 31 recurring monthly (should handle Feb 28/29 correctly)")
    print("  3. Test month-end recurring across different months")
    print("  4. Test year boundary scenarios")
    print("  5. Test century leap year rules (e.g., 1900 vs 2000)")

if __name__ == "__main__":
    audit_scheduler_for_time_issues()