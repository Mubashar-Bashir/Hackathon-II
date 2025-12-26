# ADR 004: Month-End and Leap Year Handling Strategy

## Status
Accepted

## Context
Recurring tasks need to handle edge cases when calculating next occurrence dates, particularly for month-end scenarios (e.g., Jan 31 → Feb 28/29) and leap year calculations (e.g., Feb 29 → Feb 28 in non-leap years). We need to decide how to handle these edge cases.

## Decision
When calculating recurring task dates, if the target date doesn't exist in the target month, the system will schedule to the next valid date in that month.

## Rationale
- **User expectations**: Users expect recurring tasks to continue working rather than fail
- **Consistency**: Provides consistent behavior across all month-end scenarios
- **Simplicity**: Simple rule that's easy to understand and implement
- **Reliability**: Prevents recurring tasks from breaking due to date edge cases
- **Spec alignment**: Matches the clarification that system should "skip to next valid date when target date doesn't exist"

## Alternatives Considered
1. **Error/Stop approach**: Stop recurring when encountering invalid dates (would break recurring tasks)
2. **Skip to beginning of next month**: Jump to first of next month (might miss the intended pattern)
3. **Custom logic per pattern**: Different rules for different recurrence patterns (too complex)

## Consequences
### Positive
- Recurring tasks continue working without manual intervention
- Predictable behavior that users can understand
- Handles all month-end edge cases consistently
- No recurring tasks get stuck or fail due to date issues

### Negative
- Some recurring tasks may shift slightly from their original pattern (e.g., Jan 31 → Feb 28 → Mar 28 instead of Mar 31)
- Users might not expect the date shift in month-end cases

## Implementation
- Implement `_days_in_month()` method to calculate valid days per month
- Implement `_is_leap_year()` method for leap year calculations
- In `calculate_next_occurrence()`, check if target date exists in target month
- If target date doesn't exist, use the last valid day of that month
- Use pendulum library for robust date calculations and leap year handling